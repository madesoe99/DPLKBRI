import dafsys, sys
#CONFIG_FILE = 'c:/dafapp/dplk07/default.cfg'
CONFIG_FILE = 'c:/dafapp/dplk07/testprod.cfg'

def Main(config, dtTglChecking, InitialState):

  #perlu mencari peserta wasiat ummat aktif yang tidak membayar premi dibulan sebelumnya
  dtOneMonthBefore = config.ModLibUtils.IncMonth(dtTglChecking, -1)
  y0,m0 = config.ModLibUtils.DecodeDate(dtOneMonthBefore)[:2]
  
  sSQL = 'select rwu.NO_PESERTA, rwu.REKENINGWASIATUMMAT_ID \
          from REKENINGWASIATUMMAT rwu, REKENINGDPLK r \
          where rwu.NO_PESERTA = r.no_peserta and \
                r.STATUS_DPLK = \'A\' and \
                rwu.NO_PESERTA not in \
                    (select tp.NO_PESERTA from TRANSAKSIPREMI tp \
                     where tp.ISCOMMITTED = \'T\' and \
                           DATEPART(m, tp.TGL_TRANSAKSI) = %d and \
                           DATEPART(yyyy, tp.TGL_TRANSAKSI) = %d) \
          order by rwu.NO_PESERTA' \
          % (m0,y0)
  rSQL = config.CreateSQL(sSQL).RawResult
  
  config.BeginTransaction()
  try:
    rSQL.First()
    while not rSQL.Eof:
    
      print 'Memproses peserta %s: ' % (rSQL.no_peserta)    
      
      #ambil info besar premi di rekening wasiat ummat
      oRWU = config.CreatePObjImplProxy('RekeningWasiatUmmat')
      oRWU.Key = rSQL.rekeningwasiatummat_id
      
      #update kewajiban wasiat ummat peserta = nilai besar premi
      #update juga status collectivity-nya
      oR = config.CreatePObjImplProxy('RekeningDPLK')
      oR.Key = rSQL.no_peserta
      if InitialState :
         oR.kewajiban_wasiat_ummat = oRWU.besar_premi
      else :
         oR.kewajiban_wasiat_ummat = oR.kewajiban_wasiat_ummat + oRWU.besar_premi
      oR.collectivity_wasiat_ummat = 'F'
      
      rSQL.Next()
    
    config.Commit()
  except:
    config.Rollback()
    raise

  return 1

def ScriptMain(config, tglAwal, tglAkhir):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # pid: Process ID of this script
  # monfilename: Monitor file name to store status
  state = 1
  
  if tglAwal[2] != '-' or tglAwal[5] != '-' \
     or tglAkhir[2] != '-' or tglAkhir[5] != '-' :
     raise Exception, 'ERROR' + 'Format tanggal salah DD-MM-YYY (untuk tanggal awal dan akhir)'
  d = 1
  m = int(tglAwal[3:5])
  y = int(tglAwal[6:])
  app = config.AppObject
  dtTglAwal = config.ModLibUtils.EncodeDate(y,m,d)
  m = int(tglAkhir[3:5])
  y = int(tglAkhir[6:])
  dtTglAkhir = config.ModLibUtils.EncodeDate(y,m,d)
  
  if dtTglAwal >= dtTglAkhir :
     raise Exception, 'ERROR' + 'Tanggal proses minimal berbeda 1 bln'
  
  consoleID = 'KolektibilitasWasiatUmmat'

  print '%s. Tanggal Awal = %s' % ('Pengecekan Kolektibilitas Peserta Wasiat Ummat',tglAwal)
  print 'Tanggal Akhir = %s' % tglAkhir
  print 'mulai berlangsung\r\n'
  try:
    print 'progress'
    
    try:
      dtTglProcess = dtTglAwal
      while dtTglProcess < dtTglAkhir :            
        
        dtTglProcess = config.ModLibUtils.IncMonth(dtTglProcess, 1)
        #main task right here
        Main(config, dtTglProcess,state)
        state = 0

    finally:
      print ' telah selesai\r\n'
  except:
    print ': Error\r\n' + str(sys.exc_info()[1]) + '\r\n'
    raise


#main function
config = dafsys.OpenConfig(CONFIG_FILE)


if len(sys.argv) < 3:
      raise Exception, 'argument error' +  'Exec_CollectivityWasiatUmmatAwal.py <Begin date DD-MM-YYYY> <End date DD-MM-YYYY>'
#
print 'Configuration File : %s' % CONFIG_FILE
ScriptMain(config,sys.argv[2],sys.argv[3])
print 'Configuration File : %s' % CONFIG_FILE
