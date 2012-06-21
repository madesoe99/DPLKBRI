import sys
sys.path.append('c:/dafapp/dplk07/script_modules')

import moduleapi, transaksiapi

def HitungBiaya(config, classJenisBiaya, rSQL, kode_jenis_transaksi, tglHitung, FixValue, TotalDana):
  if classJenisBiaya == 'BiayaPengelolaanDana':
    #tentukan proporsi biaya
    proporsiBiaya = transaksiapi.HitungProporsiBiaya(config, kode_jenis_transaksi, \
        rSQL.no_peserta, tglHitung)
    config.SendDebugMsg('proporsiBiaya='+str(proporsiBiaya))            
    #hitung biaya (administrasi tahunan / pengelolaan dana)
    besarBiaya = proporsiBiaya * FixValue * TotalDana         
  else:
    proporsiBiaya = transaksiapi.HitungProporsiBiayaAdmTahunan(config, rSQL.no_peserta, tglHitung)      
    besarBiaya = proporsiBiaya * FixValue
  
  return besarBiaya

def CreateLogFile(config, dtTglTransaksi):
  t = str(dtTglTransaksi[2])+str(dtTglTransaksi[1])+str(dtTglTransaksi[0])[:2]
  sBaseFileName = 'BiayaTahunan_%s_%s.txt' % (
     t, config.FormatDateTime('ddmmyy_hhnnsszzz', config.Now())
     )
  sFileName = config.UserHomeDirectory + sBaseFileName

  return open(sFileName, 'w')
  
def GetParameter(config, classJenisBiaya, SRR):
  oP = config.CreatePObjImplProxy('Parameter')  
  #tentukan handling khusus untuk jenis biaya tahunan yang berbeda   
  if classJenisBiaya == 'BiayaAdmTahunan':
    #biaya yang tetap untuk semua peserta
    kode_jenis_transaksi = 'D'
    oP.Key = 'BIAYA_ADM_TAHUNAN'
    FixValue = oP.Numeric_Value    
  elif classJenisBiaya == 'BiayaPengelolaanDana':
    #biaya yang ditentukan berdasarkan persentase
    kode_jenis_transaksi = 'C'
    oP.Key = 'BATAS_SRR_BIAYA_PENGELOLAAN' ; batas_srr = oP.Numeric_Value
    config.SendDebugMsg('batas SRR='+str(batas_srr))    
    if SRR <= batas_srr:
      config.SendDebugMsg('<= 100jt')    
      oP.Key = 'PERSEN_BIAYA_PENGELOLAAN_1' ; FixValue = oP.Numeric_Value / 100
    else:
      config.SendDebugMsg('> 100jt')
      oP.Key = 'PERSEN_BIAYA_PENGELOLAAN_2' ; FixValue = oP.Numeric_Value / 100
    
  return FixValue, kode_jenis_transaksi  

def GetJumlahPeserta(config, ID_SRRCalc):
  sSQLJumlah = 'select count(r.no_peserta) as JumlahPeserta \
          from HISTORISRR h, REKENINGDPLK r \
          where r.STATUS_DPLK = \'A\' and \
                h.no_peserta = r.no_peserta and \
                h.ID_SRRCalcRincian in \
                (select ID_SRRCalcRincian \
                from SRRCalcRincian \
                where ID_SRRCalc = %d) ' % (ID_SRRCalc)
  rSQLJumlah = config.CreateSQL(sSQLJumlah).RawResult
  
  return rSQLJumlah

def GetPeserta(config, ID_SRRCalc):
  sSQL = 'select r.no_peserta, h.SRR, r.AKUM_DANA_IURAN_PK, r.AKUM_DANA_IURAN_PST, \
                 r.AKUM_DANA_PENGEMBANGAN, r.akum_dana_peralihan \
          from HISTORISRR h, REKENINGDPLK r \
          where r.STATUS_DPLK = \'A\' and \
                h.no_peserta = r.no_peserta and \
                h.ID_SRRCalcRincian in \
                (select ID_SRRCalcRincian \
                from SRRCalcRincian \
                where ID_SRRCalc = %d) \
          order by r.no_peserta;' \
          % (ID_SRRCalc)
  rSQL = config.CreateSQL(sSQL).RawResult
  
  return rSQL
     
def CreateBiayaTahunan(config, classJenisBiaya, tglHitung, idBatch, noPeserta, \
  valueBiaya):
  
  oRekening = config.CreatePObjImplProxy('RekeningDPLK')
  oRekening.Key = noPeserta
  oBiaya = config.CreatePObject(classJenisBiaya)
  moduleapi.TransCostOpr(config, oRekening, oBiaya, valueBiaya)
  
  if classJenisBiaya == 'BiayaPengelolaanDana':
    oBiaya.kode_jenis_transaksi = 'C'
  elif classJenisBiaya == 'BiayaAdmTahunan':
    oBiaya.kode_jenis_transaksi = 'D'

  oBiaya.no_peserta = noPeserta
  oBiaya.ID_TransactionBatch = idBatch
  oBiaya.isCommitted = 'T'
  oBiaya.user_id = config.SecurityContext.UserID
  oBiaya.user_id_auth = config.SecurityContext.UserID
  oBiaya.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]
  oBiaya.tgl_transaksi = config.ModLibUtils.EncodeDate(tglHitung[0],\
    tglHitung[1],tglHitung[2])
  oBiaya.tgl_sistem = oBiaya.tgl_otorisasi = config.Now()
  oBiaya.keterangan = '%s peserta %s' % (classJenisBiaya, noPeserta)
  
  #biaya tahunan memakai branchcode dan terminal id Admin
  oBiaya.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oBiaya.branch_code = config.SecurityContext.GetUserInfo()[4]
  
  return 1

def Main(config, tglHitung, idBatch, classJenisBiaya):
#   import rpdb2; rpdb2.start_embedded_debugger("000")  
  ID_SRRCalc = moduleapi.GetLastIDSRRCalc(config)
    
  rSQLJumlah = GetJumlahPeserta(config, ID_SRRCalc) #ambil jumlah peserta yang dapat bagi hasil bulan ini    
  rSQL = GetPeserta(config, ID_SRRCalc) #ambil semua peserta yang dapat bagi hasil bulan ini
  
  #siapkan objek Parameter Biaya default
  TotalDana = 1.0;  i = 0; n = rSQLJumlah.JumlahPeserta 
  rSQL.First()
  config.BeginTransaction()
  try:  
    f = CreateLogFile(config, tglHitung)
    try:
      while not rSQL.Eof:
        config.SendDebugMsg(rSQL.no_peserta)
        FixValue, kode_jenis_transaksi = GetParameter(config, classJenisBiaya, rSQL.SRR)
        TotalDana = rSQL.AKUM_DANA_IURAN_PK + rSQL.AKUM_DANA_IURAN_PST + \
          rSQL.AKUM_DANA_PENGEMBANGAN + rSQL.akum_dana_peralihan            
        besarBiaya = HitungBiaya(config, classJenisBiaya, rSQL, kode_jenis_transaksi, tglHitung, FixValue, TotalDana)            
        f.write('nomor peserta:%s|biaya:%s|total dana:%s|SRR:%s\n'%(rSQL.no_peserta, besarBiaya, TotalDana, rSQL.SRR))          
        #bikin transaksi DPLK-nya plus authorize it
        CreateBiayaTahunan(config, classJenisBiaya, tglHitung, idBatch, rSQL.no_peserta, besarBiaya)          
#         config.FlushUpdates()        
        i += 1
        rSQL.Next()
    finally:
      f.close()

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
  idBatch = parameter.FirstRecord.idbatch
  code = parameter.FirstRecord.code
  y,m,d = config.ModLibUtils.DecodeDate(parameter.FirstRecord.tglhitung)
  tglHitung = [y,m,d]
  
  if code == 1:
    nameBiayaMasal = 'Biaya Administrasi Tahunan'
    classJenisBiaya = 'BiayaAdmTahunan'
  elif code == 2:
    nameBiayaMasal = 'Biaya Pengelolaan Dana'
    classJenisBiaya = 'BiayaPengelolaanDana'
  
  consoleID = classJenisBiaya + '_' + str(pid)

  sJobName = '%s. TaskID = %s' % (nameBiayaMasal,pid)
  app.WriteConsole(sJobName + ': mulai berlangsung\r\n')
  try:
    app.CreateConsole(consoleID, 'progress')
    try:
      app.SwitchDefaultConsole(consoleID)      
            
      #main task right here
      Main(config, tglHitung, idBatch, classJenisBiaya)

      app.WriteConsole(sJobName + ': telah selesai\r\n')
    finally:
      app.CloseConsole(consoleID)
  except:
    app.WriteConsole(sJobName + ': Error\r\n' + str(sys.exc_info()[1]) + '\r\n')
    raise
