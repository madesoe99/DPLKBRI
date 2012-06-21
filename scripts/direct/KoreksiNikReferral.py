import string, sys, dafsys
sys.path.append('c:/dafapp/dplk07/script_modules')
import transaksiapi

file_user = 'KoreksiNIKReferral.txt'
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
      print 'NIK LAMA : %s ' % (val[0])
      print 'NIK baru : %s ' % (val[1])
      UpdateNikReferral(config, val)
      I += 1
    config.Commit()
  except:
    config.Rollback()
    raise 'Error'

def UpdateNikReferral(config, val):
  tgl = '11-01-2010'
  
  sUpdTrans = "update nasabahdplk \
                set no_referensi = \'%s\'\
                where no_referensi = \'%s\'\
                  and tgl_registrasi >= '11-01-2010'"\
                % (val[1],val[0])
  config.ExecSQL(sUpdTrans)
  
## MAIN PROGRAM    
config = dafsys.OpenConfig('c:/dafapp/dplk07/default.cfg')
#config = dafsys.OpenConfig('c:/dafapp/dplk07/testprod.cfg')
DoKoreksi(config)
    
