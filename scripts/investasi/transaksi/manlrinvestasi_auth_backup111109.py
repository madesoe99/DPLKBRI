def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  id = parameter.FirstRecord.id

  oTransLRInvestasi = config.CreatePObjImplProxy('TransLRInvestasi')
  oTransLRInvestasi.Key = id
  oInvestasi = oTransLRInvestasi.LInvestasi

  config.BeginTransaction()
  try:
    oTransLRInvestasi.isCommitted = 'T'
    oTransLRInvestasi.tgl_otorisasi = config.Now()
    oTransLRInvestasi.user_id_auth = config.SecurityContext.userid
    oTransLRInvestasi.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]

    if oInvestasi.kode_jns_investasi == 'A':
      # deposito
      oTransLRInvestasi.no_bilyet = oInvestasi.no_bilyet
    elif oInvestasi.kode_jns_investasi == 'B':
      # obligasi
      oObligasi = oInvestasi.CastAs('Obligasi')
      oTransLRInvestasi.nama_investasi = oObligasi.nama_obligasi
    elif oInvestasi.kode_jns_investasi == 'C':
      # Reksadana
      oReksadana = oInvestasi.CastAs('Reksadana')
      oTransLRInvestasi.nama_investasi = oReksadana.nama_reksadana
    else:
      raise Exception, 'Kesalahan Otorisasi' + 'Kode jenis investasi \'%s\' tidak dikenali.' % (str(oInvestasi.kode_jns_investasi))

    oInvestasi.akum_LR += oTransLRInvestasi.mutasi_kredit - oTransLRInvestasi.mutasi_debet
    oInvestasi.last_update = config.Now()

    config.Commit()
  except:
    config.Rollback()
    raise

  return 1

