import sys, re

def SavePacket(config, historiSet, oHistoriGiroHarian, acc_giro):

  n = historiSet.RecordCount
  sGrossNomorPeserta = ''
  for i in range(n):
    histori = historiSet.GetRecord(i)
    
    #buat objek HistoriGiro
    oHG = config.CreatePObject('HistoriGiro')
    oHG.acc_giro = acc_giro
    oHG.ID_HistoriGiroHarian = oHistoriGiroHarian.ID_HistoriGiroHarian
    oHG.Nomor_Batch_CoreBanking = histori.NomorBatch
    oHG.Nomor_Urut = histori.NomorUrut
    oHG.Nomor_Referensi = histori.NomorReferensi        
    oHG.Kode_Mnemonic = histori.JenisMutasi
    oHG.Nominal = histori.Nominal
    oHG.Transaksi_Peserta = histori.TransaksiPeserta
    oHG.isTransaksiCreated = 'F'
    
    #proses nomor peserta (lebih baik pake Regex)
    if re.search('[0-9]+',histori.NomorPeserta):
      r = re.search('[0-9]+',histori.NomorPeserta)
      if len(r.group()) == 11:
        oHG.Nomor_Peserta = r.group()
	oHG.Keterangan = histori.NomorPeserta    
      else:
        oHG.Keterangan = histori.NomorPeserta    

  if n > 0:
    return histori.NomorUrut
  else:
    #packetnya kosong, tidak ada record
    return '-999'

def Main(config, dtTglTransaksi):
  #preparing session
  sessionID = config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING', 'AppName') + \
    config.SecurityContext.userID
  
  #ambil info semua giro DPLK
  sSQL = 'select acc_giro, acc_histori_giro, no_giro from MasterGiro '\
    'order by acc_giro'
  rSQL = config.CreateSQL(sSQL).RawResult

  progress = config.ProgressTracker
  progress.ProgressLevel1()
  progress.ProgressLevel2()
  
  config.BeginTransaction()
  try:
    rSQL.First()
    while not rSQL.Eof:
      progress.SetProgressInfo2(1, 'Memproses Giro %s: ' % (rSQL.no_giro))

      #ambil riwayat giro core banking (bagian yang pertama)
      param = config.AppObject.CreateValues(\
        ['FirstPage', 1],
        ['NomorRekening', rSQL.no_giro],
        ['TanggalTransaksi', dtTglTransaksi])
      ph = config.AppObject.rexecscript(sessionID,'remote/GetHistoriGiro',param,0)

      if not ph.packet.GetDataset(0).GetRecord(0).IsErr:
        #jika berhasil getting historiGiro
        progress.SetProgressInfo2(2, 'Memproses Giro %s return packet 1' \
          % (rSQL.no_giro))
        
        #buat objek oHistoriGiroHarian
        oHGH = config.CreatePObject('HistoriGiroHarian')
        oHGH.Tanggal_Histori = dtTglTransaksi
        oHGH.acc_giro = rSQL.acc_giro
        oHGH.isReconciled = oHGH.isTransactionProceed = 'F'
        config.FlushUpdates()
      
        #simpan paket pertama yang berhasil diambil
        lastNomorUrut = SavePacket(config, ph.Packet.histori, oHGH, rSQL.acc_giro)
        
      else:
        #ada error saat mengambil
        raise 'Error First GetHistoriGiro', \
          str(ph.packet.GetDataset(0).GetRecord(0).ErrMessage)      
      
      isLastPage = ph.packet.GetDataset(0).GetRecord(0).IsLastPage
      i = 2
      #while lastNomorUrut != '-999' and not isLastPage:
      while not isLastPage:
        #jika pengambilan pertama tidak kosong dan bukan lastpage
        #ambil riwayat giro core banking yang selanjutnya
        
        param = config.AppObject.CreateValues(\
            ['FirstPage', 0],
            ['NomorRekening', rSQL.no_giro],
            ['NomorUrut', lastNomorUrut],
            ['TanggalTransaksi', dtTglTransaksi])
        ph = config.AppObject.rexecscript(sessionID,'remote/GetHistoriGiro',param,0)
        
        if not ph.packet.GetDataset(0).GetRecord(0).IsErr:
          #jika berhasil getting historiGiro berikutnya
          progress.SetProgressInfo2(2, 'Memproses Giro %s return packet %d' \
            % (rSQL.no_giro,i))
          
          #simpan paket berikutnya yang berhasil diambil
          lastNomorUrut = SavePacket(config, ph.packet.histori, oHGH, rSQL.acc_giro)
      
          #cek is last page
          isLastPage = ph.packet.GetDataset(0).GetRecord(0).IsLastPage 
          
        else:
          #ada error saat mengambil
          raise 'Error First GetHistoriGiro', \
            str(ph.packet.GetDataset(0).GetRecord(0).ErrMessage)
            
        #inkremen progres level 2
        i += 1      
  
      rSQL.Next()

    config.Commit()
  except:
    config.Rollback()
    raise    
  
  return 1
  
def UpdateNominalSum(config, dtTglTransaksi):

  config.BeginTransaction()
  try:
    y,m,d = config.ModLibUtils.DecodeDate(dtTglTransaksi)[:3]
    sSQL = 'update HISTORIGIROHARIAN \
            set HISTORIGIROHARIAN.SUM_NOMINAL = \
                (select x.snk-x.snd as sum_nominal \
                 from (select sum_kredit.ID_HISTORIGIROHARIAN, \
                              isnull(sum_kredit.sum_nominal_kredit,0.0) as snk, \
                              isnull(sum_debit.sum_nominal_debit,0.0) as snd \
                       from (select SUM(hg.NOMINAL) as sum_nominal_kredit, \
                                    hg.ID_HISTORIGIROHARIAN \
                             from HISTORIGIRO hg \
                             where hg.KODE_MNEMONIC = \'C\' \
                             group by hg.ID_HISTORIGIROHARIAN) as sum_kredit \
                            full outer join \
                            (select SUM(hg.NOMINAL) as sum_nominal_debit, \
                                    hg.ID_HISTORIGIROHARIAN \
                             from HISTORIGIRO hg \
                             where hg.KODE_MNEMONIC = \'D\' \
                             group by hg.ID_HISTORIGIROHARIAN) as sum_debit \
                            on sum_debit.ID_HISTORIGIROHARIAN = \
                            sum_kredit.ID_HISTORIGIROHARIAN) as x \
                 where x.ID_HISTORIGIROHARIAN = HISTORIGIROHARIAN.ID_HISTORIGIROHARIAN) \
            where HISTORIGIROHARIAN.TANGGAL_HISTORI = \'%s\'' \
            % ('%d-%d-%d' % (y,m,d))
    rSQL = config.ExecSQL(sSQL)
  
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
  
  consoleID = 'GetHistoriGiro_' + str(pid)

  sJobName = '%s. TaskID = %s' % ('Ambil Riwayat Giro DPLK',pid)
  app.WriteConsole(sJobName + ': mulai berlangsung\r\n')
  try:
    app.CreateConsole(consoleID, 'progress')
    try:
      app.SwitchDefaultConsole(consoleID)      
            
      #main task right here
      Main(config, dtTglTransaksi)
      config.FlushUpdates()
      UpdateNominalSum(config, dtTglTransaksi)

      app.WriteConsole(sJobName + ': telah selesai\r\n')
    finally:
      app.CloseConsole(consoleID)
  except:
    app.WriteConsole(sJobName + ': Error\r\n' + str(sys.exc_info()[1]) + '\r\n')
    raise
