import sys, string
sys.path.append('c:/dafapp/dplk07/script_modules')

import transaksiapi

def FormEndSetData(uideflist, uiname, objdata):
  config = uideflist.config

  #set field Transaksi
  uipTransaksi = uideflist.uipTransaksi
  recTransaksi = uipTransaksi.Dataset.AddRecord()
  recTransaksi.saldo_iuran_pk = recTransaksi.saldo_iuran_pst = \
    recTransaksi.saldo_pengembangan = recTransaksi.saldo_peralihan = 0.0
  #batch transaksi diset lewat FormShow saja!
  
  return 0
  
def FormGeneralProcessData(uideflist, data):
  config = uideflist.Config
  rec = data.uipTransaksi.GetRecord(0)
  recNasabah = data.uipNasabah.GetRecord(0)

  try:
    #buat objek PengalihanDariDPLKLain baru
    oP = config.CreatePObject('PengalihanDariDPLKLain')

    tgl = config.ModDateTime.DecodeDate(rec.tgl_transaksi)
    oP.tgl_transaksi = config.ModDateTime.EncodeDate(tgl[0], tgl[1], tgl[2])

    oP.keterangan = rec.keterangan
    oP.kode_dp = rec.GetFieldByName('LLDP.kode_dp')

    #tidak ada pengesetan nomor DPLK untuk pengalihan dari DPK Lain
    #oP.no_dplk_lain = rec.no_dplk_lain

    oP.saldo_iuran_pk = rec.saldo_iuran_pk
    oP.saldo_iuran_pst = rec.saldo_iuran_pst
    oP.saldo_pengembangan = rec.saldo_pengembangan
    oP.saldo_peralihan = rec.saldo_peralihan

    #set field parent (TransaksiDPLK)
    oP.mutasi_iuran_pk = oP.mutasi_iuran_pst = oP.mutasi_pengembangan = 0.0
    oP.mutasi_peralihan = oP.saldo_iuran_pk + oP.saldo_iuran_pst + \
      oP.saldo_pengembangan + oP.saldo_peralihan

    oP.no_peserta = recNasabah.no_peserta
    oP.kode_jenis_transaksi = 'P'
    oP.ID_TransactionBatch = rec.GetFieldByName('LTransactionBatch.ID_TransactionBatch')

    #set status
    oP.isCommitted = 'F'
    oP.user_id = config.SecurityContext.UserID
    oP.terminal_id = config.SecurityContext.GetSessionInfo()[1]
    oP.tgl_sistem = config.Now()
    oP.branch_code = rec.TB_BranchCode

    #assign kode paket investasi current
    transaksiapi.SetPaketInvestasi(config, oP)

  except:
    raise Exception, '\nProses Error' +  str(sys.exc_info()[1])

  return 0
