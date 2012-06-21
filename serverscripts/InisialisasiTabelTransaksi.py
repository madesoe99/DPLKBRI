import sys, DBAppFramework, dafdb

# MAIN MODULE CALLER -----------------------------------------------------------

config = DBAppFramework.GetConfig()

#setting old DPLK DB connection 
con = dafdb.getDBConnection('c:/dafapp/dplk/default.cfg','PRIMARY_DATABASE')
con.Connect()

try:  
  try:    
    ## STEP 0 ##
    print 'STEP 0: add column isDeleted to Transaksi_DPLK table'
    con.BeginTransaction()
    con.ExecuteQuery('alter table Transaksi_DPLK add isDeleted char(1)')
    con.ExecuteQuery('alter table Transaksi_DPLK add Operator_Added varchar(5)')
    con.Commit()
  except:
    con.Rollback()
    raise
    
  try:
    ## STEP 1 ##
    print 'STEP 1: update field isDeleted=\'T\' utk Transaksi_DPLK yang sudah terhapus'
    
    #ambil data yang ada di tabel Transaksi_DPLK_Deleted
    q = con.GetQuery('select ID_TRANSAKSI from TRANSAKSI_DPLK_DELETED')
    
    con.BeginTransaction()
    while not q.Eof():
      #update field isDeleted='T'
      res = con.ExecuteQuery('update Transaksi_DPLK set isDeleted=\'T\' \
        where ID_Transaksi=%d' % (q.GetFieldValue('ID_TRANSAKSI')))
      
      print str(q.GetFieldValue('ID_TRANSAKSI'))      
    
      q.Next()
    
    con.Commit()
  except:
    con.Rollback()
    raise
  
  try:
    ## STEP 2 ##
    print 'STEP 2: update field Operator_Added dengan value dari field Operator, \
          jika NULL diberi value \'ADMIN\''        
    con.BeginTransaction()
    
    #update field Operator_Added = Operator, bila field Operator tidak NULL
    res = con.ExecuteQuery('update Transaksi_DPLK set Operator_Added=TRIM(Operator) \
      where Operator is not null')
    #update field Operator_Added = ADMIN, bila field Operator = NULL
    res = con.ExecuteQuery('update Transaksi_DPLK set Operator_Added=\'ADMIN\' \
      where Operator is null')
    #update field Operator_Added = ADMIN, bila field Operator_Added = NULL
    #antisipasi jika hasil TRIM menghasilkan kosong/NULL
    res = con.ExecuteQuery('update Transaksi_DPLK set Operator_Added=\'ADMIN\' \
      where Operator_Added is null')
      
    con.Commit()
  except:
    con.Rollback()
    raise
  
  print 'Sukses menginisialisasi tabel Transaksi_DPLK!!!'
    
  con.Disconnect()
except:
  raise
