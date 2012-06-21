def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  id = parameter.FirstRecord.id

  oRegEditNasabahDPLKCorporate = config.CreatePObjImplProxy('RegEditNasabahDPLKCorporate')
  oRegEditNasabahDPLKCorporate.Key = id

  config.BeginTransaction()
  try:
    if oRegEditNasabahDPLKCorporate.operation_code == 'E':
      oNasabahDPLKCorporate = oRegEditNasabahDPLKCorporate.LNasabahDPLKCorporate
      oNasabahDPLKCorporate.operation_code = 'F'

    oRegEditNasabahDPLKCorporate.Delete()

    config.Commit()
  except:
    config.Rollback()
    raise

  return 1

