import com.ihsan.util.modman as modman

#moduleapi = modman.getModule(config, 'moduleapi')

def CreateTransPiutangLRInvestasi(config, oBagiHasilDeposito):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  oTransPiutangLRInvestasi = config.CreatePObject('TransPiutangLRInvestasi')
  oTransPiutangLRInvestasi.LInvestasi = oBagiHasilDeposito.LDeposito
  oTransPiutangLRInvestasi.no_bilyet = oBagiHasilDeposito.LDeposito.no_bilyet
  oTransPiutangLRInvestasi.LTransactionBatch = oBagiHasilDeposito.LTransactionBatch
  oTransPiutangLRInvestasi.kode_jns_investasi = oBagiHasilDeposito.LDeposito.kode_jns_investasi
  oTransPiutangLRInvestasi.kode_jenis_trinvestasi = 'E' # piutang bagi hasil deposito
  oTransPiutangLRInvestasi.tgl_transaksi = moduleapi.DateTimeTupleToFloat(config, oBagiHasilDeposito.tgl_transaksi)
  oTransPiutangLRInvestasi.mutasi_debet = oBagiHasilDeposito.nominal
  oTransPiutangLRInvestasi.mutasi_kredit = 0.0
  oTransPiutangLRInvestasi.isCommitted = 'T'

  oTransPiutangLRInvestasi.tgl_sistem = moduleapi.DateTimeTupleToFloat(config, oBagiHasilDeposito.tgl_sistem)
  oTransPiutangLRInvestasi.tgl_otorisasi = moduleapi.DateTimeTupleToFloat(config, oBagiHasilDeposito.tgl_otorisasi)
  oTransPiutangLRInvestasi.user_id = oBagiHasilDeposito.user_id
  oTransPiutangLRInvestasi.user_id_auth = oBagiHasilDeposito.user_id_auth
  oTransPiutangLRInvestasi.terminal_id = oBagiHasilDeposito.terminal_id
  oTransPiutangLRInvestasi.terminal_id_auth = oBagiHasilDeposito.terminal_id_auth

  oTransPiutangLRInvestasi.LTransLRInvestasi = oBagiHasilDeposito

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  id = parameter.FirstRecord.id

  oBagiHasilDeposito = config.CreatePObjImplProxy('BagiHasilDeposito')
  oBagiHasilDeposito.Key = id
  oDeposito = oBagiHasilDeposito.LDeposito

  config.BeginTransaction()
  try:
    oBagiHasilDeposito.isCommitted = 'T'
    oBagiHasilDeposito.tgl_otorisasi = config.Now()
    oBagiHasilDeposito.user_id_auth = config.SecurityContext.userid
    oBagiHasilDeposito.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]
    oBagiHasilDeposito.no_bilyet = oDeposito.no_bilyet
    oBagiHasilDeposito.kode_subjns_LRInvestasi = 'A'

    # bagi hasil non tunai (belum kapitalisir), masih dianggap piutang pendapatan
    CreateTransPiutangLRInvestasi(config, oBagiHasilDeposito)

    oDeposito.akum_piutangLR += oBagiHasilDeposito.nominal
    oDeposito.akum_LR += oBagiHasilDeposito.nominal
    oDeposito.last_update = config.Now()

    config.Commit()
  except:
    config.Rollback()
    raise

  return 1