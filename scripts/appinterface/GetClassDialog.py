def GetFormDialogName(config, className):
  if className == 'TransactionBatch':
    formName = 'transaksi/fViewPickBatchDetail'
  elif className == 'HistoriGiroHarian':
    formName = 'transaksi/qViewDaftarHistoriGiro'
    
  return formName

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)
  
  try:
    formDialogName = GetFormDialogName(config,parameter.FirstRecord.classID) 
    returnpacket.CreateValues(['formName',formDialogName])    
  except:
    raise  

  return 1
