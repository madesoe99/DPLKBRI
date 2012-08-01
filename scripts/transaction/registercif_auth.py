import sys, time
#sys.path.append('c:/dafapp/dplk/script_modules')
#sys.path.append('c:/dafapp/dplk/scripts/transaksi')
#import moduleapi, transaksiapi, AuthorizeTransaksi

import com.ihsan.foundation.appserver as appserver
import com.ihsan.util.modman as modman 

modman.loadStdModules(globals(),
  [
    "moduleapi",
    "transaksiapi",
    "scripts#transaksi.AuthorizeTransaksi"  
  ]
)

def CreateHistoriAhliWaris(config, oRegisterAhliWaris):
  oNasabahDPLK = oRegisterAhliWaris.LNasabahDPLK
  
  oHistoriAhliWaris = config.CreatePObject('HistoriAhliWaris')
  oHistoriAhliWaris.LNasabahDPLK = oNasabahDPLK
  oHistoriAhliWaris.auth_user_id = config.SecurityContext.userid
  oHistoriAhliWaris.keterangan = oRegisterAhliWaris.keterangan
  oHistoriAhliWaris.no_referensi = oRegisterAhliWaris.no_referensi
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

def UpdateAhliWaris(config, oRegisterAhliWaris):
  oNasabahDPLK = oRegisterAhliWaris.LNasabahDPLK
  
  Ls_AhliWaris = oNasabahDPLK.Ls_AhliWaris
  Ls_AhliWaris.DeleteAllPObjs()

  Ls_RegisterAhliWarisDetail = oRegisterAhliWaris.Ls_RegisterAhliWarisDetail
  while not Ls_RegisterAhliWarisDetail.EndOfList:
    oRegisterAhliWarisDetail = Ls_RegisterAhliWarisDetail.CurrentElement

    oAhliWaris = config.CreatePObject('AhliWaris')
    oAhliWaris.LNasabahDPLK = oNasabahDPLK
    oAhliWaris.hubungan_keluarga = oRegisterAhliWarisDetail.hubungan_keluarga
    oAhliWaris.jenis_kelamin = oRegisterAhliWarisDetail.jenis_kelamin
    oAhliWaris.keterangan = oRegisterAhliWarisDetail.keterangan
    oAhliWaris.nama_lengkap = oRegisterAhliWarisDetail.nama_lengkap
    oAhliWaris.nomor_urut_prioritas = oRegisterAhliWarisDetail.nomor_urut_prioritas
    oAhliWaris.status_ahli_waris = oRegisterAhliWarisDetail.status_ahli_waris
    
    if oRegisterAhliWarisDetail.tanggal_lahir != None:
      oAhliWaris.tanggal_lahir = moduleapi.DateTimeTupleToFloat(config, oRegisterAhliWarisDetail.tanggal_lahir)
    
    Ls_RegisterAhliWarisDetail.Next()
#--

"""
def CountCostVal(config, oRekInvDPLK):
  akum_dana = oRekeningDPLK.akum_dana_pengembangan + \
    oRekeningDPLK.akum_dana_peralihan + oRekeningDPLK.akum_dana_iuran_pst + \
    oRekeningDPLK.akum_dana_iuran_pk

  ## Tambahan By Ade Herman 2011-07-22 ----#
  #  Hitung jumlah perubahan paket selama 1 tahun takwim
  #  jika lebih > 2 maka akan dikenakan biaya sebesar 0.5%

  yearNow = config.FormatDateTime('yyyy', config.Now())
  #config.SendDebugMsg('year...... : '+str(yearNow))
  sSQL = 'select count(hppi.no_peserta) as totPindah from HISTORIPINDAHPAKETINVESTASI hppi ' \
         'where hppi.NO_PESERTA = \'%s\'  '\
          ' and datepart(year,hppi.tanggal_histori) = \'%s\' '\
          % (oRekeningDPLK.no_peserta, yearNow)
  #config.SendDebugMsg('sQL : ' + sSQL)
  rSQL = config.CreateSQL(sSQL).RawResult

  ### End By Ade Herman 2011-07-22 ----

  oP = config.CreatePObjImplProxy('Parameter')
  oP.Key = 'PERSEN_BIAYA_PINDAH_INVESTASI'
  biayaPindah = oP.Numeric_Value
  
  ## Tambahan By Ade Herman 2011-07-25 ---
  if rSQL.totPindah <= 2:
     #config.SendDebugMsg('No Peserta          ...... : '+str(oRekeningDPLK.no_peserta))
     #config.SendDebugMsg('Jumlah Pindah Paket ...... : '+str(rSQL.totPindah))
     biayaPindah = 0
  ## End 2011-07-25

  #set parameter persen biaya pindah paket investasi
  # Sementara di tutup Dulu
  #oP = config.CreatePObjImplProxy('Parameter')
  #oP.Key = 'PERSEN_BIAYA_PINDAH_INVESTASI'
  #return akum_dana * (oP.Numeric_Value / 100)
  return akum_dana * (biayaPindah / 100)
#--
  
def CreateBiayaAdmTransaksi(config, oRegisterPindahPaketInvestasi, oRekInvDPLK):
  oBiayaAdmTransaksi = config.CreatePObject('BiayaAdmTransaksi')
  oBiayaAdmTransaksi.isPindahPaket = 'T'
  oBiayaAdmTransaksi.branch_code = \
    oRegisterPindahPaketInvestasi.LUserApp.LBranchLocation.branch_code
  oBiayaAdmTransaksi.no_peserta = oRegisterPindahPaketInvestasi.no_peserta
  oBiayaAdmTransaksi.isCommitted = 'T'
  oBiayaAdmTransaksi.LPaketInvestasi = oRekeningDPLK.LPaketInvestasi
  oBiayaAdmTransaksi.keterangan = \
    'BiayaAdmTransaksi Pemindahan Paket Investasi peserta %s, %s ke %s' \
    % (oBiayaAdmTransaksi.no_peserta,\
       oRekeningDPLK.kode_paket_investasi,\
       oRegisterPindahPaketInvestasi.kode_paket_investasi)
  
  oBiayaAdmTransaksi.ID_TransactionBatch = \
    oRegisterPindahPaketInvestasi.ID_TransactionBatch
  oBiayaAdmTransaksi.terminal_id = oRegisterPindahPaketInvestasi.terminal_id
  oBiayaAdmTransaksi.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]
  oBiayaAdmTransaksi.user_id = oRegisterPindahPaketInvestasi.user_id
  oBiayaAdmTransaksi.user_id_auth = config.SecurityContext.userid
  oBiayaAdmTransaksi.tgl_sistem = config.Now()
  oBiayaAdmTransaksi.tgl_otorisasi = config.Now()
  #ita-250609-ambil tgl batch, bkn now
  #y,m,d = time.localtime()[:3]
  y, m, d = oRegisterPindahPaketInvestasi.LTransactionBatch.tgl_used[:3]

  oBiayaAdmTransaksi.tgl_transaksi = config.ModLibUtils.EncodeDate(y,m,d)

  moduleapi.TransCostOpr(config, oRekeningDPLK, oBiayaAdmTransaksi, \
    CountCostVal(config,oRekeningDPLK))
#--

def CreateTransaksiPaketInvestasi(config, oRegisterPindahPaketInvestasi, oRekInvDPLK):
  #parameter isNew = 0: minuskan saldo untuk paket investasi lama
  #isNew = 1: munculkan saldo untuk paket investasi baru
  #sebenarnya ada kode khusus untuk jenis pindah paket: F - ubah jenis investasi
  oL = config.CreatePObject('TransaksiDPLK')
  oN = config.CreatePObject('TransaksiDPLK')
  oL.kode_jenis_transaksi = oN.kode_jenis_transaksi = 'F'    
  #DI BAWAH MERUPAKAN KODE LAMA
  #oL = config.CreatePObject('TransaksiDPLKManual')
  #oN = config.CreatePObject('TransaksiDPLKManual')    

  #minuskan saldo, untuk transaksi Lama
  oL.mutasi_iuran_pk = -oRekeningDPLK.akum_dana_iuran_pk
  oL.mutasi_iuran_pst = -oRekeningDPLK.akum_dana_iuran_pst
  oL.mutasi_pengembangan = -oRekeningDPLK.akum_dana_pengembangan
  oL.mutasi_peralihan = -oRekeningDPLK.akum_dana_peralihan
  oL.kode_paket_investasi = oRekeningDPLK.kode_paket_investasi        
  
  #pluskan saldo, untuk transaksi New
  oN.mutasi_iuran_pk = oRekeningDPLK.akum_dana_iuran_pk
  oN.mutasi_iuran_pst = oRekeningDPLK.akum_dana_iuran_pst
  oN.mutasi_pengembangan = oRekeningDPLK.akum_dana_pengembangan
  oN.mutasi_peralihan = oRekeningDPLK.akum_dana_peralihan
  oN.kode_paket_investasi = \
    oRegisterPindahPaketInvestasi.LPaketInvestasi.kode_paket_investasi    

  #assign nilai umum
  oL.keterangan = oN.keterangan = 'Transaksi untuk penyeimbangan pindah paket investasi'
  oL.no_peserta = oN.no_peserta = oRekeningDPLK.no_peserta
  oL.ID_TransactionBatch = oN.ID_TransactionBatch = \
    oRegisterPindahPaketInvestasi.ID_TransactionBatch
  oL.branch_code = oN.branch_code = \
    oRegisterPindahPaketInvestasi.LUserApp.LBranchLocation.branch_code
  oL.isCommitted = oN.isCommitted = 'F'
  oL.user_id = oN.user_id = config.SecurityContext.UserID
  oL.terminal_id = oN.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oL.tgl_sistem = oN.tgl_sistem = config.Now()
  #ita-250609-ambil tgl batch, bkn now
  #y,m,d = time.localtime()[:3]
  y, m, d = oRegisterPindahPaketInvestasi.LTransactionBatch.tgl_used[:3]

  oL.tgl_transaksi = oN.tgl_transaksi = config.ModLibUtils.EncodeDate(y,m,d)
 
  #otorisasi langsung, lama dulu kemudian yang baru
  AuthorizeTransaksi.ApproveOperation(config, 'TransaksiDPLK', oL.ID_Transaksi)  
  AuthorizeTransaksi.ApproveOperation(config, 'TransaksiDPLK', oN.ID_Transaksi)  

  # hapus detail akumulasi paket lama, buat sesuai jenis investasi paket yang baru
  oRekeningDPLK.Ls_DetailAkumPengembangan.DeleteAllPObjs()
  kode_paket = oN.kode_paket_investasi
  sSQLJenisInvest = 'SELECT kode_jns_investasi, maks_proporsi \
  FROM RINCIANPAKETINVESTASI\
  WHERE kode_paket_investasi = \'%s\' ' % (kode_paket)
  rSQLJenisInvest = config.CreateSQL(sSQLJenisInvest).RawResult
  while not rSQLJenisInvest.Eof:
	akum = rSQLJenisInvest.maks_proporsi / 100 * oRekeningDPLK.akum_dana_pengembangan
	oDetailAkum = config.CreatePObject('DetailAkumPengembangan')
	oDetailAkum.no_peserta            = oN.no_peserta
	oDetailAkum.kode_paket_investasi  = kode_paket
	oDetailAkum.kode_jns_investasi    = rSQLJenisInvest.kode_jns_investasi
	oDetailAkum.Nilai_Akumulasi       = akum	
	rSQLJenisInvest.Next()    
#--
"""
  
def CreateHistoriPindahPaketInvestasi(config, oRegisterPindahPaketInvestasi):
  oRekInvDPLK = oRegisterPindahPaketInvestasi.LRekeningDPLK

  oHPPI = config.CreatePObject('HistoriPindahPaketInvestasi')
  oHPPI.LRekeningDPLK = oRekInvDPLK
  oHPPI.auth_user_id = config.SecurityContext.userid
  oHPPI.keterangan = oRegisterPindahPaketInvestasi.keterangan
  oHPPI.no_referensi = oRegisterPindahPaketInvestasi.no_referensi
  oHPPI.tanggal_histori = config.Now()
  oHPPI.terminal_id = oRekInvDPLK.last_terminal_id
  oHPPI.user_id = oRekInvDPLK.user_id

  Ls_RekeningDPLK = oRekInvDPLK.Ls_RekeningDPLK
  Ls_RekeningDPLK.First()
  while not Ls_RekeningDPLK.EndOfList:
    oRekDPLK = Ls_RekeningDPLK.CurrentElement
    if oRekDPLK.is_deleted == 'F':
      oHPPD = config.CreatePObject('HistoriPindahPaketDetail')
      oHPPD.LHistoriPindahPaketInvestasi = oHPPI
      oHPPD.LPaketInvestasi = oRekDPLK.LPaketInvestasi
      oHPPD.LRekeningDPLK = oRekDPLK.LRekeningDPLK
      oHPPD.LRekInvDPLK = oRekDPLK.LRekInvDPLK
      oHPPD.pct_alokasi = oRekDPLK.pct_alokasi
      oHPPD.akum_iuran_pk = oRekDPLK.akum_iuran_pk
      oHPPD.akum_iuran_pst = oRekDPLK.akum_iuran_pst
      oHPPD.akum_iuran_tmb = oRekDPLK.akum_iuran_tmb
      oHPPD.akum_psl = oRekDPLK.akum_psl
      oHPPD.akum_pmb_pk = oRekDPLK.akum_pmb_pk
      oHPPD.akum_pmb_pst = oRekDPLK.akum_pmb_pst
      oHPPD.akum_pmb_tmb = oRekDPLK.akum_pmb_tmb
      oHPPD.akum_pmb_psl = oRekDPLK.akum_pmb_psl
      oHPPD.SRR_AKHIR = oRekDPLK.SRR_AKHIR
      oHPPD.tgl_srr_akhir = oRekDPLK.tgl_srr_akhir
      oHPPD.jml_unit = oRekDPLK.jml_unit
      oHPPD.nilai_unit = oRekDPLK.nilai_unit
      oHPPD.jml_pesan_unit = oRekDPLK.jml_pesan_unit
      oHPPD.jml_redeem_unit = oRekDPLK.jml_redeem_unit
      oHPPD.jml_unit_pk = oRekDPLK.jml_unit_pk
      oHPPD.jml_unit_pst = oRekDPLK.jml_unit_pst
      oHPPD.jml_unit_tmb = oRekDPLK.jml_unit_tmb
      oHPPD.jml_unit_psl = oRekDPLK.jml_unit_psl    

    Ls_RekeningDPLK.Next()

  return oHPPI
#--

def UpdatePindahPaketInvestasi(config, oRegisterPindahPaketInvestasi):
  oRekInvDPLK = oRegisterPindahPaketInvestasi.LRekeningDPLK
  
  #CreateBiayaAdmTransaksi(config, oRegisterPindahPaketInvestasi, oRekInvDPLK)

  #create transaksi manual untuk 'memindahkan' saldo paket investasi lama ke baru
  #CreateTransaksiPaketInvestasi(config, oRegisterPindahPaketInvestasi, oRekInvDPLK) 

  #ubah paket investasi menjadi paket investasi yang baru
  #Ls_RekeningDPLK = oRekInvDPLK.Ls_RekeningDPLK
  #Ls_RekeningDPLK.DeleteAllPObjs()

  existRekDPLK = []
  Ls_RekeningDPLK = oRekInvDPLK.Ls_RekeningDPLK
  Ls_RekeningDPLK.First()
  while not Ls_RekeningDPLK.EndOfList:
    oRekDPLK = Ls_RekeningDPLK.CurrentElement
    if oRekDPLK.is_deleted == 'F':
      oRekDPLK.is_deleted = 'T'    
    existRekDPLK.append(oRekDPLK.nomor_rekening)    
    Ls_RekeningDPLK.Next()

  Ls_RegPindahPaketDetil = oRegisterPindahPaketInvestasi.Ls_RegPindahPaketDetil
  while not Ls_RegPindahPaketDetil.EndOfList:
    oRegPindahPaketDetil = Ls_RegPindahPaketDetil.CurrentElement
    nomor_rekening = "%s_%s" % (oRegPindahPaketDetil.LRegPindahPaket.no_rekening, oRegPindahPaketDetil.kode_paket_investasi)
    if nomor_rekening in existRekDPLK:
      oRekDPLK = config.CreatePObjImplProxy('RekeningDPLK')
      oRekDPLK.Key = nomor_rekening
    else:
      oRekDPLK = config.CreatePObject('RekeningDPLK')
      oRekDPLK.nomor_rekening = nomor_rekening
      oRekDPLK.LRekInvDPLK = oRekInvDPLK
      oRekDPLK.LPaketInvestasi = oRegPindahPaketDetil.LPaketInvestasi
      oRekDPLK.akum_iuran_pk = 0.0
      oRekDPLK.akum_iuran_pst = 0.0
      oRekDPLK.akum_iuran_tmb = 0.0
      oRekDPLK.akum_psl = 0.0
      oRekDPLK.akum_pmb_pk = 0.0
      oRekDPLK.akum_pmb_pst = 0.0
      oRekDPLK.akum_pmb_tmb = 0.0
      oRekDPLK.akum_pmb_psl = 0.0
      oRekDPLK.SRR_AKHIR = 0.0
      oRekDPLK.tgl_srr_akhir = moduleapi.DateTimeTupleToFloat(config, oRegisterPindahPaketInvestasi.tanggal_register)
      oRekDPLK.jml_unit = 0.0
      oRekDPLK.nilai_unit = 0.0
      oRekDPLK.jml_pesan_unit = 0.0
      oRekDPLK.jml_redeem_unit = 0.0
      oRekDPLK.jml_unit_pk = 0.0
      oRekDPLK.jml_unit_pst = 0.0
      oRekDPLK.jml_unit_tmb = 0.0
      oRekDPLK.jml_unit_psl   = 0.0
    
    oRekDPLK.pct_alokasi = oRegPindahPaketDetil.proporsi  
    oRekDPLK.is_deleted = 'F'
    
    Ls_RegPindahPaketDetil.Next()

  """
  #cek jika ikut autodebet atau tidak
  if oRekeningDPLK.status_autodebet == 'T':
    #Edit SI nasabah, ubah giro yang akan didebet
  
    #ambil no rekening autodebet peserta
    oRekeningDPLK.Ls_RekeningAutoDebet.First()
    oRekAutodebet = oRekeningDPLK.Ls_RekeningAutoDebet.CurrentElement

    y,m,d = oRekeningDPLK.tgl_pensiun[:3]
    #transaksiapi.EditSI(config, oRekeningDPLK.no_peserta, oRekAutodebet.no_rekening, \
    #  oRekeningDPLK.LPaketInvestasi.no_giro, '20', '1', oRekeningDPLK.iuran_pst, \
    #  config.ModLibUtils.EncodeDate(y,m,d))
#     isNeedLoginCoreBanking = config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING', \
#     'NeedLoginCoreBanking')
#     if isNeedLoginCoreBanking == 'T':
# 	sessionID = config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING', 'AppName') + \
# 	config.SecurityContext.UserID
# 	param = config.AppObject.CreateValues(['no_peserta', oRekeningDPLK.no_peserta],\
# 	['kode_paket_investasi', oRekeningDPLK.kode_paket_investasi])
# 	try:
# 	    rph = config.AppObject.rexecscript(sessionID, 'remote/UpdateKodePaketInvestasiKiblat', param, 1)
# 	    if rph.FirstRecord.IsErr:
# 		raise Exception, '\nError update kode paket investasi' + str(rph.FirstRecord.ErrMessage)
# 	except:
# 	    raise
  """
  Ls_RegPindahPaketDetil.DeleteAllPObjs()
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
  oHistoriUbahAlamat.alamat_rw = oNasabahDPLK.alamat_rw
  oHistoriUbahAlamat.alamat_kelurahan = oNasabahDPLK.alamat_kelurahan
  oHistoriUbahAlamat.alamat_kecamatan = oNasabahDPLK.alamat_kecamatan
  #oHistoriUbahAlamat.alamat_kota = oNasabahDPLK.alamat_kota
  #oHistoriUbahAlamat.alamat_propinsi = oNasabahDPLK.alamat_propinsi
  oHistoriUbahAlamat.LATKecamatan = oNasabahDPLK.LATKecamatan
  oHistoriUbahAlamat.LATKota = oNasabahDPLK.LATKota
  oHistoriUbahAlamat.LATPropinsi = oNasabahDPLK.LATPropinsi
  oHistoriUbahAlamat.LATKodePos = oNasabahDPLK.LATKodePos
  #oHistoriUbahAlamat.alamat_kode_pos = oNasabahDPLK.alamat_kode_pos
  oHistoriUbahAlamat.alamat_telepon = oNasabahDPLK.alamat_telepon
  oHistoriUbahAlamat.alamat_telepon2 = oNasabahDPLK.alamat_telepon2
  #oHistoriUbahAlamat.alamat_email = oNasabahDPLK.alamat_email

  oHistoriUbahAlamat.alamat_surat_jalan = oNasabahDPLK.alamat_surat_jalan
  oHistoriUbahAlamat.alamat_surat_jalan2 = oNasabahDPLK.alamat_surat_jalan2
  oHistoriUbahAlamat.alamat_surat_rtrw = oNasabahDPLK.alamat_surat_rtrw
  oHistoriUbahAlamat.alamat_surat_rw = oNasabahDPLK.alamat_surat_rw
  oHistoriUbahAlamat.alamat_surat_kelurahan = oNasabahDPLK.alamat_surat_kelurahan
  oHistoriUbahAlamat.alamat_surat_kecamatan = oNasabahDPLK.alamat_surat_kecamatan
  #oHistoriUbahAlamat.alamat_surat_kota = oNasabahDPLK.alamat_surat_kota
  #oHistoriUbahAlamat.alamat_surat_propinsi = oNasabahDPLK.alamat_surat_propinsi
  oHistoriUbahAlamat.LASKecamatan = oNasabahDPLK.LASKecamatan
  oHistoriUbahAlamat.LASKota = oNasabahDPLK.LASKota
  oHistoriUbahAlamat.LASPropinsi = oNasabahDPLK.LASPropinsi
  oHistoriUbahAlamat.LASKodePos = oNasabahDPLK.LASKodePos
  #oHistoriUbahAlamat.alamat_surat_kode_pos = oNasabahDPLK.alamat_surat_kode_pos
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
  oHistoriUbahAlamat.LAKKodePos = oNasabahDPLK.LAKKodePos
  #oHistoriUbahAlamat.alamat_kantor_kode_pos = oNasabahDPLK.alamat_kantor_kode_pos
  oHistoriUbahAlamat.alamat_kantor_telepon = oNasabahDPLK.alamat_kantor_telepon
  oHistoriUbahAlamat.alamat_kantor_telepon2 = oNasabahDPLK.alamat_kantor_telepon2
  
  return oHistoriUbahAlamat
#--

def UpdateAlamat(config, oRegisterUbahAlamat):
  oNasabahDPLK = oRegisterUbahAlamat.LNasabahDPLK
  
  oNasabahDPLK.alamat_jalan = oRegisterUbahAlamat.alamat_jalan
  oNasabahDPLK.alamat_jalan2 = oRegisterUbahAlamat.alamat_jalan2
  oNasabahDPLK.alamat_rtrw = oRegisterUbahAlamat.alamat_rtrw
  oNasabahDPLK.alamat_rw = oRegisterUbahAlamat.alamat_rw
  oNasabahDPLK.alamat_kelurahan = oRegisterUbahAlamat.alamat_kelurahan
  oNasabahDPLK.alamat_kecamatan = oRegisterUbahAlamat.alamat_kecamatan
  #oNasabahDPLK.alamat_kota = oRegisterUbahAlamat.alamat_kota
  #oNasabahDPLK.alamat_propinsi = oRegisterUbahAlamat.alamat_propinsi
  oNasabahDPLK.LATKecamatan = oRegisterUbahAlamat.LATKecamatan
  oNasabahDPLK.LATKota = oRegisterUbahAlamat.LATKota
  oNasabahDPLK.LATPropinsi = oRegisterUbahAlamat.LATPropinsi
  oNasabahDPLK.LATKodePos = oRegisterUbahAlamat.LATKodePos
  #oNasabahDPLK.alamat_kode_pos = oRegisterUbahAlamat.alamat_kode_pos
  oNasabahDPLK.alamat_telepon = oRegisterUbahAlamat.alamat_telepon
  oNasabahDPLK.alamat_telepon2 = oRegisterUbahAlamat.alamat_telepon2
  #oNasabahDPLK.alamat_email = oRegisterUbahAlamat.alamat_email

  oNasabahDPLK.alamat_surat_jalan = oRegisterUbahAlamat.alamat_surat_jalan
  oNasabahDPLK.alamat_surat_jalan2 = oRegisterUbahAlamat.alamat_surat_jalan2
  oNasabahDPLK.alamat_surat_rtrw = oRegisterUbahAlamat.alamat_surat_rtrw
  oNasabahDPLK.alamat_surat_rw = oRegisterUbahAlamat.alamat_surat_rw
  oNasabahDPLK.alamat_surat_kelurahan = oRegisterUbahAlamat.alamat_surat_kelurahan
  oNasabahDPLK.alamat_surat_kecamatan = oRegisterUbahAlamat.alamat_surat_kecamatan
  #oNasabahDPLK.alamat_surat_kota = oRegisterUbahAlamat.alamat_surat_kota
  #oNasabahDPLK.alamat_surat_propinsi = oRegisterUbahAlamat.alamat_surat_propinsi
  oNasabahDPLK.LASKecamatan = oRegisterUbahAlamat.LASKecamatan
  oNasabahDPLK.LASKota = oRegisterUbahAlamat.LASKota
  oNasabahDPLK.LASPropinsi = oRegisterUbahAlamat.LASPropinsi
  oNasabahDPLK.LASKodePos = oRegisterUbahAlamat.LASKodePos
  #oNasabahDPLK.alamat_surat_kode_pos = oRegisterUbahAlamat.alamat_surat_kode_pos
  oNasabahDPLK.alamat_surat_telepon = oRegisterUbahAlamat.alamat_surat_telepon
  oNasabahDPLK.alamat_surat_telepon2 = oRegisterUbahAlamat.alamat_surat_telepon2

  oNasabahDPLK.alamat_kantor_jalan = oRegisterUbahAlamat.alamat_kantor_jalan
  oNasabahDPLK.alamat_kantor_kelurahan = oRegisterUbahAlamat.alamat_kantor_kelurahan
  oNasabahDPLK.alamat_kantor_kecamatan = oRegisterUbahAlamat.alamat_kantor_kecamatan
  #oNasabahDPLK.alamat_kantor_kota = oRegisterUbahAlamat.alamat_kantor_kota
  #oNasabahDPLK.alamat_kantor_propinsi = oRegisterUbahAlamat.alamat_kantor_propinsi
  oNasabahDPLK.LAKKecamatan = oRegisterUbahAlamat.LAKKecamatan
  oNasabahDPLK.LAKKota = oRegisterUbahAlamat.LAKKota
  oNasabahDPLK.LAKPropinsi = oRegisterUbahAlamat.LAKPropinsi
  oNasabahDPLK.LAKKodePos = oRegisterUbahAlamat.LAKKodePos
  #oNasabahDPLK.alamat_kantor_kode_pos = oRegisterUbahAlamat.alamat_kantor_kode_pos
  oNasabahDPLK.alamat_kantor_telepon = oRegisterUbahAlamat.alamat_kantor_telepon
  oNasabahDPLK.alamat_kantor_telepon2 = oRegisterUbahAlamat.alamat_kantor_telepon2
#--

def CreateHistoriIuran(config, oRegisterIuran):
  oRekInvDPLK = oRegisterIuran.LRekeningDPLK
  oHistoriIuran = config.CreatePObject('HistoriIuran')
  
  oHistoriIuran.LRekeningDPLK = oRekInvDPLK
  oHistoriIuran.auth_user_id = config.SecurityContext.userid
  oHistoriIuran.keterangan = oRegisterIuran.keterangan
  oHistoriIuran.no_referensi = oRegisterIuran.no_referensi
  oHistoriIuran.tanggal_histori = config.Now()
  oHistoriIuran.terminal_id = oRekInvDPLK.last_terminal_id
  oHistoriIuran.user_id = oRekInvDPLK.user_id
  oHistoriIuran.iuran_pst = oRekInvDPLK.iuran_pst
  oHistoriIuran.iuran_pk = oRekInvDPLK.iuran_pk
  oHistoriIuran.iuran_tmb = oRekInvDPLK.iuran_tmb
  oHistoriIuran.sistem_pembayaran_iuran = oRekInvDPLK.sistem_pembayaran_iuran
  oHistoriIuran.tgl_penarikan_iuran = oRekInvDPLK.tgl_penarikan_iuran
  oHistoriIuran.reksumber_no = oRekInvDPLK.reksumber_no
  oHistoriIuran.reksumber_nama = oRekInvDPLK.reksumber_nama

  return oHistoriIuran
#--

def UpdateIuran(config, oRegisterIuran):
  oRekInvDPLK = oRegisterIuran.LRekeningDPLK
  
  oRekInvDPLK.iuran_pst = oRegisterIuran.iuran_pst
  oRekInvDPLK.iuran_pk = oRegisterIuran.iuran_pk
  oRekInvDPLK.iuran_tmb = oRegisterIuran.iuran_tmb
  oRekInvDPLK.sistem_pembayaran_iuran = oRegisterIuran.sistem_pembayaran_iuran
  oRekInvDPLK.tgl_penarikan_iuran = oRegisterIuran.tgl_penarikan_iuran
  oRekInvDPLK.reksumber_no = oRegisterIuran.reksumber_no
  oRekInvDPLK.reksumber_nama = oRegisterIuran.reksumber_nama
  
  """
  #cek ikut autodebet atau tidak
  if oNasabahDPLK.LRekeningDPLK.status_autodebet == 'T':
    #Edit SI, ubah jumlah yang akan diautodebet

    #ambil no rekening autodebet peserta
    oRekeningDPLK.Ls_RekeningAutoDebet.First()
    oRekAutodebet = oRekeningDPLK.Ls_RekeningAutoDebet.CurrentElement
     
    y,m,d = oRekeningDPLK.tgl_pensiun[:3]
    #transaksiapi.EditSI(config, oRekeningDPLK.no_peserta, oRekAutodebet.no_rekening, \
    #  oRekeningDPLK.LPaketInvestasi.no_giro, '20', '1', oRekeningDPLK.iuran_pst, \
    #  config.ModLibUtils.EncodeDate(y,m,d))
  """
#--

# otorisasi register anuitas
def UpdateAnuitas(config, oRegisterAnuitas):
  oRegisterAnuitas.LRekeningDPLK.status_anuitas = 'T'
  
  oRA = config.CreatePObject('RekeningAnuitas')
  #oRA.LRekeningDPLK = oRegisterAnuitas.LRekeningDPLK
  oRA.no_rekening = oRegisterAnuitas.no_rekening
  oRA.no_rekening_anuitas = oRegisterAnuitas.no_rekening_anuitas
  oRA.nama_asuransi = oRegisterAnuitas.nama_asuransi
  oRA.no_polis_anuitas = oRegisterAnuitas.no_polis_anuitas
  oRA.nominal_anuitas = oRegisterAnuitas.nominal_anuitas
  oRA.LNasabahDPLK = oRegisterAnuitas.LNasabahDPLK

  y,m,d = oRegisterAnuitas.tgl_pembelian_anuitas[:3]
  oRA.tgl_pembelian_anuitas = config.ModLibUtils.EncodeDate(y,m,d) 

  oRA.tanggal_register = oRegisterAnuitas.tanggal_register
  oRA.keterangan = oRegisterAnuitas.keterangan
  oRA.user_id = oRegisterAnuitas.user_id
  oRA.terminal_id = oRegisterAnuitas.terminal_id
  oRA.tanggal_auth = config.Now()
  oRA.auth_user_id = config.SecurityContext.userid
  oRA.auth_terminal_id = config.SecurityContext.GetSessionInfo()[1]

  oRegisterAnuitas.LRekeningDPLK.LRekeningAnuitas = oRA
  
# otorisasi register autodebt

"""
def GetRekeningAutoDebetByNasabah(config, oNasabahDPLK):
  strSQL = '\
    select no_rekening \
    from RekeningAutoDebet \
    where no_peserta = \'%s\'' \
    % (oNasabahDPLK.no_peserta)
  resSQL = config.CreateSQL(strSQL).RawResult

  oRekeningAutoDebet = config.CreatePObjImplProxy('RekeningAutoDebet')
  oRekeningAutoDebet.SetKey('no_rekening',resSQL.no_rekening)
  oRekeningAutoDebet.SetKey('no_peserta',oNasabahDPLK.no_peserta)

  return oRekeningAutoDebet

def CreateHistoriAutodebet(config, oNasabahDPLK, oRekeningAutoDebet, \
  noReferensi):
  oRekeningDPLK = oNasabahDPLK.LRekeningDPLK

  oHistoriAutodebet = config.CreatePObject('HistoriAutodebet')
  oHistoriAutodebet.no_referensi = noReferensi
  oHistoriAutodebet.no_peserta = oRekeningDPLK.no_peserta
  oHistoriAutodebet.terminal_id = oRekeningDPLK.last_terminal_id
  oHistoriAutodebet.user_id = oRekeningDPLK.user_id
  oHistoriAutodebet.auth_user_id = config.SecurityContext.userid
  oHistoriAutodebet.tanggal_histori = config.Now()

  oHistoriAutodebet.no_rekening = oRekeningAutoDebet.no_rekening
  oHistoriAutodebet.nama_rekening = oRekeningAutoDebet.nama_rekening
  oHistoriAutodebet.tanggal_autodebet = oRekeningAutoDebet.tanggal_autodebet

  return oHistoriAutodebet

def UpdateStatusAutodebetOut(config, oRekeningAutoDebet):
  #cek status login ke CoreBanking  
  isNeedLoginCoreBanking = config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING', \
    'NeedLoginCoreBanking')
  if isNeedLoginCoreBanking == 'T': 
    #cabut dulu status autodebet di CoreBanking    
  
    #ambil info giro di paket investasi 
    oPI = config.CreatePObjImplProxy('PaketInvestasi')
    oPI.Key = oRekeningAutoDebet.LRekeningDPLK.kode_paket_investasi
    
    #remote eksekusi removing SI core banking
    #transaksiapi.RemoveSI(config, oRekeningAutoDebet.no_peserta, \
    #  oRekeningAutoDebet.no_rekening, oPI.no_giro)
  
    #cek juga bila ikut autodebet wasiat ummat
    if oRekeningAutoDebet.LRekeningDPLK.status_wasiat_ummat == 'T':
      pass
      #cabut juga autodebet untuk pembayaran premi wasiat ummat
      #transaksiapi.RemoveSI(config, oRekeningAutoDebet.no_peserta, \
      #  oRekeningAutoDebet.no_rekening, config.SysVarIntf.GetStringSysVar('GIROCOREBANKING', \
      #  'GiroPremi'))
  
  oRekeningAutoDebet.LRekeningDPLK.status_autodebet = 'F'
  oRekeningAutoDebet.Delete()

def UpdateStatusAutodebetIn(config, oRegisterAutoDebet):
  oRegisterAutoDebet.LNasabahDPLK.LRekeningDPLK.status_autodebet = 'T'

  oRekeningAutoDebet = config.CreatePObject('RekeningAutoDebet')
  oRekeningAutoDebet.no_rekening = oRegisterAutoDebet.no_rekening
  oRekeningAutoDebet.nama_rekening = oRegisterAutoDebet.nama_rekening
  oRekeningAutoDebet.tanggal_autodebet = oRegisterAutoDebet.tanggal_autodebet
  oRekeningAutoDebet.LRekeningDPLK = oRegisterAutoDebet.LNasabahDPLK.LRekeningDPLK

  #cek status login ke CoreBanking  
  isNeedLoginCoreBanking = config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING', \
    'NeedLoginCoreBanking')
  if isNeedLoginCoreBanking == 'T':   
    #pasang status autodebet di CoreBanking
    oPI = config.CreatePObjImplProxy('PaketInvestasi')
    oPI.Key = oRekeningAutoDebet.LRekeningDPLK.kode_paket_investasi
    
    #setting untuk tanggal autodebet
    #tanggal pensiun sebagai tanggal kadaluarsa
    y1,m1,d1 = oRekeningAutoDebet.LRekeningDPLK.tgl_pensiun[:3]
    
    #tanggal SI pertama
    y0,m0,d = time.localtime()[:3]
    d0 = oRekeningAutoDebet.tanggal_autodebet
    yReg,mReg = oRegisterAutoDebet.LNasabahDPLK.tgl_registrasi[:2]    
    if (y0 == yReg and m0 == mReg) or (d > d0):
      #tahun dan bulan terdaftar peserta sama dengan tahun dan bulan saat ini
      #berarti ini peserta baru yang sudah membayar iuran pertama saat pendaftaran
      #ambil tanggal autodebet untuk bulan depan
      #ATAU
      #tanggal autodebet bulan ini sudah lewat, ambil tanggal autodebet bulan depan      
      dtNextMonth = config.ModLibUtils.IncMonth(config.ModLibUtils.Now(),1)
      y0,m0 = config.ModLibUtils.DecodeDate(dtNextMonth)[:2]
            
    #remote eksekusi creating New SI iuran core banking
    #transaksiapi.CreateSI(config, oRekeningAutoDebet.no_peserta, \
    #  oRekeningAutoDebet.no_rekening, oPI.no_giro, '1', \
    #  oRekeningAutoDebet.LRekeningDPLK.iuran_pst, \
    #  config.ModLibUtils.EncodeDate(y0,m0,d0), config.ModLibUtils.EncodeDate(y1,m1,d1))
        
    #cek peserta ikut wasiat ummat
    if oRekeningAutoDebet.LRekeningDPLK.status_wasiat_ummat == 'T':
      #ikut wasiat ummat, daftarkan juga autodebet untuk pembayaran premi
      
      #ambil info rekening wasiat ummat 
      oRekeningAutoDebet.LRekeningDPLK.Ls_RekeningWasiatUmmat.First()
      oRWU = oRekeningAutoDebet.LRekeningDPLK.Ls_RekeningWasiatUmmat.CurrentElement
      
      #remote eksekusi creating New SI premi core banking
      #transaksiapi.CreateSI(config, oRekeningAutoDebet.no_peserta, \
      #  oRekeningAutoDebet.no_rekening, config.SysVarIntf.GetStringSysVar('GIROCOREBANKING', \
      #  'GiroPremi'), '2', oRWU.besar_premi, \
      #  config.ModLibUtils.EncodeDate(y0,m0,d0), \
      #  config.ModLibUtils.EncodeDate(y1,m1,d1))      
      
# otorisasi register wasiat ummat
"""

def CreateHistAsuransi(config, oRegisterAsuransi):
  oRekInvDPLK = oRegisterAsuransi.LRekeningDPLK
  oRekAsuransi = oRekInvDPLK.LRekAsuransi
  
  oHistAsuransi = config.CreatePObject('HistAsuransi')

  oHistAsuransi.LRekeningDPLK = oRekInvDPLK
  oHistAsuransi.auth_user_id = config.SecurityContext.userid
  oHistAsuransi.keterangan = oRegisterAsuransi.keterangan
  oHistAsuransi.no_referensi = oRegisterAsuransi.no_referensi
  oHistAsuransi.tanggal_histori = config.Now()
  oHistAsuransi.terminal_id = oRekInvDPLK.last_terminal_id
  oHistAsuransi.user_id = oRekInvDPLK.user_id

  oHistAsuransi.tunggakan_premi = oRekAsuransi.tunggakan_premi
  oHistAsuransi.alasan_berhenti = oRegisterAsuransi.alasan_berhenti
  oHistAsuransi.tgl_akseptasi = moduleapi.DateTimeTupleToFloat(config, oRekAsuransi.tgl_akseptasi)
  oHistAsuransi.tgl_berakhir = config.Now()
  oHistAsuransi.no_polis = oRekAsuransi.no_polis
  oHistAsuransi.besar_premi = oRekAsuransi.besar_premi
  oHistAsuransi.manfaat_asuransi = oRekAsuransi.manfaat_asuransi

  return oHistAsuransi
#--

def UpdateStatusAsuransiOut(config, oRegisterAsuransi):
  oRekInvDPLK = oRegisterAsuransi.LRekeningDPLK
  oRekAsuransi = oRekInvDPLK.LRekAsuransi
  
  oRekInvDPLK.status_asuransi = 'F'
  #oRekInvDPLK.tgl_akseptasi = moduleapi.DateTimeTupleToFloat(config, oRekAsuransi.tgl_akseptasi)
  
  #nullkan kolektibilitas dan kewajiban wasiat ummat
  oRekInvDPLK.collectivity_asuransi = None
  oRekInvDPLK.kewajiban_asuransi = None

  """
  #cek ikut autodebet atau tidak
  if oRekeningDPLK.status_autodebet == 'T':
    #ikut autodebet, cabut autodebet untuk pembayaran premi juga
    
    #cek status login ke CoreBanking  
    isNeedLoginCoreBanking = config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING', \
      'NeedLoginCoreBanking')
    if isNeedLoginCoreBanking == 'T': 
      #cabut dulu status autodebet di CoreBanking    
    
      #ambil info rekening autodebet
      oRekeningDPLK.Ls_RekeningAutoDebet.First()
      oRekeningAutoDebet = \
        oRekeningWasiatUmmat.LRekeningDPLK.Ls_RekeningAutoDebet.CurrentElement
      
      #remote eksekusi removing SI core banking
      #transaksiapi.RemoveSI(config, oRekeningAutoDebet.no_peserta, \
      #  oRekeningAutoDebet.no_rekening, config.SysVarIntf.GetStringSysVar('GIROCOREBANKING', \
      #  'GiroPremi'))
  """
  oRekAsuransi.Delete()
#--

def UpdateStatusAsuransiIn(config, oRegisterAsuransi, parameter):
  oRekAsuransi = config.CreatePObject('RekAsuransi')
  oRekAsuransi.user_id = oRegisterAsuransi.user_id
  oRekAsuransi.auth_user_id = config.SecurityContext.userid
  oRekAsuransi.no_polis = parameter.FirstRecord.no_polis
  oRekAsuransi.besar_premi = parameter.FirstRecord.besar_premi
  oRekAsuransi.manfaat_asuransi = parameter.FirstRecord.manfaat_asuransi
  oRekAsuransi.tgl_akseptasi = parameter.FirstRecord.tgl_akseptasi
  oRekAsuransi.LRekeningDPLK = oRegisterAsuransi.LRekeningDPLK
  
  #set sekaligus tanggal berakhir wasiat ummat = tgl pensiun peserta
  y,m,d = oRekAsuransi.LRekeningDPLK.tgl_pensiun[:3] 
  oRekAsuransi.tgl_berakhir = config.ModLibUtils.EncodeDate(y,m,d)
  
  """ Update RekInvDPLK """
  oRekInvDPLK = oRekAsuransi.LRekeningDPLK
  oRekInvDPLK.LRekAsuransi = oRekAsuransi
  oRekInvDPLK.status_asuransi = 'T'
  #inisialisasi kolektibilitas dan kewajiban wasiat ummat
  oRekInvDPLK.collectivity_asuransi = 'T'
  oRekInvDPLK.kewajiban_asuransi = 0.0
  
  """
  #cek peserta apakah ikut autodebet
  if oRekeningWasiatUmmat.LRekeningDPLK.status_autodebet == 'T':
    #peserta ikut autodebet, daftarkan SI juga untuk premi bulanannya
    
    #cek status login ke CoreBanking  
    isNeedLoginCoreBanking = config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING', \
      'NeedLoginCoreBanking')
    if isNeedLoginCoreBanking == 'T':   
      #pasang status autodebet di CoreBanking
      
      #ambil info rekening autodebet
      oRekeningWasiatUmmat.LRekeningDPLK.Ls_RekeningAutoDebet.First()
      oRekeningAutoDebet = \
        oRekeningWasiatUmmat.LRekeningDPLK.Ls_RekeningAutoDebet.CurrentElement
            
      #setting untuk tanggal autodebet
      #tanggal pensiun sebagai tanggal kadaluarsa
      y1,m1,d1 = oRekeningAutoDebet.LRekeningDPLK.tgl_pensiun[:3]
      
      #tanggal SI pertama
      y0,m0,d = time.localtime()[:3]
      d0 = oRekeningAutoDebet.tanggal_autodebet
      if d > d0:
        #tanggal autodebet bulan ini sudah lewat, ambil tanggal autodebet bulan depan
        dtNextMonth = config.ModLibUtils.IncMonth(config.ModLibUtils.Now(),1)
        y0,m0 = config.ModLibUtils.DecodeDate(dtNextMonth)[:2]
                
      #remote eksekusi creating New SI premi core banking
      #transaksiapi.CreateSI(config, oRekeningAutoDebet.no_peserta, \
      #  oRekeningAutoDebet.no_rekening, config.SysVarIntf.GetStringSysVar('GIROCOREBANKING', \
      #  'GiroPremi'), '2', oRekeningWasiatUmmat.besar_premi, \
      #  config.ModLibUtils.EncodeDate(y0,m0,d0), \
      #  config.ModLibUtils.EncodeDate(y1,m1,d1))
  """
#--

# otorisasi register ubah UbahStatusKerja
def CreateHistoriUbahStatusKerja(config, oRegisterUbahStatusKerja):
  oNasabahDPLK = oRegisterUbahStatusKerja.LNasabahDPLK
  oRekeningDPLK = oRegisterUbahStatusKerja.LRekeningDPLK

  oHistoriUbahStatusKerja = config.CreatePObject('HistoriUbahStatusKerja')

  oHistoriUbahStatusKerja.LNasabahDPLK = oNasabahDPLK
  oHistoriUbahStatusKerja.LRekeningDPLK = oRekeningDPLK
  oHistoriUbahStatusKerja.auth_user_id = config.SecurityContext.userid
  oHistoriUbahStatusKerja.keterangan = oRegisterUbahStatusKerja.keterangan
  oHistoriUbahStatusKerja.no_referensi = oRegisterUbahStatusKerja.no_referensi
  oHistoriUbahStatusKerja.tanggal_histori = config.Now()
  oHistoriUbahStatusKerja.terminal_id = oNasabahDPLK.last_terminal_id
  oHistoriUbahStatusKerja.user_id = oNasabahDPLK.user_id

  oHistoriUbahStatusKerja.jenis_transaksi = oRegisterUbahStatusKerja.jenis_transaksi
  oHistoriUbahStatusKerja.LNasabahDPLKCorporate = oRegisterUbahStatusKerja.LNasabahDPLKCorporate
  
  return oHistoriUbahStatusKerja
#--

"""
def ClearAlamatKantor(oNasabahDPLK):
  oNasabahDPLK.LNasabahDPLKCorporate = None
  oNasabahDPLK.nama_perusahaan = ''
  oNasabahDPLK.LJenisUsaha = None
  oNasabahDPLK.LKepemilikan = None
  oNasabahDPLK.alamat_kantor_jalan = ''
  oNasabahDPLK.alamat_kantor_kelurahan = ''
  oNasabahDPLK.alamat_kantor_kecamatan = ''
  #oNasabahDPLK.alamat_kantor_kota = ''
  #oNasabahDPLK.alamat_kantor_propinsi = ''
  oNasabahDPLK.LAKKecamatan = None
  oNasabahDPLK.LAKKota = None
  oNasabahDPLK.LAKPropinsi = None
  oNasabahDPLK.alamat_kantor_kode_pos = ''
  oNasabahDPLK.alamat_kantor_telepon = ''
  oNasabahDPLK.alamat_kantor_telepon2 = ''
#--
"""

def UpdateUbahStatusKerja(config, oRegisterUbahStatusKerja):
  oRekeningDPLK = oRegisterUbahStatusKerja.LRekeningDPLK

  if oRegisterUbahStatusKerja.jenis_transaksi == 'O':
    #ClearAlamatKantor(oNasabahDPLK)
    oRekeningDPLK.LNasabahDPLKCorporate = None
  else:
    oRekeningDPLK.LNasabahDPLKCorporate = oRegisterUbahStatusKerja.LNasabahDPLKCorporate
    #oNasabahDPLK.nama_perusahaan = oRegisterUbahStatusKerja.LNasabahDPLKCorporate.nama_perusahaan
    #oNasabahDPLK.LJenisUsaha = oRegisterUbahStatusKerja.LNasabahDPLKCorporate.LJenisUsaha
    #oNasabahDPLK.LKepemilikan = oRegisterUbahStatusKerja.LNasabahDPLKCorporate.LKepemilikan
    #oNasabahDPLK.alamat_kantor_jalan = oRegisterUbahStatusKerja.LNasabahDPLKCorporate.alamat_kantor_jalan
    #oNasabahDPLK.alamat_kantor_kelurahan = oRegisterUbahStatusKerja.LNasabahDPLKCorporate.alamat_kantor_kelurahan
    #oNasabahDPLK.alamat_kantor_kecamatan = oRegisterUbahStatusKerja.LNasabahDPLKCorporate.alamat_kantor_kecamatan
    #oNasabahDPLK.alamat_kantor_kota = oRegisterUbahStatusKerja.LNasabahDPLKCorporate.alamat_kantor_kota
    #oNasabahDPLK.alamat_kantor_propinsi = oRegisterUbahStatusKerja.LNasabahDPLKCorporate.alamat_kantor_propinsi
    #oNasabahDPLK.LAKKecamatan = oRegisterUbahStatusKerja.LNasabahDPLKCorporate.LAKKecamatan
    #oNasabahDPLK.LAKKota = oRegisterUbahStatusKerja.LNasabahDPLKCorporate.LAKKota
    #oNasabahDPLK.LAKPropinsi = oRegisterUbahStatusKerja.LNasabahDPLKCorporate.LAKPropinsi
    #oNasabahDPLK.alamat_kantor_kode_pos = oRegisterUbahStatusKerja.LNasabahDPLKCorporate.alamat_kantor_kode_pos
    #oNasabahDPLK.alamat_kantor_telepon = oRegisterUbahStatusKerja.LNasabahDPLKCorporate.alamat_kantor_telepon
    #oNasabahDPLK.alamat_kantor_telepon2 = oRegisterUbahStatusKerja.LNasabahDPLKCorporate.alamat_kantor_telepon2
#--

# otorisasi koreksi data lain-lain (regeditnasabahrekening)
def UpdateNasabahDPLK(config, oRegEditNasabahRekening):
  oNasabahDPLK = config.CreatePObjImplProxy('NasabahDPLK')
  oNasabahDPLK.Key = oRegEditNasabahRekening.no_peserta
  
  #cek perubahan tanggal lahir ada di bagian UpdateRekInvDPLK
  #terkait dengan perubahan tanggal pensiun dan tanggal berakhir autodebet

  oNasabahDPLK.nama_lengkap = oRegEditNasabahRekening.nama_lengkap
  oNasabahDPLK.tempat_lahir = oRegEditNasabahRekening.tempat_lahir
  oNasabahDPLK.tanggal_lahir = oRegEditNasabahRekening.tanggal_lahir
  oNasabahDPLK.jenis_kelamin = oRegEditNasabahRekening.jenis_kelamin
  oNasabahDPLK.golongan_darah = oRegEditNasabahRekening.golongan_darah
  oNasabahDPLK.agama = oRegEditNasabahRekening.agama
  oNasabahDPLK.pendidikan_terakhir = oRegEditNasabahRekening.pendidikan_terakhir  
  oNasabahDPLK.status_perkawinan = oRegEditNasabahRekening.status_perkawinan  
  oNasabahDPLK.LDaerahAsal = oRegEditNasabahRekening.LDaerahAsal
  oNasabahDPLK.kewarganegaraan = oRegEditNasabahRekening.kewarganegaraan
  oNasabahDPLK.no_identitas_diri = oRegEditNasabahRekening.no_identitas_diri
  oNasabahDPLK.tgl_exp_identitas = oRegEditNasabahRekening.tgl_exp_identitas
  oNasabahDPLK.jenis_kartu_identitas = oRegEditNasabahRekening.jenis_kartu_identitas
  oNasabahDPLK.tgl_renewal_identitas = config.ModDateTime.Now()
  
  #oNasabahDPLK.LKelompok = oRegEditNasabahRekening.LKelompok
  oNasabahDPLK.alamat_email = oRegEditNasabahRekening.alamat_email
  oNasabahDPLK.NPWP = oRegEditNasabahRekening.NPWP  
  #oNasabahDPLK.LLDPLain = oRegEditNasabahRekening.LLDPLain
  
  oNasabahDPLK.keterangan = oRegEditNasabahRekening.keterangan
  oNasabahDPLK.nama_perusahaan = oRegEditNasabahRekening.nama_perusahaan
  oNasabahDPLK.LKepemilikan = oRegEditNasabahRekening.LKepemilikan
  
  oNasabahDPLK.user_id = oRegEditNasabahRekening.user_id
  oNasabahDPLK.terminal_id = oRegEditNasabahRekening.terminal_id
  oNasabahDPLK.auth_user_id = config.SecurityContext.userid
  oNasabahDPLK.last_terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oNasabahDPLK.last_update = config.ModDateTime.Now()
  oNasabahDPLK.isCommitted = 'T'
  oNasabahDPLK.operation_code = 'F'

  return oNasabahDPLK
#--

def UpdateRekInvDPLK(config, oRegEditRekening):
  oRekInvDPLK = config.CreatePObjImplProxy('RekInvDPLK')
  oRekInvDPLK.Key = oRegEditRekening.no_rekening
  
  oRekInvDPLK.LSumberDana = oRegEditRekening.LSumberDana
  oRekInvDPLK.usia_pensiun = oRegEditRekening.usia_pensiun
  oRekInvDPLK.tgl_pensiun = oRegEditRekening.tgl_pensiun
  oRekInvDPLK.tgl_pensiun_dipercepat = oRegEditRekening.tgl_pensiun_dipercepat
  oRekInvDPLK.LTujuanBukaRekening = oRegEditRekening.LTujuanBukaRekening
  #oRekInvDPLK.tujuan_pembukaan_rekening = oRegEditRekening.tujuan_pembukaan_rekening
  oRekInvDPLK.kirim_statemen = oRegEditRekening.kirim_statemen
  oRekInvDPLK.confidential_code = oRegEditRekening.confidential_code
  oRekInvDPLK.keterangan = oRegEditRekening.keterangan
  
  oRekInvDPLK.ispesertapengalihan = oRegEditRekening.ispesertapengalihan
  oRekInvDPLK.LKelompok = oRegEditRekening.LKelompok
  oRekInvDPLK.LLDPLain = oRegEditRekening.LLDPLain
  
  return oRekInvDPLK
#--

def UpdateKYCNasabah(config, oRegEditKYCNasabah):
  oNasabahDPLK = oRegEditKYCNasabah.LNasabahDPLK
  
  oNasabahDPLK.ibu_kandung = oRegEditKYCNasabah.ibu_kandung
  oNasabahDPLK.beneficial_owner = oRegEditKYCNasabah.beneficial_owner
  oNasabahDPLK.penghasilan_tetap = oRegEditKYCNasabah.penghasilan_tetap
  oNasabahDPLK.penghasilan_tambahan = oRegEditKYCNasabah.penghasilan_tambahan
  oNasabahDPLK.LNegara = oRegEditKYCNasabah.LNegara
  oNasabahDPLK.LJenisUsaha = oRegEditKYCNasabah.LJenisUsaha
  oNasabahDPLK.LJenisPekerjaan = oRegEditKYCNasabah.LJenisPekerjaan
  oNasabahDPLK.LJenisPekerjaanDetail = oRegEditKYCNasabah.LJenisPekerjaanDetail
  oNasabahDPLK.status_pep = oRegEditKYCNasabah.status_pep
  oNasabahDPLK.keterangan_pep = oRegEditKYCNasabah.keterangan_pep
  oNasabahDPLK.risk_flag_request = oRegEditKYCNasabah.risk_flag_request
  oNasabahDPLK.status_risk_request = oRegEditKYCNasabah.status_risk_request
  
  oNasabahDPLK.HUBUNGAN_KELENGKAPAN = oRegEditKYCNasabah.HUBUNGAN_KELENGKAPAN
  oNasabahDPLK.nama_orang_tua = oRegEditKYCNasabah.nama_orang_tua
  oNasabahDPLK.LJenisUsahaOrtu = oRegEditKYCNasabah.LJenisUsahaOrtu
  oNasabahDPLK.LJenisPekerjaanOrtu = oRegEditKYCNasabah.LJenisPekerjaanOrtu
  oNasabahDPLK.LJenisPekerjaanDetailOrtu = oRegEditKYCNasabah.LJenisPekerjaanDetailOrtu
  oNasabahDPLK.nama_perusahaan_ortu = oRegEditKYCNasabah.nama_perusahaan_ortu
  oNasabahDPLK.penghasilan_orang_tua = oRegEditKYCNasabah.penghasilan_orang_tua
  
  #oNasabahDPLK.limit_credit = oRegEditKYCNasabah.limit_credit
  #oNasabahDPLK.limit_debit = oRegEditKYCNasabah.limit_debit
  #oNasabahDPLK.limit_frek_credit = oRegEditKYCNasabah.limit_frek_credit
  #oNasabahDPLK.limit_frek_debit = oRegEditKYCNasabah.limit_frek_debit
  
def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  id = parameter.FirstRecord.id

  oRegisterCIF = config.CreatePObjImplProxy('RegisterCIF')
  oRegisterCIF.Key = id

  config.BeginTransaction()
  try:
    if oRegisterCIF.kode_jenis_registercif == 'W':
      oRegisterAhliWaris = oRegisterCIF.CastAs('RegisterAhliWaris')
      CreateHistoriAhliWaris(config, oRegisterAhliWaris)
      UpdateAhliWaris(config, oRegisterAhliWaris)
      oRegisterAhliWaris.Ls_RegisterAhliWarisDetail.DeleteAllPObjs()

    elif oRegisterCIF.kode_jenis_registercif == 'P':
      oRegisterPindahPaketInvestasi = oRegisterCIF.CastAs('RegisterPindahPaketInvestasi')
      CreateHistoriPindahPaketInvestasi(config, oRegisterPindahPaketInvestasi)
      UpdatePindahPaketInvestasi(config, oRegisterPindahPaketInvestasi)
      
    elif oRegisterCIF.kode_jenis_registercif == 'A':
      oRegisterUbahAlamat = oRegisterCIF.CastAs('RegisterUbahAlamat')
      CreateHistoriUbahAlamat(config, oRegisterUbahAlamat)
      UpdateAlamat(config, oRegisterUbahAlamat)
      
    elif oRegisterCIF.kode_jenis_registercif == 'I':
      oRegisterIuran = oRegisterCIF.CastAs('RegisterIuran')
      CreateHistoriIuran(config, oRegisterIuran)
      UpdateIuran(config, oRegisterIuran)
      
    elif oRegisterCIF.kode_jenis_registercif == 'N':
      oRegisterAnuitas = oRegisterCIF.CastAs('RegisterAnuitas')
      UpdateAnuitas(config, oRegisterAnuitas)
    
    elif oRegisterCIF.kode_jenis_registercif == 'D':
      """
      oRegisterAutoDebet = oRegisterCIF.CastAs('RegisterAutoDebet')
      if oRegisterAutoDebet.jenis_transaksi == 'O':
        # berhenti autodebet
        oRekeningAutoDebet = GetRekeningAutoDebetByNasabah(config, oNasabahDPLK)
        
        noReferensi = oRegisterAutoDebet.no_referensi
        CreateHistoriAutodebet(config, oNasabahDPLK, oRekeningAutoDebet, \
          noReferensi)
        UpdateStatusAutodebetOut(config, oRekeningAutoDebet)
      else:
        UpdateStatusAutodebetIn(config, oRegisterAutoDebet)
      """
      pass
    
    elif oRegisterCIF.kode_jenis_registercif == 'U':
      oRegisterAsuransi = oRegisterCIF.CastAs('RegisterAsuransi')
      if oRegisterAsuransi.jenis_transaksi == 'O':
        CreateHistAsuransi(config, oRegisterAsuransi)
        UpdateStatusAsuransiOut(config, oRegisterAsuransi)
      else:
        UpdateStatusAsuransiIn(config, oRegisterAsuransi, parameter)

    elif oRegisterCIF.kode_jenis_registercif == 'K':
      oRegisterUbahStatusKerja = oRegisterCIF.CastAs('RegisterUbahStatusKerja')
      if oRegisterUbahStatusKerja.jenis_transaksi == 'O':
        # berhenti UbahStatusKerja
        CreateHistoriUbahStatusKerja(config, oRegisterUbahStatusKerja)
      UpdateUbahStatusKerja(config, oRegisterUbahStatusKerja)

    elif oRegisterCIF.kode_jenis_registercif == 'Z':
      oRegEditNasabahRekening = oRegisterCIF.CastAs('RegEditNasabahRekening')
      UpdateNasabahDPLK(config, oRegEditNasabahRekening)

    elif oRegisterCIF.kode_jenis_registercif == 'Y':
      oRegEditKYCNasabah = oRegisterCIF.CastAs('RegEditKYCNasabah')
      UpdateKYCNasabah(config, oRegEditKYCNasabah)
    
    elif oRegisterCIF.kode_jenis_registercif == 'X':
      oRegEditRekening = oRegisterCIF.CastAs('RegEditRekening')
      UpdateRekInvDPLK(config, oRegEditRekening)

    else:
      # hanya untuk kepentingan debug
      raise Exception,'\n\nPERINGATAN\nKode jenis Register CIF tidak dikenali.'

    oRegisterCIF.Delete()
    config.Commit()

  except:
    config.Rollback()
    raise

  return 1