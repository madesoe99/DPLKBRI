import sys, string
sys.path.append('c:/dafapp/dplk07/script_modules')
sys.path.append('c:/dafapp/dplk07/scripts/transaksi')

import lockupdate, AuthorizeTransaksi

dictJenisTransaksi = {'R':'IuranPendaftaran',\
  'T':'TransaksiDPLK','P':'TransaksiPremi','I':'TransLRInvestasi'}
dictMetadata = {'TransaksiDPLK':'IuranPeserta','TransaksiPremi':'TitipanPremi'}

def GetAllGiroPaket(config):
  tGiroPaket = []
  sSQL = 'select no_giro from PaketInvestasi'
  rSQL = config.CreateSQL(sSQL).RawResult
  
  rSQL.First()
  while not rSQL.Eof:
    tGiroPaket.append(rSQL.no_giro)
    rSQL.Next()

  return tGiroPaket

def ReconcileTransaksi(config, rSQL, tTglTransaksi, batchType):
  config.SendDebugMsg('ReconcileTransaksi')
  #cek jenis batch yang dipakai untuk transaksi
  #dictJenisTransaksi = {'R':'IuranPendaftaran',\
  #  'T':'TransaksiDPLK','P':'TransaksiPremi','I':'TransLRInvestasi'}
  #dictMetadata = {'TransaksiDPLK':'IuranPeserta','TransaksiPremi':'TitipanPremi'}

  jenisTransaksi = dictJenisTransaksi[batchType]

  #cari objek transaksi yang ada dalam batch type tanggal tTglTransaksi
  #dengan nomor peserta tertentu
  y,m,d = tTglTransaksi[:3]
  sSQLSearch = 'select t.ID_Transaksi, t.Ref_CoreBanking \
                from %s as t, TransactionBatch as tb \
                where tb.tgl_used = \'%s\' and \
                      tb.batch_type = \'%s\' and \
                      tb.batch_sub_type = \'T\' and \
                      t.ID_TransactionBatch = tb.ID_TransactionBatch and \
                      t.no_peserta = \'%s\'' \
                % (jenisTransaksi,'%d-%d-%d' % (y,m,d),batchType, rSQL.NOMOR_PESERTA)
  config.SendDebugMsg('sSQLSearch '+ str(sSQLSearch))
  rSQLSearch = config.CreateSQL(sSQLSearch).RawResult

  rSQLSearch.First()
  while not rSQLSearch.Eof:
    config.SendDebugMsg('rec_crs_rec_1')
    #cek referensi core banking transaksi 
    if rSQLSearch.Ref_CoreBanking == \
      rSQL.NOMOR_BATCH_COREBANKING+'.'+rSQL.NOMOR_URUT:
      config.SendDebugMsg('rec_crs_rec_2')

      #ketemu transaksi yang dimaksud, proses setujui otorisasi
      if jenisTransaksi in ['TransaksiDPLK','TransaksiPremi']:
        jenisTransaksi = dictMetadata[jenisTransaksi]

      config.SendDebugMsg('rec_crs_rec_3')
      AuthorizeTransaksi.AuthorizeOperationNonTrans(config, jenisTransaksi, \
        rSQLSearch.ID_Transaksi, 'A')

    config.SendDebugMsg('rec_crs_rec_4')
    rSQLSearch.Next()

  return 1

def CreatingResultSet(config, dtTglTransaksi, tTglTransaksi):    
  #ambil HistoriGiroHarian dan HistoriGiro dari tabel sesuai tanggal
  #hanya pilih transaksi unsettled, skip yang settled       [SALAH, REV BY ITA 24SEPT08]    
  #hanya pilih transaksi SETTLED, skip yang UNSETTLED
  #pilih histori yang memiliki informasi Nomor Peserta
  #pilih kode mnemonic (kode debit/credit) yang Credit saja.
  config.SendDebugMsg('rec_crs1')

  y,m,d = tTglTransaksi[:3]
  sSQL = 'select hgh.ID_HISTORIGIROHARIAN, \
                 mg.NO_GIRO, \
                 hg.ACC_GIRO, \
                 hg.NOMOR_BATCH_COREBANKING, \
                 hg.NOMOR_URUT, \
                 hg.NOMOR_PESERTA, \
                 hg.NOMINAL \
          from HISTORIGIROHARIAN hgh, HISTORIGIRO hg, MASTERGIRO mg \
          where hgh.TANGGAL_HISTORI = \'%s\' and \
                hgh.ID_HISTORIGIROHARIAN = hg.ID_HISTORIGIROHARIAN and \
                hg.ACC_GIRO = mg.ACC_GIRO and \
                hg.NOMOR_PESERTA is not null and \
                hg.TRANSAKSI_PESERTA = 1 and \
                hg.KODE_MNEMONIC = \'C\' \
          order by hgh.ID_HISTORIGIROHARIAN, \
                   mg.NO_GIRO, \
                   hg.NOMOR_PESERTA' \
          % ('%d-%d-%d' % (y,m,d))
  config.SendDebugMsg('sSQL '+ str(sSQL))
  rSQL = config.CreateSQL(sSQL).RawResult

  #ambil info semua giro paket investasi, giro premi dan giro pendaftaran
  tGiroPaket = GetAllGiroPaket(config)
  giroPremi = config.SysVarIntf.GetStringSysVar('GIROCOREBANKING', 'GiroPremi')
  giroPendaftaran = config.SysVarIntf.GetStringSysVar('GIROCOREBANKING', 'GiroPendaftaran')
  giroReturnInvestasi = config.SysVarIntf.GetStringSysVar('GIROCOREBANKING', \
    'GiroReturnInvestasi')
  
  config.SendDebugMsg('rec_crs2')
  progress = config.ProgressTracker
  progress.ProgressLevel1()

  lastNoGiro = 'inisialisasi pertama'
  batchType = ''
  rSQL.First()
  while not rSQL.Eof:
    config.SendDebugMsg('rec_crs while1')
    #transaksi unsettled, cek lastNoGiro      
    if lastNoGiro != rSQL.NO_GIRO:
      # nomor giro berbeda, pilih batch type sesuai jenis nomor giro 
      progress.SetProgressInfo2(1, 'Memproses Nomor Giro %s: ' % (rSQL.NO_GIRO))
      
      if rSQL.NO_GIRO in tGiroPaket:
        #transaksi giro paket, rekonsiliasi transaksi iuran peserta
        batchType = 'T'
      elif rSQL.NO_GIRO == giroPremi:
        #transaksi giro premi, rekonsiliasi transaksi titipan premi
        batchType = 'P'
      elif rSQL.NO_GIRO == giroPendaftaran:
        #transaksi giro pendaftaran, rekonsiliasi transaksi iuran pendaftaran
        batchType = 'R'
      elif rSQL.NO_GIRO == giroReturnInvestasi:
        #transaksi giro return investasi
        #mungkin rekonsiliasi transaksi investasi TransLRInvestasi
        batchType = 'I'
      else:
        #No Giro tidak terdefinisi
        raise 'Error Giro','Nomor Giro %s tidak terdefinisi' % (rSQL.NO_GIRO)               

      #update nilai lastID_HISTORIGIROHARIAN
      lastNoGiro = rSQL.NO_GIRO
      
    if batchType != 'I':
      #selain untuk transaksi Investasi (transaksi Investasi dipending)
      #transaksi Giro unsettled, reconcile transaksi for this
      ReconcileTransaksi(config, rSQL, tTglTransaksi, batchType)

    rSQL.Next()

  config.SendDebugMsg('rec_crs3-HapusTransaksi@Reconcile')
  #preparing remove transaksi (tolak otorisasi)
  #asumsi semua transaksi iuran peserta, titipan premi dan iuran pendaftaran dicek
  listTransaksi = [['R','IuranPendaftaran'],['T','TransaksiDPLK'],['P','TransaksiPremi']]  
  for transaksi in listTransaksi:
    config.SendDebugMsg('rec_crs_for1')
    #perlu menghapus transaksi yang tidak ter-'commit' 
    #(tidak ada padanan di CoreBanking)
    sSQLRemove = 'select t.ID_Transaksi \
                  from %s as t, TransactionBatch as tb \
                  where tb.tgl_used = \'%s\' and \
                        tb.batch_type = \'%s\' and \
                        tb.batch_sub_type = \'T\' and \
                        t.ID_TransactionBatch = tb.ID_TransactionBatch and \
                        t.isCommitted = \'F\'' \
                  % (transaksi[1],'%d-%d-%d' % (y,m,d),transaksi[0])
    config.SendDebugMsg('sSQLRemove='+ str(sSQLRemove))
    rSQLRemove = config.CreateSQL(sSQLRemove).RawResult

    rSQLRemove.First()
    while not rSQLRemove.Eof:
      config.SendDebugMsg('rec_crs_while2')
      #proses tolak otorisasi

#       jenisTransaksi = dictJenisTransaksi[batchType]
      jenisTransaksi = dictJenisTransaksi[transaksi[0]]
#       dictJenisTransaksi = {
#         'R':'IuranPendaftaran'
#         ,'T':'TransaksiDPLK'
#         ,'P':'TransaksiPremi'
#         ,'I':'TransLRInvestasi'
#       }
      if jenisTransaksi in ['TransaksiDPLK','TransaksiPremi']:
        jenisTransaksi = dictMetadata[jenisTransaksi]
        # TransaksiDPLK -> IuranPeserta, TransaksiPremi -> TitipanPremi

      config.SendDebugMsg('rec_crs_while2_1')
      AuthorizeTransaksi.AuthorizeOperationNonTrans(config, jenisTransaksi, \
          rSQLRemove.ID_Transaksi, 'R')
      config.SendDebugMsg('rec_crs_while2_2')
      rSQLRemove.Next()

  return 1

def Main(config, dtTglTransaksi, tTglTransaksi):
  config.BeginTransaction()
  try:
    CreatingResultSet(config, dtTglTransaksi, tTglTransaksi)

    #update isReconciled Histori Giro Harian
    lockupdate.UpdateProcess(config, 'HistoriGiroHarian', \
      'isReconciled = \'T\'', \
      'Tanggal_Histori = \'%s\'' \
        % ('%d-%d-%d' % (tTglTransaksi[0],tTglTransaksi[1],tTglTransaksi[2])), \
      'isReconciled = \'F\'')
    
    config.Commit()
  except:
    config.Rollback()
    raise

  return 1  

def DAFLongScriptMain(config, parameter, pid, monfilename):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # pid: Process ID of this script
  # monfilename: Monitor file name to store status

  app = config.AppObject
  dtTglTransaksi = parameter.FirstRecord.tglTransaksi
  y,m,d = config.ModLibUtils.DecodeDate(dtTglTransaksi)
  tTglTransaksi = [y,m,d]
  
  consoleID = 'ReconcileTransaksiHistoriGiro_' + str(pid)

  sJobName = '%s. TaskID = %s' % ('Rekonsiliasi Transaksi Giro DPLK',pid)
  app.WriteConsole(sJobName + ': mulai berlangsung\r\n')
  try:
    app.CreateConsole(consoleID, 'progress')
    try:
      app.SwitchDefaultConsole(consoleID)      
            
      #main task right here
      Main(config, dtTglTransaksi, tTglTransaksi)

      app.WriteConsole(sJobName + ': telah selesai\r\n')
    finally:
      app.CloseConsole(consoleID)
  except:
    app.WriteConsole(sJobName + ': Error\r\n' + str(sys.exc_info()[1]) + '\r\n')
    raise
