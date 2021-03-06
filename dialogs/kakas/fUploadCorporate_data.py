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

def checkKodePos(config, kode_pos):
  id_kodepos = ''
  kode_propinsi = ''
  kode_kota = ''
  
  strSQL = '''
    SELECT id_kodepos, kode_propinsi, kode_kota FROM DaerahKodePos WHERE kode_pos = '%s'
    ''' % (kode_pos)
  resSQL = config.CreateSQL(strSQL).RawResult
  if not resSQL.Eof:
    id_kodepos = resSQL.id_kodepos
    kode_propinsi = resSQL.kode_propinsi
    kode_kota = resSQL.kode_kota
  
  return id_kodepos, kode_propinsi, kode_kota

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

def checkKecamatan(config, nama_kecamatan):
  kode_kecamatan = ''
  
  strSQL = '''
    SELECT kode_kecamatan FROM DaerahKecamatan WHERE nama_kecamatan = '%s'
    ''' % (nama_kecamatan)
  resSQL = config.CreateSQL(strSQL).RawResult
  if not resSQL.Eof:
    kode_kecamatan = resSQL.kode_kecamatan
  
  return kode_kecamatan

def checkJenisPekerjaan(config, nama_jenis_pekerjaan):
  kode_jp = ''
  
  strSQL = '''
    SELECT kode_jenis_pekerjaan FROM JenisPekerjaan WHERE nama_jenis_pekerjaan = '%s'
    ''' % (nama_jenis_pekerjaan)
  resSQL = config.CreateSQL(strSQL).RawResult
  if not resSQL.Eof:
    kode_jp = resSQL.kode_jenis_pekerjaan
  
  return kode_jp

def checkJabatanPekerjaan(config, nama_jabatan, kode_jp):
  kode_jpd = ''
  
  strSQL = '''
    SELECT jpd.jpd_id FROM JENISPEKERJAANDETAIL jpd\
    INNER JOIN JENISJABATAN jj ON jj.kode_jenis_jabatan = jpd.kode_jenis_jabatan
    WHERE jj.nama_jenis_jabatan = '%s' AND jpd.kode_jenis_pekerjaan = '%s'
    ''' % (nama_jabatan, kode_jp)
  resSQL = config.CreateSQL(strSQL).RawResult
  if not resSQL.Eof:
    kode_jpd = resSQL.jpd_id
  
  return kode_jpd

def checkSumberDana(config, sumber_dana):
  kode_status = ''
  
  strSQL = '''
    SELECT sumber_dana FROM SumberDana WHERE sumber_dana = '%s'
    ''' % (sumber_dana)
  resSQL = config.CreateSQL(strSQL).RawResult
  if not resSQL.Eof:
    kode_status = resSQL.sumber_dana
  
  return kode_status

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

def checkKewarganegaraan(status_wn):
  kode_status = ''
  status_wn = str(status_wn).lower()
  
  if status_wn in ['1', 'ina', 'wni']:
    kode_status = '1'  
  elif status_wn in ['2', 'wna']:
    kode_status = '2'
    
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

def checkTrueFalse(status):
  kode_status = ''
  status = str(status).lower()
  
  if status in ['y', 'yes']:
    kode_status = 'T'  
  elif status in ['n', 'no']:
    kode_status = 'F'
    
  return kode_status

def checkSistemBayarIuran(sistem_bayar_iuran):
  kode_status = ''
  sistem_bayar_iuran = str(sistem_bayar_iuran).lower()
  
  if sistem_bayar_iuran in ['n', 'non rutin']:
    kode_status = 'N'  
  elif sistem_bayar_iuran in ['r', 'rutin']:
    kode_status = 'R'
    
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
  app = config.AppObject
  app.ConCreate('out')
  app.ConWriteln('mulai...')

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
        '''
        workBookExcel = workBookXLS
        _Line = _checkLine
        tanggal_lahir = None
        if not str(workBookExcel.GetCellValue(_Line,9)).strip() in ['', 'None']:
          try:
            tanggal_lahir = workBookExcel.GetCellValue(_Line,9)
          except:
            pass
      
        sSQL = """
          INSERT INTO UPLOADCORPREGISTERPESERTA_TMP (
            NAMA_LENGKAP,
            NO_REFERENSI,
            ALAMAT_JALAN,
            ALAMAT_RTRW,
            ALAMAT_PROPINSI,
            ALAMAT_KOTA,
            TEMPAT_LAHIR,
            TANGGAL_LAHIR,
            STATUS_PERKAWINAN,
            JENIS_KELAMIN,
            NPWP,
            IBU_KANDUNG,
            IS_AUTH,
            IS_VALID) 
          VALUES ('%s','%s','%s','%s','%s','%s','%s',%s,'%s','%s','%s','%s','%s','%s')""" \
          % (\
            required_field,\
            str(workBookExcel.GetCellValue(_Line,3)).strip(),\
            str(workBookExcel.GetCellValue(_Line,4)).strip(),\
            str(workBookExcel.GetCellValue(_Line,5)).strip(),\
            str(workBookExcel.GetCellValue(_Line,6)).strip(),\
            str(workBookExcel.GetCellValue(_Line,7)).strip(),\
            str(workBookExcel.GetCellValue(_Line,8)).strip(),\
            tanggal_lahir,\
            checkStatusPerkawinan(str(workBookExcel.GetCellValue(_Line,10)).strip()),\
            checkJenisKelamin(str(workBookExcel.GetCellValue(_Line,11)).strip()),\
            str(workBookExcel.GetCellValue(_Line,12)).strip(),\
            str(workBookExcel.GetCellValue(_Line,13)).strip(),\
            'F',\
            'T')
        config.ExecSQL(sSQL)
        
        sSQL = """
          UPDATE 
            UPLOADCORPREGISTERPESERTA_TMP 
          SET 
            UPLOADCORPREGISTERPESERTA_TMP.KODE_PROPINSI = DAERAHASAL.KODE_PROPINSI
          FROM UPLOADCORPREGISTERPESERTA_TMP
            INNER JOIN DAERAHASAL ON DAERAHASAL.NAMA_PROPINSI = UPLOADCORPREGISTERPESERTA_TMP.ALAMAT_PROPINSI"""
        sSQl = """
          UPDATE
            UPLOADCORPREGISTERPESERTA_TMP t
          SET
            t.KODE_PROPINSI = x.KODE_PROPINSI
          FROM
            (SELECT KODE_PROPINSI FROM DAERAHASAL ) x
          WHERE
            x.NAMA_PROPINSI = t.ALAMAT_PROPINSI"""
        config.ExecSQL(sSQL)
        
        sSQL = """
          UPDATE 
            UPLOADCORPREGISTERPESERTA_TMP 
          SET 
            UPLOADCORPREGISTERPESERTA_TMP.KODE_KOTA = DAERAHKOTA.KODE_KOTA
          FROM UPLOADCORPREGISTERPESERTA_TMP
            INNER JOIN DAERAHKOTA ON DAERAHKOTA.NAMA_KOTA = UPLOADCORPREGISTERPESERTA_TMP.ALAMAT_KOTA"""
        sSQl = """
          UPDATE
            UPLOADCORPREGISTERPESERTA_TMP t
          SET
            t.KODE_KOTA = x.KODE_KOTA
          FROM
            (SELECT KODE_KOTA FROM DAERAHKOTA ) x
          WHERE
            x.NAMA_KOTA = t.ALAMAT_KOTA"""
        config.ExecSQL(sSQL)
        
        sSQL = """
          UPDATE 
            UPLOADCORPREGISTERPESERTA_TMP
          SET 
            IS_VALID = 'F'
            KETERANGAN = 'Data belum lengkap...'
          WHERE
            NO_REFERENSI = 'None'
            OR ALAMAT_JALAN = 'None',
            OR ALAMAT_RTRW = 'None',
            OR KODE_PROPINSI = 'None',
            OR KODE_KOTA = 'None',
            OR TEMPAT_LAHIR = 'None',
            OR TANGGAL_LAHIR IS NULL,
            OR STATUS_PERKAWINAN = '',
            OR JENIS_KELAMIN = '',
            OR NPWP = 'None',
            OR IBU_KANDUNG = 'None'"""
        config.ExecSQL(sSQL)
        '''
        
        if (_trxCount % 50) == 0:
          app.ConWriteln('%d data diproses...' % _trxCount)
        
        _checkLine += 1
        required_field = str(workBookXLS.GetCellValue(_checkLine,2)).strip()      
    elif oUC.upload_type == 'K':
      _startLine = 8
      _checkLine = _startLine
      required_field = str(workBookXLS.GetCellValue(_checkLine,2)).strip()
      while required_field not in ['', 'None']:
        _trxCount += 1
        CreateUCKoreksiPeserta(config, workBookXLS, oUC, required_field, _checkLine)
        if (_trxCount % 50) == 0:
          app.ConWriteln('%d data diproses...' % _trxCount)
        
        _checkLine += 1
        required_field = str(workBookXLS.GetCellValue(_checkLine,2)).strip()      
    elif oUC.upload_type == 'W':
      _startLine = 8
      _checkLine = _startLine
      required_field = str(workBookXLS.GetCellValue(_checkLine,2)).strip()
      while required_field not in ['', 'None']:
        _trxCount += 1
        CreateUCAhliWaris(config, workBookXLS, oUC, required_field, _checkLine)
        if (_trxCount % 50) == 0:
          app.ConWriteln('%d data diproses...' % _trxCount)
        
        _checkLine += 1
        required_field = str(workBookXLS.GetCellValue(_checkLine,2)).strip()      
    elif oUC.upload_type == 'I':
      _startLine = 11
      _checkLine = _startLine
      required_field = str(workBookXLS.GetCellValue(_checkLine,4)).strip()
      while required_field not in ['', 'None']:
        _trxCount += 1
        CreateUCIuranPeserta(config, workBookXLS, oUC, required_field, _checkLine)
        if (_trxCount % 50) == 0:
          app.ConWriteln('%d data diproses...' % _trxCount)
        
        _checkLine += 1
        required_field = str(workBookXLS.GetCellValue(_checkLine,4)).strip()      
    elif oUC.upload_type == 'R':
      _startLine = 8
      _checkLine = _startLine
      required_field = str(workBookXLS.GetCellValue(_checkLine,4)).strip()
      while required_field not in ['', 'None']:
        _trxCount += 1
        CreateUCBiayaDaftar(config, workBookXLS, oUC, required_field, _checkLine)
        if (_trxCount % 50) == 0:
          app.ConWriteln('%d data diproses...' % _trxCount)
        
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
  oRP.alamat_rw = str(workBookExcel.GetCellValue(_Line,6)).strip()
  #oRP.kode_propinsi = checkPropinsi(config, str(workBookExcel.GetCellValue(_Line,7)).strip())
  #oRP.kode_kota = checkKota(config, str(workBookExcel.GetCellValue(_Line,8)).strip())
  if workBookExcel.GetCellValue(_Line,9) != None:
    oRP.id_kodepos, oRP.kode_propinsi, oRP.kode_kota = checkKodePos(config, str(int(workBookExcel.GetCellValue(_Line,9))))
  
  oRP.tempat_lahir = str(workBookExcel.GetCellValue(_Line,10)).strip()
  
  #import rpdb2; rpdb2.start_embedded_debugger("solusi", True, True)
  if not str(workBookExcel.GetCellValue(_Line,11)).strip() in ['', 'None']:
    try:
      oRP.tanggal_lahir = workBookExcel.GetCellValue(_Line,11)
    except:
      pass
  
  if workBookExcel.GetCellValue(_Line,12) != None:
    oRP.status_perkawinan = checkStatusPerkawinan(str(workBookExcel.GetCellValue(_Line,12)).strip())
  
  if workBookExcel.GetCellValue(_Line,13) != None:
    oRP.jenis_kelamin = checkJenisKelamin(str(workBookExcel.GetCellValue(_Line,13)).strip())
  
  oRP.NPWP = str(workBookExcel.GetCellValue(_Line,14)).strip()
  oRP.ibu_kandung = str(workBookExcel.GetCellValue(_Line,15)).strip()
  oRP.email = str(workBookExcel.GetCellValue(_Line,16)).strip()
  oRP.telepon1 = str(workBookExcel.GetCellValue(_Line,17)).strip()
  oRP.telepon2 = str(workBookExcel.GetCellValue(_Line,18)).strip()
  
  if workBookExcel.GetCellValue(_Line,19) != None:
    oRP.kewarganegaraan = checkKewarganegaraan(str(workBookExcel.GetCellValue(_Line,19)).strip())
  
  if workBookExcel.GetCellValue(_Line,20) != None:
    oRP.kode_jenis_pekerjaan = checkJenisPekerjaan(config, str(workBookExcel.GetCellValue(_Line,20)).strip())
  
  if oRP.kode_jenis_pekerjaan != '' and workBookExcel.GetCellValue(_Line,21) != None:
    oRP.jpd_id = checkJabatanPekerjaan(config, str(workBookExcel.GetCellValue(_Line,21)).strip(), oRP.kode_jenis_pekerjaan)
  
  if workBookExcel.GetCellValue(_Line,22) != None:
    oRP.sumber_dana = checkSumberDana(config, str(workBookExcel.GetCellValue(_Line,22)).strip())
  
  oRP.penghasilan_setahun = float(workBookExcel.GetCellValue(_Line,23))
  oRP.reksumber_no = str(workBookExcel.GetCellValue(_Line,24)).strip()
  
  if workBookExcel.GetCellValue(_Line,25) != None:
    oRP.ispesertapengalihan = checkTrueFalse(str(workBookExcel.GetCellValue(_Line,25)).strip())
  
  if workBookExcel.GetCellValue(_Line,26) != None:
    oRP.sistem_pembayaran_iuran = checkSistemBayarIuran(str(workBookExcel.GetCellValue(_Line,26)).strip())
  
  oRP.tgl_debet_rekening = int(workBookExcel.GetCellValue(_Line,27))
  oRP.pct_pi_fix = int(workBookExcel.GetCellValue(_Line,28))
  oRP.pct_pi_eq = int(workBookExcel.GetCellValue(_Line,29))
  oRP.pct_pi_mm = int(workBookExcel.GetCellValue(_Line,30))
  oRP.usia_pensiun = int(workBookExcel.GetCellValue(_Line,31))
  
  if workBookExcel.GetCellValue(_Line,32) != None:
    oRP.ikut_asuransi = checkTrueFalse(str(workBookExcel.GetCellValue(_Line,32)).strip())
  
  oRP.is_auth = 'F'
  oRP.is_valid = 'T'
  
  oRP.keterangan = ''
  if oRP.no_referensi in ['', 'None']\
    or oRP.alamat_jalan in ['', 'None']\
    or oRP.alamat_rtrw in ['', 'None']\
    or oRP.alamat_rw in ['', 'None']\
    or oRP.id_kodepos in ['', 'None']\
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

def CreateUCKoreksiPeserta(config, workBookExcel, oUploadCorporate, requiredField, _Line):
  oKP = config.CreatePObject("UploadCorpKoreksiPeserta")
  oKP.LUploadCorporate = oUploadCorporate
  
  oKP.no_peserta = checkExistingPeserta(config, \
    str(workBookExcel.GetCellValue(_Line,2)).strip(), \
    str(workBookExcel.GetCellValue(_Line,3)).strip())
  oKP.no_referensi = str(workBookExcel.GetCellValue(_Line,4)).strip()
  oKP.alamat_jalan = str(workBookExcel.GetCellValue(_Line,5)).strip()
  oKP.alamat_jalan2 = str(workBookExcel.GetCellValue(_Line,6)).strip()
  oKP.alamat_rtrw = str(workBookExcel.GetCellValue(_Line,7)).strip()
  oKP.kode_propinsi = checkPropinsi(config, str(workBookExcel.GetCellValue(_Line,8)).strip())
  oKP.kode_kota = checkKota(config, str(workBookExcel.GetCellValue(_Line,9)).strip())
  oKP.kode_kecamatan = checkKecamatan(config, str(workBookExcel.GetCellValue(_Line,10)).strip())
  oKP.alamat_kelurahan = str(workBookExcel.GetCellValue(_Line,11)).strip()
  oKP.alamat_kode_pos = str(workBookExcel.GetCellValue(_Line,12)).strip()
  oKP.alamat_telepon = str(workBookExcel.GetCellValue(_Line,13)).strip()
  oKP.alamat_telepon2 = str(workBookExcel.GetCellValue(_Line,14)).strip()
  oKP.is_auth = 'F'
  oKP.is_valid = 'T'
  
  oKP.keterangan = ''
  if oKP.no_referensi in ['', 'None']\
    or oKP.alamat_jalan in ['', 'None']\
    or oKP.alamat_rtrw in ['', 'None']\
    or oKP.kode_propinsi in ['', 'None']\
    or oKP.kode_kota in ['', 'None']\
    or oKP.alamat_kode_pos in [None]\
    or oKP.alamat_telepon in ['', 'None']\
    or oKP.alamat_telepon2 in ['', 'None']:
    oKP.is_valid = 'F'
    oKP.keterangan = 'Data tidak lengkap... '
#--end--CreateUCKoreksiPeserta

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
    
  
  