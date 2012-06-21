import sys, re, DBAppFramework
sys.path.append('c:/dafapp/dplk07/script_modules')
sys.path.append('c:/dafapp/dplk07/scripts/transaksi')

import lockupdate

config = DBAppFramework.GetConfig()

sSQL = 'select * from HistoriGiro h where h.Keterangan is not null'
rSQL = config.CreateSQL(sSQL).RawResult

config.BeginTransaction()
try:
  rSQL.First()
  i = 1
  while not rSQL.Eof:
    #proses nomor peserta (lebih baik pake Regex) yang masih ada di bagian keterangan
    if re.search('[0-9]+',rSQL.Keterangan):
      r = re.search('[0-9]+',rSQL.Keterangan)
      if len(r.group()) == 11:
        #update Nomor Peserta yang berasal dari keterangan
        lockupdate.UpdateProcess(config, 'HistoriGiro', \
        'Nomor_Peserta = \'%s\',Keterangan = Null' % (r.group()), \
        'ID_HistoriGiroHarian = %d and Acc_Giro = \'%s\' and Nomor_Urut = \'%s\'' \
          % (rSQL.ID_HistoriGiroHarian,rSQL.Acc_Giro,rSQL.Nomor_Urut), \
        'Nomor_Peserta is Null')
        print '#%d Nomor Peserta : %s' % (i,r.group())
        i += 1
      #else: do nothing
      
    rSQL.Next()

  #flushing to database
  config.FlushUpdates()
  
  print 'Sukses mereshape tabel HistoriGiro...'

  config.Commit()
except:
  config.Rollback()
  raise
