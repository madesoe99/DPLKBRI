import com.ihsan.util.modman as modman
import sys, calendar, time

dictFund = {'A':'DPLK-MM',
            'B':'DPLK-FIX',
            'C':'DPLK-EQ',
           }
def HitungAccrue(config, rate, nom_pokok, nhari, n):
  y,m,d = config.ModLibUtils.DecodeDate(config.Now())
  if nhari == 1:
    nhari = NumOfDay(y)
    
  if IsEndOfMonth(y,m,d) and d > n:
    n = d - n
  accrue = round((rate / 100) * (n / nhari) * nom_pokok,2)
  config.SendDebugMsg(str(rate))
  config.SendDebugMsg(str(n))
  config.SendDebugMsg(str(nhari))
  config.SendDebugMsg(str(nom_pokok))
  config.SendDebugMsg(str(accrue))
  return accrue

def NumOfDay(year):
  if calendar.isleap(year):
    n = 366
  else:
    n = 365
    
  return n
  
def IsEndOfMonth(y,m,d):
  a,b = calendar.monthrange(y,m)
  
  return d == b
  
def FormatDate(tgl):
  if tgl == None: restgl = ''
  else: restgl = '%s/%s/%s' % (tgl[1],tgl[2],tgl[0])

  return restgl

def runSQL(config, sSQL):
  print 'SQL:> \n', sSQL
  t1 = time.clock()
  if config.ExecSQL(sSQL) < 0:
    raise #'runSQL', config.GetDBConnErrorInfo()
  t2 = time.clock()
  
  print '>>... %.8f seconds\n' % (t2-t1)
    
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
  moduleapi = modman.getModule(config, 'moduleapi')
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
  moduleapi = modman.getModule(config, 'moduleapi')
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
  if oDeposito.LPayingAgent.IsNull:
    JenisTransaksi = 'RFOP'
  else:
    JenisTransaksi = 'RVP'
  JenisTransaksi = JenisTransaksi + '-DEPO'
  TanggalTransaksi = FormatDate(oDeposito.tgl_buka)
  TanggalSettlement = FormatDate(oDeposito.tgl_settlement)
  ClientID = SubAccountId = dictFund[oDeposito.kode_paket_investasi]
  SecurityType = oDeposito.kode_subjns_LRInvestasi
  subCustodian = 'BRI'
  if oDeposito.LBroker.IsNull:
    broker = 'NA'
  else:
    broker = oDeposito.LBroker.broker_code
  if oDeposito.LPayingAgent.IsNull:
    bankId = ''
    bankAcc = ''
  else:
    bankId = oDeposito.LPayingAgent.agent_code
    bankAcc = oDeposito.LPayingAgent.agent_name 
  MaturityDate = FormatDate(oDeposito.tgl_jatuh_tempo)
  if oDeposito.jenisJatuhTempo == 0:
    Periode = oDeposito.jenisJatuhTempo
  else:
    Periode = oDeposito.jenisJatuhTempo * 30
  BilyetBank = oDeposito.kode_pihak_ketiga
  BilyetNumber = oDeposito.no_bilyet
  BilyetAccount = oDeposito.Rekening_Deposito
  InterestAmmount = HitungAccrue(config, oDeposito.equivalent_rate, oDeposito.nominal_pembukaan, oDeposito.LAccrual.accrual_day, oDeposito.LAccrual.accrual_month)
  if oDeposito.treatmentPokok == 'A': 
    if oDeposito.kapitalisir_rollover == 'F':
      MaturityInstruction = 1 #ARO Nominal
    else:
      MaturityInstruction = 2 #ARO Interest
  else:
    MaturityInstruction = 0 #FULL REDEEM
  
  scriptlessstatus = 'N'
  status = 'A'
  statusdesc = 'APPROVAL ENTRY'
  
  sSQL = "INSERT INTO TrxToCIM (IDTransaksiDPLK,JenisTransaksi,TanggalTransaksi,TanggalSettlement,ClientID,\
  SubAccountId,SecurityType,subCustodian,broker,scriptlessstatus,bankId,bankAcc,Nominal,InterestRate,\
  MaturityDate,Periode,BilyetBank,BilyetNumber,BilyetAccount,InterestAmmount,MaturityInstruction,\
  Status,StatusDesc,CIM_SendStatus) VALUES (%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%s,%s,'%s',\
  '%s','%s','%s','%s',%s,'%s','%s','%s','F')" % (oTransPiutangInvestasi.id_transaksiinvestasi,JenisTransaksi,TanggalTransaksi,\
  TanggalSettlement,ClientID,SubAccountId,SecurityType,subCustodian,broker,\
  scriptlessstatus,bankId,bankAcc,oDeposito.nominal_pembukaan,oDeposito.equivalent_rate,MaturityDate,\
  Periode,BilyetBank,BilyetNumber,BilyetAccount,InterestAmmount,MaturityInstruction,status,statusdesc)
  
  config.SendDebugMsg(sSQL)
  runSQL(config, sSQL)
  
# biaya buka deposito
def CreateBiayaBuka(config, oDeposito, oRegisterDeposito):
  moduleapi = modman.getModule(config, 'moduleapi')
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
  config.SendDebugMsg('InsertRegisterAuthorized')
  sSQL = "INSERT INTO REGISTERINVESTASIAUTHORIZED\
          SELECT * FROM REGISTERINVESTASI\
          WHERE id_registerinvestasi = %s;\
          INSERT INTO RINCIANREGISTERINVESTASIAUTHORIZED\
          SELECT * FROM RINCIANREGISTERINVESTASI\
          WHERE id_registerinvestasi = %s;\
          INSERT INTO LINKINVESTASIREGISTER VALUES (%s, %s);" \
          % (id_register, id_register, id_deposito, id_register) 
  config.SendDebugMsg(sSQL)
  i = config.ExecSQL(sSQL)
  if i < 0:
    raise #'insert register authorized error', str(sys.exc_info()[1])

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)
  moduleapi = modman.getModule(config, 'moduleapi')

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

    #InsertRegisterAuthorized(config, id, oDeposito.id_investasi)
    oRegisterDeposito.Ls_RincianRegisterDeposito.DeleteAllPObjs()
    oRegisterDeposito.Ls_RincianRegisterInvestasi.DeleteAllPObjs()
    oRegisterDeposito.Delete()

    config.Commit()
  except:
    config.Rollback()
    raise #'register deposito error', str(sys.exc_info()[1])

  return 1

