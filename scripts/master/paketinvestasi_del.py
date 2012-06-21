def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  kode_paket_investasi = parameter.FirstRecord.kode_paket_investasi
  
  config.BeginTransaction()
  try:
    oPaketInvestasi = config.CreatePObjImplProxy('PaketInvestasi')
    oPaketInvestasi.Key = kode_paket_investasi
    Ls_RincianPaketInvestasi = oPaketInvestasi.Ls_RincianPaketInvestasi
    Ls_RincianPaketInvestasi.DeleteAllPObjs()
    oPaketInvestasi.Delete()

    config.Commit()
  except:
    config.Rollback()
    raise

  return 1
