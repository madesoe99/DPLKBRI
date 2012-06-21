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
  rec.status_biaya_daftar = 'F'
  rec.ikut_asuransi = 'F'
  rec.kirim_statemen = 'N'
  rec.iuran_pk = 0.0
  rec.iuran_pst = 0.0
  rec.kewarganegaraan = '1'
  
  #set parameter
  recP = uideflist.uipParameter.Dataset.AddRecord()
  oP = config.CreatePObjImplProxy('Parameter')
  oP.Key = 'MIN_JML_IURAN_PST'
  recP.MIN_JML_IURAN_PST = oP.Numeric_Value
  
  oP.Key = 'MIN_JML_IURAN_PK'
  recP.MIN_JML_IURAN_PK = oP.Numeric_Value

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
      rec.SetFieldByName("LBranchLocation.branch_code", oND.LBranchLocation.branch_code)
      rec.SetFieldByName("LBranchLocation.BranchName", oND.LBranchLocation.BranchName)
      rec.nama_lengkap = oND.nama_lengkap
      rec.tempat_lahir = oND.tempat_lahir
      rec.SetFieldByName("tanggal_lahir", oND.tanggal_lahir)
      rec.no_identitas_diri = oND.no_identitas_diri
      rec.jenis_kelamin = oND.jenis_kelamin  
      
      if not oND.LDaerahAsal.IsNull:
        rec.SetFieldByName("LDaerahAsal.kode_propinsi", oND.LDaerahAsal.kode_propinsi)
        rec.SetFieldByName("LDaerahAsal.nama_propinsi", oND.LDaerahAsal.nama_propinsi)
      
      if not oND.LKelompok.IsNull:
        rec.SetFieldByName("LKelompok.kode_kelompok", oND.LKelompok.kode_kelompok)
        rec.SetFieldByName("LKelompok.nama_kelompok", oND.LKelompok.nama_kelompok)
      
      rec.kewarganegaraan = oND.kewarganegaraan      
      rec.SetFieldByName("LNegara.kode_negara", oND.LNegara.kode_negara)
      rec.SetFieldByName("LNegara.nama_negara", oND.LNegara.nama_negara)
      rec.golongan_darah = oND.golongan_darah
      rec.agama = oND.agama
      rec.pendidikan_terakhir = oND.pendidikan_terakhir
      rec.penghasilan_tetap = oND.penghasilan_tetap
      rec.penghasilan_tambahan = oND.penghasilan_tambahan
      rec.status_perkawinan = oND.status_perkawinan
      rec.alamat_email = oND.alamat_email
      
      rec.alamat_jalan = oND.alamat_jalan
      rec.alamat_jalan2 = oND.alamat_jalan2
      rec.alamat_rtrw = oND.alamat_rtrw
      rec.alamat_kelurahan = oND.alamat_kelurahan
      rec.alamat_kecamatan = oND.alamat_kecamatan
      rec.alamat_kota = oND.alamat_kota
      rec.alamat_propinsi = oND.alamat_propinsi
      rec.alamat_kode_pos = oND.alamat_kode_pos
      rec.alamat_telepon = oND.alamat_telepon
      rec.alamat_telepon2 = oND.alamat_telepon2
      
      rec.alamat_surat_jalan = oND.alamat_surat_jalan
      rec.alamat_surat_jalan2 = oND.alamat_surat_jalan2
      rec.alamat_surat_rtrw = oND.alamat_surat_rtrw
      rec.alamat_surat_kelurahan = oND.alamat_surat_kelurahan
      rec.alamat_surat_kecamatan = oND.alamat_surat_kecamatan
      rec.alamat_surat_kota = oND.alamat_surat_kota
      rec.alamat_surat_propinsi = oND.alamat_surat_propinsi
      rec.alamat_surat_kode_pos = oND.alamat_surat_kode_pos
      rec.alamat_surat_telepon = oND.alamat_surat_telepon
      rec.alamat_surat_telepon2 = oND.alamat_surat_telepon2
      
      rec.NPWP = oND.NPWP
      if not oND.LJenisPekerjaan.IsNull:
        rec.SetFieldByName("LJenisPekerjaan.kode_jenis_pekerjaan", oND.LJenisPekerjaan.kode_jenis_pekerjaan)
        rec.SetFieldByName("LJenisPekerjaan.nama_jenis_pekerjaan", oND.LJenisPekerjaan.nama_jenis_pekerjaan)
      
      if not oND.LNasabahDPLKCorporate.IsNull:
        rec.SetFieldByName("LNasabahDPLKCorporate.kode_nasabah_corporate", oND.LNasabahDPLKCorporate.kode_nasabah_corporate)
        rec.SetFieldByName("LNasabahDPLKCorporate.nama_perusahaan", oND.LNasabahDPLKCorporate.nama_perusahaan)
      
      rec.nama_perusahaan = oND.nama_perusahaan
      
      if not oND.LJenisUsaha.IsNull:
        rec.SetFieldByName("LJenisUsaha.kode_jenis_usaha", oND.LJenisUsaha.kode_jenis_usaha)
        rec.SetFieldByName("LJenisUsaha.nama_jenis_usaha", oND.LJenisUsaha.nama_jenis_usaha)
      
      if not oND.LKepemilikan.IsNull:
        rec.SetFieldByName("LKepemilikan.kode_pemilikan", oND.LKepemilikan.kode_pemilikan)
        rec.SetFieldByName("LKepemilikan.keterangan", oND.LKepemilikan.keterangan)      
      rec.alamat_kantor_jalan = oND.alamat_kantor_jalan
      rec.alamat_kantor_kelurahan = oND.alamat_kantor_kelurahan
      rec.alamat_kantor_kecamatan = oND.alamat_kantor_kecamatan
      rec.alamat_kantor_kota = oND.alamat_kantor_kota
      rec.alamat_kantor_propinsi = oND.alamat_kantor_propinsi
      rec.alamat_kantor_kode_pos = oND.alamat_kantor_kode_pos
      rec.alamat_kantor_telepon = oND.alamat_kantor_telepon
      rec.alamat_kantor_telepon2 = oND.alamat_kantor_telepon2
      
      if not oND.LLDPLain.IsNull:
        rec.SetFieldByName("LLDPLain.kode_dp", oND.LLDPLain.kode_dp)
        rec.SetFieldByName("LLDPLain.nama_dp", oND.LLDPLain.nama_dp)
      rec.keterangan_registrasi = oND.keterangan
      
      #Ls_RegNRAhliWaris vs Ls_AhliWaris
      Ls_AhliWaris = oND.Ls_AhliWaris
      Ls_AhliWaris.First()
      while not Ls_AhliWaris.EndOfList:
        oAW = Ls_AhliWaris.CurrentElement
        
        regAW = uideflist.uipRegNRAhliWaris.Dataset.AddRecord()
        #regAW.LRegisterNasabahRekening = rec
        regAW.hubungan_keluarga = oAW.hubungan_keluarga
        regAW.jenis_kelamin = oAW.jenis_kelamin
        regAW.keterangan = oAW.keterangan
        regAW.nama_lengkap = oAW.nama_lengkap
        regAW.nomor_urut_prioritas = oAW.nomor_urut_prioritas
        regAW.status_ahli_waris = oAW.status_ahli_waris
        regAW.SetFieldByName('tanggal_lahir', oAW.tanggal_lahir)
        
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

  sReturnMsg = "Peserta baru telah siap didaftarkan..."
  no_peserta = oRegisterNasabahRekening.no_peserta_existing
  if oRegisterNasabahRekening.no_peserta_existing in ['', 0, None]:
    strCounter = moduleapi.GetCounterNumber(config, 'NASABAHDPLK', kode_cab_daftar)
    no_peserta = '%s%08d' % (moduleapi.TruncateString(kode_cab_daftar, 3), strCounter)
  else:
    sReturnMsg = "Rekening baru telah didaftarkan untuk peserta terdaftar..."

  uideflist.PostReturnMessage = \
    '''%s\n\n
    Nomor peserta: %s a/n. %s\n
    Nomor rekening: %s'''\
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

  if rec.no_referensi in ['', None]:
    raise Exception, '\n\nPERINGATAN' \
      '\nNomor Referensi belum terdefinisi! Mohon isi dahulu.'

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

  if rec.nasabah_korporat:
    if oData.LNasabahDPLKCorporate.IsNull:
      raise Exception, \
        '\n\nPERINGATAN' \
        '\nData Perusahaan belum terdefinisi! Mohon isi dahulu.'

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
      
      
      