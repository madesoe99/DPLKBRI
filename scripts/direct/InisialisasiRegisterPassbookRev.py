import dafsys

# update rekeningdplk
# set has_passbook = 'T'
# where status_dplk = 'A'

config = dafsys.OpenConfig('c:/dafapp/dplk07/testprod.cfg')
config.BeginTransaction()
try:
  sSQL = "SELECT no_peserta \
  FROM REKENINGDPLK \
  WHERE STATUS_DPLK = 'A' \
    and no_peserta not in \
        ( select no_peserta from registerpassbook ) "
        
  rSQL = config.CreateSQL(sSQL).RawResult
  while not rSQL.Eof:    
    print 'peserta : ' + rSQL.no_peserta
    oReg = config.CreatePObject('RegisterPassbook')
    oReg.no_peserta = rSQL.no_peserta
    oReg.Is_Baru_Register = 'T'
    oReg.Baris_Cetak_Terakhir = 0
    oReg.Halaman_Cetak_Terakhir = 1
    oReg.Nomor_Buku_Terakhir = 1   
    rSQL.Next()
  config.Commit()
except:
  config.Rollback()
  raise
