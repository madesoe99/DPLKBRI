import com.ihsan.util.modman as modman

#moduleapi = modman.getModule(config, 'moduleapi')

def CreateTransPiutangLRInvestasi(config, oTransLRInvestasi):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  oTransPiutangLRInvestasi = config.CreatePObject('TransPiutangLRInvestasi')
  oTransPiutangLRInvestasi.LInvestasi = oTransLRInvestasi.LInvestasi
  oTransPiutangLRInvestasi.LTransactionBatch = oTransLRInvestasi.LTransactionBatch
  oTransPiutangLRInvestasi.kode_jenis_trinvestasi = 'P' # pendapatan investasi ke piutang
  oTransPiutangLRInvestasi.tgl_transaksi = moduleapi.DateTimeTupleToFloat(config, oTransLRInvestasi.tgl_transaksi)
  oTransPiutangLRInvestasi.mutasi_debet = oTransLRInvestasi.mutasi_kredit
  oTransPiutangLRInvestasi.mutasi_kredit = 0.0
  oTransPiutangLRInvestasi.isCommitted = 'T'

  oTransPiutangLRInvestasi.tgl_sistem = moduleapi.DateTimeTupleToFloat(config, oTransLRInvestasi.tgl_sistem)
  oTransPiutangLRInvestasi.tgl_otorisasi = moduleapi.DateTimeTupleToFloat(config, oTransLRInvestasi.tgl_otorisasi)
  oTransPiutangLRInvestasi.user_id = oTransLRInvestasi.user_id
  oTransPiutangLRInvestasi.user_id_auth = oTransLRInvestasi.user_id_auth
  oTransPiutangLRInvestasi.terminal_id = oTransLRInvestasi.terminal_id
  oTransPiutangLRInvestasi.terminal_id_auth = oTransLRInvestasi.terminal_id_auth

  oTransPiutangLRInvestasi.LTransLRInvestasi = oTransLRInvestasi

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
    oTransLRInvestasi.no_bilyet = oInvestasi.no_bilyet

    CreateTransPiutangLRInvestasi(config, oTransLRInvestasi)

    oInvestasi.akum_LR = oInvestasi.akum_LR + oTransLRInvestasi.mutasi_kredit
    oInvestasi.akum_piutangLR = oInvestasi.akum_piutangLR + oTransLRInvestasi.mutasi_kredit
    oInvestasi.last_update = config.Now()

    config.Commit()
  except:
    config.Rollback()
    raise

  return 1

