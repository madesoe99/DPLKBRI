import sys, string, time
import com.ihsan.util.modman as modman
import com.ihsan.foundation.appserver as appserver

modman.loadStdModules(globals(),
  [
    'moduleapi'
  ]
)

def FormOnSetDataEx(uideflist, params):
  # procedure(uideflist: TPClassUIDefList; params: TPClassUIDataPacket)
  config = uideflist.Config
  
  sSQL = 'SELECT TOP 1 no_seri_buku FROM MASTERBUKUDPLK WHERE is_reserved=\'F\' ORDER BY no_seri_buku ASC'
  rSQL = config.CreateSQL(sSQL).RawResult
  
  no_seri_buku = rSQL.no_seri_buku
  if no_seri_buku == None:  
    sSQL = 'SELECT TOP 1 no_seri_buku FROM MASTERBUKUDPLK ORDER BY no_seri_buku DESC'
    rSQL = config.CreateSQL(sSQL).RawResult
    
    lastId = rSQL.no_seri_buku
    if lastId == None:
      lastId = 0
      
    lastId = int(lastId) + 1
    no_seri_buku = '%s' % (moduleapi.MyZFill(str(lastId), 10))

    config.BeginTransaction()
    try:
      '''INSERT INTO MASTERBUKUDPLK - RESERVE NOMOR BUKU'''
      oReg = config.CreatePObject('MasterBukuDPLK')
      oReg.no_seri_buku = no_seri_buku
      oReg.kode_cabang = config.SecurityContext.GetUserInfo()[4]
      oReg.tgl_input  = config.Now()
      oReg.user_id = config.SecurityContext.userid
      oReg.status_buku = 'F'
      oReg.is_reserved = 'T'
      
      config.Commit()
    except:
      config.Rollback()
      raise Exception, '\n\n%s' % str(sys.exc_info()[1])
  else:
    sSQL = 'UPDATE MasterBukuDPLK SET is_reserved = \'T\' WHERE no_seri_buku = \'%s\'' % no_seri_buku
    rSQL = config.ExecSQL(sSQL)
    
  uipInput = uideflist.uipInput.DataSet.AddRecord()
  uipInput.nomor_buku = no_seri_buku
    

def cancelReserveNumber(config, params, returns):
  no_seri_buku = params.FirstRecord.no_seri_buku
  
  sSQL = 'UPDATE MasterBukuDPLK SET is_reserved = \'F\' WHERE no_seri_buku = \'%s\'' % no_seri_buku
  rSQL = config.ExecSQL(sSQL)

  