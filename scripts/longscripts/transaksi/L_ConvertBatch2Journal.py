import sys
sys.path.append('c:/dafapp/dplk07/scripts/appinterface')
sys.path.append('c:/dafapp/dplk07/script_modules')

import CreateCandidateJournalItem, transaksiapi

def ConvertingBatch2Journal(config, tIDBatch):
  app = config.AppObject
  config.SendDebugMsg('convb2j_1')
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
  
  #progress = config.ProgressTracker
  #progress.ProgressLevel1()
  #progress.ProgressLevel2()

  config.SendDebugMsg('convb2j_2')
  #proses batch satu-persatu
  for idBatch in tIDBatch:      
    config.SendDebugMsg('convb2j_3')
    oTB.Key = idBatch
    app.ConWriteln('Proses Batch : %s' %oTB.no_batch,'status')

    #progress.SetProgressInfo2(1, 'Memproses Batch DPLK nomor %s: ' % (oTB.no_batch))

    #KEY RULE
    #1 batch == 1 jurnal == 1 blok jurnal
    
    #buat kandidat jurnal baru
    recCJ = dsCJ.AddRecord()
    recCJ.keterangan = 'Konversi transaksi Batch DPLK nomor %s' % (oTB.no_batch)
    
    config.SendDebugMsg('convb2j_4')
    #cek list transaksi yang dimiliki sesuai dengan tipe batch
    if (oTB.batch_type == 'R' and oTB.Ls_IuranPendaftaran.MemberCount > 0) or \
      (oTB.batch_type == 'T' and oTB.Ls_TransaksiDPLK.MemberCount > 0) or \
      (oTB.batch_type == 'P' and oTB.Ls_TransaksiPremi.MemberCount > 0) or \
      (oTB.batch_type == 'I' and oTB.Ls_TransaksiInvestasi.MemberCount > 0):
      #batch berisi transaksi, tidak kosong transaksi  
      config.SendDebugMsg('convb2j_5')
              
      #assign kandidat blok ke record kandidat jurnal baru
      dsCJB = recCJ.journalBlocks

      #buat kandidat jurnal blok (batch) yang akan dikirim
      recCJB = dsCJB.AddRecord()
      recCJB.subSystemCode = 'DPLK07'
      recCJB.classID = 'TransactionBatch'
      recCJB.keyID = idBatch
      recCJB.accountLinkType = oTB.account_link_type

      config.SendDebugMsg('convb2j_6')
      #assign kandidat item jurnal ke record kandidat blok jurnal baru
      dsCJI = recCJB.journalItems
      
      #kirim dataset journal item milik record journal block recCJB 
      config.SendDebugMsg('convb2j_7')
      CreateCandidateJournalItem.AddingTransaksiBatchToDataSet(config, dsCJI, oTB)        
      config.SendDebugMsg('convb2j_8')

    config.SendDebugMsg('convb2j_3')
  
  #kirimkan dataset kandidat jurnal(+item jurnal) ke Accounting
  #ambil info untuk rlogin dan kirimkan paketnya
  ServerName,AppName,Session_Name,UserID,Password = \
      transaksiapi.GetLoginAkuntansi(config)[:5]

  #run creating Jurnal with remote exec
  config.SendDebugMsg('cb2j_1')
  config.SendDebugMsg('ServerName: '+ str(ServerName))
  config.SendDebugMsg('AppName: '+ str(AppName))
  config.SendDebugMsg('UserID: '+ str(UserID))
  #config.SendDebugMsg('password: '+ str(Password))
  config.SendDebugMsg('Session_Name: '+ str(Session_Name))
  app.ConWriteln('Kirim ke accounting','status')
  config.BeginTransaction()
  try:
    config.AppObject.rlogin(ServerName,AppName,UserID,Password,Session_Name)
    try:      
      config.SendDebugMsg('cb2j_3')
      rPH = config.AppObject.rexecscript(Session_Name,'appinterface/RemoteCreateJournal',\
        ph, 0)
      config.SendDebugMsg('cb2j_32')
    finally:
      config.SendDebugMsg('cb2j_4')
      config.AppObject.rlogout(Session_Name)
  
    config.SendDebugMsg('cb2j_5')
    #update journal block id untuk masing-masing batch
    dsJB = rPH.Packet.GetDatasetByName('__JournalBlock')
  
    for i in range(dsJB.RecordCount):
      recJB = dsJB.GetRecord(i)
      oTB.Key = recJB.idBatch
      oTB.journal_block_id = recJB.journalBlockID
    
    config.Commit()
  except:
    config.Rollback()
    raise
  ##
##

def DAFLongScriptMain(config, parameter, pid, monfilename):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # pid: Process ID of this script
  # monfilename: Monitor file name to store status

  app = config.AppObject
  consoleID = 'KonversiBatchDPLK_' + str(pid)
  sJobName = '%s. TaskID = %s' % ('Konversi Batch ke Jurnal',pid)
  #app.WriteConsole(sJobName + ': mulai berlangsung\r\n')
  #fileLog = open(config.GetHomeDir()[:-1]+'trackedtasks/'+consoleID,'w')
  app.ConWriteln(sJobName + ': mulai berlangsung', monfilename)
  try:
    #app.CreateConsole(consoleID, 'progress')
    try:
      config.SendDebugMsg('cb2j_01')
      #app.SwitchDefaultConsole(consoleID)      

      #main task right here
      tIDBatch = []
      recInfo = parameter.FirstRecord

      config.SendDebugMsg('cb2j_02')
      if recInfo.isSingle:
        #mode konversi satuan
        tIDBatch.append(recInfo.idBatchSingle)
      else:
        #mode konversi rentang        
        y0,m0,d0 = config.ModLibUtils.DecodeDate(recInfo.tglAwal)
        y1,m1,d1 = config.ModLibUtils.DecodeDate(recInfo.tglAkhir)
        
        sSQL = 'select ID_TransactionBatch from TransactionBatch where ' \
          'tgl_used >= \'%s\' and tgl_used <= \'%s\' and account_link_type = \'S\' and '\
          'batch_status = \'C\' and journal_block_id is null order by ID_TransactionBatch' \
          % ('%d-%d-%d' % (y0,m0,d0),'%d-%d-%d' % (y1,m1,d1))
        rSQL = config.CreateSQL(sSQL).RawResult
        
        rSQL.First()
        while not rSQL.Eof:
          tIDBatch.append(rSQL.ID_TransactionBatch)
          rSQL.Next()
      
      config.SendDebugMsg('cb2j_03')
      #prosesi konversi batch
      ConvertingBatch2Journal(config, tIDBatch)

      #app.WriteConsole(sJobName + ': telah selesai\r\n')
      app.ConWriteln(sJobName + ': telah selesai', monfilename)
    finally:
      #app.CloseConsole(consoleID)
      pass#fileLog.close()
  except:
    #app.WriteConsole(sJobName + ': Error\r\n' + str(sys.exc_info()[1]) + '\r\n')
    app.ConWriteln(sJobName + ': Error\r\n' + str(sys.exc_info()[1]) + '\r\n', monfilename)
    raise
