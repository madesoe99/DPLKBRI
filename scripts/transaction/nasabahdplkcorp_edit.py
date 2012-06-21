def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  kode_nasabah_corporate = parameter.FirstRecord.kode_nasabah_corporate

  config.BeginTransaction()
  try:
    oNasabahDPLKCorporate = config.CreatePObjImplProxy('NasabahDPLKCorporate')
    oNasabahDPLKCorporate.Key = kode_nasabah_corporate

    oRegEditNasabahDPLKCorporate = config.CreatePObject('RegEditNasabahDPLKCorporate')
    oRegEditNasabahDPLKCorporate.kode_nasabah_corporate = oNasabahDPLKCorporate.kode_nasabah_corporate

    config.Commit()
  except:
    config.Rollback()
    raise

  return 1

