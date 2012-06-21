import string, sys
sys.path.append('c:/dafapp/dplk07/scripts/transaksi')
sys.path.append('c:/dafapp/dplk07/script_modules')

import AuthorizeTransaksi, transaksiapi

def FormEndSetData(uideflist, uiname, objdata):
  config = uideflist.config
  uipTransaksi = uideflist.uipTransaksi
  uipNasabah = uideflist.uipNasabah
  
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

  #set data nasabah DPLK
  recNasabah = uipNasabah.Dataset.AddRecord()
  oN = config.CreatePObjImplProxy('NasabahDPLK')
  oN.Key = recTransaksi.no_peserta

  recNasabah.nama_lengkap = oN.nama_lengkap
  recNasabah.alamat_jalan = oN.alamat_jalan
  recNasabah.alamat_rtrw = oN.alamat_rtrw
  recNasabah.alamat_kelurahan = oN.alamat_kelurahan
  recNasabah.alamat_kecamatan = oN.alamat_kecamatan
  recNasabah.alamat_kota = oN.alamat_kota
  recNasabah.alamat_kode_pos = oN.alamat_kode_pos

  return 0

def FormGeneralProcessData(uideflist, data):
  config = uideflist.Config
  rec = data.uipTransaksi.GetRecord(0)

  transaksiapi.CekBatasTarikMinPHK(config, rec.ID_Transaksi)
  transaksiapi.CekBatasTarikMaxPHK(config, rec.ID_Transaksi)

  try:
    #authorize transaksi
    dh = AuthorizeTransaksi.AuthorizeOperation(config, 'PenarikanDanaPHK', \
      rec.ID_Transaksi, 'A')

  except:
    raise '\nProses Error', str(sys.exc_info()[1])

  return 0

