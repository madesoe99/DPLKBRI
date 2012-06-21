import calendar, string, time

## temporary constants

zero_approx = 0.00001
MONTHS_ID = ('Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', \
  'Agustus', 'September', 'Oktober', 'November', 'Desember')
SHORTMOON = [4, 6, 9, 11]

dictMonth={
  1:'Jan',
  2:'Feb',
  3:'Mar',
  4:'Apr',
  5:'May',
  6:'Jun',
  7:'Jul',
  8:'Agt',
  9:'Sep',
  10:'Oct',
  11:'Nov',
  12:'Dec'
}

def GetLastIDSRRCalc(config):
  o = config.CreatePObjImplProxy('ID_GEN')
  o.Key = 'SRRCalc'
  
  return o.Last_ID - 1
  
def FormatDateOracle(tupDate):
  oradate = str(tupDate[2])+'-'+dictMonth[int(tupDate[1])]+'-'+str(tupDate[0])[2:4]    
  return oradate

def IsOddNumber(val):
  return val % 2

def IsApproxZero(val):
  # return true if val considered to be zero
  return abs(val) <= zero_approx

def IsValueNotZero(val):
  # return true if val considered to be not zero and val not None
  return val and not IsApproxZero(val)

def FormatFloatStd(config, floatVal, valIfZero = '0'):
  if IsApproxZero(floatVal):
    return valIfZero
  else:
    return config.FormatFloat('#,##0.00',floatVal)

def DateTimeTupleToFloat(config, dtTuple):
  y, m, d, h, n, s, z = dtTuple[:7]
  return config.ModDateTime.EncodeDate(y, m, d) + config.ModDateTime.EncodeTime(h, n, s, z)

def AddYearToDateTuple(config, dtTuple, nbOfYear):
  y, m, d, h, n, s, z = dtTuple[:7]
  y += nbOfYear
  if (m == 2) and (d == 29) and (not calendar.isleap(y)):
    # tanggal 29 februari, tetapi tahun yang akan datang bukan tahun kabisat
    # dibulatkan menjadi tanggal 28 februari
    d = 28

  return [y, m, d, h, n, s, z]

def GetNextDayDateTime(config, dateTimeVal, nextVal = 1):
  # return nextVal day after dateTimeVal
  return dateTimeVal + nextVal

def IntMonthToStr(intMonth):
  return MONTHS_ID[intMonth-1]

def MyZFill(strinput, maxlen):
  while len(strinput) < maxlen:
    strinput = '0' + strinput
  return strinput

def MyReccZFill(strinput, maxlen):
  if len(strinput) >= maxlen:
    return strinput
  else:
    return MyReccZFill('0' + strinput, maxlen)

def TruncateString(strinput, maxlen):
  return strinput[:maxlen]

def GetUserGroupList(config, userID):
  oUser = config.CreatePObjImplProxy('UserApp')
  oUser.key = userID
  
  hGroups = []
  UserGroupAppList = oUser.Ls_UserGroupApp
  UserGroupAppList.First()
  while not UserGroupAppList.EndOfList:
    UserGroupApp = UserGroupAppList.CurrentElement
    hGroups.append(string.upper(UserGroupApp.group_id))
    
    UserGroupAppList.Next()
  
  return hGroups

def GetGroupIDByUserID(config, user_id):
  strSQL = \
    'select group_id '\
    'from UserGroupApp '\
    'where user_id = \'%s\''\
    % (user_id)
  resSQL = config.CreateSQL(strSQL).RawResult

  if resSQL.Eof:
    raise '\nPERINGATAN','ID Group tidak ditemukan!'
  else:
    return resSQL.group_id

def IsUserGroup(config, user_id, group_id):
  # group_id must be uppercase
  #return string.upper(GetGroupIDByUserID(config, user_id)) == group_id
  return group_id in GetUserGroupList(config, user_id)

def IsUserTeller(config, user_id):
  return IsUserGroup(config, user_id, 'TELLER')

def GetJenisTransaksiDPLK(config, kode_jenis_transaksi):
  oJenisTransaksiDPLK = config.CreatePObjImplProxy('JenisTransaksiDPLK')
  oJenisTransaksiDPLK.Key = kode_jenis_transaksi
  return oJenisTransaksiDPLK

def GetBesarBiayaDaftar(config, oCalonPeserta):
  biayaDaftar = 0.0

  #cek apakah termasuk anggota peserta perusahaan
  if oCalonPeserta.IsFieldNull('kode_nasabah_corporate'):
    #bukan anggota peserta perusahaan, ambil biaya pendaftaran default
    oParameter = config.CreatePObjImplProxy('Parameter')
    oParameter.Key = 'BESAR_BIAYA_DAFTAR'
    biayaDaftar = oParameter.Numeric_Value
  else:
    #anggota peserta perusahaan
    oPerusahaan = config.CreatePObjImplProxy('NasabahDPLKCorporate')
    oPerusahaan.Key = oCalonPeserta.kode_nasabah_corporate
    biayaDaftar = oPerusahaan.biaya_daftar_anggota

  return biayaDaftar

def GetMinimalSRRBagiHasil(config):
  oParameter = config.CreatePObjImplProxy('Parameter')
  oParameter.Key = 'MINIMAL_SRR_BAGI_HASIL'

  return oParameter.Numeric_Value

def GetCounterNumber(config, id_code, param, countnum = 0):

  if countnum == 0:
    actCountNum = 1
  else:
    actCountNum = countnum
    
  config.BeginTransaction()
  try:
    strSQLLock = '\
      update counter \
      set is_locked = 1 \
      where is_locked = 0 \
        and id_code = \'%s\' \
        and param = \'%s\'' \
      % (id_code, param)

    strSQLGet = '\
      select last_id \
      from counter \
      where is_locked = 1 \
        and id_code = \'%s\' \
        and param = \'%s\'' \
      % (id_code, param)

    strSQLIncrement = '\
      update counter \
      set last_id = last_id + %d \
      where is_locked = 1 \
        and id_code = \'%s\' \
        and param = \'%s\'' \
      % (actCountNum, id_code, param)

    strSQLUnlock = '\
      update counter \
      set is_locked = 0 \
      where is_locked = 1 \
        and id_code = \'%s\' \
        and param = \'%s\'' \
      % (id_code, param)

    # set lock
    if config.ExecSQL(strSQLLock) <= 0:
      raise '\nPERINGATAN','Penguncian record tidak berhasil!'

    # get counter
    resSQL = config.CreateSQL(strSQLGet).RawResult
    if resSQL.Eof:
      raise '\nPERINGATAN','Counter tidak ditemukan!'

    # increment counter
    if config.ExecSQL(strSQLIncrement) <= 0:
      raise '\nPERINGATAN','Penguncian record tidak berhasil!'

    # set unlock
    if config.ExecSQL(strSQLUnlock) <= 0:
      raise '\nPERINGATAN','Pembukaan kunci record tidak berhasil!'

    config.Commit()
  except:
    config.Rollback()
    raise

  if countnum == 0:
    return resSQL.last_id
  else:
    return [resSQL.last_id, resSQL.last_id + actCountNum - 1]

def GetSaldoAwal(config, no_peserta, str_dari_tanggal):
  ## menghitung saldo awal pada tanggal str_dari_tanggal,
  ## untuk peserta no_peserta, dengan cara menjumlahkan
  ## total mutasi peserta tersebut hingga sebelum str_dari_tanggal,
  ## dengan mengecualikan transaksi pendaftaran (kode_jenis_transaksi A)
  ## dan pembayaran premi (kode_jenis_transaksi B)  
  strSQL = '\
    select (sum(mutasi_peralihan) + sum(mutasi_pengembangan) + \
    sum(mutasi_iuran_pst) + sum(mutasi_iuran_pk)) as saldo_awal \
      from TransaksiDPLK \
      where tgl_transaksi < \'%s\' \
        and no_peserta = \'%s\' \
        and kode_jenis_transaksi not in (\'A\',\'B\') \
        and isCommitted = \'T\'' \
    % (str_dari_tanggal, no_peserta)
  config.SendDebugMsg('saldo awal='+strSQL)
  saldo_awal = config.CreateSQL(strSQL).RawResult.saldo_awal
  if saldo_awal <> None:
    return saldo_awal
  else:
    return 0.0

def CheckRegCIFRestriction(uideflist, auiname, apobjconst):
  config = uideflist.Config

  oUserApp = config.CreatePObjImplProxy('UserApp')
  oUserApp.Key = config.SecurityContext.GetUserInfo()[0]

  if oUserApp.NoLimitLocation == 'F':
    if auiname == 'uipMaster':
      uiCalled = uideflist.GetPClassUIByName(auiname)
      no_peserta = uiCalled.ActiveRecord.no_peserta
      oRekeningDPLK = config.CreatePObjImplProxy('RekeningDPLK')
      oRekeningDPLK.Key = no_peserta

      if oRekeningDPLK.kode_cab_daftar <> oUserApp.branch_code:
        raise '\nPERINGATAN','\nAnda tidak diperkenankan mengoreksi peserta ini!'

def CheckRegCIFRestr(config, no_peserta):
  oUserApp = config.CreatePObjImplProxy('UserApp')
  oUserApp.Key = config.SecurityContext.GetUserInfo()[0]

  if oUserApp.NoLimitLocation == 'F':
    oRekeningDPLK = config.CreatePObjImplProxy('RekeningDPLK')
    oRekeningDPLK.Key = no_peserta

    if oRekeningDPLK.kode_cab_daftar <> oUserApp.branch_code:
      raise '\nPERINGATAN','\nAnda tidak diperkenankan mengoreksi peserta ini!'

def IsNasabahAvail(config, no_peserta):
  oNasabahDPLK = config.CreatePObjImplProxy('NasabahDPLK')
  oNasabahDPLK.Key = no_peserta

  if oNasabahDPLK.IsNull:
    raise '\nPERINGATAN','Nomor peserta tidak ditemukan!'

def IsPesertaAktif(config, no_peserta):
  #cek status DPLK peserta
  oRekeningDPLK = config.CreatePObjImplProxy('RekeningDPLK')
  oRekeningDPLK.Key = no_peserta

  if oRekeningDPLK.Status_DPLK != 'A':
    #peserta sudah tidak aktif
    raise '\nPERINGATAN','\nPeserta DPLK sudah tidak aktif! Perubahan data tidak bisa dilakukan untuk peserta yang sudah tidak aktif'
    
def GetUsiaPeserta(config, no_peserta):
  #cek usia sekarang peserta dan keikutsertaan wasiat ummat (format float)
  oParameter = config.CreatePObjImplProxy('Parameter')
  oParameter.Key = 'JUMLAH_HARI_SETAHUN'
  oNasabahDPLK = config.CreatePObjImplProxy('NasabahDPLK')
  oNasabahDPLK.Key = no_peserta

  JumlahHariSetahun = oParameter.Numeric_Value
  y,m,d = time.localtime()[:3]
  dtNowDate = config.ModDateTime.EncodeDate(y,m,d)
  yLahir,mLahir,dLahir = oNasabahDPLK.tanggal_lahir[:3]
  dtTglLahir = config.ModDateTime.EncodeDate(yLahir,mLahir,dLahir)
  
  return (dtNowDate - dtTglLahir) / JumlahHariSetahun
    
def IsPensiun(config, no_peserta):
    oR = config.CreatePObjImplProxy('RekeningDPLK')
    oR.Key = no_peserta
    if not oR.IsNull:
        return (config.ModLibUtils.Now() > config.ModLibUtils.EncodeDate(oR.tgl_pensiun[0],\
        oR.tgl_pensiun[1],oR.tgl_pensiun[2]))    
    
def GetToleransiByrPremi(config):
  oParameter = config.CreatePObjImplProxy('Parameter')
  oParameter.Key = 'TOLERANSI_NILAI_PREMI'

  return oParameter.Numeric_Value

def CheckRegisterCIFUniq(config, no_peserta, kode_jenis_registercif):
  strSQL = \
   'select registercif_id '\
   'from registercif '\
   'where no_peserta = \'%s\' '\
   '  and kode_jenis_registercif = \'%s\''\
   % (no_peserta, kode_jenis_registercif)
  resSQL = config.CreateSQL(strSQL).RawResult

  if not resSQL.Eof:
    raise '\nPERINGATAN','\nData tersebut sedang dikoreksi dengan jenis koreksi yang sama!'

def IsInvestasiTutup(config, oInvestasi):
  return oInvestasi.status == 'F'

def CheckTransLRInvExclusive(config, id_investasi):
  strSQL = \
   'select i.id_transaksiinvestasi '\
   'from translrinvestasi t, transaksiinvestasi i '\
   'where i.id_investasi = %d '\
   '  and iscommitted = \'F\' '\
   '  and t.id_transaksiinvestasi = i.id_transaksiinvestasi '\
   % (id_investasi)
  resSQL = config.CreateSQL(strSQL).RawResult

  if not resSQL.Eof:
    oInvestasi = config.CreatePObjImplProxy('Investasi')
    oInvestasi.Key = id_investasi
    no_bilyet = ''
    if not oInvestasi.IsNull:
      no_bilyet = oInvestasi.no_bilyet
    raise '\nPERINGATAN',\
      '\nInvestasi %s telah memiliki register transaksi.'\
      '\nSetujui atau tolak register tersebut untuk melanjutkan.'\
      % (no_bilyet)

def CheckTransPiutangInvExclusive(config, id_investasi):
  strSQL = \
   'select i.id_transaksiinvestasi '\
   'from transpiutanginvestasi t, transaksiinvestasi i '\
   'where i.id_investasi = %d '\
   '  and iscommitted = \'F\' '\
   '  and t.id_transaksiinvestasi = i.id_transaksiinvestasi '\
   % (id_investasi)
  resSQL = config.CreateSQL(strSQL).RawResult

  if not resSQL.Eof:
    oInvestasi = config.CreatePObjImplProxy('Investasi')
    oInvestasi.Key = id_investasi
    no_bilyet = ''
    if not oInvestasi.IsNull:
      no_bilyet = oInvestasi.no_bilyet
    raise '\nPERINGATAN',\
      '\nInvestasi %s telah memiliki register transaksi.'\
      '\nSetujui atau tolak register tersebut untuk melanjutkan.'\
      % (no_bilyet)

def CheckTransPiutangLRInvExclusive(config, id_investasi):
  strSQL = \
   'select i.id_transaksiinvestasi '\
   'from transpiutanglrinvestasi t, transaksiinvestasi i '\
   'where i.id_investasi = %d '\
   '  and iscommitted = \'F\' '\
   '  and t.id_transaksiinvestasi = i.id_transaksiinvestasi '\
   % (id_investasi)
  resSQL = config.CreateSQL(strSQL).RawResult

  if not resSQL.Eof:
    oInvestasi = config.CreatePObjImplProxy('Investasi')
    oInvestasi.Key = id_investasi
    no_bilyet = ''
    if not oInvestasi.IsNull:
      no_bilyet = oInvestasi.no_bilyet
    raise '\nPERINGATAN',\
      '\nInvestasi %s telah memiliki register transaksi.'\
      '\nSetujui atau tolak register tersebut untuk melanjutkan.'\
      % (no_bilyet)

def CheckTransaksiInvestasiExclusive(config, id_investasi):
  CheckTransLRInvExclusive(config, id_investasi)
  CheckTransPiutangInvExclusive(config, id_investasi)
  CheckTransPiutangLRInvExclusive(config, id_investasi)

def CheckTransactionValidity(config, oInvestasi, mode):
  if IsInvestasiTutup(config, oInvestasi) and (mode in ['uipInvestasi', 'uipDeposito', 'uipObligasi', 'uipReksadana']):
    raise '\nPERINGATAN','Investasi sudah ditutup.'
  y,m,d = oInvestasi.tgl_buka[:3]
  TB = config.ModDateTime.EncodeDate(y,m,d)
  if TB >= int(config.Now()) :
    raise '\nPERINGATAN','Transaksi tidak bisa dilakukan pada hari yang sama dgn tanggal buka'
  
  if (mode in ['uipInvestasi', 'uipDeposito', 'uipObligasi', 'uipReksadana']):
    CheckTransaksiInvestasiExclusive(config, oInvestasi.id_investasi)

def CheckHistoriRestriction(uideflist, auiname, apobjconst):
  config = uideflist.Config

  oUserApp = config.CreatePObjImplProxy('UserApp')
  oUserApp.Key = config.SecurityContext.GetUserInfo()[0]

  if oUserApp.NoLimitLocation == 'F':
    uiCalled = uideflist.GetPClassUIByName(auiname)
    no_peserta = uiCalled.ActiveRecord.no_peserta
    oRekeningDPLK = config.CreatePObjImplProxy('RekeningDPLK')
    oRekeningDPLK.Key = no_peserta

    if oRekeningDPLK.kode_cab_daftar <> oUserApp.branch_code:
      raise '\nPERINGATAN','\nAnda tidak diperkenankan melihat data peserta ini!'

def GetTransactionBatchID(config, user_id_owner, batch_status, batch_type, batch_sub_type):
  y,m,d = time.localtime()[:3]
  nowDate = '%d-%d-%d' % (y,m,d)
  strSQL = '\
    select ID_TransactionBatch \
    from TransactionBatch \
    where user_id_owner = \'%s\' and \
      batch_status = \'%s\' and \
      batch_type = \'%s\' and \
      batch_sub_type = \'%s\' and \
      tgl_used = \'%s\'' \
    % (user_id_owner, batch_status, batch_type, batch_sub_type, nowDate)
  resSQL = config.CreateSQL(strSQL).RawResult

  if resSQL.Eof:
    raise '\nPERINGATAN','\n\nBatch DPLK (transaksi ataupun registrasi) untuk '\
      'hari ini tidak ditemukan! \nHubungi Administrator untuk membuatkan batch tersebut.' 

  return resSQL.ID_TransactionBatch

def GetTransactionBatchObj(config, user_id_owner, batch_status, batch_type, batch_sub_type):
  oTransactionBatch = config.CreatePObjImplProxy('TransactionBatch')
  oTransactionBatch.Key = GetTransactionBatchID(config, user_id_owner, batch_status, batch_type, batch_sub_type)

  return oTransactionBatch

def TransCostOpr(config, oRekeningDPLK, oTransaksiDPLK, costval):  
  ##  Operasi untuk biaya administrasi transaksi
  ##  Biaya diambil secara berurutan dari:
  ##    1. akum_dana_pengembangan
  ##    2. akum_dana_iuran_pst
  ##    3. akum_dana_iuran_pk
  ##    4. akum_dana_peralihan

  #set nilai presisi float / zero_approx 
  oP = config.CreatePObjImplProxy('Parameter')
  oP.Key = 'PRESISI_ANGKA_FLOAT'
  zero_approx = oP.Numeric_Value

  whichMin = [costval, oRekeningDPLK.akum_dana_pengembangan]
  red = min(whichMin)

  #set inisialisasi mutasi
  oTransaksiDPLK.mutasi_pengembangan = 0.0
  oTransaksiDPLK.mutasi_iuran_pst = 0.0
  oTransaksiDPLK.mutasi_iuran_pk = 0.0
  oTransaksiDPLK.mutasi_peralihan = 0.0
  
  oRekeningDPLK.akum_dana_pengembangan -= red
  costval -= red
  oTransaksiDPLK.mutasi_pengembangan = -red
  
  # sinkronisasi detail akumulasi pengembangan sesuai dg proporsi paket & jenis investasinya
  Ls_DetailAkumPengembangan = oRekeningDPLK.Ls_DetailAkumPengembangan
  n = Ls_DetailAkumPengembangan.MemberCount
  Ls_DetailAkumPengembangan.First()
  sisaakum = 0
  if costval <= zero_approx: 
	for i in range(n):
	  o = Ls_DetailAkumPengembangan.CurrentElement	  
	  if (o.Nilai_Akumulasi - red) >= oRekeningDPLK.akum_dana_pengembangan:
	    #nilai akumulasi instrumen investasi paket sama dengan nilai total akumulasi pengembangan, nilai akumulasi lainnya = 0
		o.Nilai_Akumulasi -= red
	  elif o.Nilai_Akumulasi > 0:
	    o.Nilai_Akumulasi -= red * (o.LRincianPaketInvestasi.maks_proporsi / 100) + sisaakum
	    if o.Nilai_Akumulasi < 0:
		sisaakum = o.Nilai_Akumulasi
		o.Nilai_Akumulasi = 0
	  
	  Ls_DetailAkumPengembangan.Next()
  else:
	for i in range(n):
	  o = Ls_DetailAkumPengembangan.CurrentElement	  
	  o.Nilai_Akumulasi = 0
	  Ls_DetailAkumPengembangan.Next()

  if costval > zero_approx:
    whichMin = [costval, oRekeningDPLK.akum_dana_iuran_pst]
    red = min(whichMin)

    oRekeningDPLK.akum_dana_iuran_pst -= red
    costval -= red
    oTransaksiDPLK.mutasi_iuran_pst = -red

  if costval > zero_approx:
    whichMin = [costval, oRekeningDPLK.akum_dana_iuran_pk]
    red = min(whichMin)
    
    oRekeningDPLK.akum_dana_iuran_pk -= red
    costval -= red
    oTransaksiDPLK.mutasi_iuran_pk = -red
  
  if costval > zero_approx:
    whichMin = [costval, oRekeningDPLK.akum_dana_peralihan]
    red = min(whichMin)
    
    oRekeningDPLK.akum_dana_peralihan -= red
    costval -= red
    oTransaksiDPLK.mutasi_peralihan = -red
  
  if costval > zero_approx:
    #raise 'Error','Dana tidak mencukupi untuk membayar Biaya Administrasi'
    config.SendDebugMsg('Dana peserta %s tidak mencukupi untuk membayar \
      Biaya Administrasi, masih terutang Rp %0.2f' % (oRekeningDPLK.no_peserta, costval))

def FindSuperUserExceptMe(config, me):
  # fungsi untuk mencari SuperUser (have NoLimitLocation = 'T') selain User me
  ListSuperUser = []
  
  #paling gampang pake SQL
  sSQL = 'select user_id from USERAPP where NoLimitLocation = \'T\' and '\
    'user_id <> \'%s\'' % (me)
  rSQL = config.CreateSQL(sSQL).RawResult
  
  rSQL.First()
  while not rSQL.Eof:
    #masukkan hasil SQL dalam tuple ListSuperUser (insert at first)
    #untuk user ROOT akan dimasukkan manual agar tidak ganda yang masuk list
    if string.upper(rSQL.user_id) != 'ROOT':
      ListSuperUser.insert(0,rSQL.user_id) 
    
    rSQL.Next()
  
  if string.upper(me) != 'ROOT':
    #add user ROOT dalam tuple ListSuperUser manually
    ListSuperUser.insert(0,'root')
    
  return ListSuperUser

def GetSingleRPI(config, kode_paket_investasi):
  # get single rincian paket investasi based on paket investasi
  strSQL = \
    'select kode_jns_investasi '\
    'from RincianPaketInvestasi '\
    'where kode_paket_investasi = \'%s\'' \
    % (kode_paket_investasi)
  resSQL = config.CreateSQL(strSQL).RawResult

  if resSQL.Eof:
    raise '\nKesalahan GetSingleRPI','Rincian paket investasi tidak ditemukan!'

  kode_jns_investasi = resSQL.kode_jns_investasi
  resSQL.Next()
  if resSQL.Eof:
    return kode_jns_investasi
  else:
    return None

def HitungJatuhTempo(config, tglBukaTup, jenisJatuhTempo, jmlHariOnCall = None):
  # return next tglJatuhTempo datetime

  y, m, d = tglBukaTup[:3]

  if jenisJatuhTempo == 0:
    # deposito on call, hitung dari jmlHariOnCall
    tglBukaDT = config.ModDateTime.EncodeDate(y, m, d)
    return tglBukaDT + jmlHariOnCall

  if jenisJatuhTempo == 12:
    # jatuh tempo 12 bulan
    y += 1
  else:
    mNew = ((m + jenisJatuhTempo) % 12) or 12
    if mNew < m:
      y += 1
    m = mNew

  if (d >= 29) and (m == 2):
    if calendar.isleap(y):
      d = 29
    else:
      d = 28
  elif (d == 31) and (m in SHORTMOON):
    d = 30

  return config.ModDateTime.EncodeDate(y, m, d)

def IsJatuhTempo(config, oDeposito):
  nowDate = config.ModDateTime.CutDate(config.Now())
  y, m, d = oDeposito.tgl_jatuh_tempo[:3]
  jatuhTempoDT = config.ModDateTime.EncodeDate(y, m, d)

  return jatuhTempoDT <= nowDate

def GetLastDayOfMonth(m, y):
  if m == 2:
    if calendar.isleap(y):
      d = 29
    else:
      d = 28
  elif m in SHORTMOON:
    d = 30
  else:
    d = 31

  return d

def CreateLsEndOfMonth(monthFrom, yearFrom, monthUntil, yearUntil):
  ls = []
  stop = 0
  y = yearFrom
  m = monthFrom - 1
  while not stop:
    m = (m % 12) + 1

    d = GetLastDayOfMonth(m, y)
    ls.append([y, m, d])

    # set flag for the next loop
    if y >= yearUntil:
      if m >= monthUntil:
        stop = 1
    elif m >= 12:
      m = 0
      y += 1

  # end while not stop

  return ls

def resSQLRPI(config, kode_jns_investasi):
  strSQL = \
    'select kode_paket_investasi, maks_proporsi '\
    'from RincianPaketInvestasi '\
    'where kode_jns_investasi = \'%s\'; '\
    % (kode_jns_investasi)
  return config.CreateSQL(strSQL).RawResult

def resSQLJenisInvestasi(config):
  strSQL = \
    'select kode_jns_investasi, nama_jns_investasi '\
    'from JenisInvestasi; '
  return config.CreateSQL(strSQL).RawResult

def GetGLInterface(config, intf_code):
  oGLI = config.CreatePObjImplProxy('GLInterface')
  oGLI.Key = intf_code

  return oGLI  

def GetAccGiroBagiHasil(config):
  GR_BGHASIL = 'GR_BGHASIL'

  oGLI = GetGLInterface(config, GR_BGHASIL)
  if oGLI.IsNull:
    raise 'Kesalahan Kode GL Interface','\'%s\' tidak ditemukan.' % (GR_BGHASIL)

  return oGLI.account_code

def GetGiroBagiHasil(config):
  GR_BGHASIL = 'GR_BGHASIL'

  oGLI = GetGLInterface(config, GR_BGHASIL)
  if not oGLI.IsNull:
    oMasterGiro = config.CreatePObjImplProxy('MasterGiro')
    oMasterGiro.Key = oGLI.account_code

    return oMasterGiro

def CheckNoBilyetAvl(config, no_bilyet):
  strSQL = \
    'select i.id_investasi '\
    'from Investasi i, Deposito d '\
    'where (i.id_investasi = d.id_investasi) '\
    '  and (i.no_bilyet = \'%s\') '\
    % (no_bilyet)
  resSQL = config.CreateSQL(strSQL).RawResult
  resSQL.First()
  if not resSQL.Eof:
    raise 'Kesalahan No. Bilyet', 'No. Bilyet \'%s\' sudah ada.' % (no_bilyet)

def AdvanceJatuhTempo(config, oDeposito):
  oDeposito.tgl_jatuh_tempo = HitungJatuhTempo(config, oDeposito.tgl_jatuh_tempo, oDeposito.jenisJatuhTempo, oDeposito.jmlHariOnCall)
  oDeposito.rollover_counter += 1

##def resSQLRekLiabFromCheque(config, cheque_no, strInfo):
##  strSQL = \
##    'select %s '\
##    'from ListLembarCheque LLC, RekeningLiabilitas RL '\
##    'where LLC.Nomor_Rekening = RL.Nomor_Rekening '\
##    '  and LLC.No_Seri_Lembar = \'%s\' '\

def GetRekeningWasiatUmmat(config, no_peserta):
  strSQL = \
    'select rekeningwasiatummat_id '\
    'from RekeningWasiatUmmat '\
    'where no_peserta = \'%s\'; '\
    % (no_peserta)
  resSQL = config.CreateSQL(strSQL).RawResult
  resSQL.First()
  if resSQL.Eof:
    return None
    
  oRekeningWasiatUmmat = config.CreatePObjImplProxy('RekeningWasiatUmmat')
  oRekeningWasiatUmmat.Key = resSQL.rekeningwasiatummat_id 
 
  return oRekeningWasiatUmmat

def CountUnAuthTransaksiDPLK(config, no_peserta, excludeIDTrans):
  strExcludeIDTrans = '; '
  if excludeIDTrans:
    # excludeIDTrans != None
    strExcludeIDTrans = '  and ID_Transaksi <> %d ' % (excludeIDTrans)

  strSQL = \
    'select count(*) nbOfTrans '\
    'from TransaksiDPLK '\
    'where '\
    '  isCommitted = \'F\' '\
    '  and no_peserta = \'%s\' '\
    '  %s '\
    % (no_peserta, strExcludeIDTrans)
  resSQL = config.CreateSQL(strSQL).RawResult
  return resSQL.nbOfTrans

def CountUnAuthTransaksiPremi(config, no_peserta, excludeIDTrans):
  strExcludeIDTrans = '; '
  if excludeIDTrans:
    # excludeIDTrans != None
    strExcludeIDTrans = '  and ID_Transaksi <> %d ' % (excludeIDTrans)

  strSQL = \
    'select count(*) nbOfTrans '\
    'from TransaksiPremi '\
    'where '\
    '  isCommitted = \'F\' '\
    '  and no_peserta = \'%s\' '\
    '  %s '\
    % (no_peserta, strExcludeIDTrans)
  resSQL = config.CreateSQL(strSQL).RawResult
  return resSQL.nbOfTrans

def CountUnAuthIuranPendaftaran(config, no_peserta, excludeIDTrans):
  strExcludeIDTrans = '; '
  if excludeIDTrans:
    # excludeIDTrans != None
    strExcludeIDTrans = '  and ID_Transaksi <> %d ' % (excludeIDTrans)

  strSQL = \
    'select count(*) nbOfTrans '\
    'from IuranPendaftaran '\
    'where '\
    '  isCommitted = \'F\' '\
    '  and no_peserta = \'%s\' '\
    '  %s '\
    % (no_peserta, strExcludeIDTrans)
  resSQL = config.CreateSQL(strSQL).RawResult
  return resSQL.nbOfTrans

def CountUnAuthTransaksiPeserta(config, no_peserta, excludeIDTrans = None):
  return \
    CountUnAuthTransaksiDPLK(config, no_peserta, excludeIDTrans)  \
    + CountUnAuthTransaksiPremi(config, no_peserta, excludeIDTrans) \
    + CountUnAuthIuranPendaftaran(config, no_peserta, excludeIDTrans)

def GetNamaJenisInvestasi(config, kode_jns_investasi):
  o = config.CreatePObjImplProxy('JenisInvestasi')
  o.Key = kode_jns_investasi
  
  return o.nama_jns_investasi
  
def GetTotalDanaPaket(config, tgl_awal, kode_paket_investasi):
  sSQL = 'SELECT \
			SUM(mutasi_pengembangan) + \
			SUM(mutasi_iuran_pst) + \
			SUM(mutasi_iuran_pk)+ \
			SUM(mutasi_peralihan) as total_dana_paket \
			FROM RekeningDPLK R, TransaksiDPLK T \
			WHERE \
			R.no_peserta = T.no_peserta \
			AND iscommitted = \'T\' \
			AND tgl_transaksi < \'%s\'\
			AND status_dplk = \'A\' \
			AND R.kode_paket_investasi = \'%s\'' % (tgl_awal, kode_paket_investasi)
  rSQL = config.CreateSQL(sSQL).RawResult
  if rSQL.Eof or (rSQL.total_dana_paket == None):
      total_dana_paket = 0
  else:
      #total_baghas_paket = GetTotalBaghasPaket(config, tgl_baghas, tgl_baghas_plus, kode_paket_investasi)
      total_dana_paket = rSQL.total_dana_paket #- total_baghas_paket
  
  return total_dana_paket

def GetTotalDanaPeserta(config, tgl_awal, kode_paket_investasi, no_peserta):
  sSQL = 'SELECT \
			SUM(mutasi_pengembangan) + \
			SUM(mutasi_iuran_pst) + \
			SUM(mutasi_iuran_pk)+ \
			SUM(mutasi_peralihan) as total_dana_peserta \
			FROM RekeningDPLK R, TransaksiDPLK T \
			WHERE \
			R.no_peserta = T.no_peserta \
			AND tgl_transaksi < \'%s\' \
			AND status_dplk = \'A\' \
			AND iscommitted = \'T\' \
			AND R.kode_paket_investasi = \'%s\' \
			AND R.no_peserta = \'%s\'' \
			% (tgl_awal, kode_paket_investasi, no_peserta)
  rSQL = config.CreateSQL(sSQL).RawResult
  if rSQL.Eof or (rSQL.total_dana_peserta == None) :
      total_dana_peserta = 0
  else:
      #total_baghas_peserta = GetTotalBaghasPeserta(config, tgl_baghas, tgl_baghas_plus, kode_paket_investasi, no_peserta)
      total_dana_peserta = rSQL.total_dana_peserta #- total_baghas_peserta
  
  return total_dana_peserta

def GetTotalBaghasPaket(config, tgl_baghas, tgl_baghas_plus, kode_paket_investasi):
  sSQL = 'SELECT \
            ISNULL(SUM(mutasi_pengembangan),0.00) as total_baghas_paket\
            FROM RekeningDPLK R, TransaksiDPLK T \
            WHERE \
            R.no_peserta = T.no_peserta \
            AND tgl_transaksi >= \'%s\'\
            AND tgl_transaksi < \'%s\' \
            AND status_dplk = \'A\' \
            AND iscommitted = \'T\' \
            AND R.kode_paket_investasi = \'%s\' \
            AND kode_jenis_transaksi = \'G\'' \
            % (tgl_baghas, tgl_baghas_plus, kode_paket_investasi)
  rSQL = config.CreateSQL(sSQL).RawResult
  if rSQL.Eof or (rSQL.total_baghas_paket == None): total_baghas_paket = 0
  else:	total_baghas_paket = rSQL.total_baghas_paket
  
  return rSQL.total_baghas_paket

def GetTotalBaghasPeserta(config, tgl_baghas, tgl_baghas_plus, kode_paket_investasi, no_peserta):
  sSQL = 'SELECT \
            ISNULL(SUM(mutasi_pengembangan),0.00) as total_baghas_peserta\
            FROM RekeningDPLK R, TransaksiDPLK T \
            WHERE \
            R.no_peserta = T.no_peserta \
            AND tgl_transaksi >= \'%s\'\
            AND tgl_transaksi < \'%s\' \
            AND status_dplk = \'A\' \
            AND iscommitted = \'T\' \
            AND R.kode_paket_investasi = \'%s\' \
            AND kode_jenis_transaksi = \'G\'\
            AND R.no_peserta = \'%s\'' \
            % (tgl_baghas, tgl_baghas_plus, kode_paket_investasi, no_peserta)
  rSQL = config.CreateSQL(sSQL).RawResult
  if rSQL.Eof or (rSQL.total_baghas_peserta == None): total_baghas_peserta = 0
  else:	total_baghas_peserta = rSQL.total_baghas_peserta
  
  return rSQL.total_baghas_peserta

def GetDanaIdlePaket(config, kode_paket):
   sSQL = 'SELECT dana_idle FROM PaketInvestasi \
   WHERE kode_paket_investasi = \'%s\' ' % (kode_paket)
   rSQL = config.CreateSQL(sSQL).RawResult   
   if (rSQL.Eof) or (rSQL.dana_idle == None): dana_idle_paket = 0
   else: dana_idle_paket = rSQL.dana_idle   
   
   return dana_idle_paket
