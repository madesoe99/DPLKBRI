import dafsys, sys
CONFIG_FILE = 'c:/dafapp/dplk07/default.cfg'
#CONFIG_FILE = 'c:/dafapp/dplk07/testprod.cfg'

def Main(config, strSQL, InitialState):

  #perlu mencari peserta wasiat ummat aktif yang tidak membayar premi dibulan sebelumnya

  rSQLAkseptasi = config.CreateSQL(strSQL).RawResult

  config.BeginTransaction()
  try:
    rSQLAkseptasi.First()
    while not rSQLAkseptasi.Eof:    
          print 'Memproses peserta %s: ' % (rSQLAkseptasi.no_peserta)
          y,m,d = rSQLAkseptasi.tgl_akseptasi[:3]
          mAkseptasi = config.ModDateTime.EncodeDate(y,m,d)
          
          y = rSQLAkseptasi.tgl_akseptasi[0]
          m = rSQLAkseptasi.tgl_akseptasi[1]
          d = rSQLAkseptasi.tgl_akseptasi[2]
           
          sSQL = 'select NO_PESERTA from TRANSAKSIPREMI '\
               '  where ISCOMMITTED = \'T\' '\
               '    and  TGL_TRANSAKSI > %s '\
               '    and NO_PESERTA = \'%s\' '\
               '  order by NO_PESERTA ' \
                % (config.FormatDateTime('yyyy-mm-dd',mAkseptasi), rSQLAkseptasi.no_peserta)
                
          rSQL = config.CreateSQL(sSQL).RawResult
          rSQL.First()
          while not rSQL.Eof:
    
                #ambil info besar premi di rekening wasiat ummat
                oRWU = config.CreatePObjImplProxy('RekeningWasiatUmmat')
                oRWU.Key = rSQLAkseptasi.rekeningwasiatummat_id
                
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
          rSQLAkseptasi.Next()      
    config.Commit()
  except:
    config.Rollback()
    raise
  return 1


def strTglAkseptasi(config, tglAwal, tglAkhir):

  nSQL = 'select rwu.NO_PESERTA, rwu.TGL_AKSEPTASI, rwu.REKENINGWASIATUMMAT_ID \
          from REKENINGWASIATUMMAT rwu, REKENINGDPLK r \
          where rwu.NO_PESERTA = r.no_peserta and \
                r.STATUS_DPLK = \'A\' and \
                rwu.NO_PESERTA in \
                    (select n.NO_PESERTA from NASABAHDPLK n \
                     where n.TGL_REGISTRASI >= %d and \
                           n.TGL_REGISTRASI < %d) \
          order by rwu.NO_PESERTA' \
          % (tglAwal,tglAkhir)
  return nSQL
  
# End Tgl Akseptasi 

def ScriptMain(config, tglAwal, tglAkhir):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # pid: Process ID of this script
  # monfilename: Monitor file name to store status
  state = 1
  
  if tglAwal[2] != '-' or tglAwal[5] != '-' \
     or tglAkhir[2] != '-' or tglAkhir[5] != '-' :
     raise 'ERROR','Format tanggal salah DD-MM-YYY (untuk tanggal awal dan akhir)'
  d = 1
  m = int(tglAwal[3:5])
  y = int(tglAwal[6:])
  app = config.AppObject
  dtTglAwal = config.ModLibUtils.EncodeDate(y,m,d)
  m = int(tglAkhir[3:5])
  y = int(tglAkhir[6:])
  dtTglAkhir = config.ModLibUtils.EncodeDate(y,m,d)
  
  if dtTglAwal >= dtTglAkhir :
     raise 'ERROR','Tanggal proses minimal berbeda 1 bln'
  
  consoleID = 'KolektibilitasWasiatUmmat'

  print '%s. Tanggal Awal = %s' % ('Pengecekan Kolektibilitas Peserta Wasiat Ummat',tglAwal)
  print 'Tanggal Akhir = %s' % tglAkhir
  print 'mulai berlangsung\r\n'
  try:
    print 'progress'
    
    try:
      #dtTglProcess = dtTglAwal
      #while dtTglProcess < dtTglAkhir :            
        
        #Query tgl Akseptasi ....
        strSQL = strTglAkseptasi(config, dtTglAwal, dtTglAkhir +1)
        #dtTglProcess = config.ModLibUtils.IncMonth(dtTglProcess, 1)
        #main task right here
        Main(config, strSQL, state)
        state = 0

    finally:
      print ' telah selesai\r\n'
  except:
    print ': Error\r\n' + str(sys.exc_info()[1]) + '\r\n'
    raise


#main function
if __name__ == '__main__':
    config = dafsys.OpenConfig(CONFIG_FILE)


    if len(sys.argv) < 3:
          raise 'argument error', 'Exec_CollectivityWasiatUmmatAwal.py <Begin date DD-MM-YYYY> <End date DD-MM-YYYY>'
    #
    print 'Configuration File : %s' % CONFIG_FILE
    #ScriptMain(config,sys.argv[2],sys.argv[3])
    ScriptMain(config,'01-01-1999','03-10-2010')
    print 'Configuration File : %s' % CONFIG_FILE
