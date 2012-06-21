def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  kode_jns_investasi = parameter.FirstRecord.kode_jns_investasi

  config.BeginTransaction()
  try:
    oJenisInvestasi = config.CreatePObjImplProxy('JenisInvestasi')
    oJenisInvestasi.Key = kode_jns_investasi
    Ls_SubJnsTransLRInvestasi = oJenisInvestasi.Ls_SubJnsTransLRInvestasi
    Ls_SubJnsTransLRInvestasi.DeleteAllPObjs()
    oJenisInvestasi.Delete()

    config.Commit()
  except:
    config.Rollback()
    raise

  return 1
