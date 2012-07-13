import com.ihsan.util.modman as modman

#moduleapi = modman.getModule(config, 'moduleapi')

def CreateRincianSaham(config, oSaham):
  # buat satu objek rincianSaham
  # karena dalam kasus Saham, satu Saham hanya mengacu ke satu paket saja (B)

  oRincianSaham = config.CreatePObject('RincianSaham')
  oRincianSaham.LSaham = oSaham
  oRincianSaham.kode_paket_investasi = oSaham.kode_paket_investasi
  oRincianSaham.Akum_Paket = oRincianSaham.nominal = oSaham.nominal_pembukaan
  oRincianSaham.proporsi = 1
  oRincianSaham.Akum_LR_Paket = 0.0
  

def CreateSaham(config, oRegisterSaham):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  oSaham = config.CreatePObject('Saham')
  oSaham.nama_Saham = oRegisterSaham.nama_Saham
  oSaham.kode_pihak_ketiga = oRegisterSaham.kode_pihak_ketiga
  oSaham.kode_paket_investasi = oRegisterSaham.kode_paket_investasi
  oSaham.kode_jns_investasi = oRegisterSaham.kode_jns_investasi
  oSaham.tgl_buka = moduleapi.DateTimeTupleToFloat(config, oRegisterSaham.tgl_buka)
  oSaham.nominal_pembukaan = oRegisterSaham.nominal - oRegisterSaham.biaya
  oSaham.akum_nominal = oRegisterSaham.nominal - oRegisterSaham.biaya
  oSaham.akum_LR = 0.0
  oSaham.akum_piutangLR = 0.0
  oSaham.rollover_counter = 0
  oSaham.status = 'T'

  oSaham.unit_penyertaan = 0.0#oRegisterSaham.unit_penyertaan
  oSaham.NAB_awal = oRegisterSaham.NAB_awal
  oSaham.NAB_Transaksi = 0.0 
  oSaham.NAB = 0.0 #oRegisterSaham.NAB
  oSaham.kode_jns_Saham = oRegisterSaham.kode_jns_Saham
  oSaham.LCustodianBank = oRegisterSaham.LCustodianBank

  oSaham.tgl_otorisasi = config.Now()
  oSaham.last_update = config.Now()
  oSaham.user_id = oRegisterSaham.user_id
  oSaham.user_id_auth = config.SecurityContext.userid
  oSaham.terminal_id = oRegisterSaham.terminal_id
  oSaham.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]

  # create rincian Saham
  CreateRincianSaham(config, oSaham)
  
  return oSaham

def CreateTransPiutangInvestasi(config, oSaham, oRegisterSaham):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  oSubscribeSaham = config.CreatePObject('SubscribeSaham')
  oSubscribeSaham.LInvestasi = oSaham
  oSubscribeSaham.nama_investasi = oSaham.nama_Saham
  oSubscribeSaham.LTransactionBatch = oRegisterSaham.LTransactionBatch
  oSubscribeSaham.kode_jns_investasi = oRegisterSaham.kode_jns_investasi#'C' # Saham
  oSubscribeSaham.kode_jenis_trinvestasi = 'SS' # buat investasi baru, subscribe Saham
  oSubscribeSaham.tgl_transaksi = moduleapi.DateTimeTupleToFloat(config, oSaham.tgl_buka)
  oSubscribeSaham.mutasi_debet = oSaham.akum_nominal
  oSubscribeSaham.mutasi_kredit = 0.0
  #oSubscribeSaham.nilai_subscribe = oSaham.akum_nominal
  #oSubscribeSaham.unit_penyertaan = oSaham.unit_penyertaan
  oSubscribeSaham.isCommitted = 'T'

  #oSubscribeSaham.tgl_sistem = config.Now()
  #oSubscribeSaham.tgl_otorisasi = config.Now()
  oSubscribeSaham.user_id = oSaham.user_id
  oSubscribeSaham.user_id_auth = oSaham.user_id_auth
  oSubscribeSaham.terminal_id = oSaham.terminal_id
  oSubscribeSaham.terminal_id_auth = oSaham.terminal_id_auth
  
  oSubscribeSaham.nilai_subscribe = oSaham.akum_nominal
  oSubscribeSaham.NAB_Awal = 0.0
  oSubscribeSaham.NAB_Transaksi = oSubscribeSaham.NAB_Awal
  oSubscribeSaham.tgl_sistem = moduleapi.DateTimeTupleToFloat(config, oSaham.tgl_otorisasi)
  oSubscribeSaham.tgl_otorisasi = config.Now()
  #oHistR.Tgl_Informasi = oSaham.tgl_otorisasi
  oSubscribeSaham.unit_penyertaan = 0.0 #oSaham.unit_penyertaan
  oSubscribeSaham.UP_Awal = 0.0
  
# biaya subscribe
def CreateBiayaSubscribe(config, oRegisterSaham, oSaham):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  oTransLRInvestasi = config.CreatePObject('TransLRInvestasi')
  oTransLRInvestasi.LInvestasi = oSaham
  oTransLRInvestasi.LTransactionBatch = oRegisterSaham.LTransactionBatch
  oTransLRInvestasi.kode_jns_investasi = oRegisterSaham.kode_jns_investasi
  oTransLRInvestasi.kode_jenis_trinvestasi = 'D' # biaya Saham
  oTransLRInvestasi.kode_subjns_LRInvestasi = 'C-SUB' # biaya subscribe fee Saham
  oTransLRInvestasi.tgl_transaksi = moduleapi.DateTimeTupleToFloat(config, oRegisterSaham.tgl_buka)
  oTransLRInvestasi.mutasi_debet = oRegisterSaham.biaya
  oTransLRInvestasi.mutasi_kredit = 0.0
  oTransLRInvestasi.isCommitted = 'T'

  oTransLRInvestasi.tgl_sistem = config.Now()
  oTransLRInvestasi.tgl_otorisasi = config.Now()
  oTransLRInvestasi.user_id = oSaham.user_id
  oTransLRInvestasi.user_id_auth = oSaham.user_id_auth
  oTransLRInvestasi.terminal_id = oSaham.terminal_id
  oTransLRInvestasi.terminal_id_auth = oSaham.terminal_id_auth
  oTransLRInvestasi.nama_investasi = oSaham.nama_Saham

  oSaham.akum_LR -= oRegisterSaham.biaya

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  id = parameter.FirstRecord.id
  oRegisterSaham = config.CreatePObjImplProxy('RegisterSaham')
  oRegisterSaham.Key = id

  config.BeginTransaction()
  try:
    config.SendDebugMsg('aaa')
    oSaham = CreateSaham(config, oRegisterSaham)
    config.SendDebugMsg('bbb')
    CreateTransPiutangInvestasi(config, oSaham, oRegisterSaham)
    config.SendDebugMsg('ccc')

    #if oRegisterSaham.biaya > 0.0:
    #  CreateBiayaSubscribe(config, oRegisterSaham, oSaham)

    oRegisterSaham.Delete()

    config.Commit()
  except:
    config.Rollback()
    raise

  return 1

