import string, sys
sys.path.append('c:/dafapp/dplk07/scripts/transaksi')

import AuthorizeTransaksi

def FormEndSetData(uideflist, uiname, objdata):
  config = uideflist.config
  uipTransaksi = uideflist.uipTransaksi

  userID = config.SecurityContext.UserID
  recTransaksi = uipTransaksi.Dataset.GetRecord(0)

  #kode ini dikomentari dulu, save for the future
  #if recTransaksi.isCommitted == 'F':
    #belum diotorisasi, set field Transaksi
    #recTransaksi.user_id_auth = userID
    #recTransaksi.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]
    #recTransaksi.tgl_otorisasi = config.Now()

  #set branch code batch transaksi
  recTransaksi.TB_BranchCode = recTransaksi.GetFieldByName('LTransactionBatch.branch_code')

  return 0

def FormGeneralProcessData(uideflist, data):
  config = uideflist.Config
  rec = data.uipTransaksi.GetRecord(0)

  try:
    #authorize transaksi
    dh = AuthorizeTransaksi.AuthorizeOperation(config, 'TransaksiPremiManual', \
      rec.ID_Transaksi, 'A')

  except:
    raise Exception, '\nProses Error' +  str(sys.exc_info()[1])

  return 0
