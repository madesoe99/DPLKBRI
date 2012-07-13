import string, sys

def FormGeneralSetData(uideflist, uiname, objdata):
  config = uideflist.config
  uipTransaksi = uideflist.uipTransaksi

  recTransaksi = uipTransaksi.Dataset.AddRecord()

  #set field panel Data Transaksi
  recTransaksi.isDebet = 'F'
  recTransaksi.mutasi_premi = 0.0

  #setting parameter Default
  uipParameter = uideflist.uipParameter
  recParameter = uipParameter.Dataset.AddRecord()

  oParameter = config.CreatePObjImplProxy('Parameter')
  oParameter.Key = 'PRESISI_ANGKA_FLOAT'

  recParameter.PRESISI_ANGKA_FLOAT = oParameter.Numeric_Value

  return 0
  
def FormGeneralProcessData(uideflist, data):
  config = uideflist.Config
  rec = data.uipTransaksi.GetRecord(0)
  
  try:
    o = config.CreatePObject('TransaksiPremiManual')

    tgl_transaksi = config.ModDateTime.DecodeDate(rec.tgl_transaksi)
    o.tgl_transaksi = config.ModDateTime.EncodeDate(tgl_transaksi[0], \
        tgl_transaksi[1], tgl_transaksi[2])

    o.keterangan = rec.keterangan
    o.isDebet = rec.isDebet
    o.mutasi_premi = rec.mutasi_premi
    o.ID_TransactionBatch = rec.GetFieldByName('LTransactionBatch.ID_TransactionBatch')
    o.branch_code = rec.TB_BranchCode

    #assign nilai yang tidak tercantum di form
    o.isCommitted = 'F'
    o.user_id = config.SecurityContext.UserID
    o.terminal_id = config.SecurityContext.GetSessionInfo()[1]
    o.tgl_sistem = config.Now()
  except:
    raise Exception, '\nProses Error' +  str(sys.exc_info()[1])

  return 0
