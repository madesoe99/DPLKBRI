
def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  rec = parameter.FirstRecord
  id = rec.id
  flag = rec.flag
  config.BeginTransaction()
  try:
    o = config.CreatePObjImplProxy('TransaksiDPLK')
    o.key = id
    o.Flag_Pilih = flag
    config.Commit()
  except:
    config.Rollback()
    raise

  return 1
