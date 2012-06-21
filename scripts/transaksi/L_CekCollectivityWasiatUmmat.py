def Main(config, dtTglChecking):

  #perlu mencari peserta wasiat ummat aktif yang tidak membayar premi dibulan sebelumnya
  dtOneMonthBefore = config.ModLibUtils.IncMonth(dtTglChecking, -1)
  y0,m0 = config.ModLibUtils.DecodeDate(dtOneMonthBefore)[:2]
  
  sSQL = 'select rwu.NO_PESERTA, rwu.REKENINGWASIATUMMAT_ID \
          from REKENINGWASIATUMMAT rwu, REKENINGDPLK r \
          where rwu.NO_PESERTA = r.no_peserta and \
                r.STATUS_DPLK = \'A\' and \
                rwu.NO_PESERTA not in \
                    (select tp.NO_PESERTA from TRANSAKSIPREMI tp \
                     where tp.ISCOMMITTED = \'T\' and \
                           DATEPART(m, tp.TGL_TRANSAKSI) = %d and \
                           DATEPART(yyyy, tp.TGL_TRANSAKSI) = %d) \
          order by rwu.NO_PESERTA' \
          % (m0,y0)
  rSQL = config.CreateSQL(sSQL).RawResult
  
  progress = config.ProgressTracker
  progress.ProgressLevel1()

  config.BeginTransaction()
  try:
    rSQL.First()
    while not rSQL.Eof:
    
      progress.SetProgressInfo2(1, 'Memproses peserta %s: ' % (rSQL.no_peserta))    
      
      #ambil info besar premi di rekening wasiat ummat
      oRWU = config.CreatePObjImplProxy('RekeningWasiatUmmat')
      oRWU.Key = rSQL.rekeningwasiatummat_id
      
      #update kewajiban wasiat ummat peserta = nilai besar premi
      #update juga status collectivity-nya
      oR = config.CreatePObjImplProxy('RekeningDPLK')
      oR.Key = rSQL.no_peserta
      oR.kewajiban_wasiat_ummat = oR.kewajiban_wasiat_ummat + oRWU.besar_premi
      oR.collectivity_wasiat_ummat = 'F'
      
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
  dtTglChecking = parameter.FirstRecord.tglChecking
  y,m,d = config.ModLibUtils.DecodeDate(dtTglChecking)
  tTglChecking = [y,m,d]
  
  consoleID = 'KolektibilitasWasiatUmmat_' + str(pid)

  sJobName = '%s. TaskID = %s' % ('Pengecekan Kolektibilitas Peserta Wasiat Ummat',pid)
  app.WriteConsole(sJobName + ': mulai berlangsung\r\n')
  try:
    app.CreateConsole(consoleID, 'progress')
    try:
      app.SwitchDefaultConsole(consoleID)      
            
      #main task right here
      Main(config, dtTglChecking)

      app.WriteConsole(sJobName + ': telah selesai\r\n')
    finally:
      app.CloseConsole(consoleID)
  except:
    app.WriteConsole(sJobName + ': Error\r\n' + str(sys.exc_info()[1]) + '\r\n')
    raise
