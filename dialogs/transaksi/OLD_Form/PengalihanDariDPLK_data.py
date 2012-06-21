import sys, string
sys.path.append('c:/dafapp/dplk07/script_modules')

import transaksiapi

def FormEndSetData(uideflist, uiname, objdata):
  config = uideflist.config

  #set field Transaksi
  uipTransaksi = uideflist.uipTransaksi
  config.SendDebugMsg('aaa')
  recTransaksi = uipTransaksi.Dataset.AddRecord()
  config.SendDebugMsg('bbb')
  recTransaksi.saldo_iuran_pk = recTransaksi.saldo_iuran_pst = \
  recTransaksi.saldo_pengembangan = recTransaksi.saldo_peralihan = 0.0
  config.SendDebugMsg('ccc')
  #batch transaksi diset lewat FormShow saja!
  
  return 0
  
def FormGeneralProcessData(uideflist, data):
  config = uideflist.Config
  rec = data.uipTransaksi.GetRecord(0)
  recNasabah = data.uipNasabah.GetRecord(0)

  try:
    sSQL = "SELECT r.kode_paket_investasi, r.proporsi, \
    p.nav, r.no_peserta \
    FROM REKENINGDPLK r, PAKETINVESTASI p\
    WHERE r.kode_paket_investasi = p.kode_paket_investasi \
    and r.nomor_rekening = '%s'\
    and r.status_dplk = 'A'" % (recNasabah.no_peserta)
    rSQL = config.CreateSQL(sSQL).RawResult
    rSQL.First()
    while not rSQL.Eof:
      #buat objek PengalihanDariDPLKLain baru
      oP = config.CreatePObject('PengalihanDariDPLKLain')

      tgl = config.ModDateTime.DecodeDate(rec.tgl_transaksi)
      oP.tgl_transaksi = config.ModDateTime.EncodeDate(tgl[0], tgl[1], tgl[2])

      oP.keterangan = rec.keterangan
      oP.kode_dp = rec.GetFieldByName('LLDP.kode_dp')
      oP.no_dplk_lain = rec.no_dplk_lain
      proporsi = rSQL.proporsi or 0.0
      
      oP.saldo_iuran_pk = rec.saldo_iuran_pk  * proporsi / 100
      oP.saldo_iuran_pst = rec.saldo_iuran_pst * proporsi / 100
      #oP.saldo_iuran_tambahan = rec.saldo_iuran_tambahan
      oP.saldo_pengembangan = rec.saldo_pengembangan * proporsi / 100
      oP.saldo_peralihan = rec.saldo_peralihan * proporsi / 100

      oP.kode_paket_investasi = rSQL.kode_paket_investasi

      #set field parent (TransaksiDPLK)
      oP.mutasi_iuran_pk = oP.saldo_iuran_pk
      oP.mutasi_iuran_pst = oP.saldo_iuran_pst + oP.saldo_pengembangan
      #oP.mutasi_iuran_tambahan = oP.saldo_iuran_tambahan
      oP.mutasi_peralihan = oP.saldo_peralihan

      oP.nav_transaksi = rSQL.nav

      oP.unit_iuran_pst = oP.mutasi_iuran_pst / oP.nav_transaksi
      oP.unit_iuran_pk = oP.mutasi_iuran_pk / oP.nav_transaksi
      #oP.unit_iuran_tambahan = oP.mutasi_iuran_tambahan / o.nav_transaksi
      oP.unit_iuran_psl = oP.mutasi_peralihan / oP.nav_transaksi
      
      oP.no_peserta = rSQL.no_peserta
      oP.kode_jenis_transaksi = 'I'
      oP.ID_TransactionBatch = rec.GetFieldByName('LTransactionBatch.ID_TransactionBatch')

      #set status
      oP.isCommitted = 'F'
      oP.user_id = config.SecurityContext.UserID
      oP.terminal_id = config.SecurityContext.GetSessionInfo()[1]
      oP.tgl_sistem = config.Now()
      oP.branch_code = rec.TB_BranchCode

      
      rSQL.Next()

  except:
    raise '\nProses Error', str(sys.exc_info()[1])

  return 0
