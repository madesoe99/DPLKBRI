import com.ihsan.util.modman as modman

#moduleapi = modman.getModule(config, 'moduleapi')
#TransactInv = modman.getModule(config, 'TransactInv')

##bagian rolover
def RolloverInvestasi(config, oTransPiutangInvestasi, tt):
  oInvestasi = oTransPiutangInvestasi.LInvestasi
  oDeposito = oInvestasi.CastAs('Deposito')
  y,m,d = oDeposito.tgl_jatuh_tempo[:3]
  JT = config.ModDateTime.EncodeDate(y,m,d)
  if int(JT-10) < int(tt) or oDeposito.jenisJatuhTempo in (0,1):
    moduleapi = modman.getModule(config, 'moduleapi')
    moduleapi.AdvanceJatuhTempo(config, oDeposito)
  

def SetTransPiutangInvestasi(config, oTransPiutangInvestasi):
  oTransPiutangInvestasi.isCommitted = 'T'
  oTransPiutangInvestasi.tgl_otorisasi = config.Now()
  oTransPiutangInvestasi.user_id_auth = config.SecurityContext.userid
  oTransPiutangInvestasi.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]
  oTransPiutangInvestasi.no_bilyet = oTransPiutangInvestasi.LInvestasi.no_bilyet

def CreateTransPiutangLRInvestasiRO(config, isKapitalisir, oDeposito, ID_TransactionBatch, oRolloverDeposito = None):
#def CreateTransPiutangLRInvestasiRO(config, isKapitalisir, oDeposito, oTransPiutangLRInvestasi):
  # mengurangi piutang pendapatan
  
  oTransPiutangLRInvestasi = config.CreatePObject('TransPiutangLRInvestasi')
  oTransPiutangLRInvestasi.ID_TransactionBatch = ID_TransactionBatch
  if isKapitalisir:
    #oRolloverDeposito.Delete()
    oTransPiutangLRInvestasi.LTransPiutangInvestasi = oRolloverDeposito

    oRolloverDeposito.LInvestasi = oDeposito
    oRolloverDeposito.kode_jns_investasi = 'D' # rollover investasi
    oRolloverDeposito.kode_jenis_trinvestasi = 'F' # rollover investasi
    oRolloverDeposito.tgl_transaksi = config.Now()
    oRolloverDeposito.isCommitted = 'T'

    oRolloverDeposito.mutasi_debet = oDeposito.akum_piutangLR
    oRolloverDeposito.mutasi_kredit = 0.0

  oTransPiutangLRInvestasi.LInvestasi = oDeposito
  oTransPiutangLRInvestasi.no_bilyet = oDeposito.no_bilyet
  oTransPiutangLRInvestasi.kode_jns_investasi = 'D' # rollover investasi
  oTransPiutangLRInvestasi.kode_jenis_trinvestasi = 'F' # rollover investasi
  oTransPiutangLRInvestasi.tgl_transaksi = config.Now()
  oTransPiutangLRInvestasi.isCommitted = 'T'

  # menolkan akum_piutangLR di objek investasi melalui mutasi kredit senilai tersebut
  oTransPiutangLRInvestasi.mutasi_debet = 0.0
  oTransPiutangLRInvestasi.mutasi_kredit = oDeposito.akum_piutangLR

  oTransPiutangLRInvestasi.tgl_sistem = config.Now()
  oTransPiutangLRInvestasi.tgl_otorisasi = config.Now()
  oTransPiutangLRInvestasi.user_id = config.SecurityContext.userid
  oTransPiutangLRInvestasi.user_id_auth = config.SecurityContext.userid
  oTransPiutangLRInvestasi.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oTransPiutangLRInvestasi.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]

  oTransPiutangLRInvestasi.LIndukTransaksiInvestasi = oRolloverDeposito

  return oTransPiutangLRInvestasi

def KapitalisirInvestasi(config, oDeposito, oRolloverDeposito):
  CreateTransPiutangLRInvestasiRO(config, 1, oDeposito, oRolloverDeposito.ID_TransactionBatch,oRolloverDeposito)
  #CreateTransPiutangLRInvestasiRO(config, 1, oDeposito, oRolloverDeposito)

  piutang = oDeposito.akum_piutangLR
  oDeposito.akum_nominal += (oDeposito.akum_piutangLR or 0.0)
  oDeposito.akum_piutangLR = 0.0
  
  TransactInv = modman.getModule(config, 'TransactInv')
  #TransactInv.CreateRincianBagiHasil(config, oDeposito, -piutang)
  TransactInv.CreateRincianPokok(config, oDeposito, piutang)
  

def RolloverNonKapitalisir(config, oDeposito, oRolloverDeposito, isKapitalisir, nom):
  if not isKapitalisir :
    #CreateTransPiutangLRInvestasiRO(config, 0, oDeposito, oRolloverDeposito.ID_TransactionBatch)
    oDeposito.akum_piutangLR = 0.0
  # tidak ada transaksi kapitalisir,
  # artinya tidak ada penambahan ke pokok
  oRolloverDeposito.Delete()
  
  
def RolloverMain(config, oDeposito, oBatch,  isKapitalisir, nom, tgl_transaksi):

  #oTransPiutangInvestasi = config.CreatePObjImplProxy('TransPiutangInvestasi')
  #oTransPiutangInvestasi.Key = id
  oTransPiutangInvestasi = config.CreatePObject('RolloverDeposito')
  oTransPiutangInvestasi.LTransactionBatch = oBatch
  oTransPiutangInvestasi.LInvestasi = oDeposito
  y,m,d = oDeposito.tgl_jatuh_tempo[:3]
  JT = config.ModDateTime.EncodeDate(y,m,d)
  y,m,d = tgl_transaksi[:3]
  tt = config.ModDateTime.EncodeDate(y,m,d)
  if int(JT-10) > int(tt) and oDeposito.jenisJatuhTempo == 1:
     raise Exception, '\nPERINGATAN' + 'Deposito belum jatuh tempo'
  
  oDeposito.rollover_counter += 1
  RolloverInvestasi(config, oTransPiutangInvestasi,tt)
  #moduleapi.AdvanceJatuhTempo(config, oDeposito)
  
  if isKapitalisir and (oDeposito.rollover_counter >= oDeposito.jenisJatuhTempo \
    or oDeposito.jenisJatuhTempo == 0) :
    SetTransPiutangInvestasi(config, oTransPiutangInvestasi)
    
    KapitalisirInvestasi(config, oDeposito, oTransPiutangInvestasi)
    oDeposito.rollover_counter = 0
  else:
    RolloverNonKapitalisir(config, oDeposito, oTransPiutangInvestasi, isKapitalisir, nom)
    
  oDeposito.last_update = config.Now()

  return 1


##end rolover
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

  oTransPiutangLRInvestasi.LIndukTransaksiInvestasi = oBagiHasilDeposito

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
    if oDeposito.kapitalisir_rollover == 'T' :
      CreateTransPiutangLRInvestasi(config, oBagiHasilDeposito)
      oDeposito.akum_piutangLR += oBagiHasilDeposito.nominal
    #jika kapitalisir
    #if oDeposito.kapitalisir_rollover == 'T' :
    #   oDeposito.akum_nominal += oBagiHasilDeposito.nominal
       
    oDeposito.akum_LR += oBagiHasilDeposito.nominal
    TransactInv = modman.getModule(config, 'TransactInv')
    TransactInv.CreateRincianBagiHasil(config, oDeposito, oBagiHasilDeposito.nominal)
    
    oDeposito.last_update = config.Now()
    RolloverMain(config, oDeposito, oBagiHasilDeposito.LTransactionBatch, \
       oDeposito.kapitalisir_rollover == 'T', oBagiHasilDeposito.nominal, oBagiHasilDeposito.tgl_transaksi)
    config.Commit()
  except:
    config.Rollback()
    raise

  return 1

