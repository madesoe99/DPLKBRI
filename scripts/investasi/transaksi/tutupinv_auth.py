import com.ihsan.util.modman as modman

#moduleapi = modman.getModule(config, 'moduleapi')

def SetTransPiutangInvestasi(config, oTransPiutangInvestasi):
  oTransPiutangInvestasi.isCommitted = 'T'
  oTransPiutangInvestasi.tgl_otorisasi = config.Now()
  oTransPiutangInvestasi.user_id_auth = config.SecurityContext.userid
  oTransPiutangInvestasi.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]
  oTransPiutangInvestasi.no_bilyet = oTransPiutangInvestasi.LInvestasi.no_bilyet

def CreateTransPiutangLRInvestasi(config, oTransPiutangInvestasi):
  oTransPiutangLRInvestasi = config.CreatePObject('TransPiutangLRInvestasi')
  oTransPiutangLRInvestasi.LInvestasi = oTransPiutangInvestasi.LInvestasi
  oTransPiutangLRInvestasi.LTransactionBatch = oTransPiutangInvestasi.LTransactionBatch
  oTransPiutangLRInvestasi.kode_jns_investasi = oTransPiutangInvestasi.kode_jns_investasi
  oTransPiutangLRInvestasi.kode_jenis_trinvestasi = 'C' # tutup investasi
  moduleapi = modman.getModule(config, 'moduleapi')
  oTransPiutangLRInvestasi.tgl_transaksi = moduleapi.DateTimeTupleToFloat(config, oTransPiutangInvestasi.tgl_transaksi)
  oTransPiutangLRInvestasi.mutasi_debet = 0.0
  oTransPiutangLRInvestasi.mutasi_kredit = oTransPiutangInvestasi.LInvestasi.akum_piutangLR
  oTransPiutangLRInvestasi.isCommitted = 'T'

  oTransPiutangLRInvestasi.tgl_sistem = moduleapi.DateTimeTupleToFloat(config, oTransPiutangInvestasi.tgl_sistem)
  oTransPiutangLRInvestasi.tgl_otorisasi = moduleapi.DateTimeTupleToFloat(config, oTransPiutangInvestasi.tgl_otorisasi)
  oTransPiutangLRInvestasi.user_id = oTransPiutangInvestasi.user_id
  oTransPiutangLRInvestasi.user_id_auth = oTransPiutangInvestasi.user_id_auth
  oTransPiutangLRInvestasi.terminal_id = oTransPiutangInvestasi.terminal_id
  oTransPiutangLRInvestasi.terminal_id_auth = oTransPiutangInvestasi.terminal_id_auth
  oTransPiutangLRInvestasi.no_bilyet = oTransPiutangLRInvestasi.LInvestasi.no_bilyet

  oTransPiutangLRInvestasi.LTransPiutangInvestasi = oTransPiutangInvestasi

def CloseInvestasi(config, oTransPiutangInvestasi):
  oInvestasi = oTransPiutangInvestasi.LInvestasi

  oInvestasi.status = 'F'
  moduleapi = modman.getModule(config, 'moduleapi')
  oInvestasi.tgl_tutup = moduleapi.DateTimeTupleToFloat(config, oTransPiutangInvestasi.tgl_transaksi)
  oInvestasi.akum_nominal = 0.0
  oInvestasi.akum_piutangLR = 0.0
  oInvestasi.last_update = config.Now()

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  id = parameter.FirstRecord.id

  oTransPiutangInvestasi = config.CreatePObjImplProxy('TransPiutangInvestasi')
  oTransPiutangInvestasi.Key = id

  config.BeginTransaction()
  try:
    SetTransPiutangInvestasi(config, oTransPiutangInvestasi)
    CreateTransPiutangLRInvestasi(config, oTransPiutangInvestasi)
    CloseInvestasi(config, oTransPiutangInvestasi)

    config.Commit()
  except:
    config.Rollback()
    raise

  return 1

