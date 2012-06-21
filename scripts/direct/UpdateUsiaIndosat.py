import string, sys, dafsys
sys.path.append('c:/dafapp/dplk07/script_modules')
import transaksiapi

file_user = 'UpdateUsiaPensiunIndosat.csv'
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
      print 'No Peserta              [0]: %s ' %(val[0])
      print 'Tgl Pensiun             [1]: %s ' %(val[2])
      print 'Tgl Pensiun Percepat    [2]: %s ' %(val[1])
      print '###----------End --------------#'
      UpdateNasabahDPLK(config, val)
      I += 1
    config.Commit()
  except:
    config.Rollback()
    raise 'Error'

def UpdateNasabahDPLK(config, val):
    
  usia_pensiun = 45
  sUpdTrans = "UPDATE REKENINGDPLK \
               SET TGL_PENSIUN = \'%s',\
               USIA_PENSIUN  = %d ,\
               TGL_PENSIUN_DIPERCEPAT = \'%s\'\
               WHERE NO_PESERTA = \'%s\'"\
               % (val[1],usia_pensiun,val[2],val[0])
  
  config.ExecSQL(sUpdTrans)


## MAIN PROGRAM    
config = dafsys.OpenConfig('c:/dafapp/dplk07/testprod.cfg')
DoKoreksi(config)
    
