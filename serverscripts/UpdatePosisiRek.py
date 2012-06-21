import sys, dafsys, time

def Proses(config):
  oP = config.CreatePObjImplProxy('Parameter')
  oP.key = 'ACCRUE_PREV'
  tanggal = oP.varchar_value
    
  sSQL = "update posisirek \
          set saldo_pod = (select sum(akum_dana_iuran_pst) + \
          		sum(akum_dana_iuran_pk) + sum(akum_dana_pengembangan) + \
          		sum(akum_dana_peralihan) \
          		from rekeningdplk \
          		where posisirek.no_peserta = rekeningdplk.no_peserta \
          		and status_dplk = 'A') \
          where exists \
          (select 1 \
          from rekeningdplk \
          where posisirek.no_peserta = rekeningdplk.no_peserta \
          and status_dplk = 'A')" 
      
  sSQL2 = "update PAKETINVESTASI \
            set nav = (saldo_paket + (select nom_return \
            	from posisireturn \
            	where kode_jns_investasi = 'D' \
            	and tanggal = '%s')) / unit, saldo_paket = saldo_paket + (select nom_return \
            	from posisireturn \
            	where kode_jns_investasi = 'D' \
            	and tanggal = '%s')\
            where kode_paket_investasi = 'A'" % (tanggal, tanggal)
            
  sSQL3 = "update PAKETINVESTASI \
            set nav = (saldo_paket  + (select nom_return \
            	from posisireturn \
            	where kode_jns_investasi = 'O' \
            	and tanggal = '%s')) / unit, saldo_paket = saldo_paket + (select nom_return \
            	from posisireturn \
            	where kode_jns_investasi = 'O' \
            	and tanggal = '%s')\
            where kode_paket_investasi = 'B'" % (tanggal, tanggal)
            
  sSQL4 = "update PAKETINVESTASI \
            set nav = (saldo_paket + (select sum(nom_return) \
            	from posisireturn \
            	where kode_jns_investasi in ('R','S') \
            	and tanggal = '%s')) / unit , saldo_paket = saldo_paket + (select nom_return \
            	from posisireturn \
            	where kode_jns_investasi in ('R','S') \
            	and tanggal = '%s')\
            where kode_paket_investasi = 'C'" % (tanggal, tanggal) 
            
  config.BeginTransaction()
  try:
    runSQL(config, sSQL)
    runSQL(config, sSQL2)
    runSQL(config, sSQL3)
    runSQL(config, sSQL4)
    config.Commit()
  except:
    config.Rollback()
    raise str(sys.exc_info()[1])
    
def runSQL(config, sSQL):
  print 'SQL:> \n', sSQL
  t1 = time.clock()
  if config.ExecSQL(sSQL) < 0:
    raise 'runSQL', config.GetDBConnErrorInfo()
  t2 = time.clock()
  
  print '>>... %.8f seconds\n' % (t2-t1)
    
#-- MAIN
if __name__ == '__main__':
  config = dafsys.OpenConfig('c:/dafapp/dplk07/default.cfg')
  Proses(config)
    
