def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  classID = parameter.FirstRecord.classID
  keyID = parameter.FirstRecord.keyID
  
  config.BeginTransaction()
  try:
    if classID == 'TransactionBatch':
      # cabut JournalBlockID dari TransactionBatch
      oTB = config.CreatePObjImplProxy(classID)
      oTB.Key = keyID
      oTB.SetFieldByName('journal_block_id', None) 
    elif classID == 'HistoriGiroHarian':
      # cabut JournalBlockID dari HistoriGiroHarian
      oTB = config.CreatePObjImplProxy(classID)
      oTB.Key = keyID
      oTB.SetFieldByName('journal_blok_id', None) 
    
    config.Commit()
  except:
    config.Rollback()
    raise
      
  return 1
