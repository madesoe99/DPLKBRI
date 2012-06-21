import string, sys, dafsys
sys.path.append('c:/dafapp/dplk07/script_modules')
import transaksiapi

file_user = 'PertaminaGeo-01.txt'
SEP = '|'

def DoKoreksi(config):
  fl = open(file_user,'r')
  ls_fl = fl.readlines()
  count = len(ls_fl)
  config.BeginTransaction()
  try:
    I = 0
    while I<=count-1:
      val = ls_fl[I].split(SEP)
      UpdateTransaksiPK(config, val)
      I += 1
    config.Commit()
  except:
    config.Rollback()
    raise 'Error'

def UpdateTransaksiPK(config, val):
 
  sUpdTrans = "update transaksidplk \
               set mutasi_iuran_pk = %f,\
               where no_peserta = \'%s\'\
                and id_transaksi = \'%d\'"\
               % (0.0, val[0],int(val[1]))    
  config.ExecSQL(sUpdTrans)

  oRekeningDPLK = config.CreatePObjImplProxy('RekeningDPLK')
  oRekeningDPLK.key = val[0]   
  #oRekeningDPLK.akum_dana_iuran_pst = oRekeningDPLK.akum_dana_iuran_pst + float(val[2])
  oRekeningDPLK.akum_dana_iuran_pk  = oRekeningDPLK.akum_dana_iuran_pk - float(val[2])
    
def SafeFloat(f):
    fl = f
    if f == None:
        fl = 0.0

    return fl

## MAIN PROGRAM    
config = dafsys.OpenConfig('c:/dafapp/dplk07/default.cfg')
DoKoreksi(config)
    
