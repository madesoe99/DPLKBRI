import com.ihsan.util.modman as modman

#transaksiapi = modman.getModule(config, 'transaksiapi')

def resSQLAkumRek(config, kode_paket_investasi):
  strSQL = \
    'select '\
    '  sum(akum_dana_iuran_pk) sum_iuran_pk '\
    '  , sum(akum_dana_iuran_pst) sum_iuran_pst '\
    '  , sum(akum_dana_pengembangan) sum_iuran_pengembangan '\
    '  , sum(akum_dana_peralihan) sum_iuran_peralihan '\
    'from RekeningDPLK '\
    'where status_dplk = \'A\' \
     and kode_paket_investasi = \'%s\'; '\
    % (kode_paket_investasi)
  config.SendDebugMsg('dpkPaket='+strSQL)
  return config.CreateSQL(strSQL).RawResult

def resSQLAkumNominal(config, kode_paket_investasi):
  #jika satu investasi hanya dari satu paket
  #strSQL = \
  #  'select sum(akum_nominal) sum_nominal '\
  #  'from Investasi '\
  #  'where kode_paket_investasi = \'%s\'; '\

  #jika satu investasi bisa dari berbagai paket
  if kode_paket_investasi in ('A'):
    strSQL = \
      'select sum(akum_paket) sum_nominal '\
      'from RincianInvestasi R,Investasi I '\
      'where R.id_investasi = I.id_investasi '\
      ' and I.status = \'T\' '\
      ' and R.kode_paket_investasi = \'%s\'; '\
      % (kode_paket_investasi)
  else: # sukuk 'B'
    dictMapKodeInv = {'B':'O','C':'R'}
    strSQL = "select sum(akum_nominal) as sum_nominal \
            from investasi \
            where status = 'T' \
            and kode_jns_investasi = '%s'" % (dictMapKodeInv[kode_paket_investasi])
  
  config.SendDebugMsg('dpkDiinvestasikan='+strSQL)
  return config.CreateSQL(strSQL).RawResult

def resSQLInvestasiExisting(config, kode_paket_investasi, kode_jns_investasi):
  #jika satu investasi hanya dari satu paket
  #strSQL = \
  #  'select sum(akum_nominal) sum_nominal '\
  #  'from Investasi '\
  #  'where kode_paket_investasi = \'%s\ '\
  #  '  and kode_jns_investasi = \'%s\'; '\

  #jika satu investasi bisa dari berbagai paket
  if kode_jns_investasi in ('D'):
    strSQL = \
      'select sum(akum_paket) sum_nominal '\
      'from RincianInvestasi R, Investasi I '\
      'where R.kode_paket_investasi = \'%s\' '\
      '  and R.id_investasi = I.id_investasi '\
      '  and I.Status = \'T\' '\
      '  and R.kode_jns_investasi = \'%s\'; '\
      % (kode_paket_investasi, kode_jns_investasi)
  else: # sukuk 'O', reksadana 'R'
    strSQL = "select sum(akum_nominal) as sum_nominal \
            from investasi \
            where status = 'T' \
            and kode_jns_investasi = '%s'" % (kode_jns_investasi)
            
  config.SendDebugMsg('dpkInvExisting='+strSQL)  
  return config.CreateSQL(strSQL).RawResult

def resSQLCurrInv(config, kode_paket_investasi, kode_jns_investasi):
  #jika satu investasi hanya dari satu paket
  #strSQL = \
  #  'select sum(akum_nominal) sum_nominal '\
  #  'from Investasi '\
  #  'where kode_paket_investasi = \'%s\' '\
  #  '  and kode_jns_investasi = \'%s\'; '\

  #jika satu investasi bisa dari berbagai paket
  strSQL = \
    'select sum(nominal) sum_nominal '\
    'from RincianInvestasi '\
    'where kode_paket_investasi = \'%s\' '\
    '  and kode_jns_investasi = \'%s\'; '\
    % (kode_paket_investasi, kode_jns_investasi)
  return config.CreateSQL(strSQL).RawResult

def getDPKPaket(config, kode_paket_investasi):
  # mengambil total dana yang dihimpun berdasarkan paket investasi tertentu
  resSQL = resSQLAkumRek(config, kode_paket_investasi)
  if resSQL.Eof:
    return 0.0
  return resSQL.sum_iuran_pk + resSQL.sum_iuran_pst + resSQL.sum_iuran_pengembangan + resSQL.sum_iuran_peralihan

def getDPKDiinvestasikan(config, kode_paket_investasi):
  # mengambil total dana yang diinvestasikan untuk paket investasi tertentu
  resSQL = resSQLAkumNominal(config, kode_paket_investasi)
  if resSQL.Eof :
    return 0.0
  return resSQL.sum_nominal

def getCurrInvestasi(config, kode_paket_investasi, kode_jns_investasi):
  # mengambil total dana yang diinvestasikan untuk paket investasi tertentu dan jenis investasi tertentu
  resSQL = resSQLCurrInv(config, kode_paket_investasi, kode_jns_investasi)
  if resSQL.Eof:
    return 0.0
  return resSQL.sum_nominal

def getInvExisting(config, kode_paket_investasi, kode_jns_investasi):
  # mengambil investasi untuk kode paket dan jenis investasi tertentu
  resSQL = resSQLInvestasiExisting(config, kode_paket_investasi, kode_jns_investasi)
  if resSQL.Eof:
    return 0.0
  return resSQL.sum_nominal

def getPaket(config, kode_paket_investasi):
  appObject = config.GetAppObject()

  oPaketInvestasi = config.CreatePObjImplProxy('PaketInvestasi')
  oPaketInvestasi.Key = kode_paket_investasi

  #ambil info untuk rlogin dan kirimkan paketnya
  transaksiapi = modman.getModule(config, 'transaksiapi')
  ServerName, AppName, Session_Name, UserID, Password = transaksiapi.GetLoginAkuntansi(config)

  #if not appObject.lookuprsession(Session_Name):
  appObject.rlogin(ServerName, AppName, UserID, Password, Session_Name)
  try:
    config.SendDebugMsg('gngp_1')
    rPH = appObject.rexecscript(
      Session_Name
      , 'appinterface/getnominalgiropaket'
      , appObject.CreateValues(
          ['acc_giro', oPaketInvestasi.acc_giro]
          , ['branch_code', config.SysVarIntf.GetStringSysVar('SETTINGAKUNTANSI', 'BranchCodeTransaksi')]
          , ['currency_code', config.SysVarIntf.GetStringSysVar('SETTINGAKUNTANSI', 'DefaultCurrency')]
      )
    )

    config.SendDebugMsg('gngp_2')
  finally:
    config.SendDebugMsg('gngp_3')
    appObject.rlogout(Session_Name)

  return rPH.FirstRecord.nominalGiro

def getHasilInvBelumDibagikan(config):
  return 0.0
  
def getPaketInfo(config, kode_paket_investasi, kode_jns_investasi):
  dpkPaket = getDPKPaket(config, kode_paket_investasi) or 0.0
  dpkDiinvestasikan = getDPKDiinvestasikan(config, kode_paket_investasi) or 0.0
  currInvestasi = getCurrInvestasi(config, kode_paket_investasi, kode_jns_investasi) or 0.0
  nominalGiro = getPaket(config, kode_paket_investasi) or 0.0
#   nominalGiro = 10000000000.0
  dpkInvExisting = getInvExisting(config, kode_paket_investasi, kode_jns_investasi) or 0.0
  hasilInvBelumDibagikan = getHasilInvBelumDibagikan(config)

  oRPI = config.CreatePObjImplProxy('RincianPaketInvestasi')
  oRPI.SetKey('kode_paket_investasi', kode_paket_investasi)
  oRPI.SetKey('kode_jns_investasi', kode_jns_investasi)

  nilaiMaksProporsi = (oRPI.maks_proporsi or 0.0) * dpkPaket / 100.0
  #dpkTersedia = dpkPaket - dpkInvExisting
  dpkTersedia = nilaiMaksProporsi - dpkDiinvestasikan + hasilInvBelumDibagikan
#   ita 081110
#   if dpkTersedia > nilaiMaksProporsi :
#     #dpkTersedia = nilaiMaksProporsi
#     dpkTersedia = nilaiMaksProporsi - dpkInvExisting
#   end of ita
  
  #dpkTersedia = dpkPaket
  #nominalGiro = dpkPaket
  
  return dpkPaket, dpkInvExisting, dpkTersedia, nilaiMaksProporsi, nominalGiro

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)
  
  dpkPaket, dpkInvExisting, dpkTersedia, nilaiMaksProporsi, nominalGiro = getPaketInfo(
    config
    , parameter.FirstRecord.kode_paket_investasi
    , parameter.FirstRecord.kode_jns_investasi
  )

  returnpacket.CreateValues(
    ['dpkPaket', dpkPaket]
    , ['dpkInvExisting', dpkInvExisting]
    , ['dpkTersedia', dpkTersedia]
    , ['nilaiMaksProporsi', nilaiMaksProporsi]
    , ['nominalGiro', nominalGiro]
  )

  return 1

