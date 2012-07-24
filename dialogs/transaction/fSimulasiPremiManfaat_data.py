#sys.path.append('c:/dafapp/dplk07/script_modules')
#import moduleapi, transaksiapi

import sys, string
import com.ihsan.util.modman as modman
import com.ihsan.foundation.appserver as appserver

modman.loadStdModules(globals(),
  [
    "moduleapi",
    "transaksiapi"
  ]
)

def tabelpremi(config, usia_masuk, usia_pensiun):

  x = 45
  z = 0

  while x <= 65:
    if usia_pensiun == x:
       b = z
    z += 1
    x += 1

  #b = b - 45
  ratepremi = 0
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

  if ratepremi == 0:
    raise Exception, '\n\nPERHATIAN!\nRate premi tidak terdefinisi'
    
  return ratepremi

### Pengganti
def hitSimulasi(config, params, returns):

  config.SendDebugMsg('masukkkkkkkkk!!!!!!')
  
  tgl_lahir            = params.FirstRecord.GetFieldByName("tanggal_lahir")
  usia_pensiun         = params.FirstRecord.GetFieldByName("usia_pensiun")
  paket_investasi      = params.FirstRecord.GetFieldByName("paket_investasi")
  tgl_registrasi       = params.FirstRecord.GetFieldByName("tanggal_registrasi")
  premi                = params.FirstRecord.GetFieldByName("premi")
  mp                   = params.FirstRecord.GetFieldByName("manfaat_pensiun")

  config.SendDebugMsg('masuk....01')
  oParameter = config.CreatePObjImplProxy('Parameter')
  oParameter.Key = 'JUMLAH_HARI_SETAHUN'
  JumlahHariSetahun = oParameter.Numeric_Value

  if paket_investasi in ('a','A'):
     kode_investasi = 'INVESTASI_PAKET_A'

  if paket_investasi in ('b','B'):
     kode_investasi = 'INVESTASI_PAKET_B'

  if paket_investasi in ('c','C'):
     kode_investasi = 'INVESTASI_PAKET_C'

  oParameter = config.CreatePObjImplProxy('Parameter')
  oParameter.Key = kode_investasi
  tingkat_investasi = oParameter.Numeric_value

  y, m ,d       = tgl_registrasi[:3]
  tglRegistrasi = config.ModDateTime.EncodeDate(y, m, d)
  y, m, d       = tgl_lahir[:3]
  tglLahir      = config.ModDateTime.EncodeDate(y, m, d)
  usia_masuk    = int(((tglRegistrasi - tglLahir)/JumlahHariSetahun))
  ratepremi     = tabelpremi(config,usia_masuk,usia_pensiun)
  nomPremi      = premi or 0
  nomMp         = mp or 0

  if nomPremi == 0:
     if nomMp > 0:
        #config.SendDebugMsg('nomPremi')
        nomPremi = float((nomMp * ratepremi)/tingkat_investasi)/1000

  if nomPremi > 0:
     if nomMp == 0:
       # config.SendDebugMsg('nomMp')
        nomMp = float((nomPremi * 1000 * tingkat_investasi)/ratepremi)

  config.SendDebugMsg('nomPremi :'+str(nomPremi))
  config.SendDebugMsg('nomMp    :'+str(nomMp))
  
  config.BeginTransaction()
  try:
    config.SendDebugMsg('Stlh Tabel 3')
    returns.CreateValues(['usia_masuk', usia_masuk],\
    ['tingkat_investasi', tingkat_investasi],\
    ['rate_premi', ratepremi], \
    ['nominal_premi', nomPremi], \
    ['manfaat_pensiun', nomMp])
    config.Commit()
  except:
    config.Rollback()
    raise
