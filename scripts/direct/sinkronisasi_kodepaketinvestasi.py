import dafsys
import sys, string

STATUSSTRUCTURE = ';'.join([
    'IsErr:integer'
    , 'ErrMessage:string'
])

def UpdateKodePaketInvestasiKiblat(config2, fHandle, no_peserta, kode_paket_investasi):
  sSQL = 'SELECT jnsinv FROM dpl_mast WHERE nompst =\'%s\'' % (no_peserta)
  rSQL = config2.CreateSQL(sSQL).RawResult
  if not (rSQL.Eof or rSQL.jnsinv == kode_paket_investasi):
      sSQL2 = \
        'UPDATE dpl_mast SET jnsinv = \'%s\'\
        WHERE nompst = \'%s\' ' % (kode_paket_investasi, no_peserta)
    ##  print strSQL
      rSQL2 = config2.ExecSQL(sSQL2)
      if rSQL > 0:
          fHandle.write('No peserta = %s; Kode paket KIBLAT = %s; \
          Kode paket aplikasi = %s\n' % (no_peserta, rSQL.jnsinv, kode_paket_investasi))
    

config = dafsys.OpenConfig('c:/dafapp/dplk07/default.cfg')
config2 = dafsys.OpenConfig('c:/dafapp/smkiblat/default.cfg')
##config2 = dafsys.OpenConfig('c:/dafapp/kiblat/interface/default.cfg')
config2.BeginTransaction()
fHandle = open('c:/sinkronisasikodepaket.txt', 'w')
try:
  sSQL = 'SELECT no_peserta, kode_paket_investasi \
  FROM REKENINGDPLK \
  WHERE status_dplk = \'A\' \
  ORDER BY no_peserta'
  rSQL = config.CreateSQL(sSQL).RawResult  
  while not rSQL.Eof:
    print 'peserta : ' + rSQL.no_peserta
    no_peserta = rSQL.no_peserta
    kode_paket_investasi = rSQL.kode_paket_investasi
    UpdateKodePaketInvestasiKiblat(config2, fHandle, no_peserta, kode_paket_investasi)
    
    rSQL.Next()  
  config2.Commit()
  fHandle.close()
except:
  config2.Rollback()
  raise

