import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
sys.path.append('c:/dafapp/dplk07/scripts/transaksi')

import moduleapi, AuthorizeTransaksi

def CreateNasabahDPLK(config, oRegisterNasabahRekening):
  oNasabahDPLK = config.CreatePObject('NasabahDPLK')
  oNasabahDPLK.no_peserta = oRegisterNasabahRekening.no_peserta
  oNasabahDPLK.no_referensi = oRegisterNasabahRekening.no_referensi
  oNasabahDPLK.no_identitas_diri = oRegisterNasabahRekening.no_identitas_diri
  oNasabahDPLK.nama_lengkap = oRegisterNasabahRekening.nama_lengkap
  oNasabahDPLK.nama_perusahaan = oRegisterNasabahRekening.nama_perusahaan
  oNasabahDPLK.NPWP = oRegisterNasabahRekening.NPWP
  oNasabahDPLK.dplklain = oRegisterNasabahRekening.dplklain

  oNasabahDPLK.pekerjaan = oRegisterNasabahRekening.pekerjaan
  oNasabahDPLK.alamat_kantor_jalan = oRegisterNasabahRekening.alamat_kantor_jalan
  oNasabahDPLK.alamat_kantor_kelurahan = oRegisterNasabahRekening.alamat_kantor_kelurahan
  oNasabahDPLK.alamat_kantor_kecamatan = oRegisterNasabahRekening.alamat_kantor_kecamatan
  oNasabahDPLK.alamat_kantor_kota = oRegisterNasabahRekening.alamat_kantor_kota
  oNasabahDPLK.alamat_kantor_kode_pos = oRegisterNasabahRekening.alamat_kantor_kode_pos
  oNasabahDPLK.alamat_kantor_telepon = oRegisterNasabahRekening.alamat_kantor_telepon
  oNasabahDPLK.alamat_kantor_telepon2 = oRegisterNasabahRekening.alamat_kantor_telepon2
  oNasabahDPLK.alamat_kantor_propinsi = oRegisterNasabahRekening.alamat_kantor_propinsi

  oNasabahDPLK.tanggal_lahir = moduleapi.DateTimeTupleToFloat(config, oRegisterNasabahRekening.tanggal_lahir)
  oNasabahDPLK.tempat_lahir = oRegisterNasabahRekening.tempat_lahir
  oNasabahDPLK.jenis_kelamin = oRegisterNasabahRekening.jenis_kelamin
  oNasabahDPLK.no_identitas_diri = oRegisterNasabahRekening.no_identitas_diri

  oNasabahDPLK.LJenisUsaha = oRegisterNasabahRekening.LJenisUsaha
  oNasabahDPLK.LKepemilikan = oRegisterNasabahRekening.LKepemilikan
  oNasabahDPLK.LDaerahAsal = oRegisterNasabahRekening.LDaerahAsal
  oNasabahDPLK.LKelompok = oRegisterNasabahRekening.LKelompok
  oNasabahDPLK.LNasabahDPLKCorporate = oRegisterNasabahRekening.LNasabahDPLKCorporate
  oNasabahDPLK.LLDPLain = oRegisterNasabahRekening.LLDPLain

  oNasabahDPLK.alamat_jalan = oRegisterNasabahRekening.alamat_jalan
  oNasabahDPLK.alamat_jalan2 = oRegisterNasabahRekening.alamat_jalan2
  oNasabahDPLK.alamat_rtrw = oRegisterNasabahRekening.alamat_rtrw
  oNasabahDPLK.alamat_kelurahan = oRegisterNasabahRekening.alamat_kelurahan
  oNasabahDPLK.alamat_kecamatan = oRegisterNasabahRekening.alamat_kecamatan
  oNasabahDPLK.alamat_kota = oRegisterNasabahRekening.alamat_kota
  oNasabahDPLK.alamat_propinsi = oRegisterNasabahRekening.alamat_propinsi
  oNasabahDPLK.alamat_kode_pos = oRegisterNasabahRekening.alamat_kode_pos
  oNasabahDPLK.alamat_telepon = oRegisterNasabahRekening.alamat_telepon
  oNasabahDPLK.alamat_telepon2 = oRegisterNasabahRekening.alamat_telepon2
  oNasabahDPLK.alamat_email = oRegisterNasabahRekening.alamat_email

  oNasabahDPLK.alamat_surat_jalan = oRegisterNasabahRekening.alamat_surat_jalan
  oNasabahDPLK.alamat_surat_jalan2 = oRegisterNasabahRekening.alamat_surat_jalan2
  oNasabahDPLK.alamat_surat_rtrw = oRegisterNasabahRekening.alamat_surat_rtrw
  oNasabahDPLK.alamat_surat_kelurahan = oRegisterNasabahRekening.alamat_surat_kelurahan
  oNasabahDPLK.alamat_surat_kecamatan = oRegisterNasabahRekening.alamat_surat_kecamatan
  oNasabahDPLK.alamat_surat_kota = oRegisterNasabahRekening.alamat_surat_kota
  oNasabahDPLK.alamat_surat_propinsi = oRegisterNasabahRekening.alamat_surat_propinsi
  oNasabahDPLK.alamat_surat_kode_pos = oRegisterNasabahRekening.alamat_surat_kode_pos
  oNasabahDPLK.alamat_surat_telepon = oRegisterNasabahRekening.alamat_surat_telepon
  oNasabahDPLK.alamat_surat_telepon2 = oRegisterNasabahRekening.alamat_surat_telepon2

  oNasabahDPLK.isPesertaPengalihan = oRegisterNasabahRekening.isPesertaPengalihan
  oNasabahDPLK.keterangan = oRegisterNasabahRekening.keterangan
  oNasabahDPLK.tgl_registrasi = moduleapi.DateTimeTupleToFloat(config, oRegisterNasabahRekening.tanggal_register)
  oNasabahDPLK.user_id = oRegisterNasabahRekening.user_id
  oNasabahDPLK.terminal_id = oRegisterNasabahRekening.terminal_id
  oNasabahDPLK.auth_user_id = config.SecurityContext.userid
  oNasabahDPLK.last_terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oNasabahDPLK.last_update = config.ModDateTime.Now()
  oNasabahDPLK.isCommitted = 'T'
  oNasabahDPLK.operation_code = 'F'

  return oNasabahDPLK

def CreateRekeningDPLK(config, oRegisterNasabahRekening):
  oRekeningDPLK = config.CreatePObject('RekeningDPLK')
  oRekeningDPLK.no_peserta = oRegisterNasabahRekening.no_peserta
  oRekeningDPLK.akum_dana_pengembangan = 0.0
  oRekeningDPLK.akum_dana_peralihan = 0.0
  oRekeningDPLK.akum_dana_iuran_pk = 0.0
  oRekeningDPLK.akum_dana_iuran_pst = 0.0
  oRekeningDPLK.iuran_pk = oRegisterNasabahRekening.iuran_pk
  oRekeningDPLK.iuran_pst = oRegisterNasabahRekening.iuran_pst
  oRekeningDPLK.nilai_bayar_anuitas = 0.0
  oRekeningDPLK.SRR_AKHIR = 0.0

  oRekeningDPLK.status_anuitas = 'F'
  oRekeningDPLK.status_autodebet = 'F'
  oRekeningDPLK.STATUS_BIAYA_DAFTAR = oRegisterNasabahRekening.STATUS_BIAYA_DAFTAR
  oRekeningDPLK.STATUS_DPLK = 'A'
  oRekeningDPLK.status_komisi = ''
  oRekeningDPLK.status_wasiat_ummat = 'F'
  oRekeningDPLK.sumber_dana = oRegisterNasabahRekening.sumber_dana
##  oRekeningDPLK.tgl_akseptasi =
##  oRekeningDPLK.tgl_bayar_anuitas =

  oRekeningDPLK.usia_pensiun = oRegisterNasabahRekening.usia_pensiun
  tgl_pensiun = moduleapi.AddYearToDateTuple(config, oRegisterNasabahRekening.tanggal_lahir, oRegisterNasabahRekening.usia_pensiun) 
  tgl_pensiun_dipercepat = moduleapi.AddYearToDateTuple(config, oRegisterNasabahRekening.tanggal_lahir, oRegisterNasabahRekening.usia_pensiun - 10) 
  oRekeningDPLK.tgl_pensiun = moduleapi.DateTimeTupleToFloat(config, tgl_pensiun)
  oRekeningDPLK.tgl_pensiun_dipercepat = moduleapi.DateTimeTupleToFloat(config, tgl_pensiun_dipercepat)
  oRekeningDPLK.tgl_srr_akhir = moduleapi.DateTimeTupleToFloat(config, oRegisterNasabahRekening.tanggal_register)

##  oRekeningDPLK.TGL_TUTUP =

  #oRekeningDPLK.WASIAT_UMMAT = oRegisterNasabahRekening.WASIAT_UMMAT

  oRekeningDPLK.kirim_statemen = oRegisterNasabahRekening.kirim_statemen
  oRekeningDPLK.kode_cab_daftar = oRegisterNasabahRekening.kode_cab_daftar #config.SecurityContext.GetUserInfo()[4]
  oRekeningDPLK.LPaketInvestasi = oRegisterNasabahRekening.LPaketInvestasi

  oRekeningDPLK.keterangan = oRegisterNasabahRekening.keterangan
  oRekeningDPLK.user_id = oRegisterNasabahRekening.user_id
  oRekeningDPLK.auth_user_id = config.SecurityContext.userid
  oRekeningDPLK.last_terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oRekeningDPLK.last_update = config.ModDateTime.Now()
  oRekeningDPLK.operation_code = 'F'

  return oRekeningDPLK

def CreateAllAhliWaris(config, oRegisterNasabahRekening, oNasabahDPLK):
  Ls_RegNRAhliWaris = oRegisterNasabahRekening.Ls_RegNRAhliWaris
  Ls_RegNRAhliWaris.First()
  while not Ls_RegNRAhliWaris.EndOfList:
    oRegNRAhliWaris = Ls_RegNRAhliWaris.CurrentElement

    oAhliWaris = config.CreatePObject('AhliWaris')
    oAhliWaris.LNasabahDPLK = oNasabahDPLK
    oAhliWaris.nama_lengkap = oRegNRAhliWaris.nama_lengkap
    oAhliWaris.nomor_urut_prioritas = oRegNRAhliWaris.nomor_urut_prioritas
    oAhliWaris.status_ahli_waris = oRegNRAhliWaris.status_ahli_waris

    if oRegNRAhliWaris.tanggal_lahir != None:
      oAhliWaris.tanggal_lahir = moduleapi.DateTimeTupleToFloat(config, oRegNRAhliWaris.tanggal_lahir)

    oAhliWaris.jenis_kelamin = oRegNRAhliWaris.jenis_kelamin
    oAhliWaris.keterangan = oRegNRAhliWaris.keterangan
    oAhliWaris.hubungan_keluarga = oRegNRAhliWaris.hubungan_keluarga

    Ls_RegNRAhliWaris.Next()

#def CreateRekeningAutoDebet(config, oRegisterNasabahRekening, oRekeningDPLK):
#  oRekeningAutoDebet = config.CreatePObject('RekeningAutoDebet')
#  oRekeningAutoDebet.no_rekening = oRegisterNasabahRekening.no_rek_autodebet
#  oRekeningAutoDebet.nama_rekening = oRegisterNasabahRekening.nama_rek_autodebet
#  oRekeningAutoDebet.tanggal_autodebet = oRegisterNasabahRekening.tanggal_autodebet
#  oRekeningAutoDebet.LRekeningDPLK = oRekeningDPLK
#
#  return oRekeningAutoDebet

def CreateRekeningAutoDebet(config, oRegisterNasabahRekening, oRegisterDPLK):
  oRegisterAutoDebet = config.CreatePObject('RegisterAutoDebet')
  oRegisterAutoDebet.user_id = oRegisterNasabahRekening.user_id
  oRegisterAutoDebet.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oRegisterAutoDebet.tanggal_register = config.Now()
  oRegisterAutoDebet.no_referensi = oRegisterNasabahRekening.no_referensi
  oRegisterAutoDebet.no_peserta = oRegisterNasabahRekening.no_peserta
  oRegisterAutoDebet.no_rekening = oRegisterNasabahRekening.no_rek_autodebet
  oRegisterAutoDebet.nama_rekening = oRegisterNasabahRekening.nama_rek_autodebet
  oRegisterAutoDebet.tanggal_autodebet = oRegisterNasabahRekening.tanggal_autodebet
  oRegisterAutoDebet.jenis_transaksi = 'R'

  return oRegisterAutoDebet

#def CreateRekeningWasiatUmmat(config, oRegisterNasabahRekening, parameter):
#  oRekeningWasiatUmmat = config.CreatePObject('RekeningWasiatUmmat')
#  oRekeningWasiatUmmat.no_peserta = oRegisterNasabahRekening.no_peserta
#  oRekeningWasiatUmmat.user_id = oRegisterNasabahRekening.user_id
#  oRekeningWasiatUmmat.auth_user_id = config.SecurityContext.userid
#  oRekeningWasiatUmmat.no_polis = parameter.FirstRecord.no_polis
#  oRekeningWasiatUmmat.besar_premi = parameter.FirstRecord.besar_premi
#  oRekeningWasiatUmmat.tgl_akseptasi = parameter.FirstRecord.tgl_akseptasi

def CreateRegisterWasiatUmmat(config, oRegisterNasabahRekening):
  oRegisterWasiatUmmat = config.CreatePObject('RegisterWasiatUmmat')
  oRegisterWasiatUmmat.no_peserta = oRegisterNasabahRekening.no_peserta
  oRegisterWasiatUmmat.no_referensi = oRegisterNasabahRekening.no_referensi
  oRegisterWasiatUmmat.user_id = oRegisterNasabahRekening.user_id
  oRegisterWasiatUmmat.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oRegisterWasiatUmmat.tanggal_register = config.Now()
  oRegisterWasiatUmmat.jenis_transaksi = 'R'

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  id = parameter.FirstRecord.id

  oRegisterNasabahRekening = config.CreatePObjImplProxy('RegisterNasabahRekening')
  oRegisterNasabahRekening.Key = id
  
  byPassBiayaDaftar = 1
  if oRegisterNasabahRekening.isRegisteredByAdmin == 'F':
    #registrasi bukan oleh admin, cek status biaya pendaftaran
    byPassBiayaDaftar = 0
    if oRegisterNasabahRekening.STATUS_BIAYA_DAFTAR != 'T':
      raise '\n\nPERINGATAN','Pembayaran Biaya Pendaftaran belum dilakukan.'

  config.BeginTransaction()
  try:
    oNasabahDPLK = CreateNasabahDPLK(config, oRegisterNasabahRekening)
    oRekeningDPLK = CreateRekeningDPLK(config, oRegisterNasabahRekening)

    CreateAllAhliWaris(config, oRegisterNasabahRekening, oNasabahDPLK)
    if oRegisterNasabahRekening.auto_debet == 'T':
      CreateRekeningAutoDebet(config, oRegisterNasabahRekening, oRekeningDPLK)
    if oRegisterNasabahRekening.wasiat_ummat == 'T':
      CreateRegisterWasiatUmmat(config, oRegisterNasabahRekening)

    if not byPassBiayaDaftar: 
      #otorisasi 'setuju' untuk Iuran Pendaftaran dan Iuran Peserta pertama
      #AKAN DIPROSES LEWAT REKONSILIASI CORE BANKING DAN DPLK LIABILITIES
      #AuthorizeTransaksi.ApproveOperation(config, 'IuranPendaftaran', \
      #  oRegisterNasabahRekening.ID_Transaksi_IuranPendaftaran)    
      #AuthorizeTransaksi.ApproveOperation(config, 'IuranPeserta', \
      #  oRegisterNasabahRekening.ID_Transaksi_IuranPeserta)
      pass
      
    #hapus objek Register Nasabah Rekening
    oRegisterNasabahRekening.Ls_RegNRAhliWaris.DeleteAllPObjs()
    oRegisterNasabahRekening.Delete()

    config.Commit()
  except:
    config.Rollback()
    raise

  return 1
