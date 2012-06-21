import sys
sys.path.append('c:/dafapp/dplk07/scripts/appinterface')
sys.path.append('c:/dafapp/dplk07/script_modules')

import CreateCandidateJournalItem, transaksiapi

def CreatePairOfRecord(config, dataset, rSQL, oMG):
  #buat pasangan 1
  rec = dataset.AddRecord()
  rec.accountCode = rSQL.ACC_GIRO
  rec.keterangan = 'Akumulasi transaksi nomor Giro DPLK %s' % (oMG.no_giro)
  
  #informasi branch code dan currency code ada di global variabel
  rec.branchCode = config.SysVarIntf.GetStringSysVar('SETTINGAKUNTANSI', \
    'BranchCodeTransaksi')
  rec.currencyCode = config.SysVarIntf.GetStringSysVar('SETTINGAKUNTANSI', \
    'DefaultCurrency')
  
  #origin batch diganti dengan origin HistoriGiroHarian;status settled/unsettled transaksi
  rec.originBatch = str(rSQL.ID_HISTORIGIROHARIAN) + ';' + str(rSQL.TRANSAKSI_PESERTA)
         
  if rSQL.KODE_MNEMONIC == 'C':
    rec.debit = rSQL.sum_nominal_giro 
    rec.credit = 0.0   
  else:
    #rSQL.KODE_MNEMONIC == 'D'
    rec.debit = 0.0
    rec.credit = rSQL.sum_nominal_giro
    
  #buat pasangan 2
  rec2 = dataset.AddRecord()
  rec2.accountCode = oMG.acc_histori_giro
  rec2.keterangan = 'Histori akumulasi transaksi nomor Giro DPLK %s' % (oMG.no_giro)
  rec2.branchCode = rec.branchCode
  rec2.currencyCode = rec.currencyCode
  rec2.originBatch = rec.originBatch
  
  rec2.debit = rec.credit
  rec2.credit = rec.debit
    
  return

def CreatingPacket(config, dtTglTransaksi):
  #definisikan dahulu paket: record kandidat item jurnal
  ph = config.AppObject.CreatePacket()
  packet = ph.Packet
  #structure originBatch berformat "AccountLinkTypeBatch:ID_TransactionBatch[:
  #JenisTransaksi:KodePaketInvestasi]"
  packet.AddDataPacketStructureEx('__CandJournalItem', \
    'accountCode:string;branchCode:string;currencyCode:string;'\
    'debit:float;credit:float;keterangan:string;originBatch:string;')
  packet.AddDataPacketStructureEx('__CandJournalBlock', \
    'subSystemCode:string;classID:string;keyID:integer;accountLinkType:string;'\
    'journalItems:__CandJournalItem;')
  packet.AddDataPacketStructureEx('__CandJournal', \
    'keterangan:string;journalItems:__CandJournalItem;'\
    'journalBlocks:__CandJournalBlock;')
  packet.BuildAllStructure()
    
  #ambil HistoriGiroHarian dan HistoriGiro dari tabel
  #pilih histori giro yang tidak memiliki informasi Nomor Peserta
  #dan yang sudah dibuatkan transaksinya
  y,m,d = config.ModLibUtils.DecodeDate(dtTglTransaksi)
  sSQL = 'select hgh.ID_HISTORIGIROHARIAN,\
                 hgh.ACC_GIRO,\
                 hg.TRANSAKSI_PESERTA,\
                 hg.KODE_MNEMONIC,\
                 SUM(hg.NOMINAL) as sum_nominal_giro\
          from HISTORIGIROHARIAN hgh, HISTORIGIRO hg\
          where hgh.TANGGAL_HISTORI = \'%s\' and\
                hg.NOMOR_PESERTA is null and\
                hgh.ID_HISTORIGIROHARIAN = hg.ID_HISTORIGIROHARIAN and \
                hg.isTransaksiCreated = \'T\' \
          group by hgh.ID_HISTORIGIROHARIAN,\
                   hgh.ACC_GIRO,\
                   hg.KODE_MNEMONIC,\
                   hg.TRANSAKSI_PESERTA\
          order by hgh.ID_HISTORIGIROHARIAN'\
          % ('%d-%d-%d' % (y,m,d))
  rSQL = config.CreateSQL(sSQL).RawResult

  #preparing objek MasterGiro dan kandidat item jurnal
  oMG = config.CreatePObjImplProxy('MasterGiro')
  
  #siapkan dataset kandidat jurnal
  dsCJ = packet.AddNewDataset('__CandJournal')

  progress = config.ProgressTracker
  progress.ProgressLevel1()

  lastID_HISTORIGIROHARIAN = 'inisialisasi pertama'
  rSQL.First()
  while not rSQL.Eof:
    oMG.Key = rSQL.ACC_GIRO

    progress.SetProgressInfo2(1, 'Memproses Acc Giro %s: ' % (rSQL.ACC_GIRO))
    
    #cek lastID_HISTORIGIROHARIAN
    if lastID_HISTORIGIROHARIAN != rSQL.ID_HISTORIGIROHARIAN:
      #switch / create newly kandidat jurnal
      
      #buat kandidat jurnal (1 jurnal == 1 blok jurnal == 1 id HistoriGiroHarian)
      recCJ = dsCJ.AddRecord()
      recCJ.keterangan = 'Riwayat transaksi nomor Giro DPLK %s' % (oMG.no_giro)
      dsCJB = recCJ.journalBlocks 
      dsCJI_Settled = recCJ.journalItems  

      #buat kandidat blok jurnal pertama kali / HGH sudah ganti
      recCJB = dsCJB.AddRecord()
      recCJB.subSystemCode = 'DPLK07'
      recCJB.classID = 'HistoriGiroHarian'
      recCJB.accountLinkType = 'S'
      recCJB.keyID = rSQL.ID_HISTORIGIROHARIAN
      
      #update nilai lastID_HISTORIGIROHARIAN
      lastID_HISTORIGIROHARIAN = rSQL.ID_HISTORIGIROHARIAN
      
      #ganti juga dataset untuk record item jurnalnya, jika transaksinya unsettled
      if not rSQL.TRANSAKSI_PESERTA:
        dsCJI_UnSettled = recCJB.journalItems      

    #pilah kandidat item jurnal yang settled dan unsettled
    #hanya pilih yang unsettled, skip yang settled
    if not rSQL.TRANSAKSI_PESERTA:
      #transaksi Giro unsettled
      dataset = dsCJI_UnSettled
    #else:
      #transaksi Giro settled
      #dataset = dsCJI_Settled
      
    #disini harusnya mulai pairing item jurnal
    CreatePairOfRecord(config, dataset, rSQL, oMG)
    
    rSQL.Next()

  return ph

def Main(config, dtTglTransaksi):
  #creating kandidat packet
  ph = CreatingPacket(config, dtTglTransaksi) 
  
  #kirimkan dataset kandidat jurnal(+item jurnal) ke Accounting
  #ambil info untuk rlogin dan kirimkan paketnya
  ServerName,AppName,Session_Name,UserID,Password = \
      transaksiapi.GetLoginAkuntansi(config)[:5] 
  
  #run creating Jurnal with remote exec
  config.AppObject.rlogin(ServerName,AppName,UserID,Password,Session_Name)
  try:      
    rPH = config.AppObject.rexecscript(Session_Name,'appinterface/RemoteCreateJournal',\
      ph,1)
  finally:
    config.AppObject.rlogout(Session_Name)

  #update journal block id untuk masing-masing HistoriGiroHarian  
  dsJB = rPH.Packet.GetDatasetByName('__JournalBlock')
  config.BeginTransaction()
  try:
    #buat rangka objek HistoriGiroHarian
    oHGH = config.CreatePObjImplProxy('HistoriGiroHarian') 

    for i in range(dsJB.RecordCount):
      recJB = dsJB.GetRecord(i)
      #kamuflase nama, anggap idBatch (TransactionBatch) sebagai 
      #ID_HistoriGiroHarian (HistoriGiroHarian) 
      oHGH.Key = recJB.idBatch
      oHGH.journal_blok_id = recJB.journalBlockID

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
  
  consoleID = 'KonversiHistoriGiro_' + str(pid)

  sJobName = '%s. TaskID = %s' % ('Konversi Giro DPLK ke Jurnal Akuntansi',pid)
  app.WriteConsole(sJobName + ': mulai berlangsung\r\n')
  try:
    app.CreateConsole(consoleID, 'progress')
    try:
      app.SwitchDefaultConsole(consoleID)      
            
      #main task right here
      Main(config, dtTglTransaksi)

      app.WriteConsole(sJobName + ': telah selesai\r\n')
    finally:
      app.CloseConsole(consoleID)
  except:
    app.WriteConsole(sJobName + ': Error\r\n' + str(sys.exc_info()[1]) + '\r\n')
    raise
