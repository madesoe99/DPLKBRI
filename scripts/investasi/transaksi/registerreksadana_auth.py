import com.ihsan.util.modman as modman

#moduleapi = modman.getModule(config, 'moduleapi')

def CreateRincianReksadana(config, oReksadana):
  # buat satu objek rincianReksadana
  # karena dalam kasus Reksadana, satu Reksadana hanya mengacu ke satu paket saja (B)

  oRincianReksadana = config.CreatePObject('RincianReksadana')
  oRincianReksadana.LReksadana = oReksadana
  oRincianReksadana.kode_paket_investasi = oReksadana.kode_paket_investasi
  oRincianReksadana.Akum_Paket = oRincianReksadana.nominal = oReksadana.nominal_pembukaan
  oRincianReksadana.proporsi = 1
  oRincianReksadana.Akum_LR_Paket = 0.0
  

def CreateReksadana(config, oRegisterReksadana):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  oReksadana = config.CreatePObject('Reksadana')
  oReksadana.nama_reksadana = oRegisterReksadana.nama_reksadana
  oReksadana.kode_pihak_ketiga = oRegisterReksadana.kode_pihak_ketiga
  oReksadana.kode_paket_investasi = oRegisterReksadana.kode_paket_investasi
  oReksadana.kode_jns_investasi = oRegisterReksadana.kode_jns_investasi
  oReksadana.tgl_buka = moduleapi.DateTimeTupleToFloat(config, oRegisterReksadana.tgl_buka)
  oReksadana.nominal_pembukaan = oRegisterReksadana.nominal - oRegisterReksadana.biaya
  oReksadana.akum_nominal = oRegisterReksadana.nominal - oRegisterReksadana.biaya
  oReksadana.akum_LR = 0.0
  oReksadana.akum_piutangLR = 0.0
  oReksadana.rollover_counter = 0
  oReksadana.status = 'T'

  oReksadana.unit_penyertaan = 0.0#oRegisterReksadana.unit_penyertaan
  oReksadana.NAB_awal = oRegisterReksadana.NAB_awal
  oReksadana.NAB_Transaksi = 0.0 
  oReksadana.NAB = 0.0 #oRegisterReksadana.NAB
  oReksadana.kode_jns_reksadana = oRegisterReksadana.kode_jns_reksadana
  oReksadana.LCustodianBank = oRegisterReksadana.LCustodianBank

  oReksadana.LAccrual = oRegisterReksadana.LAccrual
  oReksadana.LBroker = oRegisterReksadana.LBroker
  oReksadana.LPayingAgent = oRegisterReksadana.LPayingAgent
  oReksadana.LSubJenisInv = oRegisterReksadana.LSubJenisInv
  
  oReksadana.tgl_otorisasi = config.Now()
  oReksadana.last_update = config.Now()
  oReksadana.user_id = oRegisterReksadana.user_id
  oReksadana.user_id_auth = config.SecurityContext.userid
  oReksadana.terminal_id = oRegisterReksadana.terminal_id
  oReksadana.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]

  # create rincian Reksadana
  CreateRincianReksadana(config, oReksadana)
  
  return oReksadana

def CreateTransPiutangInvestasi(config, oReksadana, oRegisterReksadana):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  oSubscribeReksadana = config.CreatePObject('SubscribeReksadana')
  oSubscribeReksadana.LInvestasi = oReksadana
  oSubscribeReksadana.nama_investasi = oReksadana.nama_reksadana
  oSubscribeReksadana.LTransactionBatch = oRegisterReksadana.LTransactionBatch
  oSubscribeReksadana.kode_jns_investasi = oRegisterReksadana.kode_jns_investasi#'C' # reksadana
  oSubscribeReksadana.kode_jenis_trinvestasi = 'S' # buat investasi baru, subscribe reksadana
  oSubscribeReksadana.tgl_transaksi = moduleapi.DateTimeTupleToFloat(config, oReksadana.tgl_buka)
  oSubscribeReksadana.mutasi_debet = oReksadana.akum_nominal
  oSubscribeReksadana.mutasi_kredit = 0.0
  #oSubscribeReksadana.nilai_subscribe = oReksadana.akum_nominal
  #oSubscribeReksadana.unit_penyertaan = oReksadana.unit_penyertaan
  oSubscribeReksadana.isCommitted = 'T'

  #oSubscribeReksadana.tgl_sistem = config.Now()
  #oSubscribeReksadana.tgl_otorisasi = config.Now()
  oSubscribeReksadana.user_id = oReksadana.user_id
  oSubscribeReksadana.user_id_auth = oReksadana.user_id_auth
  oSubscribeReksadana.terminal_id = oReksadana.terminal_id
  oSubscribeReksadana.terminal_id_auth = oReksadana.terminal_id_auth
  
  oSubscribeReksadana.nilai_subscribe = oReksadana.akum_nominal
  oSubscribeReksadana.NAB_Awal = 0.0
  oSubscribeReksadana.NAB_Transaksi = oSubscribeReksadana.NAB_Awal
  oSubscribeReksadana.tgl_sistem = moduleapi.DateTimeTupleToFloat(config, oReksadana.tgl_otorisasi)
  oSubscribeReksadana.tgl_otorisasi = config.Now()
  #oHistR.Tgl_Informasi = oReksadana.tgl_otorisasi
  oSubscribeReksadana.unit_penyertaan = 0.0 #oReksadana.unit_penyertaan
  oSubscribeReksadana.UP_Awal = 0.0
  
# biaya subscribe
def CreateBiayaSubscribe(config, oRegisterReksadana, oReksadana):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  oTransLRInvestasi = config.CreatePObject('TransLRInvestasi')
  oTransLRInvestasi.LInvestasi = oReksadana
  oTransLRInvestasi.LTransactionBatch = oRegisterReksadana.LTransactionBatch
  oTransLRInvestasi.kode_jns_investasi = oRegisterReksadana.kode_jns_investasi
  oTransLRInvestasi.kode_jenis_trinvestasi = 'D' # biaya reksadana
  oTransLRInvestasi.kode_subjns_LRInvestasi = 'C-SUB' # biaya subscribe fee reksadana
  oTransLRInvestasi.tgl_transaksi = moduleapi.DateTimeTupleToFloat(config, oRegisterReksadana.tgl_buka)
  oTransLRInvestasi.mutasi_debet = oRegisterReksadana.biaya
  oTransLRInvestasi.mutasi_kredit = 0.0
  oTransLRInvestasi.isCommitted = 'T'

  oTransLRInvestasi.tgl_sistem = config.Now()
  oTransLRInvestasi.tgl_otorisasi = config.Now()
  oTransLRInvestasi.user_id = oReksadana.user_id
  oTransLRInvestasi.user_id_auth = oReksadana.user_id_auth
  oTransLRInvestasi.terminal_id = oReksadana.terminal_id
  oTransLRInvestasi.terminal_id_auth = oReksadana.terminal_id_auth
  oTransLRInvestasi.nama_investasi = oReksadana.nama_reksadana

  oReksadana.akum_LR -= oRegisterReksadana.biaya

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  id = parameter.FirstRecord.id
  oRegisterReksadana = config.CreatePObjImplProxy('RegisterReksadana')
  oRegisterReksadana.Key = id

  config.BeginTransaction()
  try:
    oReksadana = CreateReksadana(config, oRegisterReksadana)
    CreateTransPiutangInvestasi(config, oReksadana, oRegisterReksadana)

    #if oRegisterReksadana.biaya > 0.0:
    #  CreateBiayaSubscribe(config, oRegisterReksadana, oReksadana)

    oRegisterReksadana.Delete()

    config.Commit()
  except:
    config.Rollback()
    raise

  return 1

