import sys
sys.path.append('c:/dafapp/dplk07/scripts/appinterface')
sys.path.append('c:/dafapp/dplk07/script_modules')

import CreateCandidateJournalItem, transaksiapi

def CreateSingleRecord(config, dataset, rSQL, mode, key, ket, origin_batch, debit, credit):
  if debit <> 0.0 or credit <> 0.0:
    rec = dataset.AddRecord()
    if mode == 'Giro':
      rec.accountCode = key
    else:
      o = config.CreatePObjImplProxy(mode)
      o.Key = key
      rec.accountCode = o.account_code
      
    rec.keterangan = ket
    rec.branchCode = config.SysVarIntf.GetStringSysVar('SETTINGAKUNTANSI', \
      'BranchCodeTransaksi')
    rec.currencyCode = config.SysVarIntf.GetStringSysVar('SETTINGAKUNTANSI', \
      'DefaultCurrency')
    rec.originBatch = origin_batch
    rec.debit = debit
    rec.credit = credit

def CreatePairOfRecord(config, dataset, rSQL, oMG):
  #buat pasangan 1
  dictKet = {'F':'TOLAKAN', 'T':'BERHASIL'}
  dictKet2 = {2:'reversal', 1:'dari aplikasi DPLK / Biller', 0:'dari input manual KIBLAT'}
  ket = 'Akumulasi transaksi %s %s nomor Giro DPLK %s' % (dictKet[rSQL.isTransaksiCreated], dictKet2[rSQL.Transaksi_Peserta], oMG.no_giro)
  ket2 = 'Histori akumulasi transaksi %s %s nomor Giro DPLK %s' % (dictKet[rSQL.isTransaksiCreated], dictKet2[rSQL.Transaksi_Peserta], oMG.no_giro)
  origin_batch = str(rSQL.ID_HISTORIGIROHARIAN) + ';' + str(rSQL.TRANSAKSI_PESERTA)

  if rSQL.KODE_MNEMONIC == 'C':
    debet = rSQL.sum_nominal_giro; credit = 0.0
  else: # transaksi debet 
    debet = 0.0; credit = rSQL.sum_nominal_giro
  CreateSingleRecord(config, dataset, rSQL, 'Giro', rSQL.ACC_GIRO, ket, origin_batch, debet, credit)
  if rSQL.isTransaksiCreated == 'F':
    CreateSingleRecord(config, dataset, rSQL, 'Giro', oMG.acc_histori_giro, ket2, origin_batch, credit, debet)
  else:
    if rSQL.ACC_GIRO == '11206': #pendaftaran
       CreateSingleRecord(config, dataset, rSQL, 'GLInterface', 'BBN_DAFTAR', ket2, origin_batch, credit, debet)
    else:
      if rSQL.ACC_GIRO == '11215': #premi
       CreateSingleRecord(config, dataset, rSQL, 'GLInterface', 'KW_PREMI', ket2, origin_batch, credit, debet)
      else: #iuran
       CreateSingleRecord(config, dataset, rSQL, 'GLInterface', 'KW_IURAN', ket2, origin_batch, credit, debet)
                
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
  sSQL = "select hgh.ID_HISTORIGIROHARIAN,\
                 hgh.ACC_GIRO,\
                 hg.KODE_MNEMONIC, \
                 hg.TRANSAKSI_PESERTA,\
                 hg.isTransaksiCreated,\
                 SUM(hg.NOMINAL) as sum_nominal_giro\
          from HISTORIGIROHARIAN hgh, HISTORIGIRO hg\
          where hgh.TANGGAL_HISTORI = '%s' and \
                hgh.ID_HISTORIGIROHARIAN = hg.ID_HISTORIGIROHARIAN and \
                hgh.ACC_GIRO <> '11208' \
          group by hgh.ID_HISTORIGIROHARIAN,\
                   hgh.ACC_GIRO,\
                   hg.KODE_MNEMONIC,\
                   hg.TRANSAKSI_PESERTA,\
                   hg.isTransaksiCreated\
          order by hgh.ID_HISTORIGIROHARIAN"\
          % ('%d-%d-%d' % (y,m,d))
  rSQL = config.CreateSQL(sSQL).RawResult

  #preparing objek MasterGiro dan kandidat item jurnal
  oMG = config.CreatePObjImplProxy('MasterGiro')
  
  #siapkan dataset kandidat jurnal
  dsCJ = packet.AddNewDataset('__CandJournal')

  #progress = config.ProgressTracker
  #progress.ProgressLevel1()

  lastID_HISTORIGIROHARIAN = 'inisialisasi pertama'
  rSQL.First()
  while not rSQL.Eof:
    oMG.Key = rSQL.ACC_GIRO

    #progress.SetProgressInfo2(1, 'Memproses Acc Giro %s: ' % (rSQL.ACC_GIRO))
    
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
      ph,0)
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
  #app.WriteConsole(sJobName + ': mulai berlangsung\r\n')
  
  #fileLog = open(config.GetHomeDir()[:-1]+'trackedtasks/'+consoleID,'w')
  app.ConWriteln(sJobName + ': mulai berlangsung', monfilename)
  try:
    #app.CreateConsole(consoleID, 'progress')
    try:
      #app.SwitchDefaultConsole(consoleID)      
            
      #main task right here
      Main(config, dtTglTransaksi)

      #app.WriteConsole(sJobName + ': telah selesai\r\n')
      app.ConWriteln(sJobName + ': telah selesai', monfilename)
    finally:
      #app.CloseConsole(consoleID)
      pass#fileLog.close()
  except:
    #app.WriteConsole(sJobName + ': Error\r\n' + str(sys.exc_info()[1]) + '\r\n')
    app.ConWriteln(sJobName + ': error ', monfilename)
    raise
