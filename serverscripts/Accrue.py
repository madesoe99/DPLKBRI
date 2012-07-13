import sys, dafsys, time, string
   
def HitungAccrue(config, rate, nom_pokok, nhari, n):

  accrue = (rate / 100) * (n / nhari) * nom_pokok
  
  return accrue

def HitungSPI(config, nom_pokok, nom_pari, nhari):

    spi = (nom_pari - nom_pokok) / nhari
    
    return spi

def UpdatePosisiReturn(config, nom_return, strtgl, jenis):
  sSQL = "SELECT * FROM PosisiReturn\
  WHERE tanggal = '%s'\
  and kode_jns_investasi = '%s'" % (strtgl, jenis)
  rSQL = config.CreateSQL(sSQL).RawResult
  if not rSQL.Eof:
    sExc = "UPDATE PosisiReturn \
    SET nom_return = nom_return + %s\
    WHERE tanggal = '%s'\
    and kode_jns_investasi = '%s'" % (nom_return, strtgl, jenis)
  else:
    sExc = "INSERT INTO PosisiReturn VALUES \
    ('%s','%s',%s)" % (strtgl, jenis, nom_return)
    
  config.SendDebugMsg(sExc)
  runSQL(config, sExc)
  
def UpdatePosisiReturnDeposito(config, nom_return):
  sExc = "update posisirek \
          set return_deposito = return_deposito + \
        	(%s  * (saldo_pod / (select sum(saldo_pod) from posisirek \
          where kode_paket_investasi = 'A'))) \
          where kode_paket_investasi = 'A' \
        " % (nom_return)
    
  config.SendDebugMsg(sExc)
  runSQL(config, sExc)
   
def UpdatePosisiReturnObligasi(config, nom_return):
  sExc = "update posisirek \
          set return_obligasi = return_obligasi + \
        	(%s  * (saldo_pod / (select sum(saldo_pod) from posisirek \
          where kode_paket_investasi = 'B'))) \
          where kode_paket_investasi = 'B' \
        " % (nom_return)
    
  config.SendDebugMsg(sExc)
  runSQL(config, sExc)
 
def InsertHistoriAccrue(config, tanggal, id_investasi, nominal):
  sSQL = "insert into historiaccrue values \
          ('%s', %s, 'A', %s)" % (tanggal, id_investasi, nominal)    
  runSQL(config, sSQL)
  
def UpdateAkumAccrue(config, id_investasi, nominal):
  sSQL = "SELECT * FROM akumaccrue\
  WHERE id_investasi = %s" % (id_investasi)
  rSQL = config.CreateSQL(sSQL).RawResult
  if not rSQL.Eof:
    sUpd = "update akumaccrue set nominal = nominal + %s\
    where id_investasi = %s" % (id_investasi, nominal)    
    runSQL(config, sUpd)
  else:
    sIns = "insert into akumaccrue values (%s, %s)" % (id_investasi, nominal)    
    runSQL(config, sIns)  
   
def ProsesAccrueDeposito(config): 
  config.BeginTransaction()
  try:  
    oP = config.CreatePObjImplProxy('Parameter')
    oP.key = 'JUMLAH_HARI_SETAHUN'
    nhari = oP.numeric_value
    oP.key = 'ACCRUE_PREV'
    last_acc_date = oP.varchar_value
    last_d = int(last_acc_date[:2])
    oP.key = 'ACCRUE_NOW'
    acc_date = oP.varchar_value
    d = int(acc_date[:2])
    n = d - last_d
    
    sSQL = "select * from investasi i, deposito d \
    where i.id_investasi = d.id_investasi and \
    status = 'T'"
    rSQL = config.CreateSQL(sSQL).RawResult
    rSQL.First()
    while not rSQL.Eof:
      rate = rSQL.equivalent_rate or 0.0
      nom_pokok = rSQL.nominal_pembukaan or 0.0

      accrue = HitungAccrue(config, rate, nom_pokok, nhari, n)
      UpdatePosisiReturn(config, accrue, acc_date, 'D')
      UpdatePosisiReturnDeposito(config, accrue)
      InsertHistoriAccrue(config, acc_date, rSQL.id_investasi, accrue)
      UpdateAkumAccrue(config, rSQL.id_investasi, accrue)
      
      print rSQL.id_investasi, accrue
      rSQL.Next() 
      
    config.Commit()
  except:
    config.Rollback()
    raise str(sys.exc_info()[1])

def ProsesAccrueObligasi(config): 
  config.BeginTransaction()
  try:  
    oP = config.CreatePObjImplProxy('Parameter')
    oP.key = 'JUMLAH_HARI_SETAHUN'
    nhari = oP.numeric_value
    oP.key = 'ACCRUE_PREV'
    last_acc_date = oP.varchar_value
    last_d = int(last_acc_date[:2])
    oP.key = 'ACCRUE_NOW'
    acc_date = oP.varchar_value
    d = int(acc_date[:2])
    n = d - last_d
    
    sSQL = "select *, DATEDIFF(day, GETDATE(), TGL_JATUH_TEMPO) as nhari  \
    from investasi i, obligasi o \
    where i.id_investasi = o.id_investasi and \
    status = 'T'"
    rSQL = config.CreateSQL(sSQL).RawResult
    rSQL.First()
    while not rSQL.Eof:
      rate = rSQL.er or 0.0
      nom_pokok = rSQL.nominal_pembukaan or 0.0
      nom_pari = rSQL.harga_pari or 0.0
      tgl_jt = rSQL.tgl_jatuh_tempo

      accrue = HitungAccrue(config, rate, nom_pokok, nhari, n)
      nhari = rSQL.nhari
      spi_pari = HitungSPI(config, nom_pokok, nom_pari, rSQL.nhari)
      
      UpdatePosisiReturn(config, accrue + spi_pari, acc_date, 'O')
      UpdatePosisiReturnObligasi(config, accrue + spi_pari)
      InsertHistoriAccrue(config, acc_date, rSQL.id_investasi, accrue + spi_pari)
      UpdateAkumAccrue(config, rSQL.id_investasi, accrue + spi_pari)
      
      print rSQL.id_investasi, accrue, spi_pari
      rSQL.Next() 
      
    config.Commit()
  except:
    config.Rollback()
    raise str(sys.exc_info()[1])

def UpdateParameter(config): 
  config.BeginTransaction()
  try:  
    oP = config.CreatePObjImplProxy('Parameter')
    oP.key = 'ACCRUE_NOW'
    acc_date = oP.varchar_value
    d = int(acc_date[:2]) + 1
    oP.varchar_value = string.zfill(d,2) + acc_date[2:]
    oP.key = 'ACCRUE_PREV'
    oP.varchar_value = acc_date

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
  ProsesAccrueDeposito(config)
  ProsesAccrueObligasi(config)
  UpdateParameter(config)
  
    
