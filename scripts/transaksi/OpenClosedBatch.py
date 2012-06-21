import sys
sys.path.append('c:/dafapp/dplk07/script_modules')

import transaksiapi

def ProcessOpen(config, id_batch):

  #ambil informasi batas tanggal tutup batch
  oP = config.CreatePObjImplProxy('Parameter')
  oP.Key = 'BATAS_TGL_TUTUP_BATCH'
  dtTglBatchMaks = oP.Numeric_Value
  
  #cek tanggal pakai batch yang akan dibuka kembali
  oTB = config.CreatePObjImplProxy('TransactionBatch')
  oTB.Key = id_batch
  dtTglPakaiBatch = config.ModLibUtils.EncodeDate(oTB.tgl_used[0],oTB.tgl_used[1],\
    oTB.tgl_used[2])
  if dtTglPakaiBatch <= dtTglBatchMaks:
    #tanggal pakai batch lebih dulu daripada batas tgl maksimal batch
    #pembukaan kembali batch tidak diperbolehkan
    raise '\nPERINGATAN','Batch dengan Tanggal Pakai lebih awal dari tanggal terakhir ' \
      'Bagi Hasil yakni %s,\ntidak diperbolehkan untuk dibuka kembali.' \
      % (oP.Varchar_Value) 
   
  sSQL = 'update TransactionBatch set batch_status = \'O\' where ' \
    'batch_status = \'C\' and ID_TransactionBatch = %d' % (id_batch)
  rSQL = config.ExecSQL(sSQL)
  
  oTB = config.CreatePObjImplProxy('TransactionBatch')
  oTB.Key = id_batch
  
  if not oTB.IsFieldNull('journal_block_id'):
    #ambil info untuk rlogin & lakukan notify
    ServerName,AppName,Session_Name,UserID,Password = \
      transaksiapi.GetLoginAkuntansi(config)[:5]
  
    #run notify EDIT status with remote exec 
    config.AppObject.rlogin(ServerName,AppName,UserID,Password,Session_Name)
    try:      
      config.AppObject.rexecscript(Session_Name,'appinterface/NotifyBlockStatus',\
        config.AppObject.CreateValues(['journalblockid',oTB.journal_block_id],\
        ['status','E']),1)
    finally:
      config.AppObject.rlogout(Session_Name)       
  
  return 1

def ProcessOpenAll(config):

  sSQL = 'update TransactionBatch set batch_status = \'O\' where ' \
    'batch_status = \'C\''
  rSQL = config.ExecSQL(sSQL)
  
  return 1

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  id_batch = parameter.FirstRecord.idbatch
  
  config.BeginTransaction()
  try:
    if id_batch != None and id_batch != '':
      #open transaction batch dengan batch id tertentu 
      succeedStatus = ProcessOpen(config, id_batch)
    else:
      #open all transaction batch
      #fungsi sakti ini masih DISEMBUNYIKAN KEBERADAANNYA!!!
      succeedStatus = ProcessOpenAll(config)
      
    config.Commit()
    config.FlushUpdates()
  except:
    config.Rollback()
    raise
  
  returnpacket.CreateValues(['status',succeedStatus])

  return 1
