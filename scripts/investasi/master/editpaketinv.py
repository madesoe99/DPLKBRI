def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)
  
  dsPI = parameter.GetDatasetByName('uipPaketInvestasi')
  recPI = dsPI.GetRecord(0)

  dsRPI = parameter.GetDatasetByName('uipRincianPaketInvestasi')
  
  config.BeginTransaction()
  try:
    oPI = config.CreatePObjImplProxy('PaketInvestasi')
    oPI.Key = recPI.kode_paket_investasi
    oPI.nama_paket_investasi = recPI.nama_paket_investasi
    oPI.acc_giro = recPI.acc_giro
    oPI.acc_iuran = recPI.acc_iuran
    oPI.acc_kedplklain = recPI.acc_kedplklain
    oPI.acc_manfaat = recPI.acc_manfaat
    oPI.acc_pengembangan = recPI.acc_pengembangan
    oPI.acc_peralihan = recPI.acc_peralihan
    oPI.isAktif = recPI.isAktif

    oPI.no_giro = recPI.no_giro
    oPI.dana_idle = recPI.dana_idle
    oPI.total_potensi_profit = recPI.total_potensi_profit
    oPI.total_srr = recPI.total_srr
    oPI.user_id = recPI.user_id
    oPI.last_update = recPI.last_update

    strSQL = \
      'delete from RincianPaketInvestasi '\
      'where kode_paket_investasi = \'%s\' '\
      % (recPI.kode_paket_investasi)
    config.ExecSQL(strSQL)
    
    for i in range(dsRPI.RecordCount):
      recRPI = dsRPI.GetRecord(i)

      oRPI = config.CreatePObject('RincianPaketInvestasi')
      oRPI.kode_paket_investasi = recPI.kode_paket_investasi
      oRPI.kode_jns_investasi = recRPI.GetFieldByName('LJenisInvestasi.kode_jns_investasi')
      oRPI.maks_proporsi = recRPI.maks_proporsi

    config.Commit()
  except:
    raise
    config.Rollback()


  return 1
