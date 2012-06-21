import dafsys
from string import *

def RestoreData(cfg):
  INPUT = 'daftarwutes.txt'
  OUTPUT = 'hasil_daftar_wu.txt'
  fl = open(INPUT,'r')
  flo = open(OUTPUT,'w')
  ls = fl.readlines()  
  rowCount = len(ls)
  try:    
    cfg.BeginTransaction()
    try:
          sSQLAkseptasi = 'select r.no_peserta, w.tgl_akseptasi, w.besar_premi \
                           from rekeningdplk r, rekeningwasiatummat w \
                           where r.no_peserta = w.no_peserta \
                             and r.status_dplk = \'A\'\
                             order by r.no_peserta '\
                                                                          
          rSQL = cfg.CreateSQL(sSQLAkseptasi).RawResult
          a = 1      
          rSQL.First()
          while not rSQL.eof:
             y,m,d = rSQL.tgl_akseptasi[:3]
             mDate = cfg.ModDateTime.EncodeDate(y,m,d)
             no_peserta = rSQL.no_peserta
             
             print str('No Peserta : '+ no_peserta)
              
             sSQLPremi = 'Select no_peserta,sum(mutasi_premi) as totpremi \
                            from transaksipremi \
                           where no_peserta =\'%s\'\
                             and tgl_transaksi >= \'%s\'\
                             and IsCommitted = \'T\'\
                             group by no_peserta '\
                     % (no_peserta, cfg.FormatDateTime('yyyy-mm-dd',mDate))
                     
             rSQLPremi = cfg.CreateSQL(sSQLPremi).RawResult
             rSQLPremi.First()
                    
             while not rSQLPremi.eof:
                #y,m,d = rSQLPremi.tgl_transaksi[:3]
                #mTrans = cfg.ModDateTime.EncodeDate(y,m,d)

                flo.write(no_peserta+'|'+cfg.FormatDateTime('yyyy-mm-dd',mDate) +'|'+str(rSQL.besar_premi)+'|'+str(rSQLPremi.totpremi)+'\n')
                rSQLPremi.Next()                               
             a +=1
             #flo.write(str(data)+'\n')
             rSQL.Next()

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
