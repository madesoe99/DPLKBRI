import sys, string, time
import com.ihsan.util.modman as modman
import com.ihsan.foundation.appserver as appserver

#sys.path.append('c:/dafapp/dplk/script_modules/')
#import moduleapi

moduleapi = modman.getModule(appserver.ActiveConfig, 'moduleapi')

dictRiskFlag = {'L' : 'Low', 'H' : 'High' , 'M' : 'Moderate' , '' : ''}

def OnSetDataEx(uideflist, params):
  config = uideflist.Config
  uipRegisterNasabahRekening = uideflist.uipRegisterNasabahRekening
  rec = uipRegisterNasabahRekening.Dataset.AddRecord()
  
  branch_code = config.SecurityContext.GetUserInfo()[4]
  userid = config.SecurityContext.userid
  
  oUser = config.CreatePObjImplProxy('UserApp')
  oUser.Key = userid

  #checking grup administrator
  groupID = config.SecurityContext.GroupID
  if string.upper(userid) == 'ROOT' or \
    string.upper(str(groupID)) == 'ADMIN' or oUser.NoLimitLocation == 'T':
    #user root or administrator, set isRegisteredByAdmin True
    rec.isRegisteredByAdmin = 'T'
  else:
    #bukan root or admin user
    rec.isRegisteredByAdmin = 'F'

  rec.no_peserta = 'temp'
  rec.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  rec.tanggal_register = config.Now()
  rec.user_id = userid

  oBranch = config.CreatePObjImplProxy('BranchLocation')
  oBranch.Key = branch_code
  rec.SetFieldByName('LBranchLocation.branch_code',branch_code)
  rec.SetFieldByName('LBranchLocation.BranchName',oBranch.BranchName)
  #rec.kode_cab_daftar = branch_code

  rec.nolimitlocation = oUser.NoLimitLocation
  rec.status_biaya_daftar = 'T'
  rec.ikut_asuransi = 'F'
  rec.kirim_statemen = 'N'
  rec.iuran_pk = 0.0
  rec.iuran_pst = 0.0
  rec.iuran_tmb = 0.0
  rec.kewarganegaraan = '1'
  
  #set parameter
  recP = uideflist.uipParameter.Dataset.AddRecord()
  oP = config.CreatePObjImplProxy('Parameter')
  oP.Key = 'MIN_JML_IURAN_PST'
  recP.MIN_JML_IURAN_PST = oP.Numeric_Value
  
  oP.Key = 'MIN_JML_IURAN_PK'
  recP.MIN_JML_IURAN_PK = oP.Numeric_Value

  oP.Key = 'MIN_JML_IURAN_TMB'
  recP.MIN_JML_IURAN_TMB = oP.Numeric_Value

  oP.Key = 'IS_ONLY_MIN_JML_IURAN_PST'
  recP.IS_ONLY_MIN_JML_IURAN_PST = int(oP.Numeric_Value)

  oP.Key = 'MIN_SELISIH_TGL_DAFTAR-PENSIUN'
  recP.MIN_SELISIH_TGL_DAFTAR_PENSIUN = oP.Numeric_Value

  oP.Key = 'DEFAULT_NEGARA'
  rec.SetFieldByName("LNegara.kode_negara", oP.Numeric_Value)
  rec.SetFieldByName("LNegara.nama_negara", oP.Varchar_Value)

  # set risk flag negara
  oNegara = config.CreatePObjImplProxy('Negara')
  oNegara.key = oP.Numeric_Value  
  rec.SetFieldByName("LNegara.risk_flag", dictRiskFlag[oNegara.Risk_Flag or ''])

  fr = params.FirstRecord
  if fr not in ['', 0, None]:
    if fr.mode == "exist_nasabah":
      oND = config.CreatePObjImplProxy("NasabahDPLK")
      oND.Key = fr.no_peserta
    
      #import rpdb2; rpdb2.start_embedded_debugger("solusi", True, True)
      rec.no_peserta = oND.no_peserta
      rec.no_peserta_existing = oND.no_peserta
      rec.SetFieldByName("LExistingNasabahDPLK.no_peserta", oND.no_peserta)
      rec.SetFieldByName("LExistingNasabahDPLK.nama_lengkap", oND.nama_lengkap)

      rec.ibu_kandung = oND.ibu_kandung
      rec.nama_lengkap = oND.nama_lengkap
      rec.tempat_lahir = oND.tempat_lahir
      rec.SetFieldByName("tanggal_lahir", oND.tanggal_lahir)
      rec.jenis_kelamin = oND.jenis_kelamin  
      rec.golongan_darah = oND.golongan_darah
      rec.agama = oND.agama
      rec.pendidikan_terakhir = oND.pendidikan_terakhir
      rec.status_perkawinan = oND.status_perkawinan
      
      if not oND.LDaerahAsal.IsNull:
        rec.SetFieldByName("LDaerahAsal.kode_propinsi", oND.LDaerahAsal.kode_propinsi)
        rec.SetFieldByName("LDaerahAsal.nama_propinsi", oND.LDaerahAsal.nama_propinsi)
      
      rec.kewarganegaraan = oND.kewarganegaraan      
      if not oND.LNegara.IsNull:
        rec.SetFieldByName("LNegara.kode_negara", oND.LNegara.kode_negara)
        rec.SetFieldByName("LNegara.nama_negara", oND.LNegara.nama_negara)
      
      rec.jenis_kartu_identitas = oND.jenis_kartu_identitas
      rec.no_identitas_diri = oND.no_identitas_diri
      rec.tgl_exp_identitas = oND.tgl_exp_identitas
      
      rec.alamat_email = oND.alamat_email
      rec.NPWP = oND.NPWP
      rec.penghasilan_tetap = oND.penghasilan_tetap
      rec.penghasilan_tambahan = oND.penghasilan_tambahan
      
      rec.HUBUNGAN_KELENGKAPAN = oND.HUBUNGAN_KELENGKAPAN
      rec.nama_orang_tua = oND.nama_orang_tua
      rec.nama_perusahaan_ortu = oND.nama_perusahaan_ortu
      
      if not oND.LJenisUsahaOrtu.IsNull:
        rec.SetFieldByName("LJenisUsahaOrtu.kode_jenis_usaha", oND.LJenisUsahaOrtu.kode_jenis_usaha)
        rec.SetFieldByName("LJenisUsahaOrtu.nama_jenis_usaha", oND.LJenisUsahaOrtu.nama_jenis_usaha)
        rec.SetFieldByName("LJenisUsahaOrtu.risk_flag", oND.LJenisUsahaOrtu.risk_flag)
      
      if not oND.LJenisPekerjaanOrtu.IsNull:
        rec.SetFieldByName("LJenisPekerjaanOrtu.kode_jenis_pekerjaan", oND.LJenisPekerjaanOrtu.kode_jenis_pekerjaan)
        rec.SetFieldByName("LJenisPekerjaanOrtu.nama_jenis_pekerjaan", oND.LJenisPekerjaanOrtu.nama_jenis_pekerjaan)
        rec.SetFieldByName("LJenisPekerjaanOrtu.risk_flag", oND.LJenisPekerjaanOrtu.risk_flag)
      
      if not oND.LJenisPekerjaanDetailOrtu.IsNull:
        rec.SetFieldByName("LJenisPekerjaanDetailOrtu.kode_jenis_jabatan", oND.LJenisPekerjaanDetailOrtu.kode_jenis_jabatan)
        rec.SetFieldByName("LJenisPekerjaanDetailOrtu.LJenisJabatan.nama_jenis_jabatan", oND.LJenisPekerjaanDetailOrtu.LJenisJabatan.nama_jenis_jabatan)
        rec.SetFieldByName("LJenisPekerjaanDetailOrtu.risk_flag", oND.LJenisPekerjaanDetailOrtu.risk_flag)
      
      rec.penghasilan_orang_tua = oND.penghasilan_orang_tua
      
      rec.alamat_jalan = oND.alamat_jalan
      rec.alamat_jalan2 = oND.alamat_jalan2
      
      #rec.alamat_kode_pos = oND.alamat_kode_pos
      if not oND.LATKodePos.IsNull:
        rec.SetFieldByName("LATKodePos.id_kodepos", oND.LATKodePos.id_kodepos)
        rec.SetFieldByName("LATKodePos.kode_pos", oND.LATKodePos.kode_pos)
      
      #rec.alamat_propinsi = oND.alamat_propinsi
      if not oND.LATPropinsi.IsNull:
        rec.SetFieldByName("LATPropinsi.kode_propinsi", oND.LATPropinsi.kode_propinsi)
        rec.SetFieldByName("LATPropinsi.nama_propinsi", oND.LATPropinsi.nama_propinsi)
      
      #rec.alamat_kota = oND.alamat_kota
      if not oND.LATKota.IsNull:
        rec.SetFieldByName("LATKota.kode_kota", oND.LATKota.kode_kota)
        rec.SetFieldByName("LATKota.nama_kota", oND.LATKota.nama_kota)
      
      rec.alamat_kecamatan = oND.alamat_kecamatan
      if not oND.LATKecamatan.IsNull:
        rec.SetFieldByName("LATKecamatan.kode_kecamatan", oND.LATKecamatan.kode_kecamatan)
        rec.SetFieldByName("LATKecamatan.nama_kecamatan", oND.LATKecamatan.nama_kecamatan)
      
      rec.alamat_kelurahan = oND.alamat_kelurahan
      rec.alamat_rtrw = oND.alamat_rtrw
      rec.alamat_rw = oND.alamat_rw
      rec.alamat_telepon = oND.alamat_telepon
      rec.alamat_telepon2 = oND.alamat_telepon2
      
      rec.alamat_surat_jalan = oND.alamat_surat_jalan
      rec.alamat_surat_jalan2 = oND.alamat_surat_jalan2

      #rec.alamat_surat_kode_pos = oND.alamat_surat_kode_pos
      if not oND.LASKodePos.IsNull:
        rec.SetFieldByName("LASKodePos.id_kodepos", oND.LASKodePos.id_kodepos)
        rec.SetFieldByName("LASKodePos.kode_pos", oND.LASKodePos.kode_pos)
      
      #rec.alamat_surat_propinsi = oND.alamat_surat_propinsi
      if not oND.LASPropinsi.IsNull:
        rec.SetFieldByName("LASPropinsi.kode_propinsi", oND.LASPropinsi.kode_propinsi)
        rec.SetFieldByName("LASPropinsi.nama_propinsi", oND.LASPropinsi.nama_propinsi)
      
      #rec.alamat_surat_kota = oND.alamat_surat_kota
      if not oND.LASKota.IsNull:
        rec.SetFieldByName("LASKota.kode_kota", oND.LASKota.kode_kota)
        rec.SetFieldByName("LASKota.nama_kota", oND.LASKota.nama_kota)
      
      rec.alamat_surat_kecamatan = oND.alamat_surat_kecamatan
      if not oND.LASKecamatan.IsNull:
        rec.SetFieldByName("LASKecamatan.kode_kecamatan", oND.LASKecamatan.kode_kecamatan)
        rec.SetFieldByName("LASKecamatan.nama_kecamatan", oND.LASKecamatan.nama_kecamatan)
      
      rec.alamat_surat_kelurahan = oND.alamat_surat_kelurahan
      rec.alamat_surat_rtrw = oND.alamat_surat_rtrw
      rec.alamat_surat_rw = oND.alamat_surat_rw
      rec.alamat_surat_telepon = oND.alamat_surat_telepon
      rec.alamat_surat_telepon2 = oND.alamat_surat_telepon2
      
      if not oND.LJenisPekerjaan.IsNull:
        rec.SetFieldByName("LJenisPekerjaan.kode_jenis_pekerjaan", oND.LJenisPekerjaan.kode_jenis_pekerjaan)
        rec.SetFieldByName("LJenisPekerjaan.nama_jenis_pekerjaan", oND.LJenisPekerjaan.nama_jenis_pekerjaan)
        rec.SetFieldByName("LJenisPekerjaan.risk_flag", oND.LJenisPekerjaan.risk_flag)
      
      if not oND.LJenisPekerjaanDetail.IsNull:
        rec.SetFieldByName("LJenisPekerjaanDetail.kode_jenis_jabatan", oND.LJenisPekerjaanDetail.kode_jenis_jabatan)
        rec.SetFieldByName("LJenisPekerjaanDetail.LJenisJabatan.nama_jenis_jabatan", oND.LJenisPekerjaanDetail.LJenisJabatan.nama_jenis_jabatan)
        rec.SetFieldByName("LJenisPekerjaanDetail.risk_flag", oND.LJenisPekerjaanDetail.risk_flag)
      
      rec.status_pep = oND.status_pep
      rec.keterangan_pep = oND.keterangan_pep
      rec.nama_perusahaan = oND.nama_perusahaan
      
      if not oND.LJenisUsaha.IsNull:
        rec.SetFieldByName("LJenisUsaha.kode_jenis_usaha", oND.LJenisUsaha.kode_jenis_usaha)
        rec.SetFieldByName("LJenisUsaha.nama_jenis_usaha", oND.LJenisUsaha.nama_jenis_usaha)
        rec.SetFieldByName("LJenisUsaha.risk_flag", oND.LJenisUsaha.risk_flag)
      
      if not oND.LKepemilikan.IsNull:
        rec.SetFieldByName("LKepemilikan.kode_pemilikan", oND.LKepemilikan.kode_pemilikan)
        rec.SetFieldByName("LKepemilikan.keterangan", oND.LKepemilikan.keterangan)      
      
      rec.alamat_kantor_jalan = oND.alamat_kantor_jalan
      #rec.alamat_kantor_kode_pos = oND.alamat_kantor_kode_pos
      if not oND.LAKKodePos.IsNull:
        rec.SetFieldByName("LAKKodePos.id_kodepos", oND.LAKKodePos.id_kodepos)
        rec.SetFieldByName("LAKKodePos.kode_pos", oND.LAKKodePos.kode_pos)
      
      #rec.alamat_kantor_propinsi = oND.alamat_kantor_propinsi
      if not oND.LAKPropinsi.IsNull:
        rec.SetFieldByName("LAKPropinsi.kode_propinsi", oND.LAKPropinsi.kode_propinsi)
        rec.SetFieldByName("LAKPropinsi.nama_propinsi", oND.LAKPropinsi.nama_propinsi)
      
      #rec.alamat_kantor_kota = oND.alamat_kantor_kota
      if not oND.LAKKota.IsNull:
        rec.SetFieldByName("LAKKota.kode_kota", oND.LAKKota.kode_kota)
        rec.SetFieldByName("LAKKota.nama_kota", oND.LAKKota.nama_kota)
      
      rec.alamat_kantor_kecamatan = oND.alamat_kantor_kecamatan
      if not oND.LAKKecamatan.IsNull:
        rec.SetFieldByName("LAKKecamatan.kode_kecamatan", oND.LAKKecamatan.kode_kecamatan)
        rec.SetFieldByName("LAKKecamatan.nama_kecamatan", oND.LAKKecamatan.nama_kecamatan)
      
      rec.alamat_kantor_kelurahan = oND.alamat_kantor_kelurahan
      rec.alamat_kantor_telepon = oND.alamat_kantor_telepon
      rec.alamat_kantor_telepon2 = oND.alamat_kantor_telepon2
      
      rec.REFR_NAMA = oND.REFR_NAMA
      rec.REFR_ACCNO = oND.REFR_ACCNO
      rec.REFR_UKER = oND.REFR_UKER
      rec.no_referensi = oND.no_referensi
      #rec.keterangan_registrasi = oND.keterangan
      
      #Ls_RegNRAhliWaris vs Ls_AhliWaris
      Ls_AhliWaris = oND.Ls_AhliWaris
      Ls_AhliWaris.First()
      while not Ls_AhliWaris.EndOfList:
        oAW = Ls_AhliWaris.CurrentElement
        
        regAW = uideflist.uipRegNRAhliWaris.Dataset.AddRecord()
        #regAW.LRegisterNasabahRekening = rec
        regAW.nomor_urut_prioritas = oAW.nomor_urut_prioritas
        regAW.nama_lengkap = oAW.nama_lengkap
        #regAW.status_ahli_waris = oAW.status_ahli_waris
        regAW.SetFieldByName('tanggal_lahir', oAW.tanggal_lahir)
        regAW.jenis_kelamin = oAW.jenis_kelamin
        regAW.hubungan_keluarga = oAW.hubungan_keluarga
        regAW.keterangan = oAW.keterangan
        
        Ls_AhliWaris.Next()
      
  sSQL = "SELECT * FROM paketinvestasi"
  rSQL = config.CreateSQL(sSQL).RawResult
  while not rSQL.Eof:
    recTmpPI = uideflist.uipTmpPaket.Dataset.AddRecord()
    recTmpPI.kode_pi = rSQL.kode_paket_investasi
    recTmpPI.nama_pi = rSQL.nama_paket_investasi
    rSQL.Next()
  
  return 0

def FormEndProcessData(uideflist, datapacket):
  config = uideflist.Config
  
  oRegisterNasabahRekening = uideflist.uipRegisterNasabahRekening.ActiveInstance
  kode_cab_daftar = oRegisterNasabahRekening.kode_cab_daftar

  strCounter = moduleapi.GetCounterNumber(config, 'REKINVDPLK', kode_cab_daftar)
  no_rekening = '%s%08d' % (moduleapi.TruncateString(kode_cab_daftar, 3), strCounter)

  sReturnMsg = "Peserta Baru telah siap didaftarkan..."
  no_peserta = oRegisterNasabahRekening.no_peserta_existing
  if oRegisterNasabahRekening.no_peserta_existing in ['', 0, None]:
    strCounter = moduleapi.GetCounterNumber(config, 'NASABAHDPLK', kode_cab_daftar)
    no_peserta = '%s%08d' % (moduleapi.TruncateString(kode_cab_daftar, 3), strCounter)
  else:
    sReturnMsg = "Account DPLK baru telah didaftarkan untuk peserta terdaftar..."

  uideflist.PostReturnMessage = \
    '''%s\n\n
    CIF Peserta: %s a/n. %s\n
    Nomor Account DPLK: %s'''\
    % (sReturnMsg, no_peserta, oRegisterNasabahRekening.nama_lengkap, no_rekening)

  oRegisterNasabahRekening.no_peserta = no_peserta
  oRegisterNasabahRekening.no_rekening = no_rekening

  # show message
  return 3

def uipRegisterNasabahRekeningApplyRow(sender, oData):
  config = sender.UIDefList.Config
  rec = sender.ActiveRecord
  
  # Tambahan By Ade Herman 2011-12-05'
  #if oData.pekerjaan == '5':
  #   oData.kode_jenis_usaha = '12'
  #   oData.kode_pemilikan = '5'
  #---- End -------
     
  if rec.alamat_telepon in ['', None]:
    raise Exception, '\n\nPERINGATAN' \
      '\nPada saat mengisi Alamat Tempat Tinggal,'\
      '\nTelepon 1 & Telepon 2 (Rumah/Hp) Mohon diisi dahulu.'

  #if rec.no_referensi in ['', None]:
  #  raise Exception, '\n\nPERINGATAN' \
  #    '\nNomor Referensi belum terdefinisi! Mohon isi dahulu.'

  #if len(rec.no_referensi) <> 8:
  #  raise Exception, '\n\nPERINGATAN' \
  #    '\nNomor Referensi Di isi dengan `.'

  if rec.jenis_kelamin in ['', None]:
    raise Exception, '\n\nPERINGATAN' \
      '\nJenis Kelamin belum terdefinisi! Mohon isi dahulu.'

  if rec.usia_pensiun in [None,''] or \
    (rec.usia_pensiun < 45 or rec.usia_pensiun > 65):
    raise Exception, '\n\nPERINGATAN' \
      '\nUsia Pensiun tidak valid! Usia Pensiun yang diperbolehkan antara 45 - 65 tahun.'
      
  #cek usia sekarang peserta dan keikutsertaan wasiat ummat
  y,m,d = time.localtime()[:3]
  oParameter = config.CreatePObjImplProxy('Parameter')
  oParameter.Key = 'JUMLAH_HARI_SETAHUN'
  JumlahHariSetahun = oParameter.Numeric_Value
  usiaPeserta = (config.ModDateTime.EncodeDate(y,m,d) - rec.tanggal_lahir) /JumlahHariSetahun
  
  if rec.ikut_asuransi == 'T' and usiaPeserta > 55.0:
    raise Exception, '\n\nPERINGATAN' \
      '\nStatus Ikut Asuransi tidak valid! Usia peserta Ikut '\
      'Asuransi hanya diperbolehkan dibawah usia 55 tahun.'

  #oData.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oData.kode_cab_daftar = rec.GetFieldByName('LBranchLocation.branch_code')
  
def cekPeserta(config, params, results):
  params = params.FirstRecord
  status = results.CreateValues(
    ['success', False],
    ['message', ''],
    ['no_peserta', ''],
    ['registernr_id', 0],
    ['is_otor', False]
  )
  
  #y,m,d = params.tanggal_lahir[:3]
  #tanggal_lahir = config.ModDateTime.EncodeDate(y,m,d)
  tanggal_lahir = config.FormatDateTimeForQuery(params.tanggal_lahir)
  
  sSQL = """
    SELECT * FROM NasabahDPLK 
    WHERE  ibu_kandung = '%s'
           AND nama_lengkap = '%s'
           AND tanggal_lahir =  %s
    """ % (params.ibu_kandung, params.nama_lengkap, tanggal_lahir)
  rSQL = config.CreateSQL(sSQL).RawResult
  
  if not rSQL.Eof:
    status.success = True
    status.is_otor = True
    status.no_peserta = rSQL.no_peserta
  else:
    sSQL = """
      SELECT * FROM REGISTERNASABAHREKENING 
      WHERE  ibu_kandung = '%s'
             AND nama_lengkap = '%s'
             AND tanggal_lahir =  %s
      """ % (params.ibu_kandung, params.nama_lengkap, tanggal_lahir)
    rSQL = config.CreateSQL(sSQL).RawResult
    
    if not rSQL.Eof:
      status.success = True
      status.is_otor = False
      status.registernr_id = rSQL.registernr_id
      status.no_peserta = rSQL.no_peserta
    else:
      status.message = "Peserta belum terdaftar di data kepesertaan DPLK"
      
      
      