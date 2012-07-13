import sys, string, time
import com.ihsan.util.modman as modman
import com.ihsan.foundation.appserver as appserver
import com.ihsan.foundation.pobjecthelper as phelper

moduleapi = modman.getModule(appserver.ActiveConfig, 'moduleapi')

def uipartAfterApplyRow(sender, obj):
    #config = sender.uideflist.config
    #helper = phelper.PObjectHelper(config)

    #role = helper.GetObjectByInstance('UserGroup', obj)
    #role.OnCreate()

    return 1

def checkPropinsi(config, nama_propinsi):
  kode_propinsi = ''
  
  strSQL = '''
    SELECT kode_propinsi FROM DaerahAsal WHERE nama_propinsi = '%s'
    ''' % (nama_propinsi)
  resSQL = config.CreateSQL(strSQL).RawResult
  if not resSQL.Eof:
    kode_propinsi = resSQL.kode_propinsi
  
  return kode_propinsi

def checkKota(config, nama_kota):
  kode_kota = ''
  
  strSQL = '''
    SELECT kode_kota FROM DaerahKota WHERE nama_kota = '%s'
    ''' % (nama_kota)
  resSQL = config.CreateSQL(strSQL).RawResult
  if not resSQL.Eof:
    kode_kota = resSQL.kode_kota
  
  return kode_kota

def checkRekeningPeserta(config, no_rekening, no_peserta, nama_peserta):
  oRekInvDPLK = config.CreatePObjImplProxy('RekInvDPLK')
  oRekInvDPLK.Key = no_rekening

  if not oRekInvDPLK.IsNull:
    if no_peserta == oRekInvDPLK.no_peserta\
      and nama_peserta.lower() == (oRekInvDPLK.LNasabahDPLK.nama_lengkap).lower():
      return no_peserta, no_rekening
      
  return None, None

def checkExistingPeserta(config, no_peserta, nama_peserta):
  oNasabahDPLK = config.CreatePObjImplProxy('NasabahDPLK')
  oNasabahDPLK.Key = no_peserta

  if not oNasabahDPLK.IsNull:
    if nama_peserta.lower() == str(oNasabahDPLK.nama_lengkap).lower():
      return no_peserta
      
  return None

def checkStatusPerkawinan(status_perkawinan):
  kode_status = ''
  status_perkawinan = str(status_perkawinan).lower()
  
  if status_perkawinan in ['b', 'belum menikah']:
    kode_status = '1'  
  elif status_perkawinan in ['m', 'menikah']:
    kode_status = '2'  
  elif status_perkawinan in ['d', 'janda/duda']:
    kode_status = '3'
    
  return kode_status

def checkJenisKelamin(jenis_kelamin):
  kode_status = ''
  jenis_kelamin = str(jenis_kelamin).lower()
  
  if jenis_kelamin in ['p', 'pria']:
    kode_status = 'P'  
  elif jenis_kelamin in ['w', 'wanita']:
    kode_status = 'W'
    
  return kode_status

def checkStatusAhliWaris(status_ahli_waris):
  kode_status = ''
  status_ahli_waris = str(status_ahli_waris).lower()
  
  if status_ahli_waris in ['a', 'aktif']:
    kode_status = 'A'  
  elif status_ahli_waris in ['n', 'tidak aktif']:
    kode_status = 'N'
    
  return kode_status

def checkHubunganKeluarga(hubungan_keluarga):
  kode_hk = ''
  hubungan_keluarga = str(hubungan_keluarga).lower()
  
  if hubungan_keluarga in ['p', 'peserta']:
    kode_hk = '0'  
  elif hubungan_keluarga in ['y', 'ayah']:
    kode_hk = '1'  
  elif hubungan_keluarga in ['b', 'ibu']:
    kode_hk = '2'  
  elif hubungan_keluarga in ['a', 'anak']:
    kode_hk = '3'  
  elif hubungan_keluarga in ['k', 'kakak']:
    kode_hk = '4'  
  elif hubungan_keluarga in ['d', 'adik']:
    kode_hk = '5'  
  elif hubungan_keluarga in ['i', 'istri']:
    kode_hk = '6'  
  elif hubungan_keluarga in ['s', 'suami']:
    kode_hk = '7'  
  elif hubungan_keluarga in ['l', 'lain-lain']:
    kode_hk = '8'
    
  return kode_hk

def getDateValue(tanggal_lahir):
  d,m,y = str(tanggal_lahir).split('-')
  
  m = m.lower()
  if m in ['jan']:
    m=1
  elif m in ['feb']:
    m=2
  elif m in ['mar']:
    m=3
  elif m in ['apr']:
    m=4
  elif m in ['may']:
    m=5
  elif m in ['jun']:
    m=6
  elif m in ['jul']:
    m=7
  elif m in ['aug']:
    m=8
  elif m in ['sep']:
    m=9
  elif m in ['oct']:
    m=10
  elif m in ['nov']:
    m=11
  elif m in ['dec']:
    m=12
  
  return [int(y),int(m),int(d),0,0,0,0,0,0]

def LoadUploadFile(config, filename):
  try:
    import pyFlexcel
    
    #open it
    workbook = pyFlexcel.Open(filename)
    
    #cek eksistensi worksheet
    if not workbook.IsWorksheetExist('DataImpor'):
      raise Exception, '' + 'Worksheet DataImpor tidak ditemukan! \
        \nWorksheet tempat data akan diimpor harus bernama DataImpor.'
    
    #activing worksheet
    workbook.ActivateWorksheet('DataImpor')    
  except:
    raise

  return workbook

def ValidateFile(config, kode_nasabah_corporate, upload_type):
  sSQL = """
    SELECT COUNT(1) AS count FROM UploadCorporate
    WHERE  kode_nasabah_corporate = '%s'
           AND upload_type = '%s'
           AND is_auth = 'F'
    """ % (kode_nasabah_corporate, upload_type)
  rSQL = config.CreateSQL(sSQL).RawResult
  
  if rSQL.count > 0:
    return False
  else:
    return True

def UploadData(config,params,returns):
  _userInfo = config.SecurityContext.GetUserInfo()
  _sessDate = config.Now()
  _branch_code = _userInfo[4]

  status = returns.CreateValues(
    ['sucsess',0],
    ['Is_Err',0],['Err_Message','']
  )

  rec = params.FirstRecord
  fileName =rec.filename.split('\\')[-1]

  if params.StreamWrapperCount > 0:
    sw = params.GetStreamWrapper(0)
  else:
    status.Is_Err = 1
    status.Err_Message = 'Download stream not found'
    return

  fileName ='%s__%s' % (_userInfo[0], fileName)
  fileNamePath = '%s/%s' % (config.GetGlobalSetting('USERHOMEDIR_ALL_UC'),fileName)
  sw.SaveToFile(fileNamePath)
  
  workBookXLS = LoadUploadFile(config, fileNamePath)
  kode_nasabah_corporate = workBookXLS.GetCellValue(3,3)

  isValid = ValidateFile(config, kode_nasabah_corporate, rec.upload_type)
  if not isValid:
    status.Is_Err = 1
    status.Err_Message = '''
    Terdapat data korporat dan jenis upload yang sama belum diotorisasi
    Lakukan otorisasi terlebih dahulu...'''
    return
                                    
  config.BeginTransaction()
  try :
    oUC = config.CreatePObject("UploadCorporate")
    oUC.session_filename = fileName
    oUC.session_date = int(_sessDate)
    oUC.session_time = _sessDate
    oUC.session_user_id = _userInfo[0]
    oUC.branch_code = _branch_code
    oUC.upload_type = rec.upload_type
    oUC.is_auth = 'F'
    
    oNasabahCorporate = config.CreatePObjImplProxy("NasabahDPLKCorporate")
    oNasabahCorporate.Key = kode_nasabah_corporate
    if oNasabahCorporate.IsNull:
      raise BaseException, "\n\nData perusahaan belum terdaftar..."
    oUC.LNasabahDPLKCorporate = oNasabahCorporate
    
    _trxCount = 0
    if oUC.upload_type == 'P':
      _startLine = 8
      _checkLine = _startLine
      required_field = str(workBookXLS.GetCellValue(_checkLine,2)).strip()
      while required_field not in ['', 'None']:
        _trxCount += 1
        CreateUCRegisterPeserta(config, workBookXLS, oUC, required_field, _checkLine, oUC.branch_code)
        
        _checkLine += 1
        required_field = str(workBookXLS.GetCellValue(_checkLine,2)).strip()      
    elif oUC.upload_type == 'W':
      _startLine = 8
      _checkLine = _startLine
      required_field = str(workBookXLS.GetCellValue(_checkLine,2)).strip()
      while required_field not in ['', 'None']:
        _trxCount += 1
        CreateUCAhliWaris(config, workBookXLS, oUC, required_field, _checkLine)
        
        _checkLine += 1
        required_field = str(workBookXLS.GetCellValue(_checkLine,2)).strip()      
    elif oUC.upload_type == 'I':
      _startLine = 11
      _checkLine = _startLine
      required_field = str(workBookXLS.GetCellValue(_checkLine,4)).strip()
      while required_field not in ['', 'None']:
        _trxCount += 1
        CreateUCIuranPeserta(config, workBookXLS, oUC, required_field, _checkLine)
        
        _checkLine += 1
        required_field = str(workBookXLS.GetCellValue(_checkLine,4)).strip()      
    elif oUC.upload_type == 'R':
      _startLine = 8
      _checkLine = _startLine
      required_field = str(workBookXLS.GetCellValue(_checkLine,4)).strip()
      while required_field not in ['', 'None']:
        _trxCount += 1
        CreateUCBiayaDaftar(config, workBookXLS, oUC, required_field, _checkLine)
        
        _checkLine += 1
        required_field = str(workBookXLS.GetCellValue(_checkLine,4)).strip()      
    else:
      raise BaseException, '\n\nPERINGATAN!\nJenis upload yang dipilih tidak terdaftar...'
      
    config.Commit()
    status.sucsess = _trxCount
  except:
    config.Rollback()
    status.Is_Err = 1
    status.Err_Message = str(sys.exc_info()[1])
    return

def CreateUCRegisterPeserta(config, workBookExcel, oUploadCorporate, requiredField, _Line, kode_cab_daftar):
  oRP = config.CreatePObject("UploadCorpRegisterPeserta")
  oRP.LUploadCorporate = oUploadCorporate
  oRP.nama_lengkap = requiredField
  oRP.no_referensi = str(workBookExcel.GetCellValue(_Line,3)).strip()
  oRP.alamat_jalan = str(workBookExcel.GetCellValue(_Line,4)).strip()
  oRP.alamat_rtrw = str(workBookExcel.GetCellValue(_Line,5)).strip()
  oRP.kode_propinsi = checkPropinsi(config, str(workBookExcel.GetCellValue(_Line,6)).strip())
  oRP.kode_kota = checkKota(config, str(workBookExcel.GetCellValue(_Line,7)).strip())
  oRP.tempat_lahir = str(workBookExcel.GetCellValue(_Line,8)).strip()
  
  #import rpdb2; rpdb2.start_embedded_debugger("solusi", True, True)
  if not str(workBookExcel.GetCellValue(_Line,9)).strip() in ['', 'None']:
    try:
      oRP.tanggal_lahir = workBookExcel.GetCellValue(_Line,9)
    except:
      pass
  
  oRP.status_perkawinan = checkStatusPerkawinan(str(workBookExcel.GetCellValue(_Line,10)).strip())
  oRP.jenis_kelamin = checkJenisKelamin(str(workBookExcel.GetCellValue(_Line,11)).strip())
  oRP.NPWP = str(workBookExcel.GetCellValue(_Line,12)).strip()
  oRP.ibu_kandung = str(workBookExcel.GetCellValue(_Line,13)).strip()
  oRP.is_auth = 'F'
  oRP.is_valid = 'T'
  
  oRP.keterangan = ''
  if oRP.no_referensi in ['', 'None']\
    or oRP.alamat_jalan in ['', 'None']\
    or oRP.alamat_rtrw in ['', 'None']\
    or oRP.kode_propinsi in ['', 'None']\
    or oRP.kode_kota in ['', 'None']\
    or oRP.tempat_lahir in ['', 'None']\
    or oRP.tanggal_lahir in [None]\
    or oRP.status_perkawinan in ['', 'None']\
    or oRP.jenis_kelamin in ['', 'None']\
    or oRP.npwp in ['', 'None']\
    or oRP.ibu_kandung in ['', 'None']:
    oRP.is_valid = 'F'
    oRP.keterangan = 'Data tidak lengkap... '
  
  no_peserta = ''
  is_otor = ''
  if not oRP.tanggal_lahir in [None]:
    tanggal_lahir = config.FormatDateTimeForQuery(workBookExcel.GetCellValue(_Line,9))
    sSQL = """
      SELECT no_peserta FROM NasabahDPLK 
      WHERE  ibu_kandung = '%s'
             AND nama_lengkap = '%s'
             AND tanggal_lahir =  %s
      """ % (oRP.ibu_kandung, oRP.nama_lengkap, tanggal_lahir)
    rSQL = config.CreateSQL(sSQL).RawResult
    
    if not rSQL.Eof:
      no_peserta = rSQL.no_peserta
      is_otor = 'T'
    else:
      sSQL = """
        SELECT no_peserta FROM REGISTERNASABAHREKENING 
        WHERE  ibu_kandung = '%s'
               AND nama_lengkap = '%s'
               AND tanggal_lahir =  %s
        """ % (oRP.ibu_kandung, oRP.nama_lengkap, tanggal_lahir)
      rSQL = config.CreateSQL(sSQL).RawResult
      
      if not rSQL.Eof:
        is_otor = 'F'
        no_peserta = rSQL.no_peserta
  
  if not no_peserta in ['']:
    oRP.is_valid = 'F'
    oRP.keterangan = '%sTerdaftar #%s, Otor: %s' % (oRP.keterangan, no_peserta, is_otor)
    #oRP.no_peserta = no_peserta
  else:
    strCounter = moduleapi.GetCounterNumber(config, 'REKINVDPLK', kode_cab_daftar)
    no_rekening = '%s%08d' % (moduleapi.TruncateString(kode_cab_daftar, 3), strCounter)
    
    strCounter = moduleapi.GetCounterNumber(config, 'NASABAHDPLK', kode_cab_daftar)
    no_peserta = '%s%08d' % (moduleapi.TruncateString(kode_cab_daftar, 3), strCounter)

    oRP.no_peserta = no_peserta
    oRP.no_rekening = no_rekening
#--end--CreateUCRegisterPeserta

def CreateUCAhliWaris(config, workBookExcel, oUploadCorporate, requiredField, _Line):
  oAW = config.CreatePObject("UploadCorpAhliWaris")
  oAW.LUploadCorporate = oUploadCorporate
  
  oAW.no_peserta = checkExistingPeserta(config, \
    str(workBookExcel.GetCellValue(_Line,2)).strip(), \
    str(workBookExcel.GetCellValue(_Line,3)).strip())
  oAW.nama_ahli_waris = str(workBookExcel.GetCellValue(_Line,4)).strip()
  oAW.hubungan_keluarga = checkHubunganKeluarga(str(workBookExcel.GetCellValue(_Line,5)).strip())

  if not str(workBookExcel.GetCellValue(_Line,6)).strip() in ['', 'None']:
    try:
      oAW.tanggal_lahir = workBookExcel.GetCellValue(_Line,6)
    except:
      pass

  oAW.jenis_kelamin = checkJenisKelamin(str(workBookExcel.GetCellValue(_Line,7)).strip())
  oAW.status_ahli_waris = checkStatusAhliWaris(str(workBookExcel.GetCellValue(_Line,8)).strip())
  oAW.no_urut_prioritas = workBookExcel.GetCellValue(_Line,9)
  oAW.keterangan_ahli_waris = str(workBookExcel.GetCellValue(_Line,10)).strip()
  oAW.is_auth = 'F'
  oAW.is_valid = 'T'
  
  if oAW.nama_ahli_waris in ['', 'None']:
    oAW.is_valid = 'F'
    oAW.keterangan = 'Nama Ahli Waris masih kosong'
  
  if oAW.hubungan_keluarga in ['', 'None']:
    oAW.is_valid = 'F'
    oAW.keterangan = 'Hubungan Keluarga tidak terdefinisi'
  
  if oAW.no_peserta in [None]:
    oAW.is_valid = 'F'
    oAW.keterangan = 'Nomor peserta tidak valid'
#--end--CreateUCAhliWaris

def CreateUCIuranPeserta(config, workBookExcel, oUploadCorporate, requiredField, _Line):
  oIP = config.CreatePObject("UploadCorpIuranPeserta")
  oIP.LUploadCorporate = oUploadCorporate
  oIP.no_peserta, oIP.no_rekening = checkRekeningPeserta(config, \
    requiredField, \
    str(workBookExcel.GetCellValue(_Line,2)).strip(), \
    str(workBookExcel.GetCellValue(_Line,3)).strip())
  oIP.iuran_pst = workBookExcel.GetCellValue(_Line,5)
  oIP.iuran_pk = workBookExcel.GetCellValue(_Line,6)
  oIP.is_auth = 'F'
  oIP.is_valid = 'T'
  
  oIP.keterangan = ''
  if (oIP.iuran_pst + oIP.iuran_pk) <= 0.0:
    oIP.is_valid = 'F'
    oIP.keterangan = 'Total pembayaran iuran <= 0.0'
  
  if oIP.no_peserta in [None]:
    oIP.is_valid = 'F'
    oIP.keterangan = 'Nomor peserta tidak valid'

  if oIP.no_rekening in [None]:
    oIP.is_valid = 'F'
    oIP.keterangan = 'Nomor rekening tidak valid'
#--end--CreateUCIuranPeserta
    
def CreateUCBiayaDaftar(config, workBookExcel, oUploadCorporate, requiredField, _Line):
  oIP = config.CreatePObject("UploadCorpBiayaDaftar")
  oIP.LUploadCorporate = oUploadCorporate
  oIP.no_peserta, oIP.no_rekening = checkRekeningPeserta(config, \
    requiredField, \
    str(workBookExcel.GetCellValue(_Line,2)).strip(), \
    str(workBookExcel.GetCellValue(_Line,3)).strip())
  oIP.biaya_daftar = workBookExcel.GetCellValue(_Line,5)
  oIP.is_auth = 'F'
  oIP.is_valid = 'T'
  
  oIP.keterangan = ''
  if oIP.biaya_daftar <= 0.0:
    oIP.is_valid = 'F'
    oIP.keterangan = 'Biaya daftar <= 0.0'
  
  if oIP.no_peserta in [None]:
    oIP.is_valid = 'F'
    oIP.keterangan = 'Nomor peserta tidak valid'

  if oIP.no_rekening in [None]:
    oIP.is_valid = 'F'
    oIP.keterangan = 'Nomor rekening tidak valid'
#--end--CreateUCBiayaDaftar
    
  
  