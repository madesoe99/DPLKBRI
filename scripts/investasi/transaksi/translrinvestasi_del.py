# hapus transaksi piutang investasi

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  id = parameter.FirstRecord.id

  oTransLRInvestasi = config.CreatePObjImplProxy('TransLRInvestasi')
  oTransLRInvestasi.Key = id

  config.BeginTransaction()
  try:
    oTransLRInvestasi.Delete()

    config.Commit()
  except:
    config.Rollback()
    raise

  return 1

