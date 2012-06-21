def otorTransPiutangInvestasi(config, id):
  oTransPiutangInvestasi = config.CreatePObjImplProxy('TransPiutangInvestasi')
  oTransPiutangInvestasi.Key = id
  oInvestasi = oTransPiutangInvestasi.LInvestasi

  oTransPiutangInvestasi.isCommitted = 'T'
  oTransPiutangInvestasi.tgl_otorisasi = config.Now()
  oTransPiutangInvestasi.user_id_auth = config.SecurityContext.userid
  oTransPiutangInvestasi.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]
  oTransPiutangInvestasi.no_bilyet = oInvestasi.no_bilyet

  oInvestasi.akum_nominal = oInvestasi.akum_nominal + oTransPiutangInvestasi.mutasi_debet
  oInvestasi.last_update = config.Now()

  return oTransPiutangInvestasi

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  id = parameter.FirstRecord.id

  config.BeginTransaction()
  try:
    otorTransPiutangInvestasi(config, id)

    config.Commit()
  except:
    config.Rollback()
    raise

  return 1

