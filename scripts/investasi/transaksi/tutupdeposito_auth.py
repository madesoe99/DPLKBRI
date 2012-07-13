import com.ihsan.util.modman as modman

#moduleapi = modman.getModule(config, 'moduleapi')
#TransactInv = modman.getModule(config, 'TransactInv')

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

  oTransPiutangLRInvestasi.LIndukTransaksiInvestasi = oTransPiutangInvestasi

  return oTransPiutangLRInvestasi

def CreatePenaltiTutup(config, oTutupDeposito):
  oTransLRInvestasi = config.CreatePObject('TransLRInvestasi')
  oTransLRInvestasi.LInvestasi = oTutupDeposito.LDeposito
  oTransLRInvestasi.LTransactionBatch = oTutupDeposito.LTransactionBatch
  oTransLRInvestasi.kode_jns_investasi = oTutupDeposito.kode_jns_investasi
  oTransLRInvestasi.kode_jenis_trinvestasi = 'D' # biaya
  oTransLRInvestasi.kode_subjns_LRInvestasi = 'A-PEN' # penalti penutupan deposito
  moduleapi = modman.getModule(config, 'moduleapi')
  oTransLRInvestasi.tgl_transaksi = moduleapi.DateTimeTupleToFloat(config, oTutupDeposito.tgl_transaksi)
  oTransLRInvestasi.mutasi_debet = oTutupDeposito.penalti
  oTransLRInvestasi.mutasi_kredit = 0.0
  oTransLRInvestasi.isCommitted = 'T'

  oTransLRInvestasi.tgl_sistem = moduleapi.DateTimeTupleToFloat(config, oTutupDeposito.tgl_sistem)
  oTransLRInvestasi.tgl_otorisasi = moduleapi.DateTimeTupleToFloat(config, oTutupDeposito.tgl_otorisasi)
  oTransLRInvestasi.user_id = oTutupDeposito.user_id
  oTransLRInvestasi.user_id_auth = oTutupDeposito.user_id_auth
  oTransLRInvestasi.terminal_id = oTutupDeposito.terminal_id
  oTransLRInvestasi.terminal_id_auth = oTutupDeposito.terminal_id_auth
  oTransLRInvestasi.no_bilyet = oTutupDeposito.LDeposito.no_bilyet

  oDeposito = oTutupDeposito.LDeposito
  oDeposito.akum_LR -= oTutupDeposito.penalti

  return oTransLRInvestasi

def CloseInvestasi(config, oTransPiutangInvestasi):
  oInvestasi = oTransPiutangInvestasi.LInvestasi

  oInvestasi.status = 'F'
  moduleapi = modman.getModule(config, 'moduleapi')
  oInvestasi.tgl_tutup = moduleapi.DateTimeTupleToFloat(config, oTransPiutangInvestasi.tgl_transaksi)
  #oInvestasi.akum_nominal = 0.0
  TransactInv = modman.getModule(config, 'TransactInv')
  TransactInv.CreateRincianBagiHasil(config, oInvestasi, oInvestasi.akum_LR, True)
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
    if oTransPiutangInvestasi.LInvestasi.akum_piutangLR != 0.0 :
      oTransPiutangLRInvestasi = CreateTransPiutangLRInvestasi(config, oTransPiutangInvestasi)

    #oTutupDeposito = oTransPiutangInvestasi.CastAs('TutupDeposito')
    #if oTutupDeposito.penalti >= moduleapi.zero_approx:
    #  oTransLRInvestasi = CreatePenaltiTutup(config, oTutupDeposito)
    #  oTransPiutangLRInvestasi.LTransLRInvestasi = oTransLRInvestasi

    CloseInvestasi(config, oTransPiutangInvestasi)

    config.Commit()
  except:
    config.Rollback()
    raise

  return 1