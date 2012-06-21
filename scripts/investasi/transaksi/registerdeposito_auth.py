import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi

def CreateRincianDeposito(config, oRegisterDeposito, oDeposito):
  oRincianDeposito = config.CreatePObject('RincianDeposito')
  oRincianDeposito.LDeposito = oDeposito
  oRincianDeposito.kode_paket_investasi = oRegisterDeposito.kode_paket_investasi
  oRincianDeposito.Akum_Paket = oRincianDeposito.nominal = oRegisterDeposito.nominal
  oRincianDeposito.proporsi = 1
  oRincianDeposito.Akum_LR_Paket = 0.0


def CreateRincianDeposito_SQL(config, oRegisterDeposito, oDeposito):
  Ls_RincianRegisterDeposito = oRegisterDeposito.Ls_RincianRegisterDeposito
  
  strSQL = 'Select id_rincianregisterinv \
            From RincianRegisterInvestasi \
            where id_registerinvestasi = %d ' % oRegisterDeposito.id_registerinvestasi
  resSQL = config.CreateSQL(strSQL).RawResult
  resSQL.First()
  while not resSQL.Eof:
    oRincianRegisterDeposito = config.CreatePObjImplProxy('RincianRegisterDeposito')
    oRincianRegisterDeposito.Key = resSQL.id_rincianregisterinv
    
    oRincianDeposito = config.CreatePObject('RincianDeposito')
    oRincianDeposito.LDeposito = oDeposito
    oRincianDeposito.LRincianPaketInvestasi = oRincianRegisterDeposito.LRincianPaketInvestasi
    oRincianDeposito.nominal = oRincianRegisterDeposito.nominal
    
    resSQL.Next()


def CreateDeposito(config, oRegisterDeposito):
  oDeposito = config.CreatePObject('Deposito')
  oDeposito.no_bilyet = oRegisterDeposito.no_bilyet
  oDeposito.Rekening_Deposito = oRegisterDeposito.Rekening_Deposito
  oDeposito.kode_pihak_ketiga = oRegisterDeposito.kode_pihak_ketiga
  oDeposito.kode_paket_investasi = oRegisterDeposito.kode_paket_investasi
  oDeposito.kode_jns_investasi = oRegisterDeposito.kode_jns_investasi
  oDeposito.tgl_buka = oDeposito.tgl_settlement = moduleapi.DateTimeTupleToFloat(config, oRegisterDeposito.tgl_buka)
  oDeposito.nominal_pembukaan = oRegisterDeposito.nominal
  oDeposito.akum_nominal = oRegisterDeposito.nominal
  oDeposito.akum_LR = 0.0
  oDeposito.akum_piutangLR = 0.0
  oDeposito.rollover_counter = 0
  oDeposito.status = 'T'

  oDeposito.jenisJatuhTempo = oRegisterDeposito.jenisJatuhTempo
  oDeposito.jmlHariOnCall = oRegisterDeposito.jmlHariOnCall
  oDeposito.tgl_jatuh_tempo = moduleapi.DateTimeTupleToFloat(config, oRegisterDeposito.tgl_jatuh_tempo)
  oDeposito.equivalent_rate = oRegisterDeposito.equivalent_rate
  oDeposito.treatmentPokok = oRegisterDeposito.treatmentPokok
  if oRegisterDeposito.acc_giro != '' :
    oDeposito.no_rekening = oRegisterDeposito.LMasterGiro.no_giro#oRegisterDeposito.no_rekening
  oDeposito.kapitalisir_rollover = oRegisterDeposito.kapitalisir_rollover
  
  
  oDeposito.LAccrual = oRegisterDeposito.LAccrual
  oDeposito.LBroker = oRegisterDeposito.LBroker
  oDeposito.LPayingAgent = oRegisterDeposito.LPayingAgent
  oDeposito.LSubJenisInv = oRegisterDeposito.LSubJenisInv

  oDeposito.tgl_otorisasi = config.Now()
  oDeposito.last_update = config.Now()
  oDeposito.user_id = oRegisterDeposito.user_id
  oDeposito.user_id_auth = config.SecurityContext.userid
  oDeposito.terminal_id = oRegisterDeposito.terminal_id
  oDeposito.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]

  # create rincian deposito
  CreateRincianDeposito(config, oRegisterDeposito, oDeposito)

  return oDeposito

def CreateTransPiutangInvestasi(config, oDeposito, oRegisterDeposito):
  oTransPiutangInvestasi = config.CreatePObject('TransPiutangInvestasi')
  oTransPiutangInvestasi.LInvestasi = oDeposito
  oTransPiutangInvestasi.kode_jns_investasi = 'D' # deposito
  oTransPiutangInvestasi.kode_jenis_trinvestasi = 'A' # buat investasi baru
  oTransPiutangInvestasi.tgl_transaksi = moduleapi.DateTimeTupleToFloat(config, oDeposito.tgl_buka)
  oTransPiutangInvestasi.mutasi_debet = oDeposito.akum_nominal
  oTransPiutangInvestasi.mutasi_kredit = 0.0
  oTransPiutangInvestasi.isCommitted = 'T'

  oTransPiutangInvestasi.tgl_sistem = config.Now()
  oTransPiutangInvestasi.tgl_otorisasi = config.Now()
  oTransPiutangInvestasi.user_id = oDeposito.user_id
  oTransPiutangInvestasi.user_id_auth = config.SecurityContext.userid
  oTransPiutangInvestasi.terminal_id = oDeposito.terminal_id
  oTransPiutangInvestasi.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]
  oTransPiutangInvestasi.no_bilyet = oDeposito.no_bilyet
  
  CreateTrxCIM(config, oTransPiutangInvestasi, oDeposito)

def CreateTrxCIM(config, oTransPiutangInvestasi, oDeposito):
  status = 'A'
  statusdesc = 'APPROVAL ENTRY'
  
  sSQL = "INSERT INTO TrxToCIM (IDTransaksiDPLK,JenisTransaksi,TanggalTransaksi,TanggalSettlement,ClientID,\
  SubAccountId,SecurityType,subCustodian,broker,scriptlessstatus,bankId,bankAcc,Nominal,InterestRate,\
  MaturityDate,Periode,BilyetBank,BilyetNumber,BilyetAccount,InterestAmmount,MaturityInstruction,\
  Status,StatusDesc) VALUES (oTransPiutangInvestasi.id_transaksiinvestasi,'','','','','','','','',\
  '','','','','','','','','','','','',status,statusdesc)"
  runSQL(config, sSQL)
  
# biaya buka deposito
def CreateBiayaBuka(config, oDeposito, oRegisterDeposito):
  oTransLRInvestasi = config.CreatePObject('TransLRInvestasi')
  oTransLRInvestasi.LInvestasi = oDeposito
  oTransLRInvestasi.kode_jns_investasi = 'D'
  oTransLRInvestasi.kode_jenis_trinvestasi = 'D' # biaya deposito
  oTransLRInvestasi.kode_subjns_LRInvestasi = 'A-OPEN' # biaya pembukaan deposito
  oTransLRInvestasi.tgl_transaksi = moduleapi.DateTimeTupleToFloat(config, oDeposito.tgl_buka)
  oTransLRInvestasi.mutasi_debet = oRegisterDeposito.biaya
  oTransLRInvestasi.mutasi_kredit = 0.0
  oTransLRInvestasi.isCommitted = 'T'

  oTransLRInvestasi.tgl_sistem = config.Now()
  oTransLRInvestasi.tgl_otorisasi = config.Now()
  oTransLRInvestasi.user_id = oDeposito.user_id
  oTransLRInvestasi.user_id_auth = oDeposito.user_id_auth
  oTransLRInvestasi.terminal_id = oDeposito.terminal_id
  oTransLRInvestasi.terminal_id_auth = oDeposito.terminal_id_auth
  oTransLRInvestasi.no_bilyet = oDeposito.no_bilyet

  oDeposito.akum_LR -= oRegisterDeposito.biaya

  return oTransLRInvestasi

def InsertRegisterAuthorized(config, id_register, id_deposito):
  sSQL = "INSERT INTO REGISTERINVESTASIAUTHORIZED\
          SELECT * FROM REGISTERINVESTASI\
          WHERE id_registerinvestasi = %s;\
          INSERT INTO RINCIANREGISTERINVESTASIAUTHORIZED\
          SELECT * FROM RINCIANREGISTERINVESTASI\
          WHERE id_registerinvestasi = %s;\
          INSERT INTO LINKINVESTASIREGISTER VALUES (%s, %s);" \
          % (id_register, id_register, id_deposito, id_register) 
  i = config.ExecSQL(sSQL)
  if i < 0:
    raise 'insert register authorized error', str(sys.exc_info()[1])

def runSQL(config, sSQL):
  print 'SQL:> \n', sSQL
  t1 = time.clock()
  if config.ExecSQL(sSQL) < 0:
    raise 'runSQL', config.GetDBConnErrorInfo()
  t2 = time.clock()
  
  print '>>... %.8f seconds\n' % (t2-t1)
    
def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  id = parameter.FirstRecord.id

  oRegisterDeposito = config.CreatePObjImplProxy('RegisterDeposito')
  oRegisterDeposito.Key = id
  if oRegisterDeposito.no_bilyet not in ('',None) :
    moduleapi.CheckNoBilyetAvl(config, oRegisterDeposito.no_bilyet)

  config.BeginTransaction()
  try:
    oDeposito = CreateDeposito(config, oRegisterDeposito)
    CreateTransPiutangInvestasi(config, oDeposito, oRegisterDeposito)

    if oRegisterDeposito.biaya > 0.0:
      CreateBiayaBuka(config, oDeposito, oRegisterDeposito)

    InsertRegisterAuthorized(config, id, oDeposito.id_investasi)
    oRegisterDeposito.Ls_RincianRegisterDeposito.DeleteAllPObjs()
    oRegisterDeposito.Ls_RincianRegisterInvestasi.DeleteAllPObjs()
    oRegisterDeposito.Delete()

    config.Commit()
  except:
    config.Rollback()
    raise

  return 1

