import sys, string, time
sys.path.append('c:/dafapp/dplk07/script_modules/')

import moduleapi

def FormGeneralSetData(uideflist, auiname, apobjconst):
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
  #rec.kode_cab_daftar = branchcode

  rec.nolimitlocation = oUser.NoLimitLocation
  rec.STATUS_BIAYA_DAFTAR = 'T'
  rec.WASIAT_UMMAT = 'F'
  rec.kirim_statemen = 'N'
  rec.auto_debet = 'F'
  rec.iuran_pk = 0.0
  rec.iuran_pst = 0.0
  
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


  return 0

def FormEndProcessData(uideflist, datapacket):
  config = uideflist.Config

  oRegisterNasabahRekening = uideflist.uipRegisterNasabahRekening.ActiveInstance
  kode_cab_daftar = oRegisterNasabahRekening.kode_cab_daftar

  strCounter = str(moduleapi.GetCounterNumber(config, 'NASABAHDPLK', kode_cab_daftar))
  no_peserta = '%s99%s' % (moduleapi.TruncateString(kode_cab_daftar, 3), moduleapi.MyZFill(strCounter, 6))

  uideflist.PostReturnMessage = 'Peserta siap didaftarkan dengan nomor: ' + no_peserta

  oRegisterNasabahRekening.no_peserta = no_peserta


  # show message
  return 3

def uipRegisterNasabahRekeningApplyRow(sender, oData):
  config = sender.UIDefList.Config
  rec = sender.ActiveRecord
  
  if rec.alamat_telepon in ['', None]:
    raise Exception, '\nPERINGATAN' + \
      '\nPada saat mengisi taAlamat Tempat Tinggal,'\
      '\nTelepon 1 & Telepon 2 (Rumah/Hp) Mohon diisi dahulu.'

  if rec.no_referensi in ['', None]:
    raise Exception, '\nPERINGATAN' + \
      '\nNomor Referensi belum terdefinisi! Mohon isi dahulu.'

  if len(rec.no_referensi) <> 8:
    raise Exception, '\nPERINGATAN' + \
      '\nNomor Referensi Di isi dengan NIK Karyawan.'

  if rec.jenis_kelamin in ['', None]:
    raise Exception, '\nPERINGATAN' + \
      '\nJenis Kelamin belum terdefinisi! Mohon isi dahulu.'

  if rec.usia_pensiun in [None,''] or \
    (rec.usia_pensiun < 45 or rec.usia_pensiun > 65):
    raise Exception, '\nPERINGATAN' + \
      '\nUsia Pensiun tidak valid! Usia Pensiun yang diperbolehkan antara 45 - 65 tahun.'
      
  if rec.kode_jenis_usaha in [None,'']:
    raise Exception, '\nPERINGATAN' + \
      '\nKode Jenis Usaha Belum dipilih.'

  #cek usia sekarang peserta dan keikutsertaan wasiat ummat
  y,m,d = time.localtime()[:3]
  oParameter = config.CreatePObjImplProxy('Parameter')
  oParameter.Key = 'JUMLAH_HARI_SETAHUN'
  JumlahHariSetahun = oParameter.Numeric_Value
  usiaPeserta = (config.ModDateTime.EncodeDate(y,m,d) - rec.tanggal_lahir) /JumlahHariSetahun
  
  
  #if rec.wasiat_ummat == 'T' and usiaPeserta > 55.0:
  #  raise Exception, '\nPERINGATAN' + \
  #    '\nStatus Wasiat Ummat tidak valid! Usia peserta Wasiat '\
  #    'Ummat hanya diperbolehkan dibawah usia 55 tahun.'

  if rec.nasabah_korporat:
    if oData.LNasabahDPLKCorporate.IsNull:
      raise Exception, '\nPERINGATAN' + \
        '\nData Perusahaan belum terdefinisi! Mohon isi dahulu.'

  if oData.auto_debet == 'T':
    if (oData.no_rek_autodebet == '') or (oData.no_rek_autodebet == None):
      raise Exception, '\nPERINGATAN' + \
        '\nNomor Rekening Auto Debet belum terdefinisi! Mohon isi dahulu.'

    if (oData.tanggal_autodebet < 1) or (oData.tanggal_autodebet > 31):
      raise Exception, '\nPERINGATAN' + \
        'Tanggal Auto Debet belum valid! Mohon isi dahulu.'


  #oData.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oData.kode_cab_daftar = rec.GetFieldByName('LBranchLocation.branch_code')

