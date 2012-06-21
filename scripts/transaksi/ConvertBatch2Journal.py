import sys
sys.path.append('c:/dafapp/dplk07/scripts/appinterface')
sys.path.append('c:/dafapp/dplk07/script_modules')

import CreateCandidateJournalItem, transaksiapi

def ConvertingBatch2Journal(config, tIDBatch):
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
  
  #siapkan dataset kandidat blok jurnal
  dsCJ = packet.AddNewDataset('__CandJournal')

  #buat rangka objek TransactionBatch
  oTB = config.CreatePObjImplProxy('TransactionBatch') 
  
  try:
    #proses batch satu-persatu
    for idBatch in tIDBatch:      
      oTB.Key = idBatch
            
      #KEY RULE
      #1 batch == 1 jurnal == 1 blok jurnal
      
      #buat kandidat jurnal baru
      recCJ = dsCJ.AddRecord()
      recCJ.keterangan = 'Konversi transaksi Batch DPLK nomor %s' % (oTB.no_batch)
      
      #cek list transaksi yang dimiliki sesuai dengan tipe batch
      if (oTB.batch_type == 'R' and oTB.Ls_IuranPendaftaran.MemberCount > 0) or \
        (oTB.batch_type == 'T' and oTB.Ls_TransaksiDPLK.MemberCount > 0) or \
        (oTB.batch_type == 'P' and oTB.Ls_TransaksiPremi.MemberCount > 0) or \
        (oTB.batch_type == 'I' and oTB.Ls_TransaksiInvestasi.MemberCount > 0):
        #batch berisi transaksi, tidak kosong transaksi  
        
        #siapkan dataset kandidat blok jurnal baru
        dsCJB = packet.AddNewDataset('__CandJournalBlock')
        
        #assign kandidat blok ke record kandidat jurnal baru
        recCJ.journalBlocks = dsCJB
  
        #buat kandidat jurnal blok (batch) yang akan dikirim
        recCJB = dsCJB.AddRecord()
        recCJB.subSystemCode = 'DPLK07'
        recCJB.classID = 'TransactionBatch'
        recCJB.keyID = idBatch
        recCJB.accountLinkType = oTB.account_link_type

        #siapkan dataset kandidat item jurnal baru
        dsCJI = packet.AddNewDataset('__CandJournalItem')
        
        #assign kandidat item jurnal ke record kandidat blok jurnal baru
        recCJB.journalItems = dsCJI
  
        #kirim dataset journal item milik record journal block recCJB 
        CreateCandidateJournalItem.AddingTransaksiBatchToDataSet(config, dsCJI, oTB)        
    
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
      
    #update journal block id untuk masing-masing batch
    dsJB = rPH.Packet.GetDatasetByName('__JournalBlock')
    config.BeginTransaction()
    try:
      for i in range(dsJB.RecordCount):
        recJB = dsJB.GetRecord(i)
        oTB.Key = recJB.idBatch
        oTB.journal_block_id = recJB.journalBlockID
      
      config.Commit()
    except:
      config.Rollback()
      raise
            
  except:
    raise

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)
    
  try:
    #konversi paket berbentuk record menjadi tuple
    tIDBatch = []
    dsListIDBatch = parameter.GetDatasetByName('__ListIDBatch')
    for i in range(dsListIDBatch.RecordCount):
      tIDBatch.append(dsListIDBatch.GetRecord(i).ID_TransactionBatch)

    #prosesi konversi batch
    ConvertingBatch2Journal(config, tIDBatch)
  except:
    raise  

  return 1
