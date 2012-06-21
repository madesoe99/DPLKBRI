import sys, string
sys.path.append('c:/dafapp/dplk07/script_modules')
sys.path.append('c:/dafapp/dplk07/scripts/transaksi')

import transaksiapi, lockupdate, AuthorizeTransaksi, moduleapi

IsHasFailed = 0

def CreateLogFile(config, dtTglTransaksi, pid):
  sBaseFileName = 'CTHG_%s_%s_%d.txt' % (
     config.FormatDateTime('ddmmyy', dtTglTransaksi)
     , config.FormatDateTime('ddmmyy_hhnnsszzz', config.Now())
     , pid
     )
  sFileName = config.UserHomeDirectory + sBaseFileName

  return open(sFileName, 'w')

def CloseFile(config, oFile):
  oFile.close()

def GetKodePaket(config, noGiro):
  kodePaket = ''
  sSQL = 'select kode_paket_investasi from PaketInvestasi where no_giro = \'%s\''\
    % (noGiro)
  rSQL = config.CreateSQL(sSQL).RawResult
  
  rSQL.First()
  if not rSQL.Eof:
    kodePaket = rSQL.KODE_PAKET_INVESTASI

  return kodePaket

def GetKodePaketPeserta(config, no_peserta):
  kodePaket = ''
  sSQL = "SELECT kode_paket_investasi \
  FROM RekeningDPLK \
  WHERE no_peserta = '%s'" % (no_peserta)
  rSQL = config.CreateSQL(sSQL).RawResult
  
  rSQL.First()
  if not rSQL.Eof:
    kodePaket = rSQL.KODE_PAKET_INVESTASI

  return kodePaket

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

def CreateTransaksi(config, oBatch, rSQL, oFile):
  global IsHasFailed
  berhasil = 'T'
  #cek jenis batch yang dipakai untuk transaksi
  if oBatch.batch_type == 'R':
    #pendaftaran
    jenisTransaksi = 'IuranPendaftaran'
  elif oBatch.batch_type == 'T':
    #transaksi, berarti pasti iuran peserta
    jenisTransaksi = 'IuranPeserta'
    if moduleapi.IsPensiun(config, rSQL.NOMOR_PESERTA):
      oFile.write('FAILED, Peserta sudah pensiun\n')
      IsHasFailed += 1
      return 0
  elif oBatch.batch_type == 'P':
    #premi, berarti pasti titipan premi
    #periksa rekeningwasiatummat
    if not moduleapi.GetRekeningWasiatUmmat(config, rSQL.NOMOR_PESERTA):
      oFile.write('FAILED, GetRekeningWasiatUmmat\n')
      IsHasFailed += 1
      return 0
    jenisTransaksi = 'TitipanPremi'
  elif oBatch.batch_type == 'I':
    #investasi, mungkin transaksi investasi TransLRInvestasi
    jenisTransaksi = 'TransLRInvestasi'

  #create new objek transaksi
  o = config.CreatePObject(jenisTransaksi)

  #treatment sesuai objek transaksi
  if jenisTransaksi == 'IuranPendaftaran':
    o.besar_biaya_daftar = rSQL.NOMINAL 
  elif jenisTransaksi == 'IuranPeserta':
    o.mutasi_pengembangan = o.mutasi_peralihan = o.mutasi_iuran_pk = 0.0
    o.mutasi_iuran_pst = rSQL.NOMINAL
    
    #ambil info paket investasi berdasarkan Nomor Giro yang ada di rSQL
    #supaya sesuai dengan Histori Transaksi 
    o.kode_paket_investasi = GetKodePaketPeserta(config, rSQL.NOMOR_PESERTA)#GetKodePaket(config, rSQL.NO_GIRO)
  elif jenisTransaksi == 'TitipanPremi':
    o.isDebet = 'F'
    o.mutasi_premi = rSQL.NOMINAL
  elif jenisTransaksi == 'TransLRInvestasi':
    #TBD, belum didefinisikan
    pass

  #set field umum
  o.ID_TransactionBatch = oBatch.ID_TransactionBatch
  o.no_peserta = rSQL.NOMOR_PESERTA
  o.branch_code = oBatch.branch_code    
  o.user_id = o.user_id_auth = config.SecurityContext.UserID
  o.terminal_id = o.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]
  y,m,d = oBatch.tgl_used[:3]
  o.tgl_transaksi = config.ModLibUtils.EncodeDate(y,m,d) 
  o.tgl_sistem = o.tgl_otorisasi = config.ModLibUtils.Now()
  o.keterangan = 'Transaksi dibuat dari Transaksi-Histori-Giro DPLK'
  config.SendDebugMsg('cth_ct21')
      
  #prosesi otorisasi
  AuthorizeTransaksi.AuthorizeOperationNonTrans(config, jenisTransaksi, o.ID_Transaksi, 'A')
  config.SendDebugMsg('cth_ct22')
  oFile.write(jenisTransaksi+': ')
  if oBatch.batch_type == 'T':
    # iuran peserta
    oFile.write('%-10d|%s|%s|%10.2f|%10.2f|%10.2f|%10.2f\n' %
                (o.ID_Transaksi
                 , str(o.isCommitted)
                 , str(o.kode_paket_investasi)
                 , o.mutasi_iuran_pst or 0.0
                 , o.mutasi_iuran_pk or 0.0
                 , o.mutasi_pengembangan or 0.0
                 , o.mutasi_peralihan or 0.0
                 )
    )
  elif oBatch.batch_type == 'R':
    # iuran pendaftaran
    oFile.write('%-10d|%s|%10.2f\n' %
                (o.ID_Transaksi
                 , str(o.isCommitted)
                 , o.besar_biaya_daftar or 0.0
                 )
    )
  elif oBatch.batch_type == 'P':
    # premi
    oFile.write('%-10d|%s|%10.2f\n' %
                (o.ID_Transaksi
                 , str(o.isCommitted)
                 , o.mutasi_premi or 0.0
                 )
    )

  return 1

def CreateBatch(config, batchType, dtTglTransaksi):
  #kategori batch Admin, sesuai tanggal transaksi, account link type Single
  oTB = config.CreatePObject('TransactionBatch')
  oTB.batch_type = batchType

  #batch sub type diset 'Manual'
  oTB.batch_sub_type = 'M'

  #ambil info tanggal
  y,m,d = config.ModLibUtils.DecodeDate(dtTglTransaksi)

  #tanggal pembuatan dan tanggap pakai disamakan
  oTB.tgl_create = oTB.tgl_used = config.ModDateTime.EncodeDate(y, m, d)

  #acccount link type diset 'Single' dan status batch 'Open'
  oTB.account_link_type = 'S'
  oTB.batch_status = 'O'

  #informasi tambahan untuk batch
  oTB.terminal_id_create = config.SecurityContext.GetSessionInfo()[1]
  oTB.user_id_create = oTB.user_id_owner = config.SecurityContext.UserID
  oTB.branch_code = config.SecurityContext.GetUserInfo()[4]  

  #creating nomor batch
  oTB.no_batch = 'B' + oTB.batch_type + '.' + oTB.user_id_owner + '.' + \
    str(oTB.tgl_used[0]) + \
    str(string.zfill(oTB.tgl_used[1],2)) + \
    str(string.zfill(oTB.tgl_used[2],2)) + '.' + str(oTB.ID_TransactionBatch)

  return oTB

def CreatingResultSet(config, dtTglTransaksi, oFile):
  #ambil HistoriGiroHarian dan HistoriGiro dari tabel sesuai tanggal
  #hanya pilih transaksi unsettled, skip yang settled
  #pilih histori yang memiliki informasi Nomor Peserta
  #pilih yang kode mnemonic-nya Credit (uang masuk)
  y,m,d = config.ModLibUtils.DecodeDate(dtTglTransaksi)
  sSQL = 'select hgh.ID_HISTORIGIROHARIAN,\
                 mg.NO_GIRO,\
                 hg.ACC_GIRO,\
                 hg.NOMOR_URUT,\
                 hg.NOMOR_PESERTA,\
                 hg.NOMOR_BATCH_COREBANKING,\
                 hg.NOMINAL\
          from HISTORIGIROHARIAN hgh, HISTORIGIRO hg, MASTERGIRO mg, REKENINGDPLK rk\
          where hgh.TANGGAL_HISTORI = \'%s\' and \
                hgh.ID_HISTORIGIROHARIAN = hg.ID_HISTORIGIROHARIAN and \
                hg.ACC_GIRO = mg.ACC_GIRO and \
                hg.NOMOR_PESERTA is not null and \
                hg.NOMOR_PESERTA = rk.no_peserta and \
                rk.status_dplk = \'A\' and \
                hg.TRANSAKSI_PESERTA = 0 and \
				hg.ISTRANSAKSICREATED = \'F\' and \
                hg.KODE_MNEMONIC = \'C\' \
          order by hgh.ID_HISTORIGIROHARIAN,\
                   mg.NO_GIRO,\
                   hg.NOMOR_PESERTA'\
          % ('%d-%d-%d' % (y,m,d))
  rSQL = config.CreateSQL(sSQL).RawResult

#                 and rk.no_peserta in \
#          	     (select w.no_peserta \
#          	     from RekeningWasiatUmmat w \
#          	     )                \

  #ambil info semua giro paket investasi, giro premi dan giro pendaftaran
  tGiroPaket = GetAllGiroPaket(config)
  giroPremi = config.SysVarIntf.GetStringSysVar('GIROCOREBANKING', 'GiroPremi')
  giroPendaftaran = config.SysVarIntf.GetStringSysVar('GIROCOREBANKING', 'GiroPendaftaran')
  giroReturnInvestasi = config.SysVarIntf.GetStringSysVar('GIROCOREBANKING', \
    'GiroReturnInvestasi')
  
  progress = config.ProgressTracker
  progress.ProgressLevel1()

  lastNoGiro = 'inisialisasi pertama'
  isExistBatchTransaksi = 0
  rSQL.First()
  while not rSQL.Eof:
    #transaksi unsettled, cek lastNoGiro      
    if lastNoGiro != rSQL.NO_GIRO:
      # nomor giro berbeda, ganti / create newly batch
      progress.SetProgressInfo2(1, 'Memproses Nomor Giro %s: ' % (rSQL.NO_GIRO))
      # 1 nomor giro == 1 batch (kecuali untuk batch transaksi)

      if rSQL.NO_GIRO in tGiroPaket:
        config.SendDebugMsg('if1')
        #cek apakah batch transaksi sudah dibuat
#        if not isExistBatchTransaksi:
          #batch transaksi belum ada, create new one -ditutup by ita
        oBatch = CreateBatch(config, 'T', dtTglTransaksi)
#          isExistBatchTransaksi = 1
        #else: batch transaksi sudah ada, tinggal pakai yang sudah ada
      elif rSQL.NO_GIRO == giroPremi:
        config.SendDebugMsg('if2')
        #buat batch premi
        oBatch = CreateBatch(config, 'P', dtTglTransaksi)        
      elif rSQL.NO_GIRO == giroPendaftaran:
        config.SendDebugMsg('if3')
        #buat batch pendaftaran
        oBatch = CreateBatch(config, 'R', dtTglTransaksi)         
      elif rSQL.NO_GIRO == giroReturnInvestasi:
        config.SendDebugMsg('if4')
        #buat batch investasi
        oBatch = CreateBatch(config, 'I', dtTglTransaksi)
        pass
      else:
        config.SendDebugMsg('if5')
        #No Giro tidak terdefinisi
        raise 'Error Giro','Nomor Giro %s tidak terdefinisi' % (rSQL.NO_GIRO)

      #update nilai lastID_HISTORIGIROHARIAN
      lastNoGiro = rSQL.NO_GIRO

      oFile.write('=================================================================\n')
      oFile.write('** ACC/NO GIRO: %s/%s **\n' % (str(rSQL.ACC_GIRO), str(rSQL.NO_GIRO)))
      oFile.write('** BATCH: %s **\n' % (str(oBatch.no_batch)))

    oFile.write('-----------------------------------------------------------------\n')
    oFile.write('%-10d|%-10s|%-10s|%10.2f\n' % (rSQL.ID_HISTORIGIROHARIAN, str(rSQL.NOMOR_URUT), str(rSQL.NOMOR_PESERTA), rSQL.NOMINAL or 0.0))

    config.SendDebugMsg('cth_00')
    if rSQL.NO_GIRO != giroReturnInvestasi:
      #selain untuk transaksi Investasi (transaksi Investasi dipending)
      #transaksi Giro unsettled, creating transaksi for this
      CreateTransaksi(config, oBatch, rSQL, oFile)
    config.SendDebugMsg('cth_01')

    #update status isTransaksiCreated HistoriGiro
    oHG = config.CreatePObjImplProxy('HistoriGiro')
    oHG.SetKey('ID_HistoriGiroHarian',rSQL.ID_HISTORIGIROHARIAN)
    oHG.SetKey('acc_giro',rSQL.ACC_GIRO)
    oHG.SetKey('Nomor_Urut',rSQL.NOMOR_URUT)
    #penambahan primary key#
    oHG.SetKey('Nomor_Batch_CoreBanking',rSQL.NOMOR_BATCH_COREBANKING)
    oHG.isTransaksiCreated = 'T'

    rSQL.Next()

  return 1

def Main(config, dtTglTransaksi, tTglTransaksi, oFile):
  config.BeginTransaction()
  try:
    config.SendDebugMsg('cth_m1')
    CreatingResultSet(config, dtTglTransaksi, oFile)
    
    config.SendDebugMsg('cth_m2')
    #update isTransactionProceed Histori Giro Harian
    lockupdate.UpdateProcess(config, 'HistoriGiroHarian', \
      'isTransactionProceed = \'T\'', \
      'Tanggal_Histori = \'%s\'' \
        % ('%d-%d-%d' % (tTglTransaksi[0],tTglTransaksi[1],tTglTransaksi[2])), \
      'isTransactionProceed = \'F\'')
    
    config.SendDebugMsg('cth_m3')    
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
  
  consoleID = 'BuatTransaksiHistoriGiro_' + str(pid)

  sJobName = '%s. TaskID = %s' % ('Buat Transaksi Giro DPLK',pid)
  app.WriteConsole(sJobName + ': mulai berlangsung\r\n')
  try:
    oFile = CreateLogFile(config, dtTglTransaksi, pid)
    app.CreateConsole(consoleID, 'progress')
    try:
      app.SwitchDefaultConsole(consoleID)      

      #main task right here
      Main(config, dtTglTransaksi, tTglTransaksi, oFile)

      global IsHasFailed
      if IsHasFailed:
        app.WriteConsole(sJobName + ': Terdapat %d histori giro yang TIDAK DIBUAT, silakan lihat log file:\r\n%s\r\n' % (IsHasFailed, oFile.name))
      else:
        app.WriteConsole(sJobName + ': Semua histori giro TELAH DIBUAT, silakan lihat log file:\r\n%s\r\n' % (oFile.name))

      app.WriteConsole(sJobName + ': telah selesai\r\n')
    finally:
      app.CloseConsole(consoleID)
      CloseFile(config, oFile)
  except:
    app.WriteConsole(sJobName + ': Error\r\n' + str(sys.exc_info()[1]) + '\r\n')
    raise
