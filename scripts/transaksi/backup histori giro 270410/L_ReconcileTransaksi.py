import sys, string
sys.path.append('c:/dafapp/dplk07/script_modules')
sys.path.append('c:/dafapp/dplk07/scripts/transaksi')

import lockupdate, AuthorizeTransaksi

dictJenisTransaksi = {'R':'IuranPendaftaran',\
  'T':'TransaksiDPLK','P':'TransaksiPremi','I':'TransLRInvestasi'}
dictMetadata = {'TransaksiDPLK':'IuranPeserta','TransaksiPremi':'TitipanPremi'}

def GetAllGiroPaket(config):
  giroPenampungan = config.SysVarIntf.GetStringSysVar('GIROCOREBANKING', 'GiroPenampungan')
  tGiroPaket = []
  sSQL = 'select no_giro from PaketInvestasi'
  rSQL = config.CreateSQL(sSQL).RawResult
  
  rSQL.First()
  while not rSQL.Eof:
    tGiroPaket.append(rSQL.no_giro)
    rSQL.Next()

  tGiroPaket.append(giroPenampungan)

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
  rSQLSearch = config.CreateSQL(sSQLSearch).RawResult
  config.SendDebugMsg('sSQLSearch='+sSQLSearch)
  rSQLSearch.First()
  while not rSQLSearch.Eof:
    config.SendDebugMsg(rSQL.NOMOR_PESERTA)
    #cek referensi core banking transaksi
    refdplk = rSQLSearch.Ref_CoreBanking
    if rSQLSearch.Ref_CoreBanking == rSQL.NOMOR_URUT:
      #rSQL.NOMOR_BATCH_COREBANKING+'.'+rSQL.NOMOR_URUT:
    
      #ketemu transaksi yang dimaksud, proses setujui otorisasi
      if jenisTransaksi in ['TransaksiDPLK','TransaksiPremi']:
        jenisTransaksi = dictMetadata[jenisTransaksi]

      AuthorizeTransaksi.AuthorizeOperationNonTrans(config, jenisTransaksi, \
        rSQLSearch.ID_Transaksi, 'A')
      UpdateFlagHistoriGiro(config, rSQL)

    rSQLSearch.Next()
  
  return 1
  
def UpdateFlagHistoriGiro(config, rSQL):
    oHG = config.CreatePObjImplProxy('HistoriGiro')
    oHG.SetKey('ID_HistoriGiroHarian',rSQL.ID_HISTORIGIROHARIAN)
    oHG.SetKey('acc_giro',rSQL.ACC_GIRO)
    oHG.SetKey('Nomor_Urut',rSQL.NOMOR_URUT)
    oHG.SetKey('Nomor_Batch_CoreBanking',rSQL.NOMOR_BATCH_COREBANKING)
    oHG.isTransaksiCreated = 'T'
	
def CreatingResultSet(config, dtTglTransaksi, tTglTransaksi):    
  #ambil HistoriGiroHarian dan HistoriGiro dari tabel sesuai tanggal  
  #~#~hanya pilih transaksi unsettled, skip yang settled [SALAH - rev ita 22sept08]  
  #hanya pilih transaksi SETTLED, skip yang UNSETTLED (transaksi peserta = 1)
  #pilih histori yang memiliki informasi Nomor Peserta
  #pilih kode mnemonic (kode debit/credit) yang Credit saja.
  config.SendDebugMsg('CreatingResultSet')

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
                hg.KODE_MNEMONIC = \'C\' and \
				hgh.ISRECONCILED = \'F\' \
          order by hgh.ID_HISTORIGIROHARIAN, \
                   mg.NO_GIRO, \
                   hg.NOMOR_PESERTA' \
          % ('%d-%d-%d' % (y,m,d))
  rSQL = config.CreateSQL(sSQL).RawResult
  config.SendDebugMsg('sSQL='+sSQL)
  #ambil info semua giro paket investasi, giro premi dan giro pendaftaran
  tGiroPaket = GetAllGiroPaket(config)
  giroPremi = config.SysVarIntf.GetStringSysVar('GIROCOREBANKING', 'GiroPremi')
  giroPendaftaran = config.SysVarIntf.GetStringSysVar('GIROCOREBANKING', 'GiroPendaftaran')
  giroReturnInvestasi = config.SysVarIntf.GetStringSysVar('GIROCOREBANKING', \
    'GiroReturnInvestasi')
  
  progress = config.ProgressTracker
  progress.ProgressLevel1()

  lastNoGiro = 'inisialisasi pertama'
  batchType = ''
  rSQL.First()
  while not rSQL.Eof:
    config.SendDebugMsg(rSQL.NO_GIRO)
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
        raise Exception, 'Error Giro' + 'Nomor Giro %s tidak terdefinisi' % (rSQL.NO_GIRO)               

      #update nilai lastID_HISTORIGIROHARIAN
      lastNoGiro = rSQL.NO_GIRO
      
    if batchType != 'I':
      #selain untuk transaksi Investasi (transaksi Investasi dipending)
      #transaksi Giro unsettled, reconcile transaksi for this
      ReconcileTransaksi(config, rSQL, tTglTransaksi, batchType)

    rSQL.Next()
	
  config.FlushUpdates()
  HapusTransaksiNonCommit(config, tTglTransaksi)
  
  return 1
  
def HapusTransaksiNonCommit(config, tTglTransaksi):
  #preparing remove transaksi (tolak otorisasi)
  #asumsi semua transaksi iuran peserta, titipan premi dan iuran pendaftaran dicek
  y,m,d = tTglTransaksi[:3]
  config.SendDebugMsg('hapus transaksi non commit')
  listTransaksi = [['R','IuranPendaftaran'],['T','TransaksiDPLK'],['P','TransaksiPremi']]  
  for transaksi in listTransaksi:
    #perlu menghapus transaksi yang tidak ter-'commit' 
    #(tidak ada padanan di CoreBanking)
    sSQLRemove = 'select t.ID_Transaksi, batch_type \
                  from %s as t, TransactionBatch as tb \
                  where tb.tgl_used = \'%s\' and \
                        tb.batch_type = \'%s\' and \
                        tb.batch_sub_type = \'T\' and \
                        t.ID_TransactionBatch = tb.ID_TransactionBatch and \
                        t.isCommitted = \'F\'' \
                  % (transaksi[1],'%d-%d-%d' % (y,m,d),transaksi[0])
    rSQLRemove = config.CreateSQL(sSQLRemove).RawResult
    config.SendDebugMsg('sSQLRemove='+sSQLRemove)
    rSQLRemove.First()
    while not rSQLRemove.Eof:
      #proses tolak otorisasi
      batchType = rSQLRemove.batch_type
      config.SendDebugMsg('batchType='+batchType)
      jenisTransaksi = dictJenisTransaksi[batchType]
      if jenisTransaksi in ['TransaksiDPLK','TransaksiPremi']:
        jenisTransaksi = dictMetadata[jenisTransaksi]

      AuthorizeTransaksi.AuthorizeOperationNonTrans(config, jenisTransaksi, \
          rSQLRemove.ID_Transaksi, 'R')
      rSQLRemove.Next()

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
