import string, sys
sys.path.append('c:/dafapp/dplk07/script_modules')

import transaksiapi

def FormEndSetData(uideflist, uiname, objdata):
  config = uideflist.config
  uipTransaksi = uideflist.uipTransaksi

  recTransaksi = uipTransaksi.Dataset.AddRecord()

  #set field Data Transaksi
  recTransaksi.mutasi_iuran_pk = recTransaksi.mutasi_iuran_pst = \
  recTransaksi.mutasi_pengembangan = recTransaksi.mutasi_peralihan = 0.0

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
  recN = data.uipNasabah.GetRecord(0)
  
  try:
    o = config.CreatePObject('TransaksiDPLKManual')

    tgl_transaksi = config.ModDateTime.DecodeDate(rec.tgl_transaksi)
    o.tgl_transaksi = config.ModDateTime.EncodeDate(tgl_transaksi[0], \
        tgl_transaksi[1], tgl_transaksi[2])

    o.no_peserta = recN.no_peserta
    o.kode_transaksi_manual = rec.GetFieldByName('LJenisTransaksiManual.kode_jenis_transaksi')
    o.keterangan = rec.keterangan
    o.mutasi_iuran_pk = rec.mutasi_iuran_pk
    o.mutasi_iuran_pst = rec.mutasi_iuran_pst
    o.mutasi_pengembangan = rec.mutasi_pengembangan
    o.mutasi_peralihan = rec.mutasi_peralihan
    o.ID_TransactionBatch = rec.GetFieldByName('LTransactionBatch.ID_TransactionBatch')
    o.branch_code = rec.TB_BranchCode

    #assign nilai yang tidak tercantum di form
    o.isCommitted = 'F'
    o.user_id = config.SecurityContext.UserID
    o.terminal_id = config.SecurityContext.GetSessionInfo()[1]
    o.tgl_sistem = config.Now()

    #assign kode paket investasi current
    transaksiapi.SetPaketInvestasi(config, o)

  except:
    raise '\nProses Error', str(sys.exc_info()[1])

  return 0
