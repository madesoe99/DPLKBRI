import time, sys

def LoadTemplateFile(config, folder, filename):
  try:
    import pyFlexcel
    
    #open it
    workbook = pyFlexcel.Open(folder + filename)
    
    #cek eksistensi worksheet
    if not workbook.IsWorksheetExist('DataImpor'):
      raise Exception, '' + 'Worksheet DataImpor tidak ditemukan! \
        \nWorksheet tempat data akan diimpor harus bernama DataImpor.'
    
    #activing worksheet
    workbook.ActivateWorksheet('DataImpor')    
  except:
    raise

  return workbook

def GenerateFile(config, params, returns):
  try:
    import os
    _userInfo = config.SecurityContext.GetUserInfo();
    _sessDate = config.Now()
    
    status = returns.CreateValues(
      ['sucsess',0],
      ['Is_Err',0],['Err_Message','']
    )
    
    rec = params.FirstRecord
    #raise Exception, "%s\n%s\n%s"\
    #  % (rec.upload_type, rec.kode_nasabah_corporate, rec.nama_perusahaan)
    if rec.upload_type == 'I':
      uploadDir = config.GetGlobalSetting('USERHOMEDIR_ALL_UC') + "/"
      workBookXLS = LoadTemplateFile(config, uploadDir, "TPL_IuranPesertaKorporat.xls")
      
      workBookXLS.SetCellValue(3,3, rec.kode_nasabah_corporate)
      workBookXLS.SetCellValue(5,3, rec.nama_perusahaan)
      
      oNDC = config.CreatePObjImplProxy('NasabahDPLKCorporate')
      oNDC.Key = rec.kode_nasabah_corporate
      Ls_NasabahDPLK = oNDC.Ls_NasabahDPLK
      oNDC.Ls_NasabahDPLK.First()
      i = 0
      _startLine = 11
      while not Ls_NasabahDPLK.EndOfList:
        oNDP = Ls_NasabahDPLK.CurrentElement
        
        i = i+1
        workBookXLS.SetCellValue(_startLine,1,i)
        workBookXLS.SetCellValue(_startLine,2,oNDP.no_peserta)
        workBookXLS.SetCellValue(_startLine,3,oNDP.nama_lengkap)
        
        oNDP.Ls_RekeningDPLK.First()
        oRekInvDPLK = oNDP.Ls_RekeningDPLK.CurrentElement
        no_rekening = oRekInvDPLK.no_rekening
        
        workBookXLS.SetCellValue(_startLine,4,no_rekening)
        workBookXLS.SetCellValue(_startLine,5,0.0)
        workBookXLS.SetCellValue(_startLine,6,0.0)
        _startLine=_startLine+1
        
        Ls_NasabahDPLK.Next()
      #--endwhile
        
      strSessDate = str(_sessDate)
      sBaseFileName = '%s_IURAN_%s_%s_%s.xls' % (\
        _userInfo[0], \
        str(rec.kode_nasabah_corporate).replace(' ', ''), \
        str(rec.nama_perusahaan).replace(' ', ''), \
        strSessDate.replace('.', ''))

      sFileName = uploadDir + sBaseFileName
      if os.access(sFileName, os.F_OK) == 1:
        os.remove(sFileName)
      #--endif
      workBookXLS.SaveAs(sFileName)
    
      #return packet
      sw = returns.AddStreamWrapper()
      sw.LoadFromFile(sFileName)
      sw.MIMEType = config.AppObject.GetMIMETypeFromExtension(sFileName)
    elif rec.upload_type == 'K':
      uploadDir = config.GetGlobalSetting('USERHOMEDIR_ALL_UC') + "/"
      workBookXLS = LoadTemplateFile(config, uploadDir, "TPL_KoreksiPesertaKorporat.xls")
      
      workBookXLS.SetCellValue(3,3, rec.kode_nasabah_corporate)
      workBookXLS.SetCellValue(5,3, rec.nama_perusahaan)
      
      sSQL = '''
        SELECT n.no_peserta,
               n.nama_lengkap,
               n.no_referensi,
               n.alamat_jalan,
               n.alamat_jalan2,
               n.alamat_rtrw,
               p.nama_propinsi,
               k.nama_kota,
               c.nama_kecamatan,
               n.alamat_kelurahan,
               n.alamat_kode_pos,
               n.alamat_telepon,
               n.alamat_telepon2
        FROM   NasabahDPLK n
               LEFT JOIN DaerahAsal p ON p.kode_propinsi = n.alamat_propinsi_kode
               LEFT JOIN DaerahKota k ON k.kode_kota = n.alamat_kota_kode
               LEFT JOIN DaerahKecamatan c ON c.kode_kecamatan = n.alamat_kecamatan_kode
        WHERE  n.kode_nasabah_corporate = '%s'
        ''' % rec.kode_nasabah_corporate
      rSQL = config.CreateSQL(sSQL).RawResult
      rSQL.First()
      
      i = 0
      _startLine = 8
      while not rSQL.Eof:
        i = i+1
        workBookXLS.SetCellValue(_startLine,1,i)
        workBookXLS.SetCellValue(_startLine,2,rSQL.no_peserta)
        workBookXLS.SetCellValue(_startLine,3,rSQL.nama_lengkap)
        workBookXLS.SetCellValue(_startLine,4,rSQL.no_referensi)
        workBookXLS.SetCellValue(_startLine,5,rSQL.alamat_jalan)
        workBookXLS.SetCellValue(_startLine,6,rSQL.alamat_jalan2)
        workBookXLS.SetCellValue(_startLine,7,rSQL.alamat_rtrw)
        workBookXLS.SetCellValue(_startLine,8,rSQL.nama_propinsi)
        workBookXLS.SetCellValue(_startLine,9,rSQL.nama_kota)
        workBookXLS.SetCellValue(_startLine,10,rSQL.nama_kecamatan)
        workBookXLS.SetCellValue(_startLine,11,rSQL.alamat_kelurahan)
        workBookXLS.SetCellValue(_startLine,12,rSQL.alamat_kode_pos)
        workBookXLS.SetCellValue(_startLine,13,rSQL.alamat_telepon)
        workBookXLS.SetCellValue(_startLine,14,rSQL.alamat_telepon2)
        _startLine=_startLine+1
        
        rSQL.Next()
      #--endwhile
        
      strSessDate = str(_sessDate)
      sBaseFileName = '%s_KOREKSIPESERTA_%s_%s_%s.xls' % (\
        _userInfo[0], \
        str(rec.kode_nasabah_corporate).replace(' ', ''), \
        str(rec.nama_perusahaan).replace(' ', ''), \
        strSessDate.replace('.', ''))

      sFileName = uploadDir + sBaseFileName
      if os.access(sFileName, os.F_OK) == 1:
        os.remove(sFileName)
      #--endif
      workBookXLS.SaveAs(sFileName)
    
      #return packet
      sw = returns.AddStreamWrapper()
      sw.LoadFromFile(sFileName)
      sw.MIMEType = config.AppObject.GetMIMETypeFromExtension(sFileName)
    elif rec.upload_type == 'R':
      uploadDir = config.GetGlobalSetting('USERHOMEDIR_ALL_UC') + "/"
      workBookXLS = LoadTemplateFile(config, uploadDir, "TPL_IuranBiayaDaftar.xls")
      
      workBookXLS.SetCellValue(3,3, rec.kode_nasabah_corporate)
      workBookXLS.SetCellValue(5,3, rec.nama_perusahaan)
      
      sSQL = '''
        SELECT n.no_peserta,
               n.nama_lengkap,
               r.no_rekening
        FROM   NasabahDPLK n
               INNER JOIN RekInvDPLK r ON r.no_peserta = n.no_peserta
        WHERE  n.kode_nasabah_corporate = '%s'
               AND r.status_biaya_daftar = 'F'
        ''' % rec.kode_nasabah_corporate
      rSQL = config.CreateSQL(sSQL).RawResult
      rSQL.First()
      
      i = 0
      _startLine = 8
      while not rSQL.Eof:
        i = i+1
        workBookXLS.SetCellValue(_startLine,1,i)
        workBookXLS.SetCellValue(_startLine,2,rSQL.no_peserta)
        workBookXLS.SetCellValue(_startLine,3,rSQL.nama_lengkap)
        workBookXLS.SetCellValue(_startLine,4,rSQL.no_rekening)
        workBookXLS.SetCellValue(_startLine,5,0.0)
        _startLine=_startLine+1
        
        rSQL.Next()
      #--endwhile
        
      strSessDate = str(_sessDate)
      sBaseFileName = '%s_BIAYADAFTAR_%s_%s_%s.xls' % (\
        _userInfo[0], \
        str(rec.kode_nasabah_corporate).replace(' ', ''), \
        str(rec.nama_perusahaan).replace(' ', ''), \
        strSessDate.replace('.', ''))

      sFileName = uploadDir + sBaseFileName
      if os.access(sFileName, os.F_OK) == 1:
        os.remove(sFileName)
      #--endif
      workBookXLS.SaveAs(sFileName)
    
      #return packet
      sw = returns.AddStreamWrapper()
      sw.LoadFromFile(sFileName)
      sw.MIMEType = config.AppObject.GetMIMETypeFromExtension(sFileName)
    else:
      status.Is_Err = True
      status.Err_Message = 'Jenis template tidak ditemukan...'
      return
    #--endelse
  except:
    status.Is_Err = True
    status.Err_Message = str(sys.exc_info()[1])
  