def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  id = parameter.FirstRecord.id

  oRegisterCIF = config.CreatePObjImplProxy('RegisterCIF')
  oRegisterCIF.Key = id
  
  config.BeginTransaction()
  try:
    if oRegisterCIF.kode_jenis_registercif == 'W':
      oRegisterAhliWaris = oRegisterCIF.CastAs('RegisterAhliWaris')
      oRegisterAhliWaris.Ls_RegisterAhliWarisDetail.DeleteAllPObjs()
    elif oRegisterCIF.kode_jenis_registercif == 'P':
      oRPPI = oRegisterCIF.CastAs('RegisterPindahPaketInvestasi')
      oRPPI.Ls_RegPindahPaketDetil.DeleteAllPObjs()

    oRegisterCIF.Delete()

    config.Commit()
  except:
    config.Rollback()
    raise

  return 1
