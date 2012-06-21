import sys
sys.path.append('c:/dafapp/dplk07/script_modules')

import transaksiapi

def ProcessClose(config, id_batch):
  #return berupa jumlah transaksi yang belum terotorisasi
  #return 0, berarti transaksi sudah terotorisasi semuanya
  
  #cek transaksi belum terotorisasi dalam batch
  notYetAuthorized = 0
  oTB = config.CreatePObjImplProxy('TransactionBatch')
  oTB.Key = id_batch
  
  #cek tipe batch
  if oTB.batch_type == 'R':
    #batch registrasi
    listTransaksi = oTB.Ls_IuranPendaftaran
  elif oTB.batch_type == 'T':
    #batch transaksi
    listTransaksi = oTB.Ls_TransaksiDPLK
  elif oTB.batch_type == 'P':
    #batch premi
    listTransaksi = oTB.Ls_TransaksiPremi
  elif oTB.batch_type == 'I':
    #batch premi
    listTransaksi = oTB.Ls_TransaksiInvestasi
    
  #cari transaksi belum terotorisasi dalam batch
  listTransaksi.First()
  while not listTransaksi.EndOfList:
    oTransaksi = listTransaksi.CurrentElement
    if oTransaksi.isCommitted == 'F':
      notYetAuthorized += 1
    
    listTransaksi.Next()
  
  if not notYetAuthorized:
    if not oTB.IsFieldNull('journal_block_id'):
      #batch sudah punya journal_block_id, 
      #ambil info untuk rlogin & lakukan notify
      ServerName,AppName,Session_Name,UserID,Password = \
        transaksiapi.GetLoginAkuntansi(config)[:5]

      #run notify COMPLETE status with remote exec
      config.AppObject.rlogin(ServerName,AppName,UserID,Password,Session_Name)
      try:      
        config.AppObject.rexecscript(Session_Name,'appinterface/NotifyBlockStatus',\
          config.AppObject.CreateValues(['journalblockid',oTB.journal_block_id],\
          ['status','C']),1)
      finally:
        config.AppObject.rlogout(Session_Name)       
    
    #transaksi sudah terotorisasi semua, tutup batch 
    sSQL = 'update TransactionBatch set batch_status = \'C\' where ' \
      'batch_status = \'O\' and ID_TransactionBatch = %d' % (id_batch)
    rSQL = config.ExecSQL(sSQL)
    
    if rSQL < 0:
      raise 'Update status Batch gagal!' 
      
  return notYetAuthorized

def ProcessCloseAll(config, tgl_pakai):
  notYetAuthorized = 0
  
  #cek existence batch pada tgl_pakai
  sSQLBatch = 'select ID_TransactionBatch from TransactionBatch where '\
    'tgl_used = \'%s\'' % (tgl_pakai)
  rSQLBatch = config.CreateSQL(sSQLBatch).RawResult
  
  if not rSQLBatch.Eof: 
    #ada batch pada tgl_pakai, dapatkan semua batch OPEN pada tgl_pakai
    sSQLOpenBatch = 'select ID_TransactionBatch,no_batch,journal_block_id from '\
      'TransactionBatch where batch_status = \'O\' and tgl_used = \'%s\'' \
      % (tgl_pakai)
    rSQLOpenBatch = config.CreateSQL(sSQLOpenBatch).RawResult
    
    rSQLOpenBatch.First()
    while not rSQLOpenBatch.Eof:
      #batch berstatus terbuka masih ada, coba tutup satu2 semua batch tersebut
      
      #cek journal_block_id-nya
      if rSQLOpenBatch.journal_block_id in [None,0]:
        #ID JurnalBlock kosong, boleh lakukan proses close batch tersebut    
        notYetAuthorizedTransaction = \
          ProcessClose(config, rSQLOpenBatch.ID_TransactionBatch)
      else:
        #ID JurnalBlock kosong, skip tutup batch tersebut, inkremen notYetAuthorized 
        notYetAuthorized += 1
        
      if notYetAuthorizedTransaction != 0: 
        notYetAuthorized += 1
        config.SendDebugMsg('Batch bernomor %s masih memiliki transaksi belum '\
          'terotorisasi.' % (rSQLOpenBatch.no_batch))
      
      rSQLOpenBatch.Next()  
    #end while: yang tidak masuk while berarti semua batch sudah Tutup
    
    if not notYetAuthorized: 
      #transaksi sudah terotorisasi semuanya, tutup semua batch
      sSQL = 'update TransactionBatch set batch_status = \'C\' where ' \
        'batch_status = \'O\' and tgl_used = \'%s\'' % (tgl_pakai)
      rSQL = config.ExecSQL(sSQL)
  else:
    #batch not existence
    notYetAuthorized = -999
  
  return notYetAuthorized

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  id_batch = parameter.FirstRecord.idbatch
  tgl_pakai = parameter.FirstRecord.tglpakai
  
  config.BeginTransaction()
  try:
    if id_batch != None and id_batch != '':
      #close transaction batch dengan batch number tertentu 
      succeedStatus = ProcessClose(config, id_batch)
    else:
      #close all transaction batch
      succeedStatus = ProcessCloseAll(config, tgl_pakai)
      
    config.Commit()
    config.FlushUpdates()
  except:
    config.Rollback()
    raise
  
  #konvensi succeedStatus
  # 0 batch berhasil ditutup
  # > 0 berarti masih ada sejumlah batch yang belum ditutup atau sejulah transaksi
  #   yang belum diotorisasi
  # -999 kasus khusus tergantung context 
  
  returnpacket.CreateValues(['status',succeedStatus])

  return 1
