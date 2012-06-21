import sys, time, logging, string

# DEFAULT
DATAPERPAGE = 10

def PrepareLogger(config, tgl_registrasi):
  logger = logging.getLogger('dplk07')
  sBaseFileName = 'DPLMAST_%s_%s.txt' % (
    config.FormatDateTime('yyyymmdd', tgl_registrasi)
    , config.FormatDateTime('yyyymmdd', config.Now())
  )
  hdlr = logging.FileHandler(config.UserHomeDirectory + sBaseFileName)
  formatter = logging.Formatter('%(message)s')
  hdlr.setFormatter(formatter)
  logger.addHandler(hdlr) 
  logger.setLevel(logging.INFO)
  logger.info('START %s' % config.FormatDateTime('hh:nn:ss.zzz', config.Now()))

  return logger

def WriteErrorToLog(config, msg, logger):
  logger.error(msg)

def WritePesertaToLog(config, rph, logger):
  dpl_mast = rph.Packet.GetDatasetByName('dpl_mast')
  for i in range(dpl_mast.RecordCount):
    rec = dpl_mast.GetRecord(i)
    logger.info(rec.infos)

def CekPesertaSdhTersimpan(config, rSQL, logger, sessionID):
  lsNomPst = []

  rSQL.First()
  while not rSQL.Eof:
    lsNomPst.append('\'%s\'' % (rSQL.NO_PESERTA))
    rSQL.Next()
  config.SendDebugMsg('lsNomPst '+ str(lsNomPst))

  #remote eksekusi
  try:
    for i in range(0, len(lsNomPst), DATAPERPAGE):
      param = config.AppObject.CreateValues(\
        ['lsNomPst', "(%s)" % (string.join(lsNomPst[i:i+DATAPERPAGE], ', '))]
      )
      rph = config.AppObject.rexecscript(sessionID, 'remote/CekPesertaSdhTersimpan', param, 1)
      recStatus = rph.Packet.GetDatasetByName('status').GetRecord(0)
      if recStatus.IsErr:
        msg = str(recStatus.ErrMessage)
        WriteErrorToLog(config, msg, logger)
        raise '\nError Cek Peserta: ', msg

      WritePesertaToLog(config, rph, logger)

#     stop = len(lsNomPst) <= DATAPERPAGE
#     while not stop:
#       param = config.AppObject.CreateValues(\
#         ['lsNomPst', '(%s)' % (string.join(lsNomPst[:DATAPERPAGE], ', '))]
#       )
#       rph = config.AppObject.rexecscript(sessionID, 'remote/CekPesertaSdhTersimpan', param, 1)
#       recStatus = rph.Packet.GetDatasetByName('status').GetRecord(0)
#       if recStatus.IsErr:
#         msg = str(recStatus.ErrMessage)
#         WriteErrorToLog(config, msg, logger)
#         raise '\nError Cek Peserta: ', msg
# 
#       WritePesertaToLog(config, rph, logger)
# 
#       stop = lsNomPst.index(recStatus.prevNomPst) < (len(lsNomPst)-1)
# 
#       # end while not stop

  except:
    raise

  # kembalikan posisi rSQL ke paling awal
  rSQL.First()

def CreatingPacket(config, dtTglTransaksi, tTglTransaksi, sessionID):
  #definisikan dahulu paket: record peserta dengan kode paketnya
  ph = config.AppObject.CreatePacket()
  packet = ph.Packet
  packet.AddDataPacketStructureEx('__ListPeserta', \
    'noPeserta:string;namaPeserta:string;kodePaket:string;kodeCabang:string')
  packet.BuildAllStructure()

  #ambil HistoriGiroHarian dan HistoriGiro dari tabel
  y,m,d = config.ModLibUtils.DecodeDate(dtTglTransaksi)
  sSQL = 'select n.NO_PESERTA, \
                 n.NAMA_LENGKAP, \
                 r.KODE_PAKET_INVESTASI, \
                 r.KODE_CAB_DAFTAR \
          from NasabahDPLK n, RekeningDPLK r \
          where DATEPART(year,n.tgl_registrasi) = %d and \
                DATEPART(month,n.tgl_registrasi) = %d and \
                DATEPART(day,n.tgl_registrasi) = %d and \
                n.NO_PESERTA = r.NO_PESERTA \
          order by r.KODE_PAKET_INVESTASI, n.NO_PESERTA' \
          % (y,m,d)
  rSQL = config.CreateSQL(sSQL).RawResult

  logger = PrepareLogger(config, dtTglTransaksi)
  CekPesertaSdhTersimpan(config, rSQL, logger, sessionID)
  logger.info('END')

  #siapkan dataset list peserta
  ds = packet.AddNewDataset('__ListPeserta')

  #progress = config.ProgressTracker
  #progress.ProgressLevel1()

  rSQL.First()
  i = 1
  while not rSQL.Eof:
    #progress.SetProgressInfo2(1, 'Memproses %d peserta: ' % (i))

    rec = ds.AddRecord()
    rec.noPeserta = rSQL.NO_PESERTA
    rec.namaPeserta = rSQL.NAMA_LENGKAP
    rec.kodePaket = rSQL.KODE_PAKET_INVESTASI
    #kode cabang diambil 3 karakter pertama, disesuaikan dengan CoreBanking
    rec.kodeCabang = rSQL.KODE_CAB_DAFTAR[:3]

    #inkremen progres level 1
    i += 1

    rSQL.Next()

  return ph

def Main(config, dtTglTransaksi, tTglTransaksi):
  config.BeginTransaction()
  try:
    #cek login core banking
    isNeedLoginCoreBanking = config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING', \
      'NeedLoginCoreBanking')
    if isNeedLoginCoreBanking == 'T':
      #allowed login core banking, kirim paket ke CoreBanking
      sessionID = config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING', 'AppName') + \
        config.SecurityContext.UserID

      #buat packet dan isinya
      param = CreatingPacket(config, dtTglTransaksi, tTglTransaksi, sessionID)
  
      #remote eksekusi kirim peserta DPLK core banking
      try:
        config.SendDebugMsg('sessionID '+ str(sessionID))
        rph = config.AppObject.rexecscript(sessionID, 'remote/KirimPesertaDPLK', param, 1)
        if rph.FirstRecord.IsErr:
          raise '\nError kirim peserta ke CoreBanking',str(rph.FirstRecord.ErrMessage)
      except:
        raise

    #update jumlah peserta objek HistoriKirimPeserta
    oHKP = config.CreatePObject('HistoriKirimPeserta')
#     y,m,d = time.localtime()[:3]
#     oHKP.Tanggal_Kirim = config.ModLibUtils.EncodeDate(y,m,d)
    oHKP.Tanggal_Kirim = config.Now()
    y,m,d = tTglTransaksi[:3]
    oHKP.Tanggal_Terdaftar = config.ModLibUtils.EncodeDate(y,m,d)
    oHKP.Jumlah_Peserta = param.packet.__ListPeserta.RecordCount
    oHKP.User_ID = config.SecurityContext.UserID

    #save to DB
    config.FlushUpdates()

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

  consoleID = 'SendPeserta_' + str(pid)

  sJobName = '%s. TaskID = %s' % ('Kirim Data Peserta ke Core Banking',pid)
  #app.WriteConsole(sJobName + ': mulai berlangsung\r\n')
  
  #fileLog = open(config.GetHomeDir()[:-1]+'trackedtasks/'+consoleID,'w')
  app.ConWriteln(sJobName + ': mulai berlangsung', monfilename)
  
  try:
    #app.CreateConsole(consoleID, 'progress')
    try:
      #app.SwitchDefaultConsole(consoleID)

      #main task right here
      Main(config, dtTglTransaksi, tTglTransaksi)

      #app.WriteConsole(sJobName + ': telah selesai\r\n')
      app.ConWriteln(sJobName + ': telah selesai', monfilename)
  
    finally:
      #app.CloseConsole(consoleID)
      pass
  except:
    #app.WriteConsole(sJobName + ': Error\r\n' + str(sys.exc_info()[1]) + '\r\n')
    app.ConWriteln(sJobName + ': Error '+ str(sys.exc_info()[1]))
    raise
