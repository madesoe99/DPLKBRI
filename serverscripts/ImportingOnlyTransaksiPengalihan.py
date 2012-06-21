import sys, DBAppFramework, dafdb, string, re, os, time
sys.path.append('c:/dafapp/dplk07/scripts/master')
sys.path.append('c:/dafapp/dplk07/scripts/transaction')
sys.path.append('c:/dafapp/dplk07/scripts/transaksi')

#-------------------------------------------------------------------------------
## VARIABLE GLOBAL
#-------------------------------------------------------------------------------
#IP Server yang digunakan saat menjalankan script migrasi ini
v_IP_Server = '127.0.0.1'
#Batas tahun valid yang diakui
v_TahunValid = 1800
#Kelipatan transaksi yang akan disimpan ke basisdata
v_KelipatanTransaksi = 50
#Variabel yang akan digunakan sebagai patokan awal migrasi
#Variabel ini harus diganti dengan nilai ter-commit terakhir bila ada error transaksi
#Untuk saat awal akan migrasi, nilainya diperoleh berdasarkan sort query sql 
#from TransaksiDPLK order by kelima variabel tersebut (sesuai urutan) di basisdata 
#lama (interbase/firebird). Ambil Row yang pertama (firebird memakai FIRST)
v_last_tgl_transaksi = '0200-01-06 00:00:00'
v_last_operator = 'ADMIN'
v_last_kode_jenis_transaksi = 'K'
v_last_no_peserta = '30100004982'
v_last_id_transaksi = 143788
#Berikut merupakan variabel dummy untuk mengeset variable yang invalid
v_DummyYear = 1990
v_TanggalAutodebet = 1
v_TanggalAkseptasiWasiatUmmat = 1  
v_BulanAkseptasiWasiatUmmat = 1
v_TahunAkseptasiWasiatUmmat = 1990

def ValidateDate(config, y, m, d):
  global v_TahunValid, v_DummyYear

  if y < v_TahunValid:
    y = v_DummyYear
  
  return config.ModLibUtils.EncodeDate(y, m, d)
  
#-------------------------------------------------------------------------------
## EMPTYING TABLE
#-------------------------------------------------------------------------------
def EmptyingTable(config, con, tableName):
  print 'Emptying table %s' % (tableName)
  res = config.ExecSQL('Delete from %s' % (tableName))

  return res
  
def CreateFileLog(config, JenisLog, NamaFile):  
  homeDir = config.GetHomeDir()
  pLogFile = homeDir + NamaFile
  isAddLog = 0
  if os.access(pLogFile, os.F_OK):
    #hapus file NamaFile jika ada  
    #os.remove(pLogFile)
    #TAMBAHKAN LOG-NYA SAJA
    isAddLog = 1
    
  if isAddLog:
    #tambahin log
    logFile = open(pLogFile,'a')
    logFile.write('\n----------\n')
  else:
    #buat file log baru
    logFile = open(pLogFile,'w+')

  print '\n%s anomali dicatat pada file %s' % (JenisLog, pLogFile)

  return logFile

def ConvertKodePaket(s):
  #buang spasi bila ada
  s = s.lstrip().rstrip()
  
  #mapping kode paket investasi lama dengan kode paket investasi yang baru
  dictPaketInvestasi = {'1':'A','2':'B','3':'C','4':'D','5':'E'}
  
  return dictPaketInvestasi[s]

def remakeString(s):
  #membuang spasi kosong didepan, mengganti spasi diantara kata dengan underscore
  #mengkapitalkan semua huruf, hilangkan '.'
  if s:
    s = s.lstrip().rstrip().replace('. ','_').replace('.','_').replace(' ','_').upper()
  
  return s

def CreateBatch(config, batchType, batchSubType, branchCode, dtTglTransaksi, \
  userIDOwner):
  global v_IP_Server
  
  oTB = config.CreatePObject('TransactionBatch')
  
  oTB.batch_type = batchType
  oTB.batch_sub_type = batchSubType
  oTB.branch_code = branchCode
  oTB.tgl_create = oTB.tgl_used = dtTglTransaksi
  oTB.user_id_owner = userIDOwner
  oTB.terminal_id_create = v_IP_Server
  
  #asumsi yang membuat batch ialah admin
  oTB.user_id_create = 'root' 

  # account_link_type batch diasumsikan 'Single'
  oTB.account_link_type = 'S'
  
  #status batch langsung 'Closed' 
  oTB.batch_status = 'C'
  
  #journal block id batch diset 0 supaya tidak bisa dikonversi menjadi jurnal Acc
  oTB.journal_block_id = 0
  
  #set nomor batch
  oTB.no_batch = 'B' + oTB.batch_type + '.' + oTB.user_id_owner + '.' + \
    str(oTB.tgl_used[0]) + \
    str(string.zfill(oTB.tgl_used[1],2)) + \
    str(string.zfill(oTB.tgl_used[2],2)) + '.' + str(oTB.ID_TransactionBatch)
  
  return oTB  

#-------------------------------------------------------------------------------
## STEP 0 CODE: user management table
#-------------------------------------------------------------------------------
def BranchLocation(config, con):
  print '\n\nifx_KodeCabang (semua data cabang BMI)...'
  # kosongkan BranchLocation
  res = config.ExecSQL('Delete from BranchLocation')
  if res >= 0:
    #tidak error, lanjutkan import data semua kantor cabang
    rSQL = config.CreateSQL('select i.nmrcab,i.namcab,i.cabind \
      from ifx_KodeCabang i order by i.nmrcab').RawResult
    while not rSQL.Eof:
      o = config.CreatePObject('BranchLocation')      
      o.branch_code = rSQL.nmrcab.rstrip()
      o.BranchName = rSQL.namcab.rstrip()
      
      #set cabang induk
      if rSQL.cabind != o.branch_code:
        #kantor cabang pembantu, mempunyai cabang induk
        o.masterbranch_code = rSQL.cabind 
        o.BranchStatus = 'S'
      else:
        #bukan kantor cabang pembantu
        o.BranchStatus = 'B'
      
      #sementara TimeZone disamakan untuk Waktu Indonesia Barat
      o.Branch_Time_Zone = 'B'
            
      o.user_id = 'root'
      o.last_update = config.ModLibUtils.Now()
      
      #flushing to database
      config.FlushUpdates()
      
      rSQL.Next()
    
    print 'INFORMASI!\nMohon set TimeZone tiap Cabang secara manual '\
      '(semuanya masih diset TimeZone Waktu Indonesia Barat)'
  else:
    raise 'ERROR','Gagal memproses tabel BranchLocation'

  return 1
  
def Counter(config, con):
  print '\n\nCounter (reset Tabel Counter untuk Registrasi peserta)...'
  # kosongkan Counter
  res = config.ExecSQL('Delete from COUNTER')
  if res >= 0:
    #tidak error, lanjutkan update data Counter registrasi
    config.ExecSQL('insert into COUNTER (ID_CODE, LAST_ID, IS_LOCKED, PARAM) \
                      select \'NASABAHDPLK\', 1, 0, branch_code from BRANCHLOCATION')
    print 'Tidak ada informasi tambahan'
  else:
    raise 'ERROR','Gagal memproses tabel Counter'

  return 1

def UserAppTeller(config, con):
  print '\n\nifx_DaftarTeller (semua User Teller)...'
  # kosongkan UserApp
  res = config.ExecSQL('Delete from UserApp')
  if res >= 0:
    #tidak error, lanjutkan import semua user Teller
    rSQL = config.CreateSQL('select i.userid,i.namusr,i.nmrcab \
      from ifx_DaftarTeller i order by i.namusr').RawResult  
    while not rSQL.Eof:
      #buat UserApp
      o = config.CreatePObject('UserApp')      
      o.user_id = rSQL.userid.rstrip()
      o.UserName = rSQL.namusr.rstrip()
      o.branch_code = rSQL.nmrcab
      o.Description = 'Teller Kantor Cabang %s' % (o.branch_code)
      o.NoLimitLocation = 'F'      
      #o.confidential_code =       
      
      #set untuk supervisor user
      #o.user_id1 = 'userID supervisor'

      o.last_update = config.ModLibUtils.Now()
      
      #buatkan langsung UserGroupApp
      oUGA = config.CreatePObject('UserGroupApp')
      oUGA.user_id = o.user_id
      oUGA.group_id = 'Teller'
                  
      #flushing to database
      config.FlushUpdates()
      
      rSQL.Next()
      
    print 'INFORMASI!\nMohon untuk:'\
      '\n 1) set terminal id bila user tersebut ialah Teller'\
      '\n 2) lakukan Security Data Validation'\
      '\n 3) cek kesesuaian Data Teller dengan lokasi Kantor Cabangnya saat ini'
  else:
    raise 'ERROR','Gagal memproses tabel UserApp untuk Teller'

  return 1

def UserApp(config, con):
  print '\n\nUSERDPLK...'
  # tidak perlu mengosongkan UserApp
  try:
    q = con.GetQuery('select * from USERDPLK')
    while not q.Eof():
      if q.GetFieldValue('USER_ID') != 'root':
        #kecuali root, sebab akan membuat error saat Security Data Validation
        o = config.CreatePObject('UserApp')      
        o.user_id = q.GetFieldValue('USER_ID')
        o.UserName = q.GetFieldValue('USER_NAME')
        o.Description = q.GetFieldValue('DESCRIPTION')
        o.branch_code = q.GetFieldValue('KODE_CAB_DAFTAR')    
        #o.confidential_code =       
        
        #set untuk supervisor user
        #o.user_id1 =
    
        o.last_update = config.ModLibUtils.Now()
        
      #flushing to database
      config.FlushUpdates()
              
      q.Next()
      
    print 'INFORMASI!\nMohon untuk:'\
      '\n 1) set Grup pengguna disesuaikan dengan daftar Grup yang baru secara manual'\
      '\n 2) set NoLimitLocation untuk pengguna tertentu (Admin atau selevel dengannya)'\
      '\n 3) cek kesesuaian User dengan kantor cabang user berasal secara manual'\
      '\n 4) lakukan Security Data Validation'
  except:
    raise 'ERROR','Gagal memproses tabel UserApp'

  return 1
#-------------------------------------------------------------------------------
## STEP 1 CODE: independen table
#-------------------------------------------------------------------------------
def DaerahAsal(config, con):
  print '\n\nDAERAH_ASAL...'
  # kosongkan DaerahAsal
  res = config.ExecSQL('Delete from DaerahAsal')
  if res >= 0:
    #tidak error, lanjutkan import data daerah asal lama  
    q = con.GetQuery('select * from DAERAH_ASAL')
    while not q.Eof():
      o = config.CreatePObject('DaerahAsal')      
      o.kode_propinsi = q.GetFieldValue('KODE_PROPINSI')
      o.nama_propinsi = q.GetFieldValue('NAMA_PROPINSI')
            
      o.user_id = 'root'
      o.last_update = config.ModLibUtils.Now()
      
      #flushing to database
      config.FlushUpdates()
      
      q.Next()
    
  else:
    raise 'ERROR','Gagal memproses tabel DaerahAsal'

  return 1

def JenisUsaha(config, con):
  print '\n\nJENIS_USAHA...'
  # kosongkan JenisUsaha
  res = config.ExecSQL('Delete from JenisUsaha')
  if res >= 0:
    #tidak error, lanjutkan import data jenis usaha lama  
    q = con.GetQuery('select * from JENIS_USAHA')
    while not q.Eof():
      o = config.CreatePObject('JenisUsaha')      
      o.kode_jenis_usaha = q.GetFieldValue('KODE_JENIS_USAHA')
      o.nama_jenis_usaha = q.GetFieldValue('NAMA_JENIS_USAHA')
            
      o.user_id = 'root'
      o.last_update = config.ModLibUtils.Now()

      #flushing to database
      config.FlushUpdates()

      q.Next()
    
  else:
    raise 'ERROR','Gagal memproses tabel JenisUsaha'

  return 1

def JenisPortofolio(config, con):
  print '\n\nJENIS_PORTOFOLIO...'
  print 'INFORMASI!\nUntuk jenis portofolio, mohon diisi secara manual di bagian '\
    'Investasi->Master->Jenis Investasi'

  return 1

def PaketInvestasi(config, con):
  print '\n\nPAKET_INVESTASI...'
  print 'INFORMASI!\nUntuk Paket Investasi, mohon dicek secara manual di bagian '\
    'Investasi->Master->Paket Investasi'
    
  return 1

def Kepemilikan(config, con):
  print '\n\nKEPEMILIKAN...'
  print 'INFORMASI!\nUntuk Kepemilikan, mohon dicek secara manual di bagian '\
    'Liabilitas->Master->Kepemilikan'

  return 1

def PihakKetiga(config, con):
  print '\n\nPIHAK_KETIGA...'
  # kosongkan PihakKetiga
  res = config.ExecSQL('Delete from PihakKetiga')
  if res >= 0:
    #tidak error, lanjutkan import data pihak ketiga lama  
    q = con.GetQuery('select * from PIHAK_KETIGA')
    while not q.Eof():
      o = config.CreatePObject('PihakKetiga')      
      o.kode_pihak_ketiga = q.GetFieldValue('KODE_PIHAK_KETIGA')
      o.nama_pihak_ketiga = q.GetFieldValue('NAMA_PIHAK_KETIGA')
      o.alamat_pihak_ketiga = q.GetFieldValue('ALAMAT_PIHAK3')
      
      # untuk self investment / pihak terkait cek dengan regex
      if re.search('BMI',q.GetFieldValue('KODE_PIHAK_KETIGA')):
        #ada frasa 'BMI', diasumsikan sebagai self investment
        o.self_investment = 'T'
      else:
        o.self_investment = 'F'
            
      o.user_id = 'root'
      o.last_update = config.ModLibUtils.Now()

      #flushing to database
      config.FlushUpdates()

      q.Next()
    
    print 'INFORMASI!\nMohon cek Pihak Terkait (T/F) untuk tiap data Pihak Ketiga '\
      'yang telah diimpor di bagian Investasi->Master->Pihak Ketiga'
  else:
    raise 'ERROR','Gagal memproses tabel PihakKetiga'

  return 1
  
def SumberDana(config, con):
  print '\n\nSUMBER_DANA...'
  # kosongkan SumberDana
  res = EmptyingTable(config, con, 'SumberDana')
  if res >= 0:
    #tidak error, lanjutkan import data sumber dana yang lama
    
    #ambil informasi sumber dana yang ada di field Sumber_Dana tabel Rekening_DPLK,
    #sebab DB lama tidak memiliki tabel Sumber_Dana
    q = con.GetQuery('select DISTINCT SUMBER_DANA from REKENING_DPLK')
    while not q.Eof():
      o = config.CreatePObject('SumberDana')      
      o.sumber_dana = q.GetFieldValue('SUMBER_DANA')
      
      o.user_id = 'root'
      o.last_update = config.ModLibUtils.Now()

      #flushing to database
      config.FlushUpdates()

      q.Next()
    
    print 'INFORMASI!\nMohon cek dan isi Sumber_Dana dan Keterangan untuk tiap data Sumber Dana '\
      'yang telah diimpor di bagian Liabilitas->Master->Sumber Dana'  
  else:
    raise 'ERROR','Gagal memproses tabel SumberDana'

  return 1

def KelompokNasabah(config, con):
  print '\n\nKELOMPOK_NASABAH...'
  # kosongkan Kelompok
  res = EmptyingTable(config, con, 'Kelompok')
  if res >= 0:
    #tidak error, lanjutkan import data kelompok nasabah DPLK yang lama
    
    #ambil informasi kelompok yang ada di field Kode_Kelompok tabel Nasabah_DPLK,
    #sebab tabel Kelompok_Nasabah kosong
    q = con.GetQuery('select DISTINCT KODE_KELOMPOK from NASABAH_DPLK \
      where KODE_KELOMPOK is not null and KODE_KELOMPOK <> \'\'')
    while not q.Eof():
      o = config.CreatePObject('Kelompok')      
      o.kode_kelompok = q.GetFieldValue('KODE_KELOMPOK')
      
      o.user_id = 'root'
      o.last_update = config.ModLibUtils.Now()

      #flushing to database
      config.FlushUpdates()

      q.Next()
    
    print 'INFORMASI!\nMohon cek dan isi Nama_Kelompok dan Keterangan untuk tiap data Kelompok '\
      'yang telah diimpor di bagian Liabilitas->Master->Kelompok'  
  else:
    raise 'ERROR','Gagal memproses tabel Kelompok'

  return 1
  
def LembagaDanaPensiun(config, con):
  print '\n\nLembagaDanaPensiun (LDP)...'
  # kosongkan Lembaga Dana Pensiun (LDP)
  res = EmptyingTable(config, con, 'LDP')
  if res >= 0:
    #tidak error, lanjutkan import data nama dplk lain yang lama
    
    #ambil informasi dplk lain yang ada di field:
    # 1) Nama_DPLK, Alamat tabel Pengalihan_Dari_DPLK_Lain
    # 2) Nama_DPLK2, Alamat_DPLK2 tabel Pengalihan_Ke_DPLK_Lain
    tupleSQL = ['select distinct p1.NAMA_DPLK as NAMADPLK, p1.ALAMAT as ALAMAT \
                  from PENGALIHAN_DARI_DPLK_LAIN p1', 
                'select DISTINCT p2.NAMA_DPLK2 as NAMADPLK, p2.ALAMAT_DPLK2 \
                  as ALAMAT from PENGALIHAN_KE_DPLK_LAIN p2 where p2.NAMA_DPLK2 \
                  is not null']
    for sSQL in tupleSQL:
      q = con.GetQuery(sSQL)
      while not q.Eof():
        #cek masalah kode yang dibuat dari NAMA_DPLK
        candKodeDP = remakeString(q.GetFieldValue('NAMADPLK'))
        
        #cek apakah sudah ada objek LDP dengan kode seperti candKodeDP
        o = config.CreatePObjImplProxy('LDP')
        o.Key = candKodeDP
        if o.IsNull:
          #belum ada objek dengan kode DP = candKodeDP, buat objek baru
          #cara biasa Error, dicoba dengan INSERT langsung
          #oN = config.CreatePObject('LDP')        
          #oN.kode_dp = candKodeDP
          #oN.nama_dp = q.GetFieldValue('NAMADPLK')
          #oN.alamat_dp = q.GetFieldValue('ALAMAT')
          
          #cek jenis LDP (DPLK, DPK, DPPK) dari nama dplk yang diimport
          if (re.search('DPLK_',candKodeDP)) or (re.search('DPLK',candKodeDP)):
            #termasuk 'DPLK'
            #oN.jenis_dp = 'B'
            jenisDP = 'B'
          elif (re.search('DAPEN_',candKodeDP)) or (re.search('DP_',candKodeDP)) or \
            (re.search('DPPK_',candKodeDP)):
            #termasuk 'DPPK'
            #oN.jenis_dp = 'A'
            jenisDP = 'A'
          else:
            #selainnya, semua LDP yang diimport diasumsikan sebagai 'DPK'
            #oN.jenis_dp = 'C'
            jenisDP = 'C'
    
          #oN.user_id = 'root'
          #oN.last_update = config.ModLibUtils.Now()
          y,m,d = config.ModLibUtils.DecodeDate(config.ModLibUtils.Now())[:3]
          sSQL = 'insert into LDP(KODE_DP,NAMA_DP,ALAMAT_DP,JENIS_DP, \
            USER_ID,LAST_UPDATE) values (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' \
            % (candKodeDP,q.GetFieldValue('NAMADPLK'),q.GetFieldValue('ALAMAT'),\
            jenisDP,'root','%d-%d-%d' % (y,m,d)) 
          res = config.ExecSQL(sSQL)
                  
        #flushing to database
        config.FlushUpdates()

        q.Next()
    
    print 'INFORMASI!\nMohon cek dan isi KodeDP, NamaDP, Alamat untuk tiap data LDP '\
      'yang telah diimpor di bagian Liabilitas->Master->Lembaga Dana Pensiun'\
      '\n 1) periksa semantik kode Dana Pensiun, masih banyak data sama disebabkan data lama redundan'\
      '\n 2) semua data DP yang diimport diasumsikan berjenis DPK, yang lain (DPLK / DPPK) mohon set secara manual'\
      '\n    kecuali ada keterangan tambahan yang tertera di Nama DP yang diimport'\
      '\n 3) lengkapi data untuk nama terang DP dan alamatnya'
  else:
    raise 'ERROR','Gagal memproses tabel LembagaDanaPensiun'

  return 1


#-------------------------------------------------------------------------------
## STEP 2 CODE: main reference table
#-------------------------------------------------------------------------------
def NasabahDPLK(config, con):
  global v_IP_Server, v_TahunValid 

  print '\n\nNASABAH_DPLK...'
  #kosongkan NasabahDPLK
  res = EmptyingTable(config, con, 'NasabahDPLK')
  if res >= 0:
    #tidak error, lanjutkan import data nasabah DPLK yang lama
    q = con.GetQuery('select * from NASABAH_DPLK')
    while not q.Eof():
      o = config.CreatePObject('NasabahDPLK')
      o.no_peserta = q.GetFieldValue('NO_PESERTA').lstrip().rstrip()
      o.nama_lengkap = q.GetFieldValue('NAMA_LENGKAP').lstrip().rstrip()
      y,m,d = q.GetFieldValue('TGL_REGISTRASI')[:3]
      o.tgl_registrasi = ValidateDate(config, y,m,d)
      o.tempat_lahir = q.GetFieldValue('TEMPAT_LAHIR')
      y,m,d = q.GetFieldValue('TANGGAL_LAHIR')[:3]
      o.tanggal_lahir = ValidateDate(config, y,m,d)
      
      o.pekerjaan = q.GetFieldValue('PEKERJAAN')
      o.nama_perusahaan = q.GetFieldValue('NAMA_PERUSAHAAN')
      
      if q.GetFieldValue('KODE_KELOMPOK') not in [None,' ','']: 
        o.kode_kelompok = q.GetFieldValue('KODE_KELOMPOK')
      o.kode_jenis_usaha = q.GetFieldValue('KODE_JENIS_USAHA')
      o.kode_propinsi = q.GetFieldValue('KODE_PROPINSI')
      o.kode_pemilikan = q.GetFieldValue('KODE_PEMILIKAN')
      
      o.alamat_jalan = o.alamat_surat_jalan = q.GetFieldValue('ALAMAT_JALAN')
      o.alamat_rtrw = o.alamat_surat_rtrw = q.GetFieldValue('ALAMAT_RTRW')
      o.alamat_kelurahan = o.alamat_surat_kelurahan = q.GetFieldValue('ALAMAT_KELURAHAN')
      o.alamat_kota = o.alamat_surat_kota = q.GetFieldValue('ALAMAT_KOTA')
      o.alamat_kode_pos = o.alamat_surat_kode_pos = q.GetFieldValue('ALAMAT_KODE_POS')
      o.alamat_telepon = q.GetFieldValue('ALAMAT_TELEPON')
      
      o.alamat_kantor_jalan = q.GetFieldValue('ALAMAT_KANTOR_JALAN')
      o.alamat_kantor_kota = q.GetFieldValue('ALAMAT_KANTOR_KOTA')
      o.alamat_kantor_propinsi = q.GetFieldValue('ALAMAT_KANTOR_PROPINSI')
      o.alamat_kantor_telepon = q.GetFieldValue('ALAMAT_KANTOR_TELEPON')
      
      #set info dplk lain bila ikut DPLK lain
      o.dplklain = q.GetFieldValue('DPLKLAIN')
      
      #set status export?? -> SKIP STATUS_EXPORT FROM DATA LAMA
      
      o.operation_code = 'F'
      o.isCommitted = 'T'      
      o.user_id = o.auth_user_id = 'root'
      o.last_update = config.ModLibUtils.Now()
      o.terminal_id = o.last_terminal_id = v_IP_Server 
      
      #flushing update
      config.FlushUpdates()
      
      q.Next()
    
    print 'INFORMASI!\nMohon untuk (sebab data lama tidak memuat informasi tersebut):'\
      '\n 1) set JENIS KELAMIN untuk tiap peserta secara manual'\
      '\n 2) ALAMAT SURAT (untuk kirim statement) peserta disamakan dengan data ALAMAT'\
      '\n 3) set KODE NASABAH CORPORATE bila peserta termasuk anggota peserta perusahaan tertentu'
  else:
    raise 'ERROR','Gagal memproses tabel NasabahDPLK'
  
  return 1
  
def RekeningDPLK(config, con):
  global v_IP_Server, v_TanggalAutodebet, v_TahunAkseptasiWasiatUmmat,\
    v_BulanAkseptasiWasiatUmmat,v_TanggalAkseptasiWasiatUmmat

  print '\n\nREKENING_DPLK...'
  #kosongkan RekeningDPLK, RekeningAutoDebet, RekeningWasiatUmmat
  tupleTabel = ['RekeningDPLK','RekeningAutoDebet','RekeningWasiatUmmat']
  for namaTabel in tupleTabel:
    res = EmptyingTable(config, con, namaTabel)
  
  if res >= 0:
    #tidak error, lanjutkan import data nasabah DPLK yang lama
    q = con.GetQuery('select * from REKENING_DPLK')
    while not q.Eof():
      o = config.CreatePObject('RekeningDPLK')
      o.no_peserta = q.GetFieldValue('NO_PESERTA').lstrip().rstrip()
      
      #debug code
      config.SendDebugMsg(str(q.GetFieldValue('NO_PESERTA').lstrip().rstrip()))
      
      o.akum_dana_iuran_pk = 0.0
      o.akum_dana_iuran_pst = abs(q.GetFieldValue('AKUM_DANA_IURAN'))
      o.akum_dana_pengembangan = abs(q.GetFieldValue('AKUM_DANA_PENGEMBANGAN'))
      o.akum_dana_peralihan = abs(q.GetFieldValue('AKUM_DANA_PERALIHAN'))
      
      o.iuran_pk = 0.0
      #cek hubungan dengan info KENAIKAN_IURAN di data lama
      if q.GetFieldValue('KENAIKAN_IURAN') in [None,0.0]:
        #tidak mengalami kenaikan iuran, ambil data dari besar iuran
        o.iuran_pst = q.GetFieldValue('BESAR_IURAN')
      else:
        o.iuran_pst = q.GetFieldValue('KENAIKAN_IURAN')
        
      o.kode_cab_daftar = q.GetFieldValue('KODE_CAB_DAFTAR').lstrip().rstrip()
      o.sumber_dana = q.GetFieldValue('SUMBER_DANA')
      
      #sesuaikan kode paket investasi dengan yang baru
      o.kode_paket_investasi = \
        ConvertKodePaket(q.GetFieldValue('KODE_PAKET_INVESTASI'))
      
      #cek tgl_akseptasi jika ada yang NULL
      if q.GetFieldValue('TGL_AKSEPTASI') not in [[],None]:
        #tgl_akseptasi tidak NULL
        y,m,d = q.GetFieldValue('TGL_AKSEPTASI')[:3]
        o.tgl_akseptasi = ValidateDate(config, y,m,d)
      
      o.usia_pensiun = q.GetFieldValue('USIA_PENSIUN')
      y,m,d = q.GetFieldValue('TGL_PENSIUN')[:3]
      o.tgl_pensiun = ValidateDate(config, y,m,d)
      y,m,d = q.GetFieldValue('TGL_PENSIUN_DIPERCEPAT')[:3]      
      o.tgl_pensiun_dipercepat = ValidateDate(config, y,m,d)
      
      #cek tgl_tutup jika ada yang NULL
      if q.GetFieldValue('TGL_TUTUP') not in [[],None]:
        #tgl_tutup tidak NULL
        y,m,d = q.GetFieldValue('TGL_TUTUP')[:3]
        o.tgl_tutup = ValidateDate(config, y,m,d)
      
      o.status_dplk = q.GetFieldValue('STATUS_DPLK').lstrip().rstrip()
      o.status_biaya_daftar = 'T'

      #cek tgl_srr_akhir jika ada yang NULL
      if q.GetFieldValue('TGL_SRR_AKHIR') not in [[],None]:
        #tgl_srr_akhir tidak NULL
        y,m,d = q.GetFieldValue('TGL_SRR_AKHIR')[:3]
        o.tgl_srr_akhir = ValidateDate(config, y,m,d)
        o.srr_akhir = q.GetFieldValue('SRR_AKHIR')
      else:
        #tgl_srr_akhir NULL
        o.srr_akhir = 0.0
        
      #cek status autodebet peserta
      if q.GetFieldValue('AUTODEBET_REKENING') not in [None,'0','']:
        #ikut autodebet

        #cek apakah no rekening autodebet sudah dipakai
        oRA_temp = config.CreatePObjImplProxy('RekeningAutoDebet')
        noRekAutodebet = q.GetFieldValue('AUTODEBET_REKENING').lstrip().rstrip() 
        oRA_temp.SetKey('no_rekening',noRekAutodebet)
        oRA_temp.SetKey('no_peserta',q.GetFieldValue('NO_PESERTA').lstrip().rstrip())
        if oRA_temp.IsNull:
          #belum ada no rekening autodebet yang sama
          #buatkan rekening autodebet
          #oRA = config.CreatePObject('RekeningAutoDebet')
          #oRA.no_rekening = noRekAutodebet
          
          #oRA.LRekeningDPLK = o
          #if q.GetFieldValue('AUTODEBET_NAMA') not in [None,'']:
          #  oRA.nama_rekening = q.GetFieldValue('AUTODEBET_NAMA')
          namaRekening = q.GetFieldValue('AUTODEBET_NAMA')
          
          o.status_autodebet = 'T'
          
          #ganti sintax dengan insert SQL
          sSQL = 'insert into RekeningAutoDebet(NAMA_REKENING,NO_REKENING,NO_PESERTA,TANGGAL_AUTODEBET) \
            values (\'%s\',\'%s\',\'%s\',%d)' \
            % (namaRekening,noRekAutodebet,q.GetFieldValue('NO_PESERTA').lstrip().rstrip(),\
              v_TanggalAutodebet) 
          res = config.ExecSQL(sSQL)
                    
          #DIDAPATKAN DARI MANAKAH DATA INI...???
          #SEMENTARA DIASUMSIKAN TANGGAL 1 TIAP BULANNYA
          #oRA_temp.tanggal_autodebet = v_TanggalAutodebet
        else:
          #sudah ada no rekening autodebet yang sama
          print '\nINFO: peserta %s seharusnya tercatat sebagai autodebet \
            dengan no rekening autodebet %s, tetapi no rekening tersebut \
            bentrok dengan peserta lain. Mohon dihandle secara manual.' \
            % (q.GetFieldValue('NO_PESERTA').lstrip().rstrip(),noRekAutodebet)
      else:
        #tidak ikut autodebet
        o.status_autodebet = 'F'
        
      #cek status wasiat ummat peserta
      if q.GetFieldValue('WASIAT_UMMAT').lstrip().rstrip() == 'T':
        #peserta ikut wasiat ummat
        o.status_wasiat_ummat = 'T'
        o.collectivity_wasiat_ummat = 'T'
        o.kewajiban_wasiat_ummat = 0.0
        
        #create objek rekening wasiat ummat
        oRWU = config.CreatePObject('RekeningWasiatUmmat')
        oRWU.auth_user_id = oRWU.user_id = 'root'
        oRWU.LRekeningDPLK = o
        oRWU.besar_premi = q.GetFieldValue('PREMI_ASURANSI')
        oRWU.manfaat_asuransi = q.GetFieldValue('MANFAAT_ASURANSI')
        if q.GetFieldValue('NO_POLIS') not in [None,0.0]:
          oRWU.no_polis = q.GetFieldValue('NO_POLIS')
        #diset sama dengan tanggal pensiun
        y,m,d = q.GetFieldValue('TGL_PENSIUN')[:3]
        oRWU.tgl_berakhir = ValidateDate(config, y,m,d)
        
        #DIDAPATKAN DARI MANA INFORMASI INI ???
        oRWU.tgl_akseptasi = ValidateDate(config, \
          v_TahunAkseptasiWasiatUmmat,v_BulanAkseptasiWasiatUmmat,\
          v_TanggalAkseptasiWasiatUmmat)
      else:
        #tidak ikut wasiat ummat
        o.status_wasiat_ummat = 'F'
      
      #cek status anuitas peserta lewat status status DPLK
      if q.GetFieldValue('STATUS_DPLK').lstrip().rstrip() == 'N':
        #peserta sudah non aktif  
        o.status_anuitas = 'T'
        
        if q.GetFieldValue('TGL_BAYAR_ANUITAS') != None:
          o.tgl_bayar_anuitas = q.GetFieldValue('TGL_BAYAR_ANUITAS')
        if q.GetFieldValue('NILAI_BAYAR_ANUITAS') not in [None,0.0]:
          o.nilai_bayar_anuitas = q.GetFieldValue('NILAI_BAYAR_ANUITAS')
          
      elif q.GetFieldValue('STATUS_DPLK').lstrip().rstrip() == 'A':
        #peserta masih aktif
        o.status_anuitas = 'F'
        o.nilai_bayar_anuitas = 0.0
      #else:
        #peserta berstatus 'Suspend' 
        #tidak ada peserta yang berstatus ini pada data lama
      
      #asumsi semua dikirim ke Rumah (alamat rumah)
      o.kirim_statemen = 'R'
      o.operation_code = 'F'
      o.user_id = o.auth_user_id = 'root'
      o.last_update = config.ModLibUtils.Now()
      o.last_terminal_id = v_IP_Server
      
      #informasi yang tidak dipergunakan
      #CARA_BAYAR
      #STATUS_KOMISI
      #POTENSI_PROFIT_LOSS
            
      #flushing database
      config.FlushUpdates()
      
      q.Next()
    
    print 'INFORMASI!\nMohon untuk (sebab data lama tidak memuat informasi tersebut):'\
      '\n 1) cek AKUM DANA IURAN PK dan IURAN PK secara manual bila peserta termasuk anggota peserta perusahaan tertentu'\
      '\n    (asumsi di set nilai 0)'\
      '\n 2) cek KIRIM STATEMENT, asumsi dikirim ke alamat rumah peserta (data kirim statement lama berbeda/tidak terdefinisi jelas)'\
      '\n 3) DATA KRUSIAL! Mohon isi Tanggal Autodebet untuk tiap peserta yang ikut autodebet'\
      '\n    (untuk sementara semuanya diasumsikan tanggal 1)'\
      '\n 4) peserta Wasiat Ummat DIASUMSIKAN TIDAK ADA TUNGGAKAN PREMI!'\
      '\n 5) tanggal akseptasi peserta Wasiat Ummat MASIH DIKOSONGKAN!'
  else:
    raise 'ERROR','Gagal memproses tabel RekeningDPLK'

  return 1

#-------------------------------------------------------------------------------
## STEP 3 CODE: Nasabah-related table
#-------------------------------------------------------------------------------

def UbahAlamat(config, con):
  global v_IP_Server

  print '\n\nHISTORI_PINDAH_ALAMAT...'
  # kosongkan HistoriUbahAlamat
  res = config.ExecSQL('Delete from HistoriUbahAlamat')
  if res >= 0:
    #tidak error, lanjutkan import data histori pindah alamat lama  
    q = con.GetQuery('select * from HISTORI_PINDAH_ALAMAT')
    while not q.Eof():
      o = config.CreatePObject('HistoriUbahAlamat')
      o.alamat_jalan = q.GetFieldValue('HIST_ALAMAT_JALAN')
      o.alamat_kelurahan = q.GetFieldValue('HIST_ALAMAT_KELURAHAN')
      o.alamat_kode_pos = q.GetFieldValue('HIST_ALAMAT_KODE_POS')
      o.alamat_kota = q.GetFieldValue('HIST_ALAMAT_KOTA')
      o.alamat_rtrw = q.GetFieldValue('HIST_ALAMAT_RTRW')
      o.alamat_telepon = q.GetFieldValue('HIST_ALAMAT_TELEPON')
      
      o.no_referensi = q.GetFieldValue('NO_REFERENSI')
      y,m,d = q.GetFieldValue('TGL_PINDAH')[:3]
      o.tanggal_histori = ValidateDate(config, y,m,d)
      o.no_peserta = q.GetFieldValue('NO_PESERTA')
      o.keterangan = 'hasil import data lama'

      o.user_id = o.auth_user_id = 'root'
      o.terminal_id = v_IP_Server

      #flushing to database
      config.FlushUpdates()

      q.Next()
    
    print 'INFORMASI!\nMohon cek data Histori Ubah Alamat yang baru saja diimpor'
  else:
    raise 'ERROR','Gagal memproses tabel HistoriUbahAlamat'

  return 1

def HistoriIuran(config, con):
  global v_IP_Server

  print '\n\nHISTORI_IURAN...'
  # kosongkan HistoriIuran
  res = config.ExecSQL('Delete from HistoriIuran')
  if res >= 0:
    #tidak error, lanjutkan import data histori iuran lama  
    q = con.GetQuery('select * from HISTORI_IURAN')
    while not q.Eof():
      o = config.CreatePObject('HistoriIuran')
      o.iuran_pk = 0.0
      o.iuran_pst = q.GetFieldValue('BESAR_IURAN_LAMA')
      
      o.no_referensi = q.GetFieldValue('NO_REFERENSI')
      y,m,d = q.GetFieldValue('TGL_UBAH')[:3]
      o.tanggal_histori = ValidateDate(config, y,m,d)
      o.no_peserta = q.GetFieldValue('NO_PESERTA')

      o.user_id = o.auth_user_id = 'root'
      o.terminal_id = v_IP_Server

      #flushing to database
      config.FlushUpdates()

      q.Next()
    
    print 'INFORMASI!\nMohon cek data Histori Iuran yang baru saja diimpor'
  else:
    raise 'ERROR','Gagal memproses tabel HistoriIuran'

  return 1

def AhliWaris(config, con):
  global v_TahunValid

  print '\n\nPENERIMA_MANFAAT...'
  # kosongkan AhliWaris
  res = config.ExecSQL('Delete from AhliWaris')
  if res >= 0:
    #tidak error, lanjutkan import data Ahli Waris lama  
    q = con.GetQuery('select * from PENERIMA_MANFAAT order by NO_PESERTA, '\
      'NO_URUT_TRM_MANFAAT')
    
    #persiapkan file ImportAhliWaris.log
    logFile = CreateFileLog(config, 'AhliWaris', 'ImportAhliWaris.log')

    lastNoPeserta = q.GetFieldValue('NO_PESERTA')
    i = 1
    while not q.Eof():
      o = config.CreatePObject('AhliWaris')
      o.nama_lengkap = q.GetFieldValue('NM_TRM_MANFAAT')
      o.jenis_kelamin = q.GetFieldValue('JENIS_KELAMIN')
      
      if q.GetFieldValue('TGL_LAHIR_MANFAAT') not in [None,[]]:
        y,m,d = q.GetFieldValue('TGL_LAHIR_MANFAAT')[:3]
        o.tanggal_lahir = ValidateDate(config, y,m,d)

        if y <= v_TahunValid:
          #lebih kecil dari tahun valid
          #diganti dengan tahun dummy logging ke log
          print '\nData asal NO_URUT_TRM_MANFAAT Penerima Manfaat %s memiliki \
            anomali TGL_LAHIR_MANFAAT (diganti dengan tahun dummy)' \
            % (q.GetFieldValue('NO_URUT_TRM_MANFAAT'))
            
          #log ke file ImportAhliWaris.log 
          logFile.write('Data asal NO_URUT_TRM_MANFAAT Penerima Manfaat %s memiliki anomali TGL_LAHIR_MANFAAT (tahun = %d)' \
            % (q.GetFieldValue('NO_URUT_TRM_MANFAAT'),y)+'\n')        
          
      o.hubungan_keluarga = q.GetFieldValue('KODE_HUB_KELUARGA')
      
      #asumsi semua ahli waris masih aktif
      o.status_ahli_waris = 'A'

      #ubah cara penomoran urut prioritas ahli waris
      if q.GetFieldValue('NO_PESERTA') != lastNoPeserta:
        #peserta berbeda, reset nomor urut ahli waris dan lastNoPeserta
        i= 1
        lastNoPeserta = q.GetFieldValue('NO_PESERTA') 
      
      o.nomor_urut_prioritas = i
      i += 1
      o.no_peserta = lastNoPeserta
      o.keterangan = 'hasil import data lama'

      #flushing to database
      config.FlushUpdates()

      q.Next()

    #close file ImportAhliWaris.log
    logFile.close()
    
    print 'INFORMASI!\nMohon untuk (sebab data lama tidak memuat informasi tersebut):'\
      '\n 1) cek STATUS AHLI WARIS, diasumsikan semua masih aktif'
  else:
    raise 'ERROR','Gagal memproses tabel AhliWaris'

  return 1

#-------------------------------------------------------------------------------
## STEP 4 CODE: Transaksi-related table
#-------------------------------------------------------------------------------

def BagiHasil(config, con):
  print '\n\nBAGI_HASIL...'
  # kosongkan BagiHasil
  res = config.ExecSQL('Delete from BagiHasil')
  lastdtTglTransaksi = 0
  lastOperator = ''
  if res >= 0:
    #tidak error, lanjutkan import data bagi hasil lama  
    q = con.GetQuery('select  KODE_PAKET_INVESTASI, IDBGHASIL, TGL_BAGI_HASIL, \
                              KEUNTUNGAN_DIBAGIKAN, INDEKS \
                      from    BAGI_HASIL t')
    while not q.Eof():    
      #create bagi hasil
      o = config.CreatePObject('BagiHasil')
      o.indeks = q.GetFieldValue('INDEKS')
      o.keuntungan_dibagikan = q.GetFieldValue('KEUNTUNGAN_DIBAGIKAN')
      o.kode_paket_investasi = \
        ConvertKodePaket(q.GetFieldValue('KODE_PAKET_INVESTASI'))
      
      y,m,d = q.GetFieldValue('TGL_BAGI_HASIL')[:3]
      dtTglBagiHasil = ValidateDate(config, y,m,d)
      o.tgl_bagi_hasil = dtTglBagiHasil        
      
      #flushing to database
      config.FlushUpdates()

      q.Next()
    
    print 'INFORMASI!\ntidak ada info'
  else:
    raise 'ERROR','Gagal memproses tabel BagiHasil'
  
  return 1

def Pendaftaran(config, con):  
  global v_IP_Server

  print '\n\nPENDAFTARAN...'
  # konversi dari Pendaftaran ke tabel IuranPendaftaran
  # kosongkan IuranPendaftaran
  res = config.ExecSQL('Delete from IuranPendaftaran')
  lastdtTglTransaksi = 0
  lastOperator = ''
  if res >= 0:
    #tidak error, lanjutkan import data (iuran) pendaftaran lama  
    q = con.GetQuery('select  p.ID_TRANSAKSI,\
                              p.CATATAN_PENDAFTARAN,\
                              p.BIAYA_DAFTAR,\
                              t.NO_PESERTA,\
                              t.TGL_TRANSAKSI,\
                              t.OPERATOR_ADDED\
                      from    TRANSAKSI_DPLK t,\
                              PENDAFTARAN p\
                      where   p.ID_TRANSAKSI = t.ID_TRANSAKSI\
                      order by t.TGL_TRANSAKSI, t.OPERATOR_ADDED, t.NO_PESERTA, \
                               t.ID_TRANSAKSI')
    while not q.Eof():    
      #create iuran pendaftaran
      o = config.CreatePObject('IuranPendaftaran')
      o.besar_biaya_daftar = q.GetFieldValue('BIAYA_DAFTAR')
      
      y,m,d = q.GetFieldValue('TGL_TRANSAKSI')[:3]
      dtTglTransaksi = ValidateDate(config, y,m,d)
      o.tgl_transaksi = o.tgl_otorisasi = o.tgl_sistem = dtTglTransaksi        

      o.no_peserta = q.GetFieldValue('NO_PESERTA')
      o.keterangan = 'hasil import data lama: %s' \
        % (q.GetFieldValue('CATATAN_PENDAFTARAN'))
      o.isCommitted = 'T'
      if q.GetFieldValue('OPERATOR_ADDED') != None:
        o.user_id = o.user_id_auth = q.GetFieldValue('OPERATOR_ADDED')
      else:
        #bila nama operator null, diasumsikan dilakukan oleh 'Admin'
        o.user_id = o.user_id_auth = 'admin'
      o.terminal_id = o.terminal_id_auth = v_IP_Server

      #set branch code menjadi di 'Kantor Pusat' (301)
      o.branch_code = '301'

      #create batch pendaftaran sesuai tanggal transaksi      
      if lastdtTglTransaksi != dtTglTransaksi or lastOperator != o.user_id:
        #tanggal transaksi / nama operator berbeda, 
        #reset batchID, lastdtTglTransaksi, lastOperator
        oTB = CreateBatch(config, 'R', 'M', o.branch_code, \
          dtTglTransaksi, o.user_id)
        lastdtTglTransaksi = dtTglTransaksi
        lastOperator = o.user_id  
      
      o.ID_TransactionBatch = oTB.ID_TransactionBatch
      
      #flushing to database
      config.FlushUpdates()

      q.Next()
    
    print 'INFORMASI!\nDisebabkan data lama tidak memuat informasi tertentu, maka:'\
      '\n 1) cabang pendaftaran semua data diasumsikan dilakukan di 301 - Kantor Pusat Arthaloka'\
      '\n 2) nama operator yang NULL diasumsikan dilakukan oleh ADMIN'
  else:
    raise 'ERROR','Gagal memproses tabel IuranPendaftaran'
  
  return 1
  
def TransaksiPremi(config, con):
  global v_IP_Server, v_TahunValid

  print '\n\nBAYAR_PREMI...'
  # konversi dari BayarPremi ke tabel TitipanPremi
  # kosongkan TransaksiPremi, TitipanPremi, SetoranPremi, TransaksiPremiManual 
  res = config.ExecSQL('Delete from TransaksiPremi')
  lastdtTglTransaksi = 0
  lastOperator = ''
  if res >= 0:
    #tidak error, lanjutkan import data (transaksi premi) bayar premi lama  
    q = con.GetQuery('select  p.ID_TRANSAKSI,\
                              p.CATATAN_BAYAR_PREMI,\
                              t.NO_PESERTA,\
                              t.TGL_TRANSAKSI,\
                              t.MUTASI_PREMI,\
                              t.OPERATOR_ADDED\
                      from    TRANSAKSI_DPLK t,\
                              BAYAR_PREMI p\
                      where   p.ID_TRANSAKSI = t.ID_TRANSAKSI\
                      order by t.TGL_TRANSAKSI, t.OPERATOR_ADDED, t.NO_PESERTA, \
                               t.ID_TRANSAKSI')

    #persiapkan file ImportTransaksiPremi.log
    logFile = CreateFileLog(config, 'TransaksiPremi', 'ImportTransaksiPremi.log')

    while not q.Eof():    
      #create titipan premi
      o = config.CreatePObject('TitipanPremi')
      o.mutasi_premi = q.GetFieldValue('MUTASI_PREMI')
      
      y,m,d = q.GetFieldValue('TGL_TRANSAKSI')[:3]
      dtTglTransaksi = ValidateDate(config, y,m,d)
      #cek validitas tanggal
      if y <= v_TahunValid:
        #terdapat anomali data tanggal
        print '\nINFO: ID Transaksi Premi %d memiliki anomali tahun transaksi \
          (diset dengan tahun dummy)' % (q.GetFieldValue('ID_TRANSAKSI'))
          
        #log ke file ImportTransaksiPremi.log
        logFile.write('ID Transaksi Premi %d memiliki anomali tanggal transaksi (tahun = %d)' \
          % (q.GetFieldValue('ID_TRANSAKSI'),y)+'\n')        

      o.tgl_transaksi = o.tgl_otorisasi = o.tgl_sistem = dtTglTransaksi        

      o.no_peserta = q.GetFieldValue('NO_PESERTA')
      o.keterangan = 'hasil import data lama: %s' \
        % (q.GetFieldValue('CATATAN_BAYAR_PREMI'))
      o.isCommitted = 'T'
      o.isDebet = 'F'
      if q.GetFieldValue('OPERATOR_ADDED') != None:
        o.user_id = o.user_id_auth = q.GetFieldValue('OPERATOR_ADDED')
      else:
        #bila nama operator null, diasumsikan dilakukan oleh 'Admin'
        o.user_id = o.user_id_auth = 'admin'
      o.terminal_id = o.terminal_id_auth = v_IP_Server

      #set branch code menjadi di 'Kantor Pusat' (301)
      o.branch_code = '301'

      #create batch premi sesuai tanggal transaksi      
      if lastdtTglTransaksi != dtTglTransaksi or lastOperator != o.user_id:
        #tanggal transaksi / nama operator berbeda, 
        #reset batchID, lastdtTglTransaksi, lastOperator
        oTB = CreateBatch(config, 'P', 'M', o.branch_code, \
          dtTglTransaksi, o.user_id)
        lastdtTglTransaksi = dtTglTransaksi
        lastOperator = o.user_id 
      
      o.ID_TransactionBatch = oTB.ID_TransactionBatch
      
      #flushing to database
      config.FlushUpdates()

      q.Next()

    #close file ImportTransaksiPremi.log
    logFile.close()
    
    print 'INFORMASI!\nDisebabkan data lama tidak memuat informasi tertentu, maka:'\
      '\n 1) cabang tempat transaksi dilakukan semua data diasumsikan dilakukan di 301 - Kantor Pusat Arthaloka'\
      '\n 2) semua transaksi bayar premi diasumsikan sebagai transaksi titipan premi'\
      '\n 3) nama operator yang NULL diasumsikan dilakukan oleh ADMIN'
  else:
    raise 'ERROR','Gagal memproses tabel TitipanPremi (TransaksiPremi)'
  
  return 1
  
def TransaksiDPLK(config, con):
  global v_KelipatanTransaksi, v_TahunValid, v_last_tgl_transaksi, \
    v_last_operator, v_last_kode_jenis_transaksi, v_last_no_peserta, \
    v_last_id_transaksi

  print '\n\nTRANSAKSI_DPLK...'
  # konversi dari tiap jenis Transaksi_DPLK ke tiap tabel TransaksiDPLK
  # kosongkan TransaksiDPLK, PengalihanDariDPLKLain, PengalihanKeDPLKLain, 
  # PengambilanManfaat
  dictNamaTabel = {1:'TransaksiDPLK',2:'PengalihanDariDPLKLain',\
    3:'PengalihanKeDPLKLain',4:'PengambilanManfaat'}
  res = 0
  
  #kode berikut ditutup sebab menggunakan commit per-N transaksi
  #supaya hasil commit sebelumnya tidak dihapus
  #i = 1
  #while res >= 0 and i <= 4:
  #  res = config.ExecSQL('Delete from %s' % (dictNamaTabel[i]))
  #  i += 1
  
  lastdtTglTransaksi = 0
  lastOperator = ''
  if res >= 0:
    #tidak error, lanjutkan import data (transaksi DPLK) transaksi_DPLK lama
    #ambil data yang tidak termasuk dalam transaki DPLK 'deleted'
    #data terurut berdasarkan tanggal transaksi, nama operator, 
    #kode jenis transaksi, no peserta, id transaksi   
    q = con.GetQuery('select  t.ID_TRANSAKSI, \
                              t.NO_PESERTA, \
                              t.TGL_TRANSAKSI, \
                              t.KODE_JENIS_TRANSAKSI, \
                              t.OPERATOR_ADDED, \
                              t.MUTASI_DANA_IURAN, \
                              t.MUTASI_DANA_PERALIHAN, \
                              t.MUTASI_PENGEMBANGAN, \
                              t.MUTASI_BAGI_HASIL, \
                              t.MUTASI_POTONGAN_IURAN, \
                              t.MUTASI_POTONGAN_PENGEMBANGAN, \
                              t.MUTASI_POTONGAN_PERALIHAN, \
                              t.MUTASI_PAJAK, \
                              t.KD_PAKET_INV \
                      from    TRANSAKSI_DPLK t \
                      where   t.KODE_JENIS_TRANSAKSI in (\'I\',\'H\') and \
                              t.ISDELETED is NULL and \
                              ((t.TGL_TRANSAKSI > \'%s\') OR \
                               (t.TGL_TRANSAKSI = \'%s\' AND \
                                  t.OPERATOR_ADDED > \'%s\') OR \
                               (t.TGL_TRANSAKSI = \'%s\' AND \
                                  t.OPERATOR_ADDED = \'%s\' AND \
                                  t.KODE_JENIS_TRANSAKSI > \'%s\') OR \
                               (t.TGL_TRANSAKSI = \'%s\' AND \
                                  t.OPERATOR_ADDED = \'%s\' AND \
                                  t.KODE_JENIS_TRANSAKSI = \'%s\' AND \
                                  t.NO_PESERTA > \'%s\') OR \
                               (t.TGL_TRANSAKSI = \'%s\' AND \
                                  t.OPERATOR_ADDED = \'%s\' AND \
                                  t.KODE_JENIS_TRANSAKSI = \'%s\' AND \
                                  t.NO_PESERTA = \'%s\' AND \
                                  t.ID_TRANSAKSI > %d)) \
                      order by t.TGL_TRANSAKSI, t.OPERATOR_ADDED, t.KODE_JENIS_TRANSAKSI, \
                               t.NO_PESERTA, t.ID_TRANSAKSI' \
                      % (v_last_tgl_transaksi, v_last_tgl_transaksi, v_last_operator, \
                         v_last_tgl_transaksi, v_last_operator, v_last_kode_jenis_transaksi, \
                         v_last_tgl_transaksi, v_last_operator, v_last_kode_jenis_transaksi, \
                         v_last_no_peserta, v_last_tgl_transaksi, v_last_operator, \
                         v_last_kode_jenis_transaksi, v_last_no_peserta, v_last_id_transaksi))
    
    #persiapkan file ImportTransaksiDPLK.log
    logFile = CreateFileLog(config, 'TransaksiDPLK', 'ImportTransaksiDPLK.log')
    
    i = 1
    config.BeginTransaction()
    try:
      while not q.Eof():
        #debug code
        config.SendDebugMsg('id transaksi '+str(q.GetFieldValue('ID_TRANSAKSI')))
        config.SendDebugMsg('transaksi ke-'+str(i))
            
        #cek untuk tiap tanggal yang terdapat dalam transaksi DPLK
        y,m,d = q.GetFieldValue('TGL_TRANSAKSI')[:3]
        dtTglTransaksi = ValidateDate(config, y,m,d)
        
        #cek validitas tanggal
        if y <= v_TahunValid:
          #terdapat anomali data tanggal
          print '\nINFO: ID Transaksi DPLK %d memiliki anomali tahun transaksi \
            (diset dengan tahun dummy)' % (q.GetFieldValue('ID_TRANSAKSI'))
  
          #log ke file ImportTransaksiDPLK.log
          logFile.write('ID Transaksi DPLK %d memiliki anomali tanggal transaksi (tahun = %d)' \
            % (q.GetFieldValue('ID_TRANSAKSI'),y)+'\n')

        branchCode = '301'
        #default operator untuk migrasi ialah 'root'
        if q.GetFieldValue('OPERATOR_ADDED') != None:
          operatorName = q.GetFieldValue('OPERATOR_ADDED')
        else:
          #bila nama operator null, diasumsikan dilakukan oleh 'root'
          operatorName = 'root'
  
        #create batch transaksi sesuai tanggal transaksi      
        if lastdtTglTransaksi != dtTglTransaksi or lastOperator != operatorName:
          #tanggal transaksi berbeda, reset batchID dan lastdtTglTransaksi
          oTB = CreateBatch(config, 'T', 'M', branchCode, \
            dtTglTransaksi, operatorName)
          lastdtTglTransaksi = dtTglTransaksi
          lastOperator = operatorName 
        
        #cek jenis transaksi pada tanggal yang bersangkutan
        kodeJenisTransaksi = q.GetFieldValue('KODE_JENIS_TRANSAKSI')
        if kodeJenisTransaksi == 'I':
          PengalihanDariDPLKLain(config, con, oTB, q, dtTglTransaksi)
        elif kodeJenisTransaksi == 'K':          
          IuranPeserta(config, con, oTB, q, dtTglTransaksi)
        elif kodeJenisTransaksi == 'H':          
          PengalihanKeDPLKLain(config, con, oTB, q, dtTglTransaksi)
        elif kodeJenisTransaksi == 'E':          
          PenarikanDana(config, con, oTB, q, dtTglTransaksi)
        elif kodeJenisTransaksi == 'J':          
          PengambilanManfaat(config, con, oTB, q, dtTglTransaksi)
        elif kodeJenisTransaksi == 'C':          
          BiayaPengelolaanDana(config, con, oTB, q, dtTglTransaksi)
        elif kodeJenisTransaksi == 'D':          
          BiayaAdmTahunan(config, con, oTB, q, dtTglTransaksi)
        elif kodeJenisTransaksi == 'G':          
          TransaksiBagiHasil(config, con, oTB, q, dtTglTransaksi)
        elif kodeJenisTransaksi == 'F':          
          PindahPaketInvestasi(config, con, oTB, q, dtTglTransaksi)
  
        #flushupdate database 
        config.FlushUpdates()
          
        #cek counter i
        if i % v_KelipatanTransaksi == 0:
          #tampilkan data transaksi terakhir yang akan di-commit
          y,m,d,h,mi,s = q.GetFieldValue('TGL_TRANSAKSI')[:6]
          config.SendDebugMsg('tgl transaksi (last committed) (y:m:d h:mi:s) %d:%d:%d %d:%d:%d' \
            % (y,m,d,h,mi,s))
          config.SendDebugMsg('nama operator  (last committed) '+str(q.GetFieldValue('OPERATOR_ADDED')))
          config.SendDebugMsg('kode transaksi (last committed) '+str(q.GetFieldValue('KODE_JENIS_TRANSAKSI')))
          config.SendDebugMsg('no peserta     (last committed) '+str(q.GetFieldValue('NO_PESERTA')))
          config.SendDebugMsg('id transaksi   (last committed) '+str(q.GetFieldValue('ID_TRANSAKSI')))
        
          #tiap kelipatan v_KelipatanTransaksi (variabel global) transaksi
          #dicommit          
          config.Commit()
          
          #BeginTransaction lagi
          config.BeginTransaction()
          
        #inkremen
        i += 1
        q.Next()
        
      #commit untuk data yang masih tersisa 
      config.Commit()         
    except:
      config.Rollback()
      raise
            
    #close file ImportTransaksiDPLK.log
    logFile.close()
    
    print '\nINFORMASI!\nDisebabkan data lama tidak memuat informasi tertentu, maka:'\
      '\n 1) cabang tempat transaksi dilakukan semua data diasumsikan dilakukan di 301 - Kantor Pusat Arthaloka'\
      '\n 2) coba cek file c:/dafapp/*.log yang berisi transaksi bersifat anomali'
  else:
    raise 'ERROR','Gagal memproses tabel TransaksiDPLK'
  
  return 1

def PengalihanDariDPLKLain(config, con, oTransactionBatch, query, dtTglTransaksi):
  global v_IP_Server

  print '\n\nPENGALIHAN_DARI_DPLK_LAIN...'
  
  #ambil data lengkap PENGALIHAN DARI DPLK LAIN dari tabel untuk id transaksi tertentu
  q = con.GetQuery('select t.NAMA_DPLK, \
                           t.NO_DPLK_LAIN \
                    from   PENGALIHAN_DARI_DPLK_LAIN t \
                    where  t.ID_TRANSAKSI = %d' \
                    % (query.GetFieldValue('ID_TRANSAKSI')))
  
  if not q.Eof():
    #create transaksi Pengalihan Dari DPLK Lain
    o = config.CreatePObject('PengalihanDariDPLKLain')
    
    if q.GetFieldValue('NO_DPLK_LAIN') != None:
      o.no_dplk_lain = q.GetFieldValue('NO_DPLK_LAIN')  
  
    #asumsi nama DP sudah terdaftar dalam LDP (sudah diimport sebelumnya)
    o.kode_dp = remakeString(q.GetFieldValue('NAMA_DPLK'))
    
    o.saldo_iuran_pk = o.saldo_iuran_pst = o.saldo_pengembangan = 0.0  
    o.saldo_peralihan = query.GetFieldValue('MUTASI_DANA_PERALIHAN')
      
    #set untuk field parent (TransaksiDPLK) 
    o.mutasi_iuran_pk = o.mutasi_iuran_pst = o.mutasi_pengembangan = 0.0
    o.mutasi_peralihan = o.saldo_peralihan
    
    o.tgl_transaksi = o.tgl_otorisasi = o.tgl_sistem = dtTglTransaksi        
    o.no_peserta = query.GetFieldValue('NO_PESERTA')
    o.keterangan = 'hasil import data lama ID transaksi: %d' \
      % (query.GetFieldValue('ID_TRANSAKSI'))
    o.isCommitted = 'T'
    if query.GetFieldValue('OPERATOR_ADDED') != None:
      o.user_id = o.user_id_auth = query.GetFieldValue('OPERATOR_ADDED')
    o.terminal_id = o.terminal_id_auth = v_IP_Server
    o.ID_TransactionBatch = oTransactionBatch.ID_TransactionBatch
    if query.GetFieldValue('KD_PAKET_INV') != None:
      o.kode_paket_investasi = ConvertKodePaket(query.GetFieldValue('KD_PAKET_INV')) 
  
    #set branch code menjadi di 'Kantor Pusat' (301)
    o.branch_code = '301'
    
    #cek jenis LDP untuk mengeset kode jenis transaksi Pengalihan dari DPLK lain
    #A = DPPK, B = DPLK, C = DPK
    dictJenisDP = {'A':'O','B':'I','C':'P'}
    o.kode_jenis_transaksi = dictJenisDP[o.LLDP.jenis_dp]
      
  return 1

def IuranPeserta(config, con, oTransactionBatch, query, dtTglTransaksi):
  global v_IP_Server

  print '\n\nIURAN_PESERTA...'
  
  #ambil data lengkap IURAN PESERTA dari tabel untuk id transaksi tertentu
  q = con.GetQuery('select t.CATATAN_BAYAR_IURAN \
                    from   IURAN_PESERTA t \
                    where  t.ID_TRANSAKSI = %d' \
                    % (query.GetFieldValue('ID_TRANSAKSI')))
  
  if not q.Eof():
    #create transaksi Iuran Peserta, asumsi tidak ada titipan premi saat iuran peserta
    o = config.CreatePObject('IuranPeserta')
    
    if q.GetFieldValue('CATATAN_BAYAR_IURAN') != None:
      o.catatan_bayar_iuran = q.GetFieldValue('CATATAN_BAYAR_IURAN')  
  
    #set untuk field parent (TransaksiDPLK) 
    o.mutasi_iuran_pk = o.mutasi_peralihan = o.mutasi_pengembangan = 0.0
    o.mutasi_iuran_pst = query.GetFieldValue('MUTASI_DANA_IURAN')
    
    o.tgl_transaksi = o.tgl_otorisasi = o.tgl_sistem = dtTglTransaksi        
    o.no_peserta = query.GetFieldValue('NO_PESERTA')
    o.keterangan = 'hasil import data lama ID transaksi: %d' \
      % (query.GetFieldValue('ID_TRANSAKSI'))
    o.isCommitted = 'T'
    if query.GetFieldValue('OPERATOR_ADDED') != None:
      o.user_id = o.user_id_auth = query.GetFieldValue('OPERATOR_ADDED')
    o.terminal_id = o.terminal_id_auth = v_IP_Server
    o.ID_TransactionBatch = oTransactionBatch.ID_TransactionBatch
    if query.GetFieldValue('KD_PAKET_INV') != None:
      o.kode_paket_investasi = ConvertKodePaket(query.GetFieldValue('KD_PAKET_INV')) 
  
    #set branch code menjadi di 'Kantor Pusat' (301)
    o.branch_code = '301'

  return 1

def PengalihanKeDPLKLain(config, con, oTransactionBatch, query, dtTglTransaksi):
  global v_IP_Server

  print '\n\nPENGALIHAN_KE_DPLK_LAIN...'
  
  #ambil data lengkap PENGALIHAN KE DPLK LAIN dari tabel untuk id transaksi tertentu
  q = con.GetQuery('select t.NAMA_DPLK2, t.AKUMULASI_IURAN, \
                           t.AKUMULASI_PENGEMBANGAN, t.NO_DPLK_LAIN2, \
                           t.DANA_DIALIHKAN, t.MUTASI_BIAYA_LAIN, t.KTR_BIAYA_LAIN, \
                           t.ID_TRANSAKSI1, t.ID_TRANSAKSI12, t.USER_NAME, \
                           t.COUNT_ADVIS, t.AKUMULASI_PERALIHAN \
                    from   PENGALIHAN_KE_DPLK_LAIN t \
                    where  t.ID_TRANSAKSI = %d' \
                    % (query.GetFieldValue('ID_TRANSAKSI')))
  
  if not q.Eof():
    #create transaksi Pengalihan Ke DPLK Lain
    o = config.CreatePObject('PengalihanKeDPLKLain')
    
    #asumsi nama DP sudah terdaftar dalam LDP (sudah diimport sebelumnya)
    o.kode_dp = remakeString(q.GetFieldValue('NAMA_DPLK2'))
   
    o.saldo_iuran_pk = 0.0  
    o.saldo_iuran_pst = q.GetFieldValue('AKUMULASI_IURAN')
    o.saldo_pengembangan = q.GetFieldValue('AKUMULASI_PENGEMBANGAN')
    o.saldo_peralihan = q.GetFieldValue('AKUMULASI_PERALIHAN')
    
    o.saldo_jml_dana = o.saldo_iuran_pk + o.saldo_iuran_pst + o.saldo_pengembangan + \
      o.saldo_peralihan
      
    #ambil informasi untuk biaya adm tahunan
    if q.GetFieldValue('ID_TRANSAKSI1') not in [None,'',0]:
      #mempunyai biaya administrasi tahunan
      qBAdm = con.GetQuery('select t.MUTASI_POTONGAN_PENGEMBANGAN \
                            from   TRANSAKSI_DPLK t \
                            where  t.ID_TRANSAKSI = %d' \
                            % (q.GetFieldValue('ID_TRANSAKSI1')))
      if not qBAdm.Eof(): 
        o.biaya_administrasi = qBAdm.GetFieldValue('MUTASI_POTONGAN_PENGEMBANGAN')
        
      #buat objek biaya adm tahunan
      oBAdm = config.CreatePObject('BiayaAdmTahunan')
      oBAdm.mutasi_pengembangan = -o.biaya_administrasi
      oBAdm.mutasi_iuran_pk = oBAdm.mutasi_iuran_pst = oBAdm.mutasi_peralihan = 0.0
    
      oBAdm.tgl_transaksi = oBAdm.tgl_otorisasi = oBAdm.tgl_sistem = dtTglTransaksi          
      oBAdm.no_peserta = query.GetFieldValue('NO_PESERTA')  
      oBAdm.keterangan = 'biaya adm tahunan untuk hasil import data lama ID transaksi: %d' \
        % (q.GetFieldValue('ID_TRANSAKSI1'))
        
      oBAdm.isCommitted = 'T'
      if query.GetFieldValue('OPERATOR_ADDED') != None:
        oBAdm.user_id = oBAdm.user_id_auth = query.GetFieldValue('OPERATOR_ADDED')
    
      oBAdm.terminal_id = oBAdm.terminal_id_auth = v_IP_Server
      oBAdm.ID_TransactionBatch = oTransactionBatch.ID_TransactionBatch
      if query.GetFieldValue('KD_PAKET_INV') != None:
        oBAdm.kode_paket_investasi = \
          ConvertKodePaket(query.GetFieldValue('KD_PAKET_INV')) 
    
      #set branch code menjadi di 'Kantor Pusat' (301)
      oBAdm.branch_code = '301'

      o.ID_Transaksi_BAdmThn = oBAdm.ID_Transaksi
  
    #ambil informasi untuk biaya pengelolaan
    if q.GetFieldValue('ID_TRANSAKSI12') not in [None,'',0]:
      #mempunyai biaya pengelolaan
      qBPeng = con.GetQuery('select t.MUTASI_POTONGAN_PENGEMBANGAN \
                            from   TRANSAKSI_DPLK t \
                            where  t.ID_TRANSAKSI = %d' \
                            % (q.GetFieldValue('ID_TRANSAKSI12')))
      if not qBPeng.Eof(): 
        o.biaya_pengelolaan = qBPeng.GetFieldValue('MUTASI_POTONGAN_PENGEMBANGAN')
        
      #buat objek biaya pengelolaan
      oBPeng = config.CreatePObject('BiayaPengelolaanDana')
      oBPeng.mutasi_pengembangan = -o.biaya_pengelolaan
      oBPeng.mutasi_iuran_pk = oBPeng.mutasi_iuran_pst = oBPeng.mutasi_peralihan = 0.0
      
      oBPeng.tgl_transaksi = oBPeng.tgl_otorisasi = oBPeng.tgl_sistem = dtTglTransaksi          
      oBPeng.no_peserta = query.GetFieldValue('NO_PESERTA')  
      oBPeng.keterangan = 'biaya pengelolaan untuk hasil import data lama ID transaksi: %d' \
        % (q.GetFieldValue('ID_TRANSAKSI12'))
        
      oBPeng.isCommitted = 'T'
      if query.GetFieldValue('OPERATOR_ADDED') != None:
        oBPeng.user_id = oBPeng.user_id_auth = query.GetFieldValue('OPERATOR_ADDED')
    
      oBPeng.terminal_id = oBPeng.terminal_id_auth = v_IP_Server
      oBPeng.ID_TransactionBatch = oTransactionBatch.ID_TransactionBatch
      if query.GetFieldValue('KD_PAKET_INV') != None:
        oBPeng.kode_paket_investasi = \
          ConvertKodePaket(query.GetFieldValue('KD_PAKET_INV')) 
    
      #set branch code menjadi di 'Kantor Pusat' (301)
      oBPeng.branch_code = '301'

      o.ID_Transaksi_BPeng = oBPeng.ID_Transaksi
  
    #biaya pindah diasumsikan 0
    o.biaya_pindah = 0.0
    o.ID_Transaksi_BAdmTrans = None
    
    o.saldo_dana_dipindahkan = o.saldo_jml_dana - o.biaya_administrasi - \
      o.biaya_pengelolaan - o.biaya_pindah
    
    #jenis biaya lain diasumsikan ialah Pindah Buku
    o.jenis_biaya = 'P'
    if q.GetFieldValue('MUTASI_BIAYA_LAIN') != None:
      o.biaya_lain = q.GetFieldValue('MUTASI_BIAYA_LAIN')
    else:
      o.biaya_lain = 0.0
    o.ktr_biaya_lain = q.GetFieldValue('KTR_BIAYA_LAIN')
    
    if q.GetFieldValue('DANA_DIALIHKAN') != None:
      o.dana_dialihkan = q.GetFieldValue('DANA_DIALIHKAN')
    else:
      o.dana_dialihkan = 0.0
      
    if q.GetFieldValue('COUNT_ADVIS') != None:
      o.count_advis = q.GetFieldValue('COUNT_ADVIS')
    
    #set untuk field parent (TransaksiDPLK) 
    o.mutasi_iuran_pk = 0.0
    o.mutasi_iuran_pst = query.GetFieldValue('MUTASI_DANA_IURAN')
    o.mutasi_pengembangan = query.GetFieldValue('MUTASI_PENGEMBANGAN')
    o.mutasi_peralihan = query.GetFieldValue('MUTASI_DANA_PERALIHAN')
    
    o.tgl_transaksi = o.tgl_otorisasi = o.tgl_sistem = dtTglTransaksi          
    o.no_peserta = query.GetFieldValue('NO_PESERTA')  
    o.keterangan = 'hasil import data lama ID transaksi: %d' \
      % (query.GetFieldValue('ID_TRANSAKSI'))
      
    o.isCommitted = 'T'
    if query.GetFieldValue('OPERATOR_ADDED') != None:
      o.user_id = o.user_id_auth = query.GetFieldValue('OPERATOR_ADDED')
  
    o.terminal_id = o.terminal_id_auth = v_IP_Server
    o.ID_TransactionBatch = oTransactionBatch.ID_TransactionBatch
    if query.GetFieldValue('KD_PAKET_INV') != None:
      o.kode_paket_investasi = ConvertKodePaket(query.GetFieldValue('KD_PAKET_INV')) 
  
    #set branch code menjadi di 'Kantor Pusat' (301)
    o.branch_code = '301'

  return 1

def PenarikanDana(config, con, oTransactionBatch, query, dtTglTransaksi):
  global v_IP_Server

  print '\n\nPENARIKAN_DANA...'

  #ambil data lengkap PENARIKAN DANA dari tabel untuk id transaksi tertentu
  q = con.GetQuery('select t.SALDO_IURAN_DIBEBANI, t.PERSEN_DANA_IURAN, \
                           t.SISA_IURAN, PENARIKAN_PHK, t.DANA_DITERIMA, \
                           t.MUTASI_BIAYA_LAIN, t.KTR_BIAYA_LAIN, t.USER_NAME, \
                           t.COUNT_ADVIS, t.JML_TARIK \
                    from   PENARIKAN_DANA t \
                    where  t.ID_TRANSAKSI = %d' \
                    % (query.GetFieldValue('ID_TRANSAKSI')))
  
  if not q.Eof():
    #cek apakah termasuk penarikan dana sebagian ataukah penarikan phk
    #bila tidak terdefinisi DIANGGAP SEBAGAI penarikan sebagian
    if q.GetFieldValue('PENARIKAN_PHK') == 'T':
      #jenis penarikan PHK
      jenisPenarikan = 'PenarikanDanaPHK'
    elif q.GetFieldValue('PENARIKAN_PHK') == 'F':
      #jenis penarikan normal / sebagian / 30%
      jenisPenarikan = 'PenarikanDanaNormal'
    else:
      #tidak terdefinisi/ terdefinisi selain penarikan phk, 
      #dianggap sebagai penarikan sebagian
      jenisPenarikan = 'PenarikanDanaNormal'
    
    #create transaksi Pengalihan Ke DPLK Lain
    o = config.CreatePObject(jenisPenarikan)
    
    o.saldo_iuran_awal = q.GetFieldValue('SALDO_IURAN_DIBEBANI')  
    o.saldo_iuran_akhir = q.GetFieldValue('SISA_IURAN')
    o.jml_tarik = o.saldo_iuran_awal - o.saldo_iuran_akhir 
        
    o.biaya_tarik = abs(query.GetFieldValue('MUTASI_POTONGAN_PENGEMBANGAN') + \
      query.GetFieldValue('MUTASI_POTONGAN_IURAN') + \
      query.GetFieldValue('MUTASI_POTONGAN_PERALIHAN'))
      
    #buat objek biaya adm transaksi
    oBAdm = config.CreatePObject('BiayaAdmTransaksi')
    oBAdm.mutasi_pengembangan = -abs(query.GetFieldValue('MUTASI_POTONGAN_PENGEMBANGAN'))
    oBAdm.mutasi_iuran_pk = 0.0 
    oBAdm.mutasi_iuran_pst = -abs(query.GetFieldValue('MUTASI_POTONGAN_IURAN'))
    oBAdm.mutasi_peralihan = -abs(query.GetFieldValue('MUTASI_POTONGAN_PERALIHAN'))
    oBAdm.isPindahPaket = 'F'
    
    o.pajak = query.GetFieldValue('MUTASI_PAJAK')
    o.ID_Transaksi_BAdmTrans = oBAdm.ID_Transaksi
    
    #jenis biaya lain diasumsikan ialah Pindah Buku
    o.jenis_biaya = 'P'
    if q.GetFieldValue('MUTASI_BIAYA_LAIN') != None:
      o.biaya_lain = q.GetFieldValue('MUTASI_BIAYA_LAIN')
    else:
      o.biaya_lain = 0.0
    o.ktr_biaya_lain = q.GetFieldValue('KTR_BIAYA_LAIN')
    
    if q.GetFieldValue('DANA_DITERIMA') != None:
      o.dana_diterima = q.GetFieldValue('DANA_DITERIMA')
    else:
      o.dana_diterima = 0.0
      
    if q.GetFieldValue('COUNT_ADVIS') != None:
      o.count_advis = q.GetFieldValue('COUNT_ADVIS')
    
    #set untuk field parent (TransaksiDPLK) 
    o.mutasi_iuran_pk = 0.0
    o.mutasi_iuran_pst = query.GetFieldValue('MUTASI_DANA_IURAN')
    o.mutasi_pengembangan = query.GetFieldValue('MUTASI_PENGEMBANGAN')
    o.mutasi_peralihan = query.GetFieldValue('MUTASI_DANA_PERALIHAN')
    
    o.tgl_transaksi = o.tgl_otorisasi = o.tgl_sistem = \
      oBAdm.tgl_transaksi = oBAdm.tgl_otorisasi = oBAdm.tgl_sistem = dtTglTransaksi          
    o.no_peserta = oBAdm.no_peserta = query.GetFieldValue('NO_PESERTA')  
    o.keterangan = 'hasil import data lama ID transaksi: %d' \
      % (query.GetFieldValue('ID_TRANSAKSI'))
    oBAdm.keterangan = 'biaya transaksi untuk hasil import data lama ID transaksi: %d' \
      % (query.GetFieldValue('ID_TRANSAKSI'))
      
    o.isCommitted = oBAdm.isCommitted = 'T'
    if query.GetFieldValue('OPERATOR_ADDED') != None:
      o.user_id = o.user_id_auth = \
      oBAdm.user_id = oBAdm.user_id_auth = query.GetFieldValue('OPERATOR_ADDED')
  
    o.terminal_id = o.terminal_id_auth = \
     oBAdm.terminal_id = oBAdm.terminal_id_auth = v_IP_Server
    o.ID_TransactionBatch = oBAdm.ID_TransactionBatch = \
      oTransactionBatch.ID_TransactionBatch
    if query.GetFieldValue('KD_PAKET_INV') != None:
      o.kode_paket_investasi = oBAdm.kode_paket_investasi = \
        ConvertKodePaket(query.GetFieldValue('KD_PAKET_INV')) 
  
    #set branch code menjadi di 'Kantor Pusat' (301)
    o.branch_code = oBAdm.branch_code = '301'

  return 1

def PengambilanManfaat(config, con, oTransactionBatch, query, dtTglTransaksi):
  global v_IP_Server

  print '\n\nPENGAMBILAN_MANFAAT...'

  #ambil data lengkap PENGAMBILAN MANFAAT dari tabel untuk id transaksi tertentu
  q = con.GetQuery('select t.KODE_JNS_MANFAAT, t.STATUS_PEMOHON, \
                           t.PERSEN_BAYAR_SEKALIGUS, t.PRODUK_ANUITAS, t.ASURANSI, \
                           t.SALDO_IURAN_MANF, t.SALDO_PENGEMBANGAN, \
                           t.SALDO_JML_DANA, t.BAYAR_SEKALIGUS, t.BAYAR_ANUITAS, \
                           t.MANFAAT_STLH_PAJAK, t.MUTASI_BIAYA_LAIN, \
                           t.DANA_TUNAI_DITERIMA, t.KTR_BIAYA_LAIN, \
                           t.ID_TRANSAKSI1, t.ID_TRANSAKSI12, t.USER_NAME, \
                           t.COUNT_ADVIS, t.PENCAIRAN_DIPERCEPAT, t.SALDO_PERALIHAN \
                    from   PENGAMBILAN_MANFAAT t \
                    where  t.ID_TRANSAKSI = %d' \
                    % (query.GetFieldValue('ID_TRANSAKSI')))
  
  if not q.Eof():
    #create transaksi Pengalihan Ke DPLK Lain
    o = config.CreatePObject('PengambilanManfaat')
    
    #mapping jenis pengambilan manfaat
    dictJenisAmbilManfaat = {'A':'B','B':'D','C':'C','D':'J'}
    o.kode_jns_manfaat = dictJenisAmbilManfaat[q.GetFieldValue('KODE_JNS_MANFAAT')]
   
    o.saldo_iuran_pk = 0.0  
    o.saldo_iuran_pst = q.GetFieldValue('SALDO_IURAN_MANF')
    o.saldo_pengembangan = q.GetFieldValue('SALDO_PENGEMBANGAN')
    o.saldo_peralihan = q.GetFieldValue('SALDO_PERALIHAN')
    
    o.saldo_jml_dana = o.saldo_iuran_pk + o.saldo_iuran_pst + o.saldo_pengembangan + \
      o.saldo_peralihan
      
    #ambil informasi untuk biaya adm tahunan
    if q.GetFieldValue('ID_TRANSAKSI1') not in [None,'',0]:
      #mempunyai biaya administrasi tahunan
      qBAdm = con.GetQuery('select t.MUTASI_POTONGAN_PENGEMBANGAN \
                            from   TRANSAKSI_DPLK t \
                            where  t.ID_TRANSAKSI = %d' \
                            % (q.GetFieldValue('ID_TRANSAKSI1')))
      if not qBAdm.Eof(): 
        o.biaya_administrasi = qBAdm.GetFieldValue('MUTASI_POTONGAN_PENGEMBANGAN')
        
      #buat objek biaya adm tahunan
      oBAdm = config.CreatePObject('BiayaAdmTahunan')
      oBAdm.mutasi_pengembangan = -o.biaya_administrasi
      oBAdm.mutasi_iuran_pk = oBAdm.mutasi_iuran_pst = oBAdm.mutasi_peralihan = 0.0
    
      oBAdm.tgl_transaksi = oBAdm.tgl_otorisasi = oBAdm.tgl_sistem = dtTglTransaksi          
      oBAdm.no_peserta = query.GetFieldValue('NO_PESERTA')  
      oBAdm.keterangan = 'biaya adm tahunan untuk hasil import data lama ID transaksi: %d' \
        % (q.GetFieldValue('ID_TRANSAKSI1'))
        
      oBAdm.isCommitted = 'T'
      if query.GetFieldValue('OPERATOR_ADDED') != None:
        oBAdm.user_id = oBAdm.user_id_auth = query.GetFieldValue('OPERATOR_ADDED')
    
      oBAdm.terminal_id = oBAdm.terminal_id_auth = v_IP_Server
      oBAdm.ID_TransactionBatch = oTransactionBatch.ID_TransactionBatch
      if query.GetFieldValue('KD_PAKET_INV') != None:
        oBAdm.kode_paket_investasi = \
          ConvertKodePaket(query.GetFieldValue('KD_PAKET_INV')) 
    
      #set branch code menjadi di 'Kantor Pusat' (301)
      oBAdm.branch_code = '301'

      o.ID_Transaksi_BAdmThn = oBAdm.ID_Transaksi
  
    #ambil informasi untuk biaya pengelolaan
    if q.GetFieldValue('ID_TRANSAKSI12') not in [None,'',0]:
      #mempunyai biaya pengelolaan
      qBPeng = con.GetQuery('select t.MUTASI_POTONGAN_PENGEMBANGAN \
                            from   TRANSAKSI_DPLK t \
                            where  t.ID_TRANSAKSI = %d' \
                            % (q.GetFieldValue('ID_TRANSAKSI12')))
      if not qBPeng.Eof(): 
        o.biaya_pengelolaan = qBPeng.GetFieldValue('MUTASI_POTONGAN_PENGEMBANGAN')
        
      #buat objek biaya pengelolaan
      oBPeng = config.CreatePObject('BiayaPengelolaanDana')
      oBPeng.mutasi_pengembangan = -o.biaya_pengelolaan
      oBPeng.mutasi_iuran_pk = oBPeng.mutasi_iuran_pst = oBPeng.mutasi_peralihan = 0.0
      
      oBPeng.tgl_transaksi = oBPeng.tgl_otorisasi = oBPeng.tgl_sistem = dtTglTransaksi          
      oBPeng.no_peserta = query.GetFieldValue('NO_PESERTA')  
      oBPeng.keterangan = 'biaya pengelolaan untuk hasil import data lama ID transaksi: %d' \
        % (q.GetFieldValue('ID_TRANSAKSI12'))
        
      oBPeng.isCommitted = 'T'
      if query.GetFieldValue('OPERATOR_ADDED') != None:
        oBPeng.user_id = oBPeng.user_id_auth = query.GetFieldValue('OPERATOR_ADDED')
    
      oBPeng.terminal_id = oBPeng.terminal_id_auth = v_IP_Server
      oBPeng.ID_TransactionBatch = oTransactionBatch.ID_TransactionBatch
      if query.GetFieldValue('KD_PAKET_INV') != None:
        oBPeng.kode_paket_investasi = \
          ConvertKodePaket(query.GetFieldValue('KD_PAKET_INV')) 
    
      #set branch code menjadi di 'Kantor Pusat' (301)
      oBPeng.branch_code = '301'

      o.ID_Transaksi_BPeng = oBPeng.ID_Transaksi
  
    #biaya pencairan diasumsikan 0 (tidak ada informasi ini pada data lama)
    o.biaya_pencairan = 0.0
    o.ID_Transaksi_BAdmTrans = None
    
    o.saldo_manfaat = o.saldo_jml_dana - o.biaya_administrasi - \
      o.biaya_pengelolaan - o.biaya_pencairan     
    o.pajak = query.GetFieldValue('MUTASI_PAJAK')
    o.manfaat_stlh_pajak = q.GetFieldValue('MANFAAT_STLH_PAJAK')
    o.manfaat_tunai = q.GetFieldValue('BAYAR_SEKALIGUS')
    o.manfaat_anuitas = q.GetFieldValue('BAYAR_ANUITAS')
    o.manfaat_tunai_diterima = q.GetFieldValue('DANA_TUNAI_DITERIMA')
    
    #jenis biaya lain diasumsikan ialah Pindah Buku
    o.jenis_biaya = 'P'
    if q.GetFieldValue('MUTASI_BIAYA_LAIN') != None:
      o.biaya_lain = q.GetFieldValue('MUTASI_BIAYA_LAIN')
    else:
      o.biaya_lain = 0.0
    
    o.ahliwaris_id = q.GetFieldValue('STATUS_PEMOHON')
    
    if q.GetFieldValue('COUNT_ADVIS') != None:
      o.count_advis = q.GetFieldValue('COUNT_ADVIS')
    
    if q.GetFieldValue('ASURANSI') not in [None,''] and \
      q.GetFieldValue('PRODUK_ANUITAS') not in [None,'']:
      o.nama_anuitas = q.GetFieldValue('ASURANSI') + ' - ' + \
        q.GetFieldValue('PRODUK_ANUITAS')
  
    #set untuk field parent (TransaksiDPLK) 
    o.mutasi_iuran_pk = 0.0
    o.mutasi_iuran_pst = query.GetFieldValue('MUTASI_DANA_IURAN')
    o.mutasi_pengembangan = query.GetFieldValue('MUTASI_PENGEMBANGAN')
    o.mutasi_peralihan = query.GetFieldValue('MUTASI_DANA_PERALIHAN')
    
    o.tgl_transaksi = o.tgl_otorisasi = o.tgl_sistem = dtTglTransaksi          
    o.no_peserta = query.GetFieldValue('NO_PESERTA')  
    o.keterangan = 'hasil import data lama ID transaksi: %d' \
      % (query.GetFieldValue('ID_TRANSAKSI'))
      
    o.isCommitted = 'T'
    if query.GetFieldValue('OPERATOR_ADDED') != None:
      o.user_id = o.user_id_auth = query.GetFieldValue('OPERATOR_ADDED')
  
    o.terminal_id = o.terminal_id_auth = v_IP_Server
    o.ID_TransactionBatch = oTransactionBatch.ID_TransactionBatch
    if query.GetFieldValue('KD_PAKET_INV') != None:
      o.kode_paket_investasi = ConvertKodePaket(query.GetFieldValue('KD_PAKET_INV')) 
  
    #set branch code menjadi di 'Kantor Pusat' (301)
    o.branch_code = '301'
  
  return 1

def BiayaPengelolaanDana(config, con, oTransactionBatch, query, dtTglTransaksi):
  global v_IP_Server

  print '\n\nBIAYA_PENGELOLAAN_DANA...'
  
  #cek apakah id transaksi tercatat dalam biaya pengelolaan pengalihan ke dplk lain 
  #atau pengambilan manfaat (kode field table ID_Transaksi12)
  #ambil informasi biaya pengelolaan dana yang ada di field (trik pengganti UNION):
  # 1) ID_Transaksi tabel Pengalihan_Ke_DPLK_Lain
  # 2) ID_Transaksi tabel Pengambilan_Manfaat
  tupleSQL = ['select p1.ID_TRANSAKSI from PENGALIHAN_KE_DPLK_LAIN p1 \
                where  p1.ID_TRANSAKSI12 = %d' % (query.GetFieldValue('ID_TRANSAKSI')), 
              'select p2.ID_TRANSAKSI from PENGAMBILAN_MANFAAT p2 \
                where  p2.ID_TRANSAKSI12 = %d' % (query.GetFieldValue('ID_TRANSAKSI'))]
  flagBPengExist = 0
  for sSQL in tupleSQL:
    qCek = con.GetQuery(sSQL)
    if not qCek.Eof():
      #berarti biaya pengelolaan sudah ada di basisdata
      flagBPengExist = 1

  #qCek = con.GetQuery('select p1.ID_TRANSAKSI \
  #                     from   PENGALIHAN_KE_DPLK_LAIN p1 \
  #                     where  p1.ID_TRANSAKSI12 = %d \
  #                     union \
  #                     select p2.ID_TRANSAKSI \
  #                     from   PENGAMBILAN_MANFAAT p2 \
  #                     where  p2.ID_TRANSAKSI12 = %d' \
  #                     % (query.GetFieldValue('ID_TRANSAKSI'),\
  #                        query.GetFieldValue('ID_TRANSAKSI')))
  #if qCek.Eof():
  
  if not flagBPengExist:
    #biaya pengelolaan belum di-create dalam basisdata 
    o = config.CreatePObject('BiayaPengelolaanDana')
    
    #ambil data lengkap BIAYA PENGELOLAAN DANA dari tabel untuk id transaksi tertentu
    q = con.GetQuery('select t.SALDO_YANG_DIBEBANI \
                      from   BIAYA_PENGELOLAAN_DANA t \
                      where  t.ID_TRANSAKSI = %d' \
                      % (query.GetFieldValue('ID_TRANSAKSI')))
  
    if not q.Eof():
      if q.GetFieldValue('SALDO_YANG_DIBEBANI') != None:
        o.saldo_yang_dibebani = q.GetFieldValue('SALDO_YANG_DIBEBANI')
      else:
        o.saldo_yang_dibebani = 0.0
  
    #set untuk field parent (TransaksiDPLK) 
    o.mutasi_iuran_pk = 0.0
    o.mutasi_iuran_pst = -abs(query.GetFieldValue('MUTASI_POTONGAN_IURAN'))
    o.mutasi_pengembangan = -abs(query.GetFieldValue('MUTASI_POTONGAN_PENGEMBANGAN'))
    o.mutasi_peralihan = -abs(query.GetFieldValue('MUTASI_POTONGAN_PERALIHAN'))
    
    o.tgl_transaksi = o.tgl_otorisasi = o.tgl_sistem = dtTglTransaksi          
    o.no_peserta = query.GetFieldValue('NO_PESERTA')  
    o.keterangan = 'hasil import data lama ID transaksi: %d' \
      % (query.GetFieldValue('ID_TRANSAKSI'))
      
    o.isCommitted = 'T'
    if query.GetFieldValue('OPERATOR_ADDED') != None:
      o.user_id = o.user_id_auth = query.GetFieldValue('OPERATOR_ADDED')
  
    o.terminal_id = o.terminal_id_auth = v_IP_Server
    o.ID_TransactionBatch = oTransactionBatch.ID_TransactionBatch
    if query.GetFieldValue('KD_PAKET_INV') != None:
      o.kode_paket_investasi = ConvertKodePaket(query.GetFieldValue('KD_PAKET_INV')) 
  
    #set branch code menjadi di 'Kantor Pusat' (301)
    o.branch_code = '301'  
  
  return 1

def BiayaAdmTahunan(config, con, oTransactionBatch, query, dtTglTransaksi):
  global v_IP_Server

  print '\n\nBIAYA_ADM_TAHUNAN...'
  
  #cek apakah id transaksi tercatat dalam biaya administrasi pengalihan ke dplk lain 
  #atau pengambilan manfaat (kode field table ID_Transaksi1)
  #ambil informasi biaya pengelolaan dana yang ada di field (trik pengganti UNION):
  # 1) ID_Transaksi tabel Pengalihan_Ke_DPLK_Lain
  # 2) ID_Transaksi tabel Pengambilan_Manfaat
  tupleSQL = ['select p1.ID_TRANSAKSI from PENGALIHAN_KE_DPLK_LAIN p1 \
                where  p1.ID_TRANSAKSI1 = %d' % (query.GetFieldValue('ID_TRANSAKSI')), 
              'select p2.ID_TRANSAKSI from PENGAMBILAN_MANFAAT p2 \
                where  p2.ID_TRANSAKSI1 = %d' % (query.GetFieldValue('ID_TRANSAKSI'))]
  flagBAdmExist = 0
  for sSQL in tupleSQL:
    qCek = con.GetQuery(sSQL)
    if not qCek.Eof():
      #berarti biaya pengelolaan sudah ada di basisdata
      flagBAdmExist = 1

  #qCek = con.GetQuery('select p1.ID_TRANSAKSI \
  #                     from   PENGALIHAN_KE_DPLK_LAIN p1 \
  #                     where  p1.ID_TRANSAKSI1 = %d \
  #                     union \
  #                     select p2.ID_TRANSAKSI \
  #                     from   PENGAMBILAN_MANFAAT p2 \
  #                     where  p2.ID_TRANSAKSI1 = %d' \
  #                     % (query.GetFieldValue('ID_TRANSAKSI'),\
  #                        query.GetFieldValue('ID_TRANSAKSI')))
  #if qCek.Eof():
  
  if not flagBAdmExist:
    #biaya administrasi belum di-create dalam basisdata 
    o = config.CreatePObject('BiayaAdmTahunan')
      
    #set untuk field parent (TransaksiDPLK) 
    o.mutasi_iuran_pk = 0.0
    o.mutasi_iuran_pst = -abs(query.GetFieldValue('MUTASI_POTONGAN_IURAN'))
    o.mutasi_pengembangan = -abs(query.GetFieldValue('MUTASI_POTONGAN_PENGEMBANGAN'))
    o.mutasi_peralihan = -abs(query.GetFieldValue('MUTASI_POTONGAN_PERALIHAN'))
    
    o.tgl_transaksi = o.tgl_otorisasi = o.tgl_sistem = dtTglTransaksi          
    o.no_peserta = query.GetFieldValue('NO_PESERTA')  
    o.keterangan = 'hasil import data lama ID transaksi: %d' \
      % (query.GetFieldValue('ID_TRANSAKSI'))
      
    o.isCommitted = 'T'
    if query.GetFieldValue('OPERATOR_ADDED') != None:
      o.user_id = o.user_id_auth = query.GetFieldValue('OPERATOR_ADDED')
  
    o.terminal_id = o.terminal_id_auth = v_IP_Server
    o.ID_TransactionBatch = oTransactionBatch.ID_TransactionBatch
    if query.GetFieldValue('KD_PAKET_INV') != None:
      o.kode_paket_investasi = ConvertKodePaket(query.GetFieldValue('KD_PAKET_INV')) 
  
    #set branch code menjadi di 'Kantor Pusat' (301)
    o.branch_code = '301'  

  return 1

def TransaksiBagiHasil(config, con, oTransactionBatch, query, dtTglTransaksi):
  global v_IP_Server

  print '\n\nTransaksi BAGI_HASIL...'
  
  #cari BagiHasil untuk tanggal yang terdapat dalam transaksi DPLK
  #lalu create transaksi BagiHasil untuk tanggal tersebut
  y,m,d = config.ModLibUtils.DecodeDate(dtTglTransaksi)
  qCek = con.GetQuery('select IDBGHASIL \
                       from BAGI_HASIL \
                       where TGL_BAGI_HASIL = \'%d-%d-%d\'' \
                       % (y,m,d))
  if not qCek.Eof():
    #ketemu ID bagi hasil yang terkait dengan transaksi bagi hasil
    idbagihasil = qCek.GetFieldValue('IDBGHASIL')
  else:
    #tidak ketemu ID Bagi Hasil yang terkait dengan Transaksi Bagi Hasil
    idbagihasil = None

    #persiapkan file ImportTransaksiBagiHasil.log
    logFile = CreateFileLog(config, 'TransaksiBagiHasil', 'ImportTransaksiBagiHasil.log')
    
    #log ke file ImportTransaksiBagiHasil.log
    logFile.write('ID Transaksi Bagi Hasil %d, tanggal transaksi %d-%d-%d tidak memiliki kesamaan tanggal apapun dengan data Bagi Hasil (tabel BAGI_HASIL)' \
      % (query.GetFieldValue('ID_TRANSAKSI'),y,m,d)+'\n')
  
    #close file ImportTransaksiDPLK.log
    logFile.close()

  #create transaksi bagi hasil 
  o = config.CreatePObject('TransaksiBagiHasil')
  o.idbghasil = idbagihasil
    
  #set untuk field parent (TransaksiDPLK) 
  o.mutasi_iuran_pk = o.mutasi_iuran_pst = o.mutasi_peralihan = 0.0     
  o.mutasi_pengembangan = query.GetFieldValue('MUTASI_BAGI_HASIL')
  
  o.tgl_transaksi = o.tgl_otorisasi = o.tgl_sistem = dtTglTransaksi          
  o.no_peserta = query.GetFieldValue('NO_PESERTA')  
  o.keterangan = 'hasil import data lama ID transaksi: %d' \
    % (query.GetFieldValue('ID_TRANSAKSI'))
    
  o.isCommitted = 'T'
  if query.GetFieldValue('OPERATOR_ADDED') != None:
    o.user_id = o.user_id_auth = query.GetFieldValue('OPERATOR_ADDED')

  o.terminal_id = o.terminal_id_auth = v_IP_Server
  o.ID_TransactionBatch = oTransactionBatch.ID_TransactionBatch
  if query.GetFieldValue('KD_PAKET_INV') != None:
    o.kode_paket_investasi = ConvertKodePaket(query.GetFieldValue('KD_PAKET_INV')) 

  #set branch code menjadi di 'Kantor Pusat' (301)
  o.branch_code = '301'  
  
  return 1
  
def PindahPaketInvestasi(config, con, oTransactionBatch, query, dtTglTransaksi):
  global v_IP_Server

  print '\n\nPindahPaketInvestasi...'
  
  #ambil info histori pindah paket sesuai dengan ID_Transaksi
  q = con.GetQuery('select JUMLAH_DIPINDAHKAN, KODE_PAKET_INVESTASI2, \
                          CATATAN_UBAH_INVESTASI, KODE_PAKET_INVESTASI, \
                          SALDO_IURAN, SALDO_PENGEMBANGAN, SALDO_PERALIHAN, \
                          USER_NAME, COUNT_ADVIS \
                   from UBAH_JENIS_INVESTASI \
                   where ID_TRANSAKSI = %d' \
                   % (query.GetFieldValue('ID_TRANSAKSI')))
  if not q.Eof():  
    # 1) BUAT BIAYA TRANSAKSI UNTUK PINDAH PAKET
    o = config.CreatePObject('BiayaAdmTransaksi')
    o.isPindahPaket = 'T'
    if query.GetFieldValue('KD_PAKET_INV') != None:
      o.kode_paket_investasi = ConvertKodePaket(query.GetFieldValue('KD_PAKET_INV')) 
    o.keterangan = 'hasil import data lama ID transaksi: %d' \
      % (query.GetFieldValue('ID_TRANSAKSI'))
      
    #set untuk field parent (TransaksiDPLK) 
    o.mutasi_iuran_pk = 0.0
    
    if query.GetFieldValue('MUTASI_POTONGAN_IURAN') > 0.0:
      o.mutasi_iuran_pst = -abs(query.GetFieldValue('MUTASI_POTONGAN_IURAN'))
    else:
      o.mutasi_iuran_pst = 0.0
    
    if query.GetFieldValue('MUTASI_POTONGAN_PENGEMBANGAN') > 0.0:
      o.mutasi_pengembangan = -abs(query.GetFieldValue('MUTASI_POTONGAN_PENGEMBANGAN'))
    else:
      o.mutasi_pengembangan = 0.0
    
    if query.GetFieldValue('MUTASI_POTONGAN_PERALIHAN') > 0.0:
      o.mutasi_peralihan = -abs(query.GetFieldValue('MUTASI_POTONGAN_PERALIHAN'))
    else:
      o.mutasi_peralihan = 0.0
                            
    # 2) BUAT TRANSAKSI DPLK UNTUK ME-NOL-KAN TRANSAKSI PAKET LAMA
    oL = config.CreatePObject('TransaksiDPLK')
    oL.kode_jenis_transaksi = 'F'
    oL.kode_paket_investasi = ConvertKodePaket(q.GetFieldValue('KODE_PAKET_INVESTASI'))
    oL.keterangan = 'hasil konversi data lama ID transaksi: %d' \
      % (query.GetFieldValue('ID_TRANSAKSI'))
    
    oL.mutasi_iuran_pk = 0.0
    oL.mutasi_iuran_pst = -abs(q.GetFieldValue('SALDO_IURAN'))
    oL.mutasi_pengembangan = -abs(q.GetFieldValue('SALDO_PENGEMBANGAN'))
    oL.mutasi_peralihan = -abs(q.GetFieldValue('SALDO_PERALIHAN'))

    # 3) BUAT TRANSAKSI DPLK UNTUK MEMBUAT BARU TRANSAKSI PAKET BARU
    oN = config.CreatePObject('TransaksiDPLK')
    oN.kode_jenis_transaksi = 'F'
    oN.kode_paket_investasi = ConvertKodePaket(q.GetFieldValue('KODE_PAKET_INVESTASI2'))
    oN.keterangan = 'hasil koversi data lama ID transaksi: %d' \
      % (query.GetFieldValue('ID_TRANSAKSI'))

    oN.mutasi_iuran_pk = 0.0
    oN.mutasi_iuran_pst = abs(oL.mutasi_iuran_pst) + o.mutasi_iuran_pst 
    oN.mutasi_pengembangan = abs(oL.mutasi_pengembangan) + o.mutasi_pengembangan 
    oN.mutasi_peralihan = abs(oL.mutasi_peralihan) + o.mutasi_peralihan

    # 4) BUAT HISTORI PINDAH PAKET
    oH = config.CreatePObject('HistoriPindahPaketInvestasi')
    oH.kode_paket_investasi = oL.kode_paket_investasi    
    oH.no_referensi = 'DataLama'    

    if query.GetFieldValue('OPERATOR_ADDED') != None:
      o.user_id = o.user_id_auth = \
        oL.user_id = oL.user_id_auth = \
        oN.user_id = oN.user_id_auth = \
        oH.user_id = oH.auth_user_id = query.GetFieldValue('OPERATOR_ADDED')
    o.tgl_transaksi = o.tgl_otorisasi = o.tgl_sistem = \
      oL.tgl_transaksi = oL.tgl_otorisasi = oL.tgl_sistem = \
      oN.tgl_transaksi = oN.tgl_otorisasi = oN.tgl_sistem = \
      oH.tanggal_histori = dtTglTransaksi          
    o.no_peserta = oL.no_peserta = oN.no_peserta = \
      oH.no_peserta = query.GetFieldValue('NO_PESERTA')  
    o.terminal_id = o.terminal_id_auth = \
      oL.terminal_id = oL.terminal_id_auth = \
      oN.terminal_id = oN.terminal_id_auth = \
      oH.terminal_id = v_IP_Server
    o.ID_TransactionBatch = oL.ID_TransactionBatch = oN.ID_TransactionBatch = \
      oTransactionBatch.ID_TransactionBatch
    o.isCommitted = oL.isCommitted = oN.isCommitted = 'T'
    o.branch_code = oL.branch_code = oN.branch_code = '301'  

  return 1

def HistoriPindahPaketInvestasi(config, con):
  #not yet used
  print '\n\nUBAH_JENIS_INVESTASI...'

  return 1

#-------------------------------------------------------------------------------
## STEP 5 CODE: Investasi-related table
#-------------------------------------------------------------------------------
def ProcessingDummy(config, con):
  pass

  return 1

#-------------------------------------------------------------------------------
## STEP 6 CODE: dropping ifx-kind table
#-------------------------------------------------------------------------------
def DroppingIfxKindTable(config, con):
  print '\n\nIfx-kind table...'
  rSQL = config.CreateSQL('select s.name from sysobjects s \
    where s.type = \'U\' and s.name like \'ifx_%\'').RawResult
    
  rSQL.First()
  while not rSQL.Eof:
    print '  Dropping %s table...' % (rSQL.name)
    res = config.ExecSQL('Drop Table %s' % (rSQL.name))
    rSQL.Next()

  return 1

# MAIN MODULE CALLER -----------------------------------------------------------

config = DBAppFramework.GetConfig()

#setting old DPLK DB connection 
con = dafdb.getDBConnection('c:/dafapp/dplk/default.cfg','PRIMARY_DATABASE')
con.Connect()

try:
  print 'Mulai proses impor: '+ time.asctime()  
  ###config.BeginTransaction()
  try:
    ## STEP 0 ##
    #handling Independen Table  
    print 'STEP 0: Creating BranchLocation and User Teller first...'
  
    #ifx_KodeCabang
    ###BranchLocation(config, con)
  
    #tabel Counter (untuk registrasi peserta)
    ###Counter(config, con)
    
    #kosongkan dulu UserGroupApp
    ###EmptyingTable(config, con, 'UserGroupApp')
    
    #ifx_DaftarTeller
    ###UserAppTeller(config, con)
    
    #flushing to database
    ###config.FlushUpdates()
    ###config.Commit()
  except:
    ###config.Rollback()
    raise

  ###config.BeginTransaction()
  try:
    ## STEP 1 ##
    #handling Independen Table  
    print '\n\nSTEP 1: Processing Independen Table...'
      
    #User_DPLK: tambahan selain user Teller yag ada di STEP 0
    ###UserApp(config, con)
  
    ###DaerahAsal(config, con)
    ###JenisUsaha(config, con)
    ###JenisPortofolio(config, con)
    ###PaketInvestasi(config, con)
    ###Kepemilikan(config, con)
    ###PihakKetiga(config, con)
    ###SumberDana(config, con)
    ###KelompokNasabah(config, con)
    ###LembagaDanaPensiun(config, con)
    
    #flushing to database
    ###config.FlushUpdates()
    ###config.Commit()
  except:
    ###config.Rollback()
    raise

  ###config.BeginTransaction()
  try:
    ## STEP 2 ##
    print '\n\nSTEP 2: Processing Main Reference Table...'
  
    ###NasabahDPLK(config, con)
    ###RekeningDPLK(config, con)
  
    #flushing to database (sudah dilakukan di dalam NasabahDPLK dan RekeningDPLK)
    #config.FlushUpdates()
    ###config.Commit()
  except:
    ###config.Rollback()
    raise

  ###config.BeginTransaction()
  try:
    ## STEP 3 ##
    print '\n\nSTEP 3: Processing Nasabah-related Table...'
  
    ###UbahAlamat(config, con)
    ###HistoriIuran(config, con)
    ###AhliWaris(config, con)
  
    #flushing to database
    ###config.FlushUpdates()
    ###config.Commit()
  except:
    ###config.Rollback()
    raise

  config.BeginTransaction()
  try:
    ## STEP 4a ##
    print '\n\nSTEP 4a: processing Transaksi-related Table...'
      
    BagiHasil(config, con)
    Pendaftaran(config, con)
    TransaksiPremi(config, con)
    
    #flushing to database
    config.FlushUpdates()
    config.Commit()
  except:
    config.Rollback()
    raise

  try:
    ## STEP 4b ##
    print '\n\nSTEP 4b: processing Transaksi-related Table...'
      
    #hanya diproses untuk TransaksiDPLK yang bukan 'deleted'
    TransaksiDPLK(config, con)
  
    #SEMUA MIGRASI SPESIFIK TRANSAKSI DPLK ADA DI DALAM FUNGSI TRANSAKSIDPLK()
    #DAN DIPILIH YANG BUKAN TRANSAKSI DPLK DELETED
    #BeginTransaction(), Commit(), RollBack() ada di dalam fungsi ini
    
    #PengalihanDariDPLKLain(config, con)
    #IuranPeserta(config, con)
    #PengalihanKeDPLKLain(config, con)
    #PenarikanDana(config, con)
    #PengambilanManfaat(config, con)
    #BiayaPengelolaanDana(config, con)
    #BiayaAdmTahunan(config, con)
    #TransaksiBagiHasil(config, con)
    #PindahPaketInvestasi(config, con)
  
    #Ubah_Jenis_Investasi 
    #HistoriPindahPaketInvestasi(config, con)  
  except:
    raise

  ## STEP 5 ##
  print '\n\nSTEP 5: processing Investasi-related Table...(SKIPPED)'

  #config.BeginTransaction()
  try:
    ## STEP 6 ##
    print '\n\nSTEP 6: dropping ifx-kind table...'
    
    #dropping all ifx-kind table
    #DroppingIfxKindTable(config, con)

    #flushing to database
    #config.FlushUpdates()
    #config.Commit()
  except:
    #config.Rollback()
    raise

  print '\n\nINFORMASI PENTING TERAKHIR!'\
        '\n 1) Cek parameter BATAS_TGL_TUTUP_BATCH, sesuaikan dengan Tanggal '\
        '      Terakhir Bagi Hasil'\
        '\n 2) Tanggal Akseptasi untuk peserta yang ikut wasiat ummat TIDAK '\
        '      BISA DIDEFINISIKAN, sebab info ini tidak ada pada data lama'\
        '\n 3) Cek file .log yang ada di direktori c:\dafapp\dplk07'
  
  print 'Sukses mentransfer data basisdata DPLK lama ke basisdata DPLK baru!!!'
  print 'Selesai proses impor: '+ time.asctime()
    
  con.Disconnect()
except:
  raise
