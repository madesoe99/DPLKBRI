import sys, string
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi, transaksiapi

def tabelpremi(config, usia_masuk, usia_pensiun):

  x = 45
  z = 0

  while x <= 65:
    if usia_pensiun == x:
       b = z
    z += 1
    x += 1

  #b = b - 45
  if usia_masuk == 18:
     rate=[1.35,1.35,1.35,1.40,1.40,1.45,1.45,1.50,1.50,1.55,1.65,1.70,1.75,1.80,1.85,1.90,2.05,2.10,2.20,2.25,2.35]
     ratepremi = rate[b]
  if usia_masuk == 19:
     rate=[1.35,1.35,1.35,1.40,1.40,1.45,1.45,1.50,1.50,1.55,1.65,1.70,1.75,1.80,1.85,1.90,2.05,2.10,2.20,2.25,2.35]
     ratepremi = rate[b]
  if usia_masuk == 20:
     rate=[1.35,1.35,1.35,1.40,1.40,1.45,1.45,1.50,1.55,1.55,1.65,1.70,1.75,1.80,1.90,1.95,2.05,2.15,2.20,2.30,2.45]
     ratepremi = rate[b]
  if usia_masuk == 21:
     rate=[1.35,1.35,1.40,1.40,1.40,1.45,1.45,1.50,1.55,1.65,1.70,1.75,1.80,1.85,1.90,1.95,2.10,2.20,2.25,2.35,2.50]
     ratepremi = rate[b]
  if usia_masuk == 22:
     rate=[1.35,1.35,1.40,1.40,1.40,1.45,1.50,1.50,1.55,1.65,1.70,1.75,1.80,1.85,1.95,2.05,2.15,2.20,2.30,2.45,2.55]
     ratepremi = rate[b]
  if usia_masuk == 23:
     rate=[1.35,1.35,1.40,1.40,1.45,1.45,1.50,1.55,1.55,1.65,1.70,1.75,1.85,1.90,1.95,2.10,2.15,2.25,2.35,2.50,2.60]
     ratepremi = rate[b]
  if usia_masuk == 24:
     rate=[1.35,1.35,1.40,1.40,1.45,1.45,1.50,1.55,1.65,1.70,1.75,1.80,1.85,1.90,2.05,2.15,2.20,2.30,2.45,2.55,2.65]
     ratepremi = rate[b]
  if usia_masuk == 25:
     rate=[1.35,1.35,1.40,1.40,1.45,1.45,1.50,1.55,1.65,1.70,1.75,1.80,1.90,1.95,2.10,2.15,2.25,2.35,2.50,2.60,2.70]
     ratepremi = rate[b]
  if usia_masuk == 26:
     rate=[1.35,1.35,1.40,1.40,1.45,1.50,1.50,1.55,1.65,1.70,1.80,1.85,1.90,2.05,2.10,2.20,2.30,2.45,2.55,2.65,2.75]
     ratepremi = rate[b]
  if usia_masuk == 27:
     rate=[1.35,1.35,1.40,1.40,1.45,1.50,1.55,1.65,1.70,1.75,1.80,1.90,1.95,2.10,2.15,2.25,2.35,2.50,2.60,2.70,2.90]
     ratepremi = rate[b]
  if usia_masuk == 28:
     rate=[1.35,1.35,1.40,1.40,1.45,1.50,1.55,1.65,1.70,1.80,1.85,1.90,2.05,2.15,2.20,2.30,2.45,2.55,2.70,2.85,2.95]
     ratepremi = rate[b]
  if usia_masuk == 29:
     rate=[1.35,1.40,1.40,1.45,1.50,1.55,1.65,1.70,1.75,1.85,1.90,1.95,2.10,2.20,2.30,2.45,2.55,2.65,2.75,2.95,3.05]
     ratepremi = rate[b]
  if usia_masuk == 30:
     rate=[1.40,1.40,1.45,1.50,1.55,1.65,1.70,1.75,1.80,1.90,1.95,2.10,2.15,2.25,2.35,2.50,2.60,2.75,2.90,3.05,3.15]
     ratepremi = rate[b]
  if usia_masuk == 31:
     rate=[1.45,1.45,1.50,1.55,1.65,1.70,1.75,1.80,1.90,1.95,2.10,2.15,2.25,2.35,2.50,2.60,2.70,2.90,3.00,3.15,3.35]
     ratepremi = rate[b]
  if usia_masuk == 32:
     rate=[1.50,1.50,1.55,1.65,1.70,1.75,1.80,1.90,1.95,2.10,2.15,2.25,2.35,2.50,2.60,2.70,2.85,3.00,3.15,3.30,3.45]
     ratepremi = rate[b]
  if usia_masuk == 33:
     rate=[1.55,1.55,1.65,1.70,1.75,1.85,1.90,1.95,2.10,2.15,2.25,2.35,2.50,2.60,2.70,2.85,3.00,3.10,3.30,3.45,3.65]
     ratepremi = rate[b]
  if usia_masuk == 34:
     rate=[1.65,1.70,1.75,1.80,1.85,1.90,1.95,2.10,2.15,2.25,2.35,2.50,2.60,2.70,2.85,3.00,3.10,3.30,3.45,3.65,3.80]
     ratepremi = rate[b]
  if usia_masuk == 35:
     rate=[1.75,1.75,1.80,1.90,1.95,2.05,2.10,2.20,2.25,2.35,2.50,2.60,2.70,2.85,3.00,3.10,3.30,3.45,3.65,3.80,3.95]
     ratepremi = rate[b]
  if usia_masuk == 36:
     rate=[1.85,1.90,1.95,2.05,2.10,2.15,2.20,2.30,2.45,2.50,2.60,2.70,2.90,3.00,3.10,3.30,3.45,3.65,3.80,3.95,4.20]
     ratepremi = rate[b]
  if usia_masuk == 37:
     rate=[1.95,2.05,2.10,2.15,2.20,2.30,2.35,2.45,2.55,2.65,2.75,2.90,3.05,3.15,3.35,3.45,3.65,3.80,4.05,4.20,4.45]
     ratepremi = rate[b]
  if usia_masuk == 38:
     rate=[2.15,2.20,2.25,2.30,2.20,2.45,2.55,2.60,2.70,2.85,2.95,3.05,3.25,3.35,3.50,3.70,3.85,4.05,4.20,4.45,4.65]
     ratepremi = rate[b]
  if usia_masuk == 39:
     rate=[2.35,2.35,2.45,2.50,2.35,2.60,2.70,2.75,2.90,3.00,3.10,3.30,3.40,3.55,3.75,3.90,4.10,4.25,4.50,4.65,4.90]
     ratepremi = rate[b]
  if usia_masuk == 40:
     rate=[2.60,2.60,2.60,2.65,2.55,2.90,2.90,3.00,3.05,3.15,3.35,3.45,3.65,3.75,3.90,4.15,4.30,4.50,4.70,4.95,5.15]
     ratepremi = rate[b]
  if usia_masuk == 41:
     rate=[0.00,2.85,2.85,2.90,2.70,3.00,3.05,3.15,3.30,3.40,3.50,3.70,3.80,3.95,4.15,4.35,4.55,4.75,5.00,5.25,5.45]
     ratepremi = rate[b]
  if usia_masuk == 42:
     rate=[0.00,0.00,3.10,3.10,2.95,3.15,3.30,3.35,3.45,3.65,3.75,3.90,4.05,4.25,4.45,4.60,4.85,5.00,5.25,5.50,5.75]
     ratepremi = rate[b]
  if usia_masuk == 43:
     rate=[0.00,0.00,0.00,3.35,3.10,3.40,3.59,3.55,3.70,3.85,3.95,4.15,4.30,4.50,4.65,4.90,5.10,5.35,5.55,5.80,6.10]
     ratepremi = rate[b]
  if usia_masuk == 44:
     rate=[0.00,0.00,0.00,0.00,3.40,3.70,3.75,3.85,3.95,4.10,4.25,4.35,4.60,4.75,4.95,5.15,5.40,5.65,5.85,6.15,6.45]
     ratepremi = rate[b]
  if usia_masuk == 45:
     rate=[0.00,0.00,0.00,0.00,3.65,3.95,4.05,4.15,4.25,4.35,4.55,4.70,4.90,5.05,5.30,5.50,5.75,5.95,6.25,6.50,6.75]
     ratepremi = rate[b]
  if usia_masuk == 46:
     rate=[0.00,0.00,0.00,0.00,0.00,0.00,4.45,4.50,4.55,4.70,4.90,5.05,5.25,5.40,5.65,5.85,6.10,6.35,6.65,6.95,7.25]
     ratepremi = rate[b]
  if usia_masuk == 47:
     rate=[0.00,0.00,0.00,0.00,0.00,0.00,0.00,4.90,4.95,5.10,5.25,5.40,5.65,5.80,6.05,6.25,6.55,6.75,7.05,7.35,7.70]
     ratepremi = rate[b]
  if usia_masuk == 48:
     rate=[0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,5.45,5.55,5.70,5.85,6.05,6.25,6.50,6.70,7.00,7.30,7.55,7.85,8.15]
     ratepremi = rate[b]
  if usia_masuk == 49:
     rate=[0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,6.15,6.25,6.35,6.55,6.75,7.00,7.25,7.50,7.80,8.10,8.35,8.70]
     ratepremi = rate[b]
  if usia_masuk == 50:
     rate=[0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,6.95,7.00,7.15,7.35,7.55,7.80,8.10,8.35,8.65,8.95,9.30]
     ratepremi = rate[b]
  if usia_masuk == 51:
     rate=[0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,7.75,7.85,8.05,8.20,8.45,8.65,8.95,9.30,9.55,9.90]
     ratepremi = rate[b]
  if usia_masuk == 52:
     rate=[0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,8.65,8.70,8.90,9.10,9.35,9.65,9.90,10.25,10.60]
     ratepremi = rate[b]
  if usia_masuk == 53:
     rate=[0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,9.55,9.70,9.85,10.10,10.30,10.60,10.95,11.30]
     ratepremi = rate[b]
  if usia_masuk == 54:
     rate=[0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,10.60,10.65,10.85,11.10,11.40,11.70,12.05]
     ratepremi = rate[b]
  if usia_masuk == 55:
     rate=[0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,11.70,11.75,11.95,12.20,12.55,12.90]
     ratepremi = rate[b]
  if usia_masuk == 56:
     rate=[0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,12.85,1295,13.15,13.40,13.75]
     ratepremi = rate[b]
  if usia_masuk == 57:
     rate=[0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,14.10,14.20,14.45,14.70]
     ratepremi = rate[b]
  if usia_masuk == 58:
     rate=[0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,15.45,15.55,15.80]
     ratepremi = rate[b]
  if usia_masuk == 59:
     rate=[0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,16.95,17.05]
     ratepremi = rate[b]
  if usia_masuk == 60:
     rate=[0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,18.55]
     ratepremi = rate[b]

  return ratepremi

def ConstructReportValues(
      config
      , blnLhr
      , blnReg
      , usia_masuk
      , usia_pensiun
      , iuran_bulanan
      , kenaikan_iuran
      , paket_investasi
      , tingkat_investasi
      , pengalihan_dana
      , biaya_administrasi
      , biaya_pengelolaan
     ):

  tglNow = config.ModDateTime.DecodeDate(config.Now()) #time.localtime()[:3]
  #dtNowDate = config.ModDateTime.EncodeDate(y,m,d)

  thn_ini   = int(tglNow[0])
  usia_reg  = usia_masuk
  bln_reg   = blnReg
  bln_lahir = blnLhr
  iuran_manfaat_penurunan   = iuran_bulanan
  biaya_pengelolaan_menurun = biaya_pengelolaan

  fee_bln = 0.0
  akumulasi_sebelum_biaya = 0.0
  akumulasi_setelah_biaya = 0.0
  coverDPLK = 0.0
  vPengalihan_dana  = pengalihan_dana
  vKenaikan_iuran   = kenaikan_iuran
  vIuran_bulanan    = iuran_bulanan
  persentase_iuran  = 100
  BiayaPengelolaan  = biaya_pengelolaan
  BiayaAdministrasi = 18000  #biaya_administrasi

  no_urut = 0
  yearDeath = 0
  line = 14
  # tambahan usia masuk
  usia_masuk = (usia_masuk)

  # perubahan kekurangan 1 tahun
  v_loop = (usia_pensiun-usia_masuk)+1

  dana_akhir_tahun = (iuran_bulanan + pengalihan_dana)

  akumulasi_iuran = 0
  kenaikan_iuran1 = kenaikan_iuran
  v_loop1 = 12
  loop_data = ((12-bln_reg)+1)
  i = 1

  yearDeath = (v_loop/2)
  yearDeath -= 1

  while  i <= v_loop:

     no_urut += 1
     bgcolor = '#FFFFFF'

     # Kondisi berdasarkan bulan registrasi
     if i == 1:
        b = bln_reg
        v_loop1 = loop_data
     else:
        b = 1
        v_loop1 = 12

     # Kondisi akhir periode berdasarkan bulan kelahiran
     if i == v_loop:
        v_loop1 = bln_lahir
        loop_data = bln_lahir

     iuran_tahunan    = (iuran_bulanan * v_loop1)
     akumulasi_iuran  = iuran_tahunan + akumulasi_iuran
     vIuran_tahunan   = iuran_tahunan
     vAkumulasi_iuran = akumulasi_iuran
     vIuran_bulanan   = iuran_bulanan
     fee_bln = 0

     if i == 1:
        v_loop1 = 12

     if i == v_loop:
        v_loop1 = bln_lahir

     c = b
     while c <= v_loop1:            # ------------------------ Looping ------------
     #for c in  (v_loop1):
         config.SendDebugMsg('mulai :'+str(c))
         fee_bln = ((float(tingkat_investasi)/100)/12)*dana_akhir_tahun
         akumulasi = (fee_bln+dana_akhir_tahun)
         #config.SendDebugMsg('akumulasi :'+str(akumulasi))

         if i == 1:
            if c <> 12:
               dana_akhir_tahun = (akumulasi+iuran_bulanan)
            else:
               if akumulasi < 100000001:
                  biaya_pengelolaan = 1.25
               else:
                  biaya_pengelolaan = 1

               biaya_adm = (BiayaAdministrasi/12)*loop_data
               biaya_pengelolaan = ((float(BiayaPengelolaan)/100)/12)*loop_data
               dana_akhir_tahun = ((akumulasi-(akumulasi*biaya_pengelolaan))-biaya_adm)
               akumulasi_sebelum_biaya = akumulasi
               akumulasi_setelah_biaya = ((akumulasi-(akumulasi*biaya_pengelolaan))-biaya_adm)

         else:
            if v_loop1 == 12:   # --------------------- 12 -------------------
                if c <> 12:
                      dana_akhir_tahun =(akumulasi+iuran_bulanan)
                else:
                      if akumulasi < 100000001:
                         biaya_pengelolaan = 1.25
                      else:
                         biaya_pengelolaan = 1

                      dana_akhir_tahun = ((akumulasi-(akumulasi*(float(BiayaPengelolaan)/100)))-BiayaAdministrasi)
                      akumulasi_sebelum_biaya = akumulasi
                      akumulasi_setelah_biaya = ((akumulasi - (akumulasi*(float(BiayaPengelolaan)/100)))-BiayaAdministrasi)

            else:
                # Kondisi sesuai dengan bulan kelahiran peserta
                if c <> v_loop1:
                      dana_akhir_tahun = (akumulasi+iuran_bulanan)
                else:
                      if akumulasi < 100000001:
                         biaya_pengelolaan = 1.25
                      else:
                         biaya_pengelolaan = 1

                      biaya_adm = ((BiayaAdministrasi/12)*v_loop1)
                      biaya_pengelolaan=(((float(BiayaPengelolaan)/100)/12)*loop_data)
                      dana_akhir_tahun = ((akumulasi-(akumulasi*biaya_pengelolaan))-biaya_adm)
                      akumulasi_sebelum_biaya = akumulasi
                      akumulasi_setelah_biaya = ((akumulasi - (akumulasi*biaya_pengelolaan))-biaya_adm)

             # ---------------------- END 12 ------------
         c += 1
         # ---------------------------------- end looping -----------------------

     vAkumulasi_sebelum_biaya = akumulasi_sebelum_biaya
     vAkumulasi_setelah_biaya = akumulasi_setelah_biaya

     # Kenaikan Iuran
     #config.SendDebugMsg('masuk....08'+str(kenaikan_iuran))

     if kenaikan_iuran >= 1:
          #config.SendDebugMsg('masuk....09'+str(kenaikan_iuran))

          kenaikan_iuran = (iuran_bulanan*(float(kenaikan_iuran1)/100))
          iuran_bulanan = (iuran_bulanan+kenaikan_iuran)
          dana_akhir_tahun = (dana_akhir_tahun +iuran_bulanan)

     else:
          dana_akhir_tahun = dana_akhir_tahun + iuran_bulanan

     if  i == yearDeath:
         #config.SendDebugMsg('masuk ')
         coverDPLK = vAkumulasi_setelah_biaya

     i += 1
  # end looping

  return  akumulasi_setelah_biaya  #, v_loop, coverDPLK, yearDeath

def strSQLMonitoring(config, no_peserta):
  return \
    'select no_peserta '\
    'from monitoringalkhairat '\
    'where NO_PESERTA = \'%s\' '\
    '  and flag = \'F\' ;'\
     %( no_peserta )

### Pengganti
def hitSimulasi(config, params, returns):

  userid = config.SecurityContext.userid
  kode_cabang = config.SecurityContext.GetUserInfo()[4]

  iuran_bulanan        = params.FirstRecord.GetFieldByName("iuran_perbulan")
  tgl_registrasi       = params.FirstRecord.GetFieldByName("tanggal_registrasi")
  no_peserta           = params.FirstRecord.GetFieldByName("no_peserta")
  
  premi_perbulan       = params.FirstRecord.GetFieldByName("premi_perbulan")
  manfaat_pensiun      = params.FirstRecord.GetFieldByName("manfaat_pensiun")
  

  oRekening = config.CreatePObjImplProxy('RekeningDPLK')
  oRekening.Key = no_peserta
  paket_investasi = oRekening.kode_paket_investasi

  if paket_investasi in ('a','A'):
     kode_investasi = 'INVESTASI_PAKET_A'

  if paket_investasi in ('b','B'):
     kode_investasi = 'INVESTASI_PAKET_B'

  if paket_investasi in ('c','C'):
     kode_investasi = 'INVESTASI_PAKET_C'


  oParameter = config.CreatePObjImplProxy('Parameter')
  oParameter.Key = 'JUMLAH_HARI_SETAHUN'
  JumlahHariSetahun = oParameter.Numeric_Value

  oParameter = config.CreatePObjImplProxy('Parameter')
  oParameter.Key = 'BIAYA_ADM_TAHUNAN'
  biaya_administrasi = oParameter.Numeric_value
  biaya_administrasi = (biaya_administrasi * 2)

  oParameter = config.CreatePObjImplProxy('Parameter')
  oParameter.Key = 'PERSEN_BIAYA_PENGELOLAAN'
  biaya_pengelolaan = oParameter.Numeric_value

  oParameter = config.CreatePObjImplProxy('Parameter')
  oParameter.Key = kode_investasi
  tingkat_investasi = oParameter.Numeric_value
  
  akum_iuran = (oRekening.akum_dana_iuran_pst + oRekening.akum_dana_iuran_pk)
  akum_pengembangan = oRekening.akum_dana_pengembangan
  akum_peralihan = oRekening.akum_dana_peralihan
  saldo_awal = (akum_iuran + akum_pengembangan + akum_peralihan)
  pengalihan_dana = saldo_awal

  oNasabah      = oRekening.LNasabahDPLK
  nama_peserta  = oNasabah.nama_lengkap
  usia_pensiun  = oRekening.usia_pensiun
  y, m ,d       = tgl_registrasi[:3]
  blnReg        = m
  tglRegistrasi = config.ModDateTime.EncodeDate(y, m, d)
  y, m, d       = oNasabah.tanggal_lahir[:3]
  blnLhr        = m
  tglLahir      = config.ModDateTime.EncodeDate(y, m, d)
  usia_masuk    = int(((tglRegistrasi - tglLahir)/JumlahHariSetahun))

  ratepremi     = tabelpremi(config,usia_masuk,usia_pensiun)
  kenaikan_iuran = 0
  
  nomMp         = manfaat_pensiun or 0
  nomPremi      = premi_perbulan or 0
  
  if premi_perbulan == 0 and manfaat_pensiun == 0:
     config.SendDebugMsg('Simulasi')
     danastlhbiaya = ConstructReportValues(config, blnLhr, blnReg, usia_masuk, usia_pensiun, iuran_bulanan, kenaikan_iuran, paket_investasi, tingkat_investasi, pengalihan_dana, biaya_administrasi, biaya_pengelolaan)
     premi = ((danastlhbiaya * ratepremi)/tingkat_investasi)/1000

     nomMp         =  danastlhbiaya or 0
     nomPremi      =  premi or 0
     
  else:
     if premi_perbulan == 0:
        if manfaat_pensiun > 0:
           #config.SendDebugMsg('nomPremi')
           nomPremi = float((nomMp * ratepremi)/tingkat_investasi)/1000

     if premi_perbulan > 0:
        if manfaat_pensiun == 0:
           # config.SendDebugMsg('nomMp')
           nomMp = float((nomPremi * 1000 * tingkat_investasi)/ratepremi)

  config.SendDebugMsg('Simulasi')

  strSQLId = strSQLMonitoring(config, no_peserta)
  resSQLId = config.CreateSQL(strSQLId).RawResult
  resSQLId.First()

  
  config.SendDebugMsg('Stlh Simulasi')
  mNoPeserta = resSQLId.no_peserta  or ''


  config.BeginTransaction()
  try:

    config.SendDebugMsg('Sebelum Pilihan')
    if mNoPeserta not in (None, ''):
       config.SendDebugMsg('Simpan ke Monitoring Alkhairat')

       oMonitoring = config.CreatePObjImplProxy('MonitoringAlkhairat')
       oMonitoring.key = str(no_peserta)
       oMonitoring.usia_masuk = int(usia_masuk)
       oMonitoring.tingkat_investasi = float(tingkat_investasi)
       oMonitoring.iuran_perbulan = float(iuran_bulanan)
       oMonitoring.saldo_awal = float(saldo_awal)
       oMonitoring.rate_premi = float(ratepremi)
       oMonitoring.premi_perbulan = float(nomPremi)
       oMonitoring.manfaat_asuransi = float(nomMp)
       oMonitoring.tgl_registrasi = tglRegistrasi
       oMonitoring.tgl_input = config.Now()
       oMonitoring.flag  = 'F'
       oMonitoring.user_id = userid
       oMonitoring.branch_code = kode_cabang

    else:
    
       config.SendDebugMsg('Update ke Monitoring Alkhairat')
       
       oMonitoring = config.CreatePObject('MonitoringAlkhairat')
       oMonitoring.no_peserta = str(no_peserta)
       oMonitoring.usia_masuk = int(usia_masuk)
       oMonitoring.tingkat_investasi = float(tingkat_investasi)
       oMonitoring.iuran_perbulan = float(iuran_bulanan)
       oMonitoring.saldo_awal = float(saldo_awal)
       oMonitoring.rate_premi = float(ratepremi)
       oMonitoring.premi_perbulan = float(nomPremi)
       oMonitoring.manfaat_asuransi = float(nomMp)
       oMonitoring.tgl_registrasi = tglRegistrasi
       oMonitoring.tgl_input = config.Now()
       oMonitoring.flag  = 'F'
       oMonitoring.user_id = userid
       oMonitoring.branch_code = kode_cabang

    config.SendDebugMsg('Kirim Ke form')
    
    returns.CreateValues(['nama_peserta', nama_peserta],\
      ['usia_pensiun ', usia_pensiun], \
      ['usia_masuk', usia_masuk],\
      ['tingkat_investasi', tingkat_investasi],\
      ['rate_premi', ratepremi], \
      ['saldo_awal', saldo_awal],\
      ['nominal_premi', nomPremi],\
      ['manfaat_pensiun', nomMp])
      
    config.Commit()
  except:
    config.Rollback()
    raise

def hitSimpan(config, params, returns):

  config.SendDebugMsg('Simpan...........')
  config.BeginTransaction()
  try:

     oMonitoring = config.CreatePObject('MonitoringAlkhairat')
     oMonitoring.no_peserta = params.FirstRecord.GetFieldByName("no_peserta")
     oMonitoring.usia_masuk = params.FirstRecord.GetFieldByName("usia_masuk")
     oMonitoring.tingkat_investasi = params.FirstRecord.GetFieldByName("tingkat_investasi")
     oMonitoring.iuran_perbulan = params.FirstRecord.GetFieldByName("iuran_perbulan")
     oMonitoring.saldo_awal = params.FirstRecord.GetFieldByName("saldo_awal")
     oMonitoring.rate_premi = params.FirstRecord.GetFieldByName("rate_premi")
     oMonitoring.premi_perbulan = params.FirstRecord.GetFieldByName("premi_perbulan")
     oMonitoring.manfaat_asuransi = params.FirstRecord.GetFieldByName("manfaat_asuransi")
     oMonitoring.tgl_registrasi = params.FirstRecord.GetFieldByName("tgl_registrasi")
     oMonitoring.tgl_input = config.Now()
     oMonitoring.tgl_kirim = ''
     oMonitoring.flag  = 'F'
     
     config.Commit()
  except:
     config.Rollback()

     raise


