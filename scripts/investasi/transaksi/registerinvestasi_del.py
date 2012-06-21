def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  id = parameter.FirstRecord.id

  oRegisterInvestasi = config.CreatePObjImplProxy('RegisterInvestasi')
  oRegisterInvestasi.Key = id

  config.BeginTransaction()
  try:
    oRegisterInvestasi.Ls_RincianRegisterInvestasi.DeleteAllPObjs()
    oRegisterInvestasi.Delete()

    config.Commit()
  except:
    config.Rollback()
    raise

  return 1

