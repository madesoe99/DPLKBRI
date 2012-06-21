def FormSetDataEx(uideflist, parameter):
  config = uideflist.config
  recTB = uideflist.uipTransactionBatch.Dataset.AddRecord()
  
  oTB = config.CreatePObjImplProxy('TransactionBatch')
  oTB.Key = parameter.FirstRecord.keyID
  
  #set TransactionBatch
  recTB.ID_TransactionBatch = oTB.ID_TransactionBatch
  recTB.no_batch = oTB.no_batch
  recTB.batch_type = oTB.batch_type
  recTB.batch_sub_type = oTB.batch_sub_type
  recTB.batch_status = oTB.batch_status
  recTB.branch_code = oTB.branch_code
  
  recTB.tgl_create = config.ModLibUtils.EncodeDate(oTB.tgl_create[0],\
    oTB.tgl_create[1],oTB.tgl_create[2])
  recTB.tgl_used = config.ModLibUtils.EncodeDate(oTB.tgl_used[0],\
    oTB.tgl_used[1],oTB.tgl_used[2])

  return 0
