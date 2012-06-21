import dafsys
from string import *

def RestoreData(cfg):
  INPUT = 'rekening_koreksi.txt'
  OUTPUT = 'hasil_koreksi_biaya.txt'
  fl = open(INPUT,'r')
  flo = open(OUTPUT,'w')
  ls = fl.readlines()  
  rowCount = len(ls)
  try:    
    cfg.BeginTransaction()
    try:
        i = 0
        while i<=rowCount-1:
          print str(i+1) + ' - ' + ls[i]
          no_peserta = strip(ls[i])
          sSQL = 'select isnull(sum(mutasi_iuran_pk),0.0) as pk,\
                  isnull(sum(mutasi_iuran_pst),0.0) as pst,\
                  isnull(sum(mutasi_pengembangan),0.0) as pengembangan,\
                  isnull(sum(mutasi_peralihan),0.0) as peralihan\
                  from transaksidplk\
                  where no_peserta = \'%s\'\
                  and IsCommitted = \'T\'' % (no_peserta)
          rSQL = cfg.CreateSQL(sSQL).RawResult
          flo.write(sSQL+'\n')
          flo.write(str(i+1)+' - '+ls[i]+';pst='+str(rSQL.pst)+';pengem='+str(rSQL.pengembangan)+'\n')
          sUpdRek = 'update rekeningdplk \
                      set akum_dana_iuran_pk = %f,\
                      akum_dana_iuran_pst = %f,\
                      akum_dana_pengembangan = %f,\
                      akum_dana_peralihan = %f\
                      where no_peserta = \'%s\'' \
                      % (SafeFloat(rSQL.pk), SafeFloat(rSQL.pst), \
                         SafeFloat(rSQL.pengembangan), SafeFloat(rSQL.peralihan), no_peserta)
          cfg.ExecSQL(sUpdRek)
          sUpdDet = 'update detailakumpengembangan \
                      set nilai_akumulasi = %f\
                      where no_peserta = \'%s\' and \
                      kode_jenis_investasi = \'D\'' \
                      % (SafeFloat(rSQL.pengembangan), no_peserta)
          cfg.ExecSQL(sUpdDet)            
          i += 1
        cfg.Commit()
    except:
      cfg.Rollback()
      raise
  finally:
    fl.close()
    flo.close()

def SafeFloat(f):
    fl = f
    if f == None:
        fl = 0.0

    return fl

# Main

cfg = dafsys.OpenConfig('c:/dafapp/dplk07/default.cfg')
RestoreData(cfg)
