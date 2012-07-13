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
#Berikut merupakan variabel dummy untuk mengeset variable yang invalid
v_DummyYear = 1990
v_TanggalAkseptasiWasiatUmmat = 1  
v_BulanAkseptasiWasiatUmmat = 1
v_TahunAkseptasiWasiatUmmat = 1990

def ValidateDate(config, y, m, d):
  global v_TahunValid, v_DummyYear

  if y < v_TahunValid:
    y = v_DummyYear
  
  return config.ModLibUtils.EncodeDate(y, m, d)
  
#-------------------------------------------------------------------------------
## SCRIPT SINKRONISASI
#-------------------------------------------------------------------------------

def Sinkronisasi(config, con):
  global v_IP_Server, v_TahunAkseptasiWasiatUmmat,\
    v_BulanAkseptasiWasiatUmmat,v_TanggalAkseptasiWasiatUmmat

  res = 1
  if res >= 0:
    #tidak error, lanjutkan sinkronisasi tgl akseptasi wasiat ummat
    q = con.GetQuery('select * from REKENING_DPLK')
    while not q.Eof():
      o = config.CreatePObjImplProxy('RekeningDPLK')
      o.Key = q.GetFieldValue('NO_PESERTA').lstrip().rstrip()
      
      #cek status wasiat ummat peserta
      if q.GetFieldValue('WASIAT_UMMAT').lstrip().rstrip() == 'T':
        #peserta ikut wasiat ummat, lakukan sinkronisasi tanggal akseptasi wasiat ummat
        o.Ls_RekeningWasiatUmmat.First()
        oRWU = o.Ls_RekeningWasiatUmmat.CurentElement
        
        y,m,d = q.GetFieldValue('TGL_AKSEPTASI')[:3]
        oRWU.tgl_akseptasi = ValidateDate(config, y,m,d)
      
      #flushing database
      config.FlushUpdates()
      
      q.Next()
    
  else:
    raise Exception, 'ERROR' + 'Gagal memproses Sinkronisasi Tanggal Akseptasi Wasiat Ummat!'

  return 1

# MAIN MODULE CALLER -----------------------------------------------------------

config = DBAppFramework.GetConfig()

#setting old DPLK DB connection 
con = dafdb.getDBConnection('c:/dafapp/dplk/default.cfg','PRIMARY_DATABASE')
con.Connect()

try:
  print 'Mulai proses impor: '+ time.asctime()  
  config.BeginTransaction()
  try:
    ## STEP 2 ##
    print '\n\nProcessing Sinkronisasi Tanggal Wasiat Umat...'
  
    Sinkronisasi(config, con)
  
    #flushing to database
    config.FlushUpdates()
    config.Commit()
  except:
    config.Rollback()
    raise

  print 'Sukses sinkronisasi Tanggal Wasiat Ummat basisdata DPLK lama ke basisdata DPLK baru!!!'
  print 'Selesai proses impor: '+ time.asctime()
    
  con.Disconnect()
except:
  raise
