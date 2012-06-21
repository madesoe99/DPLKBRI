def CekHistoriKirimPeserta(config, tTglTransaksi):
  sSQL = 'select Tanggal_Kirim '\
    'from HistoriKirimPeserta '\
    'where Tanggal_Terdaftar = \'%s\'' % ('%d-%d-%d' % (tTglTransaksi[0],\
    tTglTransaksi[1],tTglTransaksi[2]))
  rSQL = config.CreateSQL(sSQL).RawResult
    
  return not rSQL.Eof
  
def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  dtTglTransaksi = parameter.FirstRecord.tglTransaksi
  tTglTransaksi = config.ModLibUtils.DecodeDate(dtTglTransaksi)
  
  try:
    result = CekHistoriKirimPeserta(config, tTglTransaksi)      
  except:
    raise
  
  returnpacket.CreateValues(['isExist',result])

  return 1
