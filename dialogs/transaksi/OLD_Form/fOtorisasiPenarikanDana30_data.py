import string, sys
sys.path.append('c:/dafapp/dplk/scripts/transaksi')
sys.path.append('c:/dafapp/dplk/script_modules')

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

  transaksiapi.CekRentangWaktuPenarikan(config, rec.no_peserta)
  transaksiapi.CekSaldoIuranMin(config, rec.no_peserta)

  try:
    #authorize transaksi
    dh = AuthorizeTransaksi.AuthorizeOperation(config, 'PenarikanDanaNormal', \
      rec.ID_Transaksi, 'A')

  except:
    raise Exception, '\nProses Error' +  str(sys.exc_info()[1])

  return 0

