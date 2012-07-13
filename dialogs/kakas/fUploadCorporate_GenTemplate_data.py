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
        
      strSessDate = str(_sessDate)
      sBaseFileName = '%s_IURAN_%s_%s_%s.xls' % (\
        _userInfo[0], \
        str(rec.kode_nasabah_corporate).replace(' ', ''), \
        str(rec.nama_perusahaan).replace(' ', ''), \
        strSessDate.replace('.', ''))

      sFileName = uploadDir + sBaseFileName
      if os.access(sFileName, os.F_OK) == 1:
        os.remove(sFileName)
      workBookXLS.SaveAs(sFileName)
    
      #return packet
      sw = returns.AddStreamWrapper()
      sw.LoadFromFile(sFileName)
      sw.MIMEType = config.AppObject.GetMIMETypeFromExtension(sFileName)
    else:
      status.Is_Err = True
      status.Err_Message = 'Jenis template tidak ditemukan...'
      return
  except:
    status.Is_Err = True
    status.Err_Message = str(sys.exc_info()[1])
  