import sys
#sys.path.append('c:/dafapp/dplk/script_modules')
#sys.path.append('c:/dafapp/dplk/scripts/transaksi')
#import moduleapi, AuthorizeTransaksi, L_SendPeserta

import com.ihsan.foundation.appserver as appserver
import com.ihsan.util.modman as modman

# application-level modules, loaded via modman
modman.loadStdModules(globals(), 
  [
    "moduleapi",
    "scripts#transaksi.AuthorizeTransaksi"
  ]
)

def CreateNasabahDPLK(config, oRegisterNasabahRekening, oUploadCorporate): 
  oNasabahDPLK = config.CreatePObject('NasabahDPLK')
    
  oNasabahDPLK.no_peserta = oRegisterNasabahRekening.no_peserta
  oNasabahDPLK.LBranchLocation = oUploadCorporate.LBranchLocation
  #oNasabahDPLK.kode_cab_daftar = oRegisterNasabahRekening.kode_cab_daftar
  oNasabahDPLK.ibu_kandung = oRegisterNasabahRekening.ibu_kandung
  oNasabahDPLK.nama_lengkap = oRegisterNasabahRekening.nama_lengkap
  oNasabahDPLK.tempat_lahir = oRegisterNasabahRekening.tempat_lahir
  oNasabahDPLK.tanggal_lahir = moduleapi.DateTimeTupleToFloat(config, oRegisterNasabahRekening.tanggal_lahir)
  oNasabahDPLK.jenis_kelamin = oRegisterNasabahRekening.jenis_kelamin
  #oNasabahDPLK.golongan_darah = oRegisterNasabahRekening.golongan_darah
  #oNasabahDPLK.agama = oRegisterNasabahRekening.agama
  #oNasabahDPLK.pendidikan_terakhir = oRegisterNasabahRekening.pendidikan_terakhir
  oNasabahDPLK.status_perkawinan = oRegisterNasabahRekening.status_perkawinan
  #oNasabahDPLK.LDaerahAsal = oRegisterNasabahRekening.LDaerahAsal
  #oNasabahDPLK.kode_propinsi = oRegisterNasabahRekening.kode_propinsi
  #oNasabahDPLK.kewarganegaraan = oRegisterNasabahRekening.kewarganegaraan
  #oNasabahDPLK.LNegara = oRegisterNasabahRekening.LNegara
  #oNasabahDPLK.kode_negara = oRegisterNasabahRekening.kode_negara
  #oNasabahDPLK.no_identitas_diri = oRegisterNasabahRekening.no_identitas_diri
  #oNasabahDPLK.tgl_exp_identitas = oRegisterNasabahRekening.tgl_exp_identitas
  
  #oNasabahDPLK.LKelompok = oRegisterNasabahRekening.LKelompok
  #oNasabahDPLK.kode_kelompok = oRegisterNasabahRekening.kode_kelompok
  #oNasabahDPLK.alamat_email = oRegisterNasabahRekening.alamat_email
  oNasabahDPLK.NPWP = oRegisterNasabahRekening.NPWP
  #oNasabahDPLK.penghasilan_tetap = oRegisterNasabahRekening.penghasilan_tetap
  #oNasabahDPLK.penghasilan_tambahan = oRegisterNasabahRekening.penghasilan_tambahan
  #oNasabahDPLK.beneficial_owner = oRegisterNasabahRekening.beneficial_owner
  #oNasabahDPLK.LLDPLain = oRegisterNasabahRekening.LLDPLain
  #oNasabahDPLK.kode_dp = oRegisterNasabahRekening.kode_dp
  
  #oNasabahDPLK.nama_orang_tua = oRegisterNasabahRekening.nama_orang_tua
  #oNasabahDPLK.LJenisPekerjaanOrtu = oRegisterNasabahRekening.LJenisPekerjaanOrtu
  #oNasabahDPLK.LJenisPekerjaanDetailOrtu = oRegisterNasabahRekening.LJenisPekerjaanDetailOrtu
  #oNasabahDPLK.LJenisUsahaOrtu = oRegisterNasabahRekening.LJenisUsahaOrtu
  #oNasabahDPLK.nama_perusahaan_ortu = oRegisterNasabahRekening.nama_perusahaan_ortu
  #oNasabahDPLK.penghasilan_orang_tua = oRegisterNasabahRekening.penghasilan_orang_tua
  
  oNasabahDPLK.alamat_jalan = oRegisterNasabahRekening.alamat_jalan
  #oNasabahDPLK.alamat_jalan2 = oRegisterNasabahRekening.alamat_jalan2
  oNasabahDPLK.alamat_rtrw = oRegisterNasabahRekening.alamat_rtrw
  #oNasabahDPLK.alamat_kelurahan = oRegisterNasabahRekening.alamat_kelurahan
  #oNasabahDPLK.alamat_kecamatan = oRegisterNasabahRekening.alamat_kecamatan
  #oNasabahDPLK.alamat_kota = oRegisterNasabahRekening.alamat_kota
  #oNasabahDPLK.alamat_propinsi = oRegisterNasabahRekening.alamat_propinsi
  #oNasabahDPLK.LATKecamatan = oRegisterNasabahRekening.LATKecamatan
  #oNasabahDPLK.LATKota = oRegisterNasabahRekening.LATKota
  oNasabahDPLK.alamat_kota_kode = oRegisterNasabahRekening.kode_kota
  #oNasabahDPLK.LATPropinsi = oRegisterNasabahRekening.LATPropinsi
  oNasabahDPLK.alamat_propinsi_kode = oRegisterNasabahRekening.kode_propinsi
  #oNasabahDPLK.alamat_kode_pos = oRegisterNasabahRekening.alamat_kode_pos
  #oNasabahDPLK.alamat_telepon = oRegisterNasabahRekening.alamat_telepon
  #oNasabahDPLK.alamat_telepon2 = oRegisterNasabahRekening.alamat_telepon2
  
  '''
  oNasabahDPLK.alamat_surat_jalan = oRegisterNasabahRekening.alamat_surat_jalan
  oNasabahDPLK.alamat_surat_jalan2 = oRegisterNasabahRekening.alamat_surat_jalan2
  oNasabahDPLK.alamat_surat_rtrw = oRegisterNasabahRekening.alamat_surat_rtrw
  oNasabahDPLK.alamat_surat_kelurahan = oRegisterNasabahRekening.alamat_surat_kelurahan
  oNasabahDPLK.alamat_surat_kecamatan = oRegisterNasabahRekening.alamat_surat_kecamatan
  #oNasabahDPLK.alamat_surat_kota = oRegisterNasabahRekening.alamat_surat_kota
  #oNasabahDPLK.alamat_surat_propinsi = oRegisterNasabahRekening.alamat_surat_propinsi
  oNasabahDPLK.LASKecamatan = oRegisterNasabahRekening.LASKecamatan
  oNasabahDPLK.LASKota = oRegisterNasabahRekening.LASKota
  oNasabahDPLK.LASPropinsi = oRegisterNasabahRekening.LASPropinsi
  oNasabahDPLK.alamat_surat_kode_pos = oRegisterNasabahRekening.alamat_surat_kode_pos
  oNasabahDPLK.alamat_surat_telepon = oRegisterNasabahRekening.alamat_surat_telepon
  oNasabahDPLK.alamat_surat_telepon2 = oRegisterNasabahRekening.alamat_surat_telepon2
  
  oNasabahDPLK.LJenisPekerjaan = oRegisterNasabahRekening.LJenisPekerjaan
  oNasabahDPLK.LJenisPekerjaanDetail = oRegisterNasabahRekening.LJenisPekerjaanDetail
  #oNasabahDPLK.kode_jenis_pekerjaan = oRegisterNasabahRekening.kode_jenis_pekerjaan
  oNasabahDPLK.status_pep = oRegisterNasabahRekening.status_pep
  oNasabahDPLK.keterangan_pep = oRegisterNasabahRekening.keterangan_pep
  '''
  
  oNasabahCorporate = oUploadCorporate.LNasabahDPLKCorporate
  oNasabahDPLK.LNasabahDPLKCorporate = oNasabahCorporate
  #oNasabahDPLK.kode_nasabah_corporate = oRegisterNasabahRekening.kode_nasabah_corporate
  oNasabahDPLK.nama_perusahaan = oNasabahCorporate.nama_perusahaan
  oNasabahDPLK.LJenisUsaha = oNasabahCorporate.LJenisUsaha
  #oNasabahDPLK.kode_jenis_usaha = oRegisterNasabahRekening.kode_jenis_usaha
  oNasabahDPLK.LKepemilikan = oNasabahCorporate.LKepemilikan
  #oNasabahDPLK.kode_pemilikan = oRegisterNasabahRekening.kode_pemilikan
  oNasabahDPLK.alamat_kantor_jalan = oNasabahCorporate.alamat_kantor_jalan
  oNasabahDPLK.alamat_kantor_kelurahan = oNasabahCorporate.alamat_kantor_kelurahan
  oNasabahDPLK.alamat_kantor_kecamatan = oNasabahCorporate.alamat_kantor_kecamatan
  #oNasabahDPLK.alamat_kantor_kota = oNasabahCorporate.alamat_kantor_kota
  #oNasabahDPLK.alamat_kantor_propinsi = oNasabahCorporate.alamat_kantor_propinsi
  oNasabahDPLK.LAKKecamatan = oNasabahCorporate.LAKKecamatan
  oNasabahDPLK.LAKKota = oNasabahCorporate.LAKKota
  oNasabahDPLK.LAKPropinsi = oNasabahCorporate.LAKPropinsi
  oNasabahDPLK.alamat_kantor_kode_pos = oNasabahCorporate.alamat_kantor_kode_pos
  oNasabahDPLK.alamat_kantor_telepon = oNasabahCorporate.alamat_kantor_telepon
  oNasabahDPLK.alamat_kantor_telepon2 = oNasabahCorporate.alamat_kantor_telepon2

  '''
  oNasabahDPLK.REFR_NAMA = oRegisterNasabahRekening.REFR_NAMA
  oNasabahDPLK.REFR_ACCNO = oRegisterNasabahRekening.REFR_ACCNO
  oNasabahDPLK.REFR_UKER = oRegisterNasabahRekening.REFR_UKER
  '''
  
  oNasabahDPLK.tgl_registrasi = moduleapi.DateTimeTupleToFloat(config, oUploadCorporate.session_time)
  oNasabahDPLK.last_update = config.ModDateTime.Now()
  oNasabahDPLK.user_id = oUploadCorporate.session_user_id
  oNasabahDPLK.auth_user_id = config.SecurityContext.userid
  oNasabahDPLK.isCommitted = 'T'
  oNasabahDPLK.last_terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oNasabahDPLK.no_referensi = oRegisterNasabahRekening.no_referensi
  #oNasabahDPLK.terminal_id = oRegisterNasabahRekening.terminal_id
  #oNasabahDPLK.keterangan = oRegisterNasabahRekening.keterangan_registrasi
  #oNasabahDPLK.isPesertaPengalihan = oRegisterNasabahRekening.isPesertaPengalihan
  #oNasabahDPLK.status_risk_request = None
  #oNasabahDPLK.risk_flag_request = None
  #oNasabahDPLK.tgl_renewal_identitas = None
  oNasabahDPLK.total_credit = 0.0
  oNasabahDPLK.total_debit = 0.0
  oNasabahDPLK.frek_credit = 0.0
  oNasabahDPLK.frek_debit = 0.0
  oNasabahDPLK.limit_credit = 0.0
  oNasabahDPLK.limit_debit = 0.0
  oNasabahDPLK.limit_frek_credit = 0.0
  oNasabahDPLK.limit_frek_debit = 0.0
  oNasabahDPLK.is_deleted = 0
  #oNasabahDPLK.LOperationCode = oRegisterNasabahRekening.LOperationCode
  oNasabahDPLK.operation_code = 'F'
  
  return oNasabahDPLK

def CreateRekInvDPLK(config, oRegisterNasabahRekening, oNasabahDPLK, oUploadCorporate):
  oRekNasabah = config.CreatePObject('RekInvDPLK') 
  
  #oRekNasabah.LSumberDana = oRegisterNasabahRekening.LSumberDana
  #oRekNasabah.sumber_dana = oRegisterNasabahRekening.sumber_dana
  oRekNasabah.no_rekening = oRegisterNasabahRekening.no_rekening
  '''
  oRekNasabah.usia_pensiun = oRegisterNasabahRekening.usia_pensiun
  oRekNasabah.sistem_pembayaran_iuran = oRegisterNasabahRekening.sistem_pembayaran_iuran
  oRekNasabah.LTujuanBukaRekening = oRegisterNasabahRekening.LTujuanBukaRekening
  oRekNasabah.tujuan_pembukaan_rekening = oRegisterNasabahRekening.tujuan_pembukaan_rekening
  oRekNasabah.tgl_pensiun = oRegisterNasabahRekening.tgl_pensiun
  oRekNasabah.tgl_pensiun_dipercepat = oRegisterNasabahRekening.tgl_pensiun_dipercepat
  oRekNasabah.kirim_statemen = oRegisterNasabahRekening.kirim_statemen
  oRekNasabah.setoran_awal = oRegisterNasabahRekening.setoran_awal
  oRekNasabah.iuran_pk = oRegisterNasabahRekening.iuran_pk
  oRekNasabah.iuran_pst = oRegisterNasabahRekening.iuran_pst
  oRekNasabah.tgl_penarikan_iuran = oRegisterNasabahRekening.tgl_penarikan_iuran
  oRekNasabah.REKSUMBER_NO = oRegisterNasabahRekening.REKSUMBER_NO
  oRekNasabah.REKSUMBER_NAMA = oRegisterNasabahRekening.REKSUMBER_NAMA
  '''
  
  '''
  #oRekNasabah.kode_cab_daftar = oRegisterNasabahRekening.kode_cab_daftar
  '''
  oRekNasabah.LBranchLocation = oUploadCorporate.LBranchLocation
  oRekNasabah.STATUS_BIAYA_DAFTAR = 'F'
  oRekNasabah.LNasabahDPLK = oNasabahDPLK
  
  '''
  oRekNasabah.no_peserta = oRegisterNasabahRekening.no_peserta
  #oRekNasabah.LRekAsuransi = oRegisterNasabahRekening.LRekAsuransi
  #oRekNasabah.rekasuransi_id = oRegisterNasabahRekening.rekasuransi_id
  #oRekNasabah.LOperationCode = oRegisterNasabahRekening.LOperationCode
  '''
  
  oRekNasabah.operation_code = 'F'
  oRekNasabah.akum_iuran_pk = 0.0
  oRekNasabah.akum_iuran_pst = 0.0
  oRekNasabah.akum_iuran_tmb = 0.0
  oRekNasabah.akum_psl = 0.0
  oRekNasabah.akum_pmb_pk = 0.0
  oRekNasabah.akum_pmb_pst = 0.0
  oRekNasabah.akum_pmb_tmb = 0.0
  oRekNasabah.akum_pmb_psl = 0.0
  oRekNasabah.STATUS_DPLK = 'A'
  #oRekNasabah.TGL_TUTUP = oRegisterNasabahRekening.TGL_TUTUP
  #oRekNasabah.status_komisi = oRegisterNasabahRekening.status_komisi
  oRekNasabah.tgl_akseptasi = config.ModDateTime.Now()
  #oRekNasabah.tgl_bayar_anuitas = oRegisterNasabahRekening.tgl_bayar_anuitas
  #oRekNasabah.nilai_bayar_anuitas = oRegisterNasabahRekening.nilai_bayar_anuitas
  oRekNasabah.user_id = oUploadCorporate.session_user_id
  oRekNasabah.auth_user_id = config.SecurityContext.userid
  oRekNasabah.last_update = config.ModDateTime.Now()
  oRekNasabah.last_terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oRekNasabah.status_anuitas = 'F'
  oRekNasabah.status_autodebet = 'F'
  oRekNasabah.status_asuransi = 'F'
  #oRekNasabah.keterangan = oRegisterNasabahRekening.keterangan_iuran
  #oRekNasabah.confidential_code = oRegisterNasabahRekening.confidential_code
  #oRekNasabah.collectivity_asuransi = oRegisterNasabahRekening.collectivity_asuransi
  #oRekNasabah.kewajiban_asuransi = oRegisterNasabahRekening.kewajiban_asuransi
  #oRekNasabah.Is_Boleh_Debet = oRegisterNasabahRekening.Is_Boleh_Debet
  #oRekNasabah.bln_tunggakan_asuransi = oRegisterNasabahRekening.bln_tunggakan_asuransi
  oRekNasabah.has_passbook = 'F'
  oRekNasabah.No_Seri_Buku = oRegisterNasabahRekening.no_seri_buku
  oRekNasabah.IS_DELETED = 0
  
  return oRekNasabah
  
def CreateHistoriBuku(config, oRegisterNasabahRekening, oUploadCorporate):
  oHistoriBuku = config.CreatePObject('HistoriBukuDPLK')
  oHistoriBuku.branch_code = oRegisterNasabahRekening.kode_cab_daftar
  oHistoriBuku.no_peserta = oRegisterNasabahRekening.no_peserta
  oHistoriBuku.no_rekening = oRegisterNasabahRekening.no_rekening
  oHistoriBuku.no_seri_buku = oRegisterNasabahRekening.no_seri_buku
  oHistoriBuku.status = 'T'
  oHistoriBuku.tgl_input = config.Now()
  oHistoriBuku.user_id = oUploadCorporate.session_user_id

def CreateRegisterPassbook(config, oRegisterNasabahRekening):
  oRegisterpassbook = config.CreatePObject('REGISTERPASSBOOK')
  oRegisterpassbook.Baris_cetak_terakhir = 0
  oRegisterpassbook.halaman_cetak_terakhir = 1
  #Id_Register
  #ID_Transaksi
  oRegisterpassbook.is_baru_register = 'T'
  #LRekeningDPLK
  #LTransaksiTerakhir
  oRegisterpassbook.no_rekening = oRegisterNasabahRekening.no_rekening
  oRegisterpassbook.nomor_buku_terakhir = 1
  #oRegisterpassbook.Tanggal_Cetak_Terakhir = config.Now()
  
def CreateRekeningDPLK(config, oRegisterNasabahRekening, oUploadCorporate):
  oRekeningDPLK = config.CreatePObject('RekeningDPLK')
  oRekeningDPLK.akum_iuran_pk = 0.0
  oRekeningDPLK.akum_iuran_pst = 0.0
  oRekeningDPLK.akum_iuran_tmb = 0.0
  oRekeningDPLK.akum_pmb_pk = 0.0
  oRekeningDPLK.akum_pmb_psl = 0.0
  oRekeningDPLK.akum_pmb_pst = 0.0
  oRekeningDPLK.akum_pmb_tmb = 0.0
  oRekeningDPLK.akum_psl = 0.0
  oRekeningDPLK.jml_pesan_unit = 0.0
  oRekeningDPLK.jml_redeem_unit = 0.0
  oRekeningDPLK.jml_unit = 0.0
  oRekeningDPLK.jml_unit_pk = 0.0
  oRekeningDPLK.jml_unit_psl = 0.0
  oRekeningDPLK.jml_unit_pst = 0.0
  oRekeningDPLK.jml_unit_tmb = 0.0
  
  kode_paket_investasi = 'A'
  proporsi = 100
  oRekeningDPLK.kode_paket_investasi = kode_paket_investasi
  #LPaketInvestasi
  #LRekInvDPLK
  #Ls_DetilTransaksiDPLK
  #Ls_HistoriSRR
  oRekeningDPLK.nilai_unit = 0.0
  oRekeningDPLK.NO_REKENING = oRegisterNasabahRekening.no_rekening
  oRekeningDPLK.nomor_rekening =  "%s_%s" % (oRegisterNasabahRekening.no_rekening, kode_paket_investasi)
  oRekeningDPLK.pct_alokasi = proporsi
  oRekeningDPLK.SRR_AKHIR = 0.0
  oRekeningDPLK.TGL_SRR_AKHIR = moduleapi.DateTimeTupleToFloat(config, oUploadCorporate.session_time)
  oRekeningDPLK.is_deleted == 'F'
  
  return oRekeningDPLK

def CreateAllAhliWaris(config, oNasabahDPLK):
  oAhliWaris = config.CreatePObject('AhliWaris')
  oAhliWaris.LNasabahDPLK = oNasabahDPLK
  oAhliWaris.nama_lengkap = "Ahli Waris"
  oAhliWaris.nomor_urut_prioritas = 1

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
  oRegisterAutoDebet.jenis_transaksi = 'R'
  oRegisterAutoDebet.nama_rekening = oRegisterNasabahRekening.nama_rek_autodebet
  #registercif_id
  oRegisterAutoDebet.tanggal_autodebet = oRegisterNasabahRekening.tanggal_autodebet

  #keterangan
  #kode_jenis_registercif
  #LJenisRegisterCIF
  #LNasabahDPLK
  #LRekeningDPLK
  #LUserApp
  oRegisterAutoDebet.no_peserta = oRegisterNasabahRekening.no_peserta
  oRegisterAutoDebet.no_referensi = oRegisterNasabahRekening.no_referensi
  oRegisterAutoDebet.no_rekening = oRegisterNasabahRekening.no_rek_autodebet
  oRegisterAutoDebet.tanggal_register = config.Now()
  oRegisterAutoDebet.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oRegisterAutoDebet.user_id = oRegisterNasabahRekening.user_id
  
  return oRegisterAutoDebet

#def CreateRekeningAsuransi(config, oRegisterNasabahRekening, parameter):
#  oRekeningAsuransi = config.CreatePObject('RekeningAsuransi')
#  oRekeningAsuransi.no_peserta = oRegisterNasabahRekening.no_peserta
#  oRekeningAsuransi.user_id = oRegisterNasabahRekening.user_id
#  oRekeningAsuransi.auth_user_id = config.SecurityContext.userid
#  oRekeningAsuransi.no_polis = parameter.FirstRecord.no_polis
#  oRekeningAsuransi.besar_premi = parameter.FirstRecord.besar_premi
#  oRekeningAsuransi.tgl_akseptasi = parameter.FirstRecord.tgl_akseptasi

def CreateRegisterAsuransi(config, oRegisterNasabahRekening, oRekeningDPLK):
  oRegisterAsuransi = config.CreatePObject('RegisterAsuransi')
  #alasan_berhenti
  oRegisterAsuransi.jenis_transaksi = 'R'
  #registercif_id
  
  #keterangan
  #kode_jenis_registercif
  #LJenisRegisterCIF
  #LNasabahDPLK
  #LRekeningDPLK
  #LUserApp
  oRegisterAsuransi.no_peserta = oRegisterNasabahRekening.no_peserta
  oRegisterAsuransi.no_referensi = oRegisterNasabahRekening.no_referensi
  oRegisterAsuransi.no_rekening = oRegisterNasabahRekening.no_rekening
  oRegisterAsuransi.tanggal_register = config.Now()
  oRegisterAsuransi.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oRegisterAsuransi.user_id = oRegisterNasabahRekening.user_id

def CreateHistoriAhliWaris(config, oRegisterAhliWaris):
  oNasabahDPLK = oRegisterAhliWaris.LNasabahDPLK
  oUploadCorporate = oRegisterAhliWaris.LUploadCorporate
  
  oHistoriAhliWaris = config.CreatePObject('HistoriAhliWaris')
  oHistoriAhliWaris.LNasabahDPLK = oNasabahDPLK
  oHistoriAhliWaris.auth_user_id = config.SecurityContext.userid
  oHistoriAhliWaris.keterangan = 'upload masal ahli waris'
  oHistoriAhliWaris.no_referensi = oUploadCorporate.session_filename
  oHistoriAhliWaris.tanggal_histori = config.Now()
  oHistoriAhliWaris.terminal_id = oNasabahDPLK.last_terminal_id
  oHistoriAhliWaris.user_id = oNasabahDPLK.user_id
  
  Ls_AhliWaris = oNasabahDPLK.Ls_AhliWaris
  Ls_AhliWaris.First()
  while not Ls_AhliWaris.EndOfList:
    oAhliWarisDetail = Ls_AhliWaris.CurrentElement

    oHistoriAhliWarisDetail = config.CreatePObject('HistoriAhliWarisDetail')
    oHistoriAhliWarisDetail.LHistoriAhliWaris = oHistoriAhliWaris
    oHistoriAhliWarisDetail.hubungan_keluarga = oAhliWarisDetail.hubungan_keluarga
    oHistoriAhliWarisDetail.jenis_kelamin = oAhliWarisDetail.jenis_kelamin
    oHistoriAhliWarisDetail.keterangan = oAhliWarisDetail.keterangan
    oHistoriAhliWarisDetail.nama_lengkap = oAhliWarisDetail.nama_lengkap
    oHistoriAhliWarisDetail.nomor_urut_prioritas = oAhliWarisDetail.nomor_urut_prioritas
    oHistoriAhliWarisDetail.status_ahli_waris = oAhliWarisDetail.status_ahli_waris
    
    if oAhliWarisDetail.tanggal_lahir != None:
      oHistoriAhliWarisDetail.tanggal_lahir = moduleapi.DateTimeTupleToFloat(config, oAhliWarisDetail.tanggal_lahir)
    
    Ls_AhliWaris.Next()

  return oHistoriAhliWaris
#--

def CreateNewAhliWaris(config, oRegisterAhliWaris):
  oNasabahDPLK = oRegisterAhliWaris.LNasabahDPLK
  
  oAhliWaris = config.CreatePObject('AhliWaris')
  oAhliWaris.LNasabahDPLK = oNasabahDPLK
  oAhliWaris.hubungan_keluarga = oRegisterAhliWaris.hubungan_keluarga
  oAhliWaris.jenis_kelamin = oRegisterAhliWaris.jenis_kelamin
  oAhliWaris.keterangan = oRegisterAhliWaris.keterangan_ahli_waris
  oAhliWaris.nama_lengkap = oRegisterAhliWaris.nama_ahli_waris
  oAhliWaris.nomor_urut_prioritas = oRegisterAhliWaris.no_urut_prioritas
  oAhliWaris.status_ahli_waris = oRegisterAhliWaris.status_ahli_waris
  
  if oRegisterAhliWaris.tanggal_lahir != None:
    oAhliWaris.tanggal_lahir = moduleapi.DateTimeTupleToFloat(config, oRegisterAhliWaris.tanggal_lahir)
#--
  
def CreateHistoriUbahAlamat(config, oRegisterUbahAlamat):
  oNasabahDPLK = oRegisterUbahAlamat.LNasabahDPLK
  
  oHistoriUbahAlamat = config.CreatePObject('HistoriUbahAlamat')

  oHistoriUbahAlamat.LNasabahDPLK = oNasabahDPLK
  oHistoriUbahAlamat.auth_user_id = config.SecurityContext.userid
  oHistoriUbahAlamat.keterangan = oRegisterUbahAlamat.keterangan
  oHistoriUbahAlamat.no_referensi = oRegisterUbahAlamat.no_referensi
  oHistoriUbahAlamat.tanggal_histori = config.Now()
  oHistoriUbahAlamat.terminal_id = oNasabahDPLK.last_terminal_id
  oHistoriUbahAlamat.user_id = oNasabahDPLK.user_id

  oHistoriUbahAlamat.alamat_jalan = oNasabahDPLK.alamat_jalan
  oHistoriUbahAlamat.alamat_jalan2 = oNasabahDPLK.alamat_jalan2
  oHistoriUbahAlamat.alamat_rtrw = oNasabahDPLK.alamat_rtrw
  oHistoriUbahAlamat.alamat_kelurahan = oNasabahDPLK.alamat_kelurahan
  oHistoriUbahAlamat.alamat_kecamatan = oNasabahDPLK.alamat_kecamatan
  #oHistoriUbahAlamat.alamat_kota = oNasabahDPLK.alamat_kota
  #oHistoriUbahAlamat.alamat_propinsi = oNasabahDPLK.alamat_propinsi
  oHistoriUbahAlamat.LATKecamatan = oNasabahDPLK.LATKecamatan
  oHistoriUbahAlamat.LATKota = oNasabahDPLK.LATKota
  oHistoriUbahAlamat.LATPropinsi = oNasabahDPLK.LATPropinsi
  oHistoriUbahAlamat.alamat_kode_pos = oNasabahDPLK.alamat_kode_pos
  oHistoriUbahAlamat.alamat_telepon = oNasabahDPLK.alamat_telepon
  oHistoriUbahAlamat.alamat_telepon2 = oNasabahDPLK.alamat_telepon2
  #oHistoriUbahAlamat.alamat_email = oNasabahDPLK.alamat_email

  """
  oHistoriUbahAlamat.alamat_surat_jalan = oNasabahDPLK.alamat_surat_jalan
  oHistoriUbahAlamat.alamat_surat_jalan2 = oNasabahDPLK.alamat_surat_jalan2
  oHistoriUbahAlamat.alamat_surat_rtrw = oNasabahDPLK.alamat_surat_rtrw
  oHistoriUbahAlamat.alamat_surat_kelurahan = oNasabahDPLK.alamat_surat_kelurahan
  oHistoriUbahAlamat.alamat_surat_kecamatan = oNasabahDPLK.alamat_surat_kecamatan
  #oHistoriUbahAlamat.alamat_surat_kota = oNasabahDPLK.alamat_surat_kota
  #oHistoriUbahAlamat.alamat_surat_propinsi = oNasabahDPLK.alamat_surat_propinsi
  oHistoriUbahAlamat.LASKecamatan = oNasabahDPLK.LASKecamatan
  oHistoriUbahAlamat.LASKota = oNasabahDPLK.LASKota
  oHistoriUbahAlamat.LASPropinsi = oNasabahDPLK.LASPropinsi
  oHistoriUbahAlamat.alamat_surat_kode_pos = oNasabahDPLK.alamat_surat_kode_pos
  oHistoriUbahAlamat.alamat_surat_telepon = oNasabahDPLK.alamat_surat_telepon
  oHistoriUbahAlamat.alamat_surat_telepon2 = oNasabahDPLK.alamat_surat_telepon2

  oHistoriUbahAlamat.alamat_kantor_jalan = oNasabahDPLK.alamat_kantor_jalan
  oHistoriUbahAlamat.alamat_kantor_kelurahan = oNasabahDPLK.alamat_kantor_kelurahan
  oHistoriUbahAlamat.alamat_kantor_kecamatan = oNasabahDPLK.alamat_kantor_kecamatan
  #oHistoriUbahAlamat.alamat_kantor_kota = oNasabahDPLK.alamat_kantor_kota
  #oHistoriUbahAlamat.alamat_kantor_propinsi = oNasabahDPLK.alamat_kantor_propinsi
  oHistoriUbahAlamat.LAKKecamatan = oNasabahDPLK.LAKKecamatan
  oHistoriUbahAlamat.LAKKota = oNasabahDPLK.LAKKota
  oHistoriUbahAlamat.LAKPropinsi = oNasabahDPLK.LAKPropinsi
  oHistoriUbahAlamat.alamat_kantor_kode_pos = oNasabahDPLK.alamat_kantor_kode_pos
  oHistoriUbahAlamat.alamat_kantor_telepon = oNasabahDPLK.alamat_kantor_telepon
  oHistoriUbahAlamat.alamat_kantor_telepon2 = oNasabahDPLK.alamat_kantor_telepon2
  """

  return oHistoriUbahAlamat
#--

def UpdateAlamat(config, oRegisterUbahAlamat):
  oNasabahDPLK = oRegisterUbahAlamat.LNasabahDPLK
  
  oNasabahDPLK.alamat_jalan = oRegisterUbahAlamat.alamat_jalan
  oNasabahDPLK.alamat_jalan2 = oRegisterUbahAlamat.alamat_jalan2
  oNasabahDPLK.alamat_rtrw = oRegisterUbahAlamat.alamat_rtrw
  oNasabahDPLK.alamat_kelurahan = oRegisterUbahAlamat.alamat_kelurahan
  oNasabahDPLK.alamat_kecamatan = oRegisterUbahAlamat.alamat_kecamatan
  #oNasabahDPLK.alamat_kota = oRegisterUbahAlamat.alamat_kota
  #oNasabahDPLK.alamat_propinsi = oRegisterUbahAlamat.alamat_propinsi
  oNasabahDPLK.LATKecamatan = oRegisterUbahAlamat.LATKecamatan
  oNasabahDPLK.LATKota = oRegisterUbahAlamat.LATKota
  oNasabahDPLK.LATPropinsi = oRegisterUbahAlamat.LATPropinsi
  oNasabahDPLK.alamat_kode_pos = oRegisterUbahAlamat.alamat_kode_pos
  oNasabahDPLK.alamat_telepon = oRegisterUbahAlamat.alamat_telepon
  oNasabahDPLK.alamat_telepon2 = oRegisterUbahAlamat.alamat_telepon2
  #oNasabahDPLK.alamat_email = oRegisterUbahAlamat.alamat_email

  """
  oNasabahDPLK.alamat_surat_jalan = oRegisterUbahAlamat.alamat_surat_jalan
  oNasabahDPLK.alamat_surat_jalan2 = oRegisterUbahAlamat.alamat_surat_jalan2
  oNasabahDPLK.alamat_surat_rtrw = oRegisterUbahAlamat.alamat_surat_rtrw
  oNasabahDPLK.alamat_surat_kelurahan = oRegisterUbahAlamat.alamat_surat_kelurahan
  oNasabahDPLK.alamat_surat_kecamatan = oRegisterUbahAlamat.alamat_surat_kecamatan
  #oNasabahDPLK.alamat_surat_kota = oRegisterUbahAlamat.alamat_surat_kota
  #oNasabahDPLK.alamat_surat_propinsi = oRegisterUbahAlamat.alamat_surat_propinsi
  oNasabahDPLK.LASKecamatan = oRegisterUbahAlamat.LASKecamatan
  oNasabahDPLK.LASKota = oRegisterUbahAlamat.LASKota
  oNasabahDPLK.LASPropinsi = oRegisterUbahAlamat.LASPropinsi
  oNasabahDPLK.alamat_surat_kode_pos = oRegisterUbahAlamat.alamat_surat_kode_pos
  oNasabahDPLK.alamat_surat_telepon = oRegisterUbahAlamat.alamat_surat_telepon
  oNasabahDPLK.alamat_surat_telepon2 = oRegisterUbahAlamat.alamat_surat_telepon2

  oNasabahDPLK.alamat_kantor_jalan = oRegisterUbahAlamat.alamat_kantor_jalan
  oNasabahDPLK.alamat_kantor_kelurahan = oRegisterUbahAlamat.alamat_kantor_kelurahan
  oNasabahDPLK.alamat_kantor_kecamatan = oRegisterUbahAlamat.alamat_kantor_kecamatan
  oNasabahDPLK.alamat_kantor_kota = oRegisterUbahAlamat.alamat_kantor_kota
  oNasabahDPLK.alamat_kantor_propinsi = oRegisterUbahAlamat.alamat_kantor_propinsi
  oNasabahDPLK.LAKKecamatan = oRegisterUbahAlamat.LAKKecamatan
  oNasabahDPLK.LAKKota = oRegisterUbahAlamat.LAKKota
  oNasabahDPLK.LAKPropinsi = oRegisterUbahAlamat.LAKPropinsi
  oNasabahDPLK.alamat_kantor_kode_pos = oRegisterUbahAlamat.alamat_kantor_kode_pos
  oNasabahDPLK.alamat_kantor_telepon = oRegisterUbahAlamat.alamat_kantor_telepon
  oNasabahDPLK.alamat_kantor_telepon2 = oRegisterUbahAlamat.alamat_kantor_telepon2
  """
#--

def DAFScriptMain(config, parameter, returnpacket):
  # import rpdb2; rpdb2.start_embedded_debugger("000")
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)
  app = config.AppObject
  app.ConCreate('out')
  app.ConWriteln('mulai...')
  
  id = parameter.FirstRecord.id

  oUploadCorporate = config.CreatePObjImplProxy('UploadCorporate')
  oUploadCorporate.Key = id

  config.BeginTransaction()
  try:
    _trxCount = 0
    if oUploadCorporate.upload_type == 'P':
      sSQL = '''
        SELECT * 
        FROM   UploadCorpRegisterPeserta
        WHERE  trx_session_id = %d
               AND is_auth = 'F'
               AND is_valid = 'T'
        ''' % oUploadCorporate.trx_session_id
      rSQL = config.CreateSQL(sSQL).RawResult
      rSQL.First()
      while not rSQL.Eof:
        _trxCount += 1
        
        oNasabahDPLK = CreateNasabahDPLK(config, rSQL, oUploadCorporate)
        CreateAllAhliWaris(config, oNasabahDPLK)
        oRekInvDPLK = CreateRekInvDPLK(config, rSQL, oNasabahDPLK, oUploadCorporate)
        #CreateRegisterPassbook(config, rSQL)
        #CreateHistoriBuku(config, rSQL, oUploadCorporate)
        CreateRekeningDPLK(config, rSQL, oUploadCorporate)
        
        oUCRegisterPeserta = config.CreatePObjImplProxy('UploadCorpRegisterPeserta')
        oUCRegisterPeserta.Key = rSQL.upload_id
        oUCRegisterPeserta.is_auth = 'T'
        
        if (_trxCount % 100) == 0:
          app.ConWriteln('%d data diproses...' % _trxCount)
        
        rSQL.Next()
    elif oUploadCorporate.upload_type == 'K':
      sSQL = '''
        SELECT * 
        FROM   UploadCorpKoreksiPeserta
        WHERE  trx_session_id = %d
               AND is_auth = 'F'
               AND is_valid = 'T'
        ORDER BY no_peserta ASC
        ''' % oUploadCorporate.trx_session_id
      rSQL = config.CreateSQL(sSQL).RawResult
      rSQL.First()
      while not rSQL.Eof:
        oUCKoreksiPeserta = config.CreatePObjImplProxy('UploadCorpKoreksiPeserta')
        oUCKoreksiPeserta.Key = rSQL.upload_id
        oUCKoreksiPeserta.is_auth = 'T'
        
        CreateHistoriUbahAlamat(config, oUCKoreksiPeserta)
        UpdateAlamat(config, oUCKoreksiPeserta)
        
        if (_trxCount % 100) == 0:
          app.ConWriteln('%d data diproses...' % _trxCount)
        
        rSQL.Next()
    elif oUploadCorporate.upload_type == 'W':
      init_peserta = ''
      sSQL = '''
        SELECT * 
        FROM   UploadCorpAhliWaris
        WHERE  trx_session_id = %d
               AND is_auth = 'F'
               AND is_valid = 'T'
        ORDER BY no_peserta ASC
        ''' % oUploadCorporate.trx_session_id
      rSQL = config.CreateSQL(sSQL).RawResult
      rSQL.First()
      while not rSQL.Eof:
        oUCAhliWaris = config.CreatePObjImplProxy('UploadCorpAhliWaris')
        oUCAhliWaris.Key = rSQL.upload_id
        oUCAhliWaris.is_auth = 'T'

        if init_peserta != rSQL.no_peserta:
          oNasabahDPLK = config.CreatePObjImplProxy('NasabahDPLK')
          oNasabahDPLK.Key = rSQL.no_peserta
          
          CreateHistoriAhliWaris(config, oUCAhliWaris)
          oNasabahDPLK.Ls_AhliWaris.DeleteAllPObjs()
        #--endif
        
        init_peserta = rSQL.no_peserta        
        CreateNewAhliWaris(config, oUCAhliWaris)

        if (_trxCount % 100) == 0:
          app.ConWriteln('%d data diproses...' % _trxCount)
        
        rSQL.Next()
    #--endwhile      

    oUploadCorporate.is_auth = 'T'

    config.Commit()
  except:
    config.Rollback()
    raise
  
  return 1
  			 
def CreateDetailAkumPengembangan(config, no_peserta, kode_paket_investasi):
    sSQL = 'SELECT kode_jns_investasi \
    FROM RINCIANPAKETINVESTASI\
    WHERE kode_paket_investasi = \'%s\' ' % (kode_paket_investasi)
    rSQL = config.CreateSQL(sSQL).RawResult
    while not rSQL.Eof:
        sSQL = 'INSERT INTO DETAILAKUMPENGEMBANGAN \
		(no_peserta, kode_paket_investasi, kode_jns_investasi, Nilai_Akumulasi) \
		VALUES (\'%s\',\'%s\',\'%s\',%f) ' % \
		(no_peserta, kode_paket_investasi, rSQL.kode_jns_investasi, 0)
        config.ExecSQL(sSQL)
	rSQL.Next()

def KirimPesertaKeCoreBanking(config, no_peserta, nama_lengkap, kode_paket, kode_cab):
    isNeedLoginCoreBanking = config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING', \
      'NeedLoginCoreBanking')
    if isNeedLoginCoreBanking == 'T':
      sessionID = config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING', 'AppName') + \
        config.SecurityContext.UserID
      param = CreatePacketPeserta(config, no_peserta, nama_lengkap, kode_paket, kode_cab, sessionID)
      try:
        rph = config.AppObject.rexecscript(sessionID, 'remote/KirimPesertaDPLK', param, 1)
        if rph.FirstRecord.IsErr:
          raise BaseException, "\n\nError kirim peserta ke CoreBanking\n%s" % str(rph.FirstRecord.ErrMessage)
      except:
        raise

    #update jumlah peserta objek HistoriKirimPeserta
    oHKP = config.CreatePObject('HistoriKirimPeserta')
    oHKP.Tanggal_Kirim = config.Now()
    y,m,d = config.ModLibUtils.DecodeDate(config.Now())
    oHKP.Tanggal_Terdaftar = config.ModLibUtils.EncodeDate(y,m,d)
    oHKP.Jumlah_Peserta = 1
    oHKP.User_ID = config.SecurityContext.UserID

def CreatePacketPeserta(config, no_peserta, nama_lengkap, kode_paket, kode_cab, sessionID):
  ph = config.AppObject.CreatePacket()
  packet = ph.Packet
  packet.AddDataPacketStructureEx('__ListPeserta', \
    'noPeserta:string;namaPeserta:string;kodePaket:string;kodeCabang:string')
  packet.BuildAllStructure()
  
  CekPesertaSdhTersimpan(config, no_peserta, sessionID)
  
  ds = packet.AddNewDataset('__ListPeserta')
  rec = ds.AddRecord()
  rec.noPeserta = no_peserta
  rec.namaPeserta = nama_lengkap
  rec.kodePaket = kode_paket
  rec.kodeCabang = kode_cab
  
  return ph
  
def CekPesertaSdhTersimpan(config, no_peserta, sessionID):
  lsNomPst = '('+config.ModLibUtils.QuotedStr(no_peserta)+')'
  try:
      param = config.AppObject.CreateValues(['lsNomPst', lsNomPst])
      rph = config.AppObject.rexecscript(sessionID, 'remote/CekPesertaSdhTersimpan', param, 1)
      recStatus = rph.Packet.GetDatasetByName('status').GetRecord(0)
      if recStatus.IsErr:
        msg = str(recStatus.ErrMessage)
        raise BaseException, "\n\nError Cek Peserta:\n" % msg
  except:
    raise