import com.ihsan.util.modman as modman

#moduleapi = modman.getModule(config, 'moduleapi')

def CreateInvestasi(config, oRegisterInvestasi):
  oInvestasi = config.CreatePObject('Investasi')
  oInvestasi.no_bilyet = oRegisterInvestasi.no_bilyet
  oInvestasi.kode_pihak_ketiga = oRegisterInvestasi.kode_pihak_ketiga
  oInvestasi.kode_paket_investasi = oRegisterInvestasi.kode_paket_investasi
  oInvestasi.kode_jns_investasi = oRegisterInvestasi.kode_jns_investasi
  moduleapi = modman.getModule(config, 'moduleapi')
  oInvestasi.tgl_buka = moduleapi.DateTimeTupleToFloat(config, oRegisterInvestasi.tgl_buka)
  oInvestasi.nominal_pembukaan = oRegisterInvestasi.nominal
  oInvestasi.akum_nominal = oRegisterInvestasi.nominal
  oInvestasi.akum_LR = 0.0
  oInvestasi.akum_piutangLR = 0.0
  oInvestasi.rollover_counter = 0
  oInvestasi.status = 'T'

  oInvestasi.tgl_otorisasi = config.Now()
  oInvestasi.last_update = config.Now()
  oInvestasi.user_id = oRegisterInvestasi.user_id
  oInvestasi.user_id_auth = config.SecurityContext.userid
  oInvestasi.terminal_id = oRegisterInvestasi.terminal_id
  oInvestasi.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]
  
  return oInvestasi

def CreateTransPiutangInvestasi(config, oInvestasi, oRegisterInvestasi):
  oTransPiutangInvestasi = config.CreatePObject('TransPiutangInvestasi')
  oTransPiutangInvestasi.LInvestasi = oInvestasi
  oTransPiutangInvestasi.LTransactionBatch = oRegisterInvestasi.LTransactionBatch
  oTransPiutangInvestasi.kode_jenis_trinvestasi = oInvestasi.kode_jns_investasi #'A' # buat investasi baru
  moduleapi = modman.getModule(config, 'moduleapi')
  oTransPiutangInvestasi.tgl_transaksi = moduleapi.DateTimeTupleToFloat(config, oInvestasi.tgl_buka)
  oTransPiutangInvestasi.mutasi_debet = oInvestasi.akum_nominal
  oTransPiutangInvestasi.mutasi_kredit = 0.0
  oTransPiutangInvestasi.isCommitted = 'T'

  oTransPiutangInvestasi.tgl_sistem = config.Now()
  oTransPiutangInvestasi.tgl_otorisasi = config.Now()
  oTransPiutangInvestasi.user_id = oInvestasi.user_id
  oTransPiutangInvestasi.user_id_auth = oInvestasi.user_id_auth
  oTransPiutangInvestasi.terminal_id = oInvestasi.terminal_id
  oTransPiutangInvestasi.terminal_id_auth = oInvestasi.terminal_id_auth

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  id = parameter.FirstRecord.id

  oRegisterInvestasi = config.CreatePObjImplProxy('RegisterInvestasi')
  oRegisterInvestasi.Key = id

  config.BeginTransaction()
  try:
    oInvestasi = CreateInvestasi(config, oRegisterInvestasi)
    CreateTransPiutangInvestasi(config, oInvestasi, oRegisterInvestasi)

    oRegisterInvestasi.Delete()

    config.Commit()
  except:
    config.Rollback()
    raise

  return 1

