import string, sys
sys.path.append('c:/dafapp/dplk07/scripts/transaksi')

import AuthorizeTransaksi

def FormEndSetData(uideflist, uiname, objdata):
  config = uideflist.config
  uipTransaksi = uideflist.uipTransaksi
  uipNasabah = uideflist.uipNasabah
  uipRWU = uideflist.uipRekeningWU
  
  userID = config.SecurityContext.UserID
  recTransaksi = uipTransaksi.Dataset.GetRecord(0)
  recRWU = uipRWU.Dataset.AddRecord()
  
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

  #set data rekening Wasiat Ummat
  sSQL = 'select no_polis,tgl_akseptasi,tgl_berakhir,besar_premi ' \
    'from RekeningWasiatUmmat where no_peserta = \'%s\'' % (recTransaksi.no_peserta)
  rSQL = config.CreateSQL(sSQL).RawResult

  if rSQL.Eof:
    #data peserta Wasiat Ummat tidak ditemukan
    recRWU.no_polis = 'Data tidak ditemukan!!!'
    recRWU.tgl_akseptasi = None
    recRWU.tgl_berakhir = None
    recRWU.besar_premi = 0.0
  else:
    recRWU.no_polis = rSQL.no_polis
    recRWU.tgl_akseptasi = rSQL.tgl_akseptasi
    recRWU.tgl_berakhir = rSQL.tgl_berakhir
    recRWU.besar_premi = rSQL.besar_premi

  return 0

def FormGeneralProcessData(uideflist, data):
  config = uideflist.Config
  rec = data.uipTransaksi.GetRecord(0)

  try:
    #authorize transaksi
    dh = AuthorizeTransaksi.AuthorizeOperation(config, 'TitipanPremi', \
      rec.ID_Transaksi, 'A')

  except:
    raise Exception, '\nProses Error' +  str(sys.exc_info()[1])

  return 0
