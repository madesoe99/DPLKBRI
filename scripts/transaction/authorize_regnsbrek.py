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

def CreateNasabahDPLK(config, oRegisterNasabahRekening): 
  oNasabahDPLK = config.CreatePObject('NasabahDPLK')
  
  oNasabahDPLK.no_peserta = oRegisterNasabahRekening.no_peserta
  #oNasabahDPLK.LBranchLocation = oRegisterNasabahRekening.LBranchLocation
  #oNasabahDPLK.kode_cab_daftar = oRegisterNasabahRekening.kode_cab_daftar
  oNasabahDPLK.ibu_kandung = oRegisterNasabahRekening.ibu_kandung
  oNasabahDPLK.nama_lengkap = oRegisterNasabahRekening.nama_lengkap
  oNasabahDPLK.tempat_lahir = oRegisterNasabahRekening.tempat_lahir
  oNasabahDPLK.tanggal_lahir = moduleapi.DateTimeTupleToFloat(config, oRegisterNasabahRekening.tanggal_lahir)
  oNasabahDPLK.jenis_kelamin = oRegisterNasabahRekening.jenis_kelamin
  oNasabahDPLK.golongan_darah = oRegisterNasabahRekening.golongan_darah
  oNasabahDPLK.agama = oRegisterNasabahRekening.agama
  oNasabahDPLK.pendidikan_terakhir = oRegisterNasabahRekening.pendidikan_terakhir
  oNasabahDPLK.status_perkawinan = oRegisterNasabahRekening.status_perkawinan
  oNasabahDPLK.LDaerahAsal = oRegisterNasabahRekening.LDaerahAsal
  #oNasabahDPLK.kode_propinsi = oRegisterNasabahRekening.kode_propinsi
  oNasabahDPLK.kewarganegaraan = oRegisterNasabahRekening.kewarganegaraan
  oNasabahDPLK.LNegara = oRegisterNasabahRekening.LNegara
  #oNasabahDPLK.kode_negara = oRegisterNasabahRekening.kode_negara
  oNasabahDPLK.JENIS_KARTU_IDENTITAS = oRegisterNasabahRekening.JENIS_KARTU_IDENTITAS
  oNasabahDPLK.no_identitas_diri = oRegisterNasabahRekening.no_identitas_diri
  oNasabahDPLK.tgl_exp_identitas = oRegisterNasabahRekening.tgl_exp_identitas
  
  #oNasabahDPLK.LKelompok = oRegisterNasabahRekening.LKelompok
  #oNasabahDPLK.kode_kelompok = oRegisterNasabahRekening.kode_kelompok
  oNasabahDPLK.alamat_email = oRegisterNasabahRekening.alamat_email
  oNasabahDPLK.NPWP = oRegisterNasabahRekening.NPWP
  oNasabahDPLK.penghasilan_tetap = oRegisterNasabahRekening.penghasilan_tetap
  oNasabahDPLK.penghasilan_tambahan = oRegisterNasabahRekening.penghasilan_tambahan
  #oNasabahDPLK.beneficial_owner = oRegisterNasabahRekening.beneficial_owner
  #oNasabahDPLK.LLDPLain = oRegisterNasabahRekening.LLDPLain
  #oNasabahDPLK.kode_dp = oRegisterNasabahRekening.kode_dp
  
  oNasabahDPLK.HUBUNGAN_KELENGKAPAN = oRegisterNasabahRekening.HUBUNGAN_KELENGKAPAN
  oNasabahDPLK.nama_orang_tua = oRegisterNasabahRekening.nama_orang_tua
  oNasabahDPLK.LJenisPekerjaanOrtu = oRegisterNasabahRekening.LJenisPekerjaanOrtu
  oNasabahDPLK.LJenisPekerjaanDetailOrtu = oRegisterNasabahRekening.LJenisPekerjaanDetailOrtu
  oNasabahDPLK.LJenisUsahaOrtu = oRegisterNasabahRekening.LJenisUsahaOrtu
  oNasabahDPLK.nama_perusahaan_ortu = oRegisterNasabahRekening.nama_perusahaan_ortu
  oNasabahDPLK.penghasilan_orang_tua = oRegisterNasabahRekening.penghasilan_orang_tua
  
  oNasabahDPLK.alamat_jalan = oRegisterNasabahRekening.alamat_jalan
  oNasabahDPLK.alamat_jalan2 = oRegisterNasabahRekening.alamat_jalan2
  oNasabahDPLK.alamat_rtrw = oRegisterNasabahRekening.alamat_rtrw
  oNasabahDPLK.alamat_rw = oRegisterNasabahRekening.alamat_rw
  oNasabahDPLK.alamat_kelurahan = oRegisterNasabahRekening.alamat_kelurahan
  oNasabahDPLK.alamat_kecamatan = oRegisterNasabahRekening.alamat_kecamatan
  #oNasabahDPLK.alamat_kode_pos = oRegisterNasabahRekening.alamat_kode_pos
  #oNasabahDPLK.alamat_kota = oRegisterNasabahRekening.alamat_kota
  #oNasabahDPLK.alamat_propinsi = oRegisterNasabahRekening.alamat_propinsi
  oNasabahDPLK.LATKodePos = oRegisterNasabahRekening.LATKodePos
  oNasabahDPLK.LATKecamatan = oRegisterNasabahRekening.LATKecamatan
  oNasabahDPLK.LATKota = oRegisterNasabahRekening.LATKota
  oNasabahDPLK.LATPropinsi = oRegisterNasabahRekening.LATPropinsi
  oNasabahDPLK.alamat_telepon = oRegisterNasabahRekening.alamat_telepon
  oNasabahDPLK.alamat_telepon2 = oRegisterNasabahRekening.alamat_telepon2
  
  oNasabahDPLK.alamat_surat_jalan = oRegisterNasabahRekening.alamat_surat_jalan
  oNasabahDPLK.alamat_surat_jalan2 = oRegisterNasabahRekening.alamat_surat_jalan2
  oNasabahDPLK.alamat_surat_rtrw = oRegisterNasabahRekening.alamat_surat_rtrw
  oNasabahDPLK.alamat_surat_rw = oRegisterNasabahRekening.alamat_surat_rw
  oNasabahDPLK.alamat_surat_kelurahan = oRegisterNasabahRekening.alamat_surat_kelurahan
  oNasabahDPLK.alamat_surat_kecamatan = oRegisterNasabahRekening.alamat_surat_kecamatan
  #oNasabahDPLK.alamat_surat_kode_pos = oRegisterNasabahRekening.alamat_surat_kode_pos
  #oNasabahDPLK.alamat_surat_kota = oRegisterNasabahRekening.alamat_surat_kota
  #oNasabahDPLK.alamat_surat_propinsi = oRegisterNasabahRekening.alamat_surat_propinsi
  oNasabahDPLK.LASKodePos = oRegisterNasabahRekening.LASKodePos
  oNasabahDPLK.LASKecamatan = oRegisterNasabahRekening.LASKecamatan
  oNasabahDPLK.LASKota = oRegisterNasabahRekening.LASKota
  oNasabahDPLK.LASPropinsi = oRegisterNasabahRekening.LASPropinsi
  oNasabahDPLK.alamat_surat_telepon = oRegisterNasabahRekening.alamat_surat_telepon
  oNasabahDPLK.alamat_surat_telepon2 = oRegisterNasabahRekening.alamat_surat_telepon2
  
  oNasabahDPLK.LJenisPekerjaan = oRegisterNasabahRekening.LJenisPekerjaan
  oNasabahDPLK.LJenisPekerjaanDetail = oRegisterNasabahRekening.LJenisPekerjaanDetail
  #oNasabahDPLK.kode_jenis_pekerjaan = oRegisterNasabahRekening.kode_jenis_pekerjaan
  oNasabahDPLK.status_pep = oRegisterNasabahRekening.status_pep
  oNasabahDPLK.keterangan_pep = oRegisterNasabahRekening.keterangan_pep
  
  #oNasabahDPLK.LNasabahDPLKCorporate = oRegisterNasabahRekening.LNasabahDPLKCorporate
  #oNasabahDPLK.kode_nasabah_corporate = oRegisterNasabahRekening.kode_nasabah_corporate
  oNasabahDPLK.nama_perusahaan = oRegisterNasabahRekening.nama_perusahaan
  oNasabahDPLK.LJenisUsaha = oRegisterNasabahRekening.LJenisUsaha
  #oNasabahDPLK.kode_jenis_usaha = oRegisterNasabahRekening.kode_jenis_usaha
  oNasabahDPLK.LKepemilikan = oRegisterNasabahRekening.LKepemilikan
  #oNasabahDPLK.kode_pemilikan = oRegisterNasabahRekening.kode_pemilikan
  oNasabahDPLK.alamat_kantor_jalan = oRegisterNasabahRekening.alamat_kantor_jalan
  oNasabahDPLK.alamat_kantor_kelurahan = oRegisterNasabahRekening.alamat_kantor_kelurahan
  oNasabahDPLK.alamat_kantor_kecamatan = oRegisterNasabahRekening.alamat_kantor_kecamatan
  #oNasabahDPLK.alamat_kantor_kode_pos = oRegisterNasabahRekening.alamat_kantor_kode_pos
  #oNasabahDPLK.alamat_kantor_kota = oRegisterNasabahRekening.alamat_kantor_kota
  #oNasabahDPLK.alamat_kantor_propinsi = oRegisterNasabahRekening.alamat_kantor_propinsi
  oNasabahDPLK.LAKKodePos = oRegisterNasabahRekening.LAKKodePos
  oNasabahDPLK.LAKKecamatan = oRegisterNasabahRekening.LAKKecamatan
  oNasabahDPLK.LAKKota = oRegisterNasabahRekening.LAKKota
  oNasabahDPLK.LAKPropinsi = oRegisterNasabahRekening.LAKPropinsi
  oNasabahDPLK.alamat_kantor_telepon = oRegisterNasabahRekening.alamat_kantor_telepon
  oNasabahDPLK.alamat_kantor_telepon2 = oRegisterNasabahRekening.alamat_kantor_telepon2

  oNasabahDPLK.REFR_NAMA = oRegisterNasabahRekening.REFR_NAMA
  oNasabahDPLK.REFR_ACCNO = oRegisterNasabahRekening.REFR_ACCNO
  oNasabahDPLK.REFR_UKER = oRegisterNasabahRekening.REFR_UKER
  
  oNasabahDPLK.tgl_registrasi = moduleapi.DateTimeTupleToFloat(config, oRegisterNasabahRekening.tanggal_register)
  oNasabahDPLK.tgl_otorisasi = config.ModDateTime.Now()
  oNasabahDPLK.last_update = config.ModDateTime.Now()
  oNasabahDPLK.user_id = oRegisterNasabahRekening.user_id
  oNasabahDPLK.auth_user_id = config.SecurityContext.userid
  oNasabahDPLK.isCommitted = 'T'
  oNasabahDPLK.last_terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oNasabahDPLK.no_referensi = oRegisterNasabahRekening.no_referensi
  oNasabahDPLK.terminal_id = oRegisterNasabahRekening.terminal_id
  oNasabahDPLK.keterangan = oRegisterNasabahRekening.keterangan_registrasi
  #oNasabahDPLK.isPesertaPengalihan = oRegisterNasabahRekening.isPesertaPengalihan
  #oNasabahDPLK.status_risk_request = None
  #oNasabahDPLK.risk_flag_request = None
  #oNasabahDPLK.tgl_renewal_identitas = None
  #oNasabahDPLK.total_credit = 0.0
  #oNasabahDPLK.total_debit = 0.0
  #oNasabahDPLK.frek_credit = 0.0
  #oNasabahDPLK.frek_debit = 0.0
  #oNasabahDPLK.limit_credit = 0.0
  #oNasabahDPLK.limit_debit = 0.0
  #oNasabahDPLK.limit_frek_credit = 0.0
  #oNasabahDPLK.limit_frek_debit = 0.0
  oNasabahDPLK.is_deleted = 0
  #oNasabahDPLK.LOperationCode = oRegisterNasabahRekening.LOperationCode
  oNasabahDPLK.operation_code = 'F'
  
  return oNasabahDPLK

def CreateRekInvDPLK(config, oRegisterNasabahRekening, ikut_asuransi):
  oRekNasabah = config.CreatePObject('RekInvDPLK') 
  
  oRekNasabah.LBranchLocation = oRegisterNasabahRekening.LBranchLocation
  oRekNasabah.isPesertaPengalihan = oRegisterNasabahRekening.isPesertaPengalihan
  oRekNasabah.LLDPLain = oRegisterNasabahRekening.LLDPLain
  oRekNasabah.LNasabahDPLKCorporate = oRegisterNasabahRekening.LNasabahDPLKCorporate
  oRekNasabah.LKelompok = oRegisterNasabahRekening.LKelompok
  oRekNasabah.tgl_registrasi = moduleapi.DateTimeTupleToFloat(config, oRegisterNasabahRekening.tanggal_register)
  oRekNasabah.tgl_otorisasi = config.ModDateTime.Now()
  
  oRekNasabah.LSumberDana = oRegisterNasabahRekening.LSumberDana
  #oRekNasabah.sumber_dana = oRegisterNasabahRekening.sumber_dana
  oRekNasabah.no_rekening = oRegisterNasabahRekening.no_rekening
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
  oRekNasabah.iuran_tmb = oRegisterNasabahRekening.iuran_tmb
  oRekNasabah.tgl_penarikan_iuran = oRegisterNasabahRekening.tgl_penarikan_iuran
  oRekNasabah.REKSUMBER_NO = oRegisterNasabahRekening.REKSUMBER_NO
  oRekNasabah.REKSUMBER_NAMA = oRegisterNasabahRekening.REKSUMBER_NAMA
  
  #oRekNasabah.LBranchLocation = oRegisterNasabahRekening.LBranchLocation
  #oRekNasabah.kode_cab_daftar = oRegisterNasabahRekening.kode_cab_daftar
  oRekNasabah.STATUS_BIAYA_DAFTAR = oRegisterNasabahRekening.status_biaya_daftar
  #oRekNasabah.LNasabahDPLK = oRegisterNasabahRekening.LNasabahDPLK
  oRekNasabah.no_peserta = oRegisterNasabahRekening.no_peserta
  #oRekNasabah.LRekAsuransi = oRegisterNasabahRekening.LRekAsuransi
  #oRekNasabah.rekasuransi_id = oRegisterNasabahRekening.rekasuransi_id
  #oRekNasabah.LOperationCode = oRegisterNasabahRekening.LOperationCode
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
  oRekNasabah.user_id = oRegisterNasabahRekening.user_id
  oRekNasabah.auth_user_id = config.SecurityContext.userid
  oRekNasabah.last_update = config.ModDateTime.Now()
  oRekNasabah.last_terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oRekNasabah.status_anuitas = 'F'
  
  oRekNasabah.status_autodebet = 'F'
  if oRekNasabah.sistem_pembayaran_iuran == 'R':
    oRekNasabah.status_autodebet = 'T'
  
  oRekNasabah.status_asuransi = ikut_asuransi
  
  oRekNasabah.keterangan = oRegisterNasabahRekening.keterangan_registrasi
  oRekNasabah.no_referensi = oRegisterNasabahRekening.no_referensi
  #oRekNasabah.confidential_code = oRegisterNasabahRekening.confidential_code
  #oRekNasabah.collectivity_asuransi = oRegisterNasabahRekening.collectivity_asuransi
  #oRekNasabah.kewajiban_asuransi = oRegisterNasabahRekening.kewajiban_asuransi
  #oRekNasabah.Is_Boleh_Debet = oRegisterNasabahRekening.Is_Boleh_Debet
  #oRekNasabah.bln_tunggakan_asuransi = oRegisterNasabahRekening.bln_tunggakan_asuransi
  oRekNasabah.No_Seri_Buku = oRegisterNasabahRekening.nomor_buku
  oRekNasabah.has_passbook = 'F'
  if not oRekNasabah.No_Seri_Buku in [0,'',None]:
    oRekNasabah.has_passbook = 'T'
  oRekNasabah.IS_DELETED = 0
  
  return oRekNasabah
  
def CreateHistoriBuku(config, oRegisterNasabahRekening):
  oHistoriBuku = config.CreatePObject('HistoriBukuDPLK')
  oHistoriBuku.branch_code = oRegisterNasabahRekening.kode_cab_daftar
  oHistoriBuku.no_peserta = oRegisterNasabahRekening.no_peserta
  oHistoriBuku.no_rekening = oRegisterNasabahRekening.no_rekening
  oHistoriBuku.no_seri_buku = oRegisterNasabahRekening.nomor_buku
  oHistoriBuku.status = 'T'
  oHistoriBuku.tgl_input = config.Now()
  oHistoriBuku.user_id = oRegisterNasabahRekening.user_id

def CreateRegisterPassbook(config, oRegisterNasabahRekening):
  oRegisterpassbook = config.CreatePObject('REGISTERPASSBOOK')
  oRegisterpassbook.Baris_Cetak_Terakhir = 0
  oRegisterpassbook.Halaman_Cetak_Terakhir = 1
  #Id_Register
  #ID_Transaksi
  oRegisterpassbook.Is_Baru_Register = 'T'
  #LRekeningDPLK
  #LTransaksiTerakhir
  oRegisterpassbook.no_rekening = oRegisterNasabahRekening.no_rekening
  oRegisterpassbook.Nomor_Buku_Terakhir = 1
  #oRegisterpassbook.Tanggal_Cetak_Terakhir = config.Now()
  
def CreateRekeningDPLK(config, oRegisterNasabahRekening, kode_paket_investasi, proporsi, no_urut):
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
  oRekeningDPLK.TGL_SRR_AKHIR = moduleapi.DateTimeTupleToFloat(config, oRegisterNasabahRekening.tanggal_register)
  oRekeningDPLK.is_deleted == 'F'
  
  return oRekeningDPLK

def CreateAllAhliWaris(config, oRegisterNasabahRekening, oNasabahDPLK):
  Ls_RegNRAhliWaris = oRegisterNasabahRekening.Ls_RegNRAhliWaris
  Ls_RegNRAhliWaris.First()
  while not Ls_RegNRAhliWaris.EndOfList:
    oRegNRAhliWaris = Ls_RegNRAhliWaris.CurrentElement

    oAhliWaris = config.CreatePObject('AhliWaris')
    #ahliwaris_id
    oAhliWaris.hubungan_keluarga = oRegNRAhliWaris.hubungan_keluarga
    oAhliWaris.jenis_kelamin = oRegNRAhliWaris.jenis_kelamin
    oAhliWaris.keterangan = oRegNRAhliWaris.keterangan
    oAhliWaris.LNasabahDPLK = oNasabahDPLK
    oAhliWaris.nama_lengkap = oRegNRAhliWaris.nama_lengkap
    #no_peserta
    oAhliWaris.nomor_urut_prioritas = oRegNRAhliWaris.nomor_urut_prioritas
    oAhliWaris.status_ahli_waris = oRegNRAhliWaris.status_ahli_waris
    if oRegNRAhliWaris.tanggal_lahir != None:
      oAhliWaris.tanggal_lahir = moduleapi.DateTimeTupleToFloat(config, oRegNRAhliWaris.tanggal_lahir)

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

def CreateRegisterAsuransi(config, oRegisterNasabahRekening):
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
  
def DAFScriptMain(config, parameter, returnpacket):
  # import rpdb2; rpdb2.start_embedded_debugger("000")
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
      raise BaseException,'\n\nPERINGATAN\nPembayaran Biaya Pendaftaran belum dilakukan.'

  config.BeginTransaction()
  try:
    if not oRegisterNasabahRekening.no_peserta_existing in [0, '', None]:
      oNasabahDPLK = oRegisterNasabahRekening.LExistingNasabahDPLK
    else:  
      oNasabahDPLK = CreateNasabahDPLK(config, oRegisterNasabahRekening)
      CreateAllAhliWaris(config, oRegisterNasabahRekening, oNasabahDPLK)
    
    oRekInvDPLK = CreateRekInvDPLK(config, oRegisterNasabahRekening, oRegisterNasabahRekening.ikut_asuransi)
    #CreateAllRekSumber(config, oRegisterNasabahRekening, oRekInvDPLK)
    #CreateRegisterPassbook(config, oRegisterNasabahRekening)
    #CreateHistoriBuku(config, oRegisterNasabahRekening)
    #if oRegisterNasabahRekening.auto_debet == 'T':
    #  CreateRekeningAutoDebet(config, oRegisterNasabahRekening, oRekeningDPLK)
    if oRegisterNasabahRekening.ikut_asuransi == 'T':
      CreateRegisterAsuransi(config, oRegisterNasabahRekening)
    
    sSQL = "SELECT * FROM RegisterNasabahRekPaket WHERE registernr_id = %s" \
      % (oRegisterNasabahRekening.registernr_id)
    rSQL = config.CreateSQL(sSQL).RawResult
    rSQL.First()
    i = 1
    #import rpdb2; rpdb2.start_embedded_debugger('solusi', True, True)
    while not rSQL.Eof:
      oRekeningDPLK = CreateRekeningDPLK(config, oRegisterNasabahRekening, rSQL.kode_paket_investasi, rSQL.proporsi, str(i))      
      CreateDetailAkumPengembangan(config, oNasabahDPLK.no_peserta, oRekeningDPLK.kode_paket_investasi)
      i += 1
      rSQL.Next()
      
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
    oRegisterNasabahRekening.Ls_RegisterNasabahRekPaket.DeleteAllPObjs()
    #oRegisterNasabahRekening.Ls_RegisterNasabahRekSumber.DeleteAllPObjs()
    oRegisterNasabahRekening.Delete()
    #KirimPesertaKeCoreBanking(config, oNasabahDPLK.no_peserta, \
    #oNasabahDPLK.nama_lengkap, oRekeningDPLK.kode_paket_investasi,\
    #oRekeningDPLK.kode_cab_daftar[:3])
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