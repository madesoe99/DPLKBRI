import sys
sys.path.append('c:/dafapp/dplk07/script_modules')

import moduleapi, transaksiapi

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
  
  #ambil jumlah peserta aktif yang tanggal registrasinya < tglHitung
  sSQLJumlah = 'select count(n.no_peserta) as JumlahPeserta \
          from NASABAHDPLK n, REKENINGDPLK r \
          where r.STATUS_DPLK = \'A\' and \
                n.tgl_registrasi < \'%s\' and \
                n.no_peserta = r.no_peserta;' \
          % ('%d-%d-%d' % (tglHitung[0],tglHitung[1],tglHitung[2]))
  rSQLJumlah = config.CreateSQL(sSQLJumlah).RawResult
  
  #ambil semua peserta aktif yang tanggal registrasinya < tglHitung
  sSQL = 'select n.no_peserta, r.AKUM_DANA_IURAN_PK, r.AKUM_DANA_IURAN_PST, \
                 r.AKUM_DANA_PENGEMBANGAN, r.akum_dana_peralihan \
          from NASABAHDPLK n, REKENINGDPLK r \
          where r.STATUS_DPLK = \'A\' and \
                n.no_peserta = r.no_peserta and \
                n.tgl_registrasi < \'%s\' \
          order by n.no_peserta;' % ('%d-%d-%d' % (tglHitung[0],tglHitung[1],tglHitung[2]))
  config.SendDebugMsg('SQL = ' + sSQL)
  rSQL = config.CreateSQL(sSQL).RawResult
  
  #siapkan objek Parameter Biaya default
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
    oP.Key = 'PERSEN_BIAYA_PENGELOLAAN'
    FixValue = oP.Numeric_Value / 100      

  #progress = config.ProgressTracker
  #progress.ProgressLevel1()

  TotalDana = 1.0
  i = 0
  n = rSQLJumlah.JumlahPeserta
  rSQL.First()
  config.BeginTransaction()
  try:
    while not rSQL.Eof:
      #progress.SetProgressInfo1(1,i+1,n)
      config.SendDebugMsg(rSQL.no_peserta)  
      #tentukan proporsi biaya
      if classJenisBiaya == 'BiayaPengelolaanDana':          
        proporsiBiaya = transaksiapi.HitungProporsiBiaya(config, kode_jenis_transaksi, \
            rSQL.no_peserta, tglHitung)      
        TotalDana = rSQL.AKUM_DANA_IURAN_PK + rSQL.AKUM_DANA_IURAN_PST + \
          rSQL.AKUM_DANA_PENGEMBANGAN + rSQL.akum_dana_peralihan
        besarBiaya = proporsiBiaya * FixValue * TotalDana
        #besarBiaya = FixValue * TotalDana         
      else:
        proporsiBiaya = transaksiapi.HitungProporsiBiayaAdmTahunan(config, rSQL.no_peserta, tglHitung)      
        besarBiaya = proporsiBiaya * FixValue
        
      config.SendDebugMsg('proporsibiaya='+str(proporsiBiaya))
      config.SendDebugMsg('besarbiaya='+str(besarBiaya))
              
      #bikin transaksi DPLK-nya plus authorize it
      CreateBiayaTahunan(config, classJenisBiaya, tglHitung, idBatch, rSQL.no_peserta, \
        besarBiaya)
        
      config.FlushUpdates()
      
      i += 1
      rSQL.Next()

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
