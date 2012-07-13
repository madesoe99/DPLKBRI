import sys, dafsys, time

def Proses(config):
  sSQL = "drop table tmpnav" 
  sSQL2 = "create table tmpnav \
          (kode_jenis_investasi varchar(1), \
          saldo float, \
          nav float, \
          unit float)" 
  sSQL3 = "insert into historinav \
          select getdate(), kode_paket_investasi, saldo_paket, nav, unit \
          from PaketInvestasi" 
  sSQL4 = "insert into tmpnav \
          select kode_jns_investasi, sum(akum_lr), sum(akum_lr) / unit, unit \
          from investasi a, prevnav b \
          where status = 'T' \
          and a.kode_jns_investasi = b.kode_jenis_investasi \
          group by kode_jns_investasi, unit" 
  sSQL5 = "drop table prevnav" 
  sSQL6 = "create table prevnav \
          (kode_paket_investasi varchar(1),\
          saldo float, \
          nav float,\
          unit float)" 
  sSQL7 = "insert into prevnav \
          select * from tmpnav" 
                    
  config.BeginTransaction()
  try:
    runSQL(config, sSQL)
    runSQL(config, sSQL2)
    runSQL(config, sSQL3)
    runSQL(config, sSQL4)
    runSQL(config, sSQL5)
    runSQL(config, sSQL6)
    runSQL(config, sSQL7)
    config.Commit()
  except:
    config.Rollback()
    raise str(sys.exc_info()[1])
    
def runSQL(config, sSQL):
  print 'SQL:> \n', sSQL
  t1 = time.clock()
  if config.ExecSQL(sSQL) < 0:
    raise Exception, 'runSQL' +  config.GetDBConnErrorInfo()
  t2 = time.clock()
  
  print '>>... %.8f seconds\n' % (t2-t1)
    
#-- MAIN
if __name__ == '__main__':
  config = dafsys.OpenConfig('c:/dafapp/dplk07/default.cfg')
  Proses(config)
    
