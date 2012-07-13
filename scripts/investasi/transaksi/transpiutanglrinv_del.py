# hapus transaksi piutang investasi

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  id = parameter.FirstRecord.id

  oTransPiutangLRInvestasi = config.CreatePObjImplProxy('TransPiutangLRInvestasi')
  oTransPiutangLRInvestasi.Key = id

  config.BeginTransaction()
  try:
    oTransPiutangLRInvestasi.Delete()

    config.Commit()
  except:
    config.Rollback()
    raise

  return 1

