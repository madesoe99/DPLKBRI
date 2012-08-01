import com.ihsan.util.modman as modman

#transaksiapi = modman.getModule(config, 'transaksiapi')

def CekKode(config, kode, nama_field, nama_tabel):
  sSQL = "select * from %s where %s = '%s'" % (nama_tabel, nama_field, kode)
  rSQL = config.CreateSQL(sSQL).RawResult
  
  return not rSQL.Eof

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)
  
  ada = CekKode(
    config
    , parameter.FirstRecord.kode      
    , parameter.FirstRecord.nama_field
    , parameter.FirstRecord.nama_tabel
  )

  returnpacket.CreateValues(
    ['ada', ada]
  )

  return 1
