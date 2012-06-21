import string, sys
sys.path.append('c:/dafapp/dplk07/scripts/transaksi')

import AuthorizeTransaksi

def FormEndSetData(uideflist, uiname, objdata):
  config = uideflist.config
  uipTransaksi = uideflist.uipTransaksi
  uipRekening = uideflist.uipRekening
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
  
  #cek apakah peserta sudah tercatat sebagai nasabah
  if not oN.IsNull:
    #peserta sudah tercatat sebagai nasabah
    recNasabah.nama_lengkap = oN.nama_lengkap
    recNasabah.alamat_jalan = oN.alamat_jalan
    recNasabah.alamat_rtrw = oN.alamat_rtrw
    recNasabah.alamat_kelurahan = oN.alamat_kelurahan
    recNasabah.alamat_kecamatan = oN.alamat_kecamatan
    recNasabah.alamat_kota = oN.alamat_kota
    recNasabah.alamat_kode_pos = oN.alamat_kode_pos
  else:
    #peserta belum terotorisasi sbg nasabah, namun sudah membayar pendaftaran
    raise '\nINFORMASI','Iuran Peserta pertama ini milik calon peserta %s yang statusnya '\
      'belum terotorisasi sebagai peserta DPLK. Iuran Iuran Peserta pertama secara otomatis akan '\
      'terotorisasi bersamaan dengan otorisasi calon peserta tersebut.'\
      % (recTransaksi.no_peserta)

  #set Rekening DPLK Nasabah
  recRekening = uipRekening.Dataset.AddRecord()
  oR = config.CreatePObjImplProxy('RekeningDPLK')
  oR.Key = recTransaksi.no_peserta

  recRekening.iuran_pk = oR.iuran_pk
  recRekening.iuran_pst = oR.iuran_pst
  recRekening.status_wasiat_ummat = oR.status_wasiat_ummat

  return 0

def FormGeneralProcessData(uideflist, data):
  config = uideflist.Config
  rec = data.uipTransaksi.GetRecord(0)

  try:
    #authorize transaksi
    dh = AuthorizeTransaksi.AuthorizeOperation(config, 'IuranPeserta', \
      rec.ID_Transaksi, 'A')

  except:
    raise '\nProses Error', str(sys.exc_info()[1])

  return 0
