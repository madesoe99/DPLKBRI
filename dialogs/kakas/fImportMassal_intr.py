def FormShow(form, parameter):
  uipTL = form.GetUIPartByName('uipTemplateList')
  uipTL.First()
  
  #set file input

def bSelectFileClick(sender):
  filename = sender.OwnerForm.OpenFileDialog('Pilih file yang akan di-upload', \
    'File Microsoft Excel (*.xls)|*.xls')
  sender.OwnerForm.GetControlByName('pInput.FileInput').Text = filename

def btnOKClick(btnOK):
  form = btnOK.OwnerForm
  app = form.ClientApplication
  
  uploadFileName = form.GetControlByName('pInput.FileInput').Text
  #cek isian upload name
  if uploadFileName == '':
    form.ShowMessage('File yang akan di-upload untuk impor massal mohon diisi!')
    return

  #cek keberadaan file
  retval = app.ExecuteScript('kakas/S_CheckUpload', \
    app.CreateValues(['uploadFileName', uploadFileName]))

  if not retval.FirstRecord.exist:
    form.ShowMessage('File upload tidak ditemukan!')
    return

  try:
    uipTL = form.GetUIPartByName('uipTemplateList')
    if app.ConfirmDialog('Anda yakin akan memproses impor massal untuk %s '\
      'dari file yang di-upload?' % (uipTL.NamaTemplate)):

      #upload item terlebih dahulu
      app.UploadItem('SaveUploadedData', [uploadFileName])
      
      #jalankan script L_ImportMassal
      templateFile = uipTL.NamaTemplate.rstrip().lstrip().replace(' ','')
      #pid = app.ExecuteScriptTrackable(
      param = app.CreateValues([execFile,'kakas/L_ImportMassal'], 
        ['uploadFileName', uploadFileName],
        ['templateFile',templateFile])

      app.ExecuteScript('longscripts/ExecuteLongScript', param)
      #pcConsole.ConsoleFilterName = 'ImportMassal_' + str(pid)

      btnOK.Enabled = btnOK.Default = 0
      btnCancel = form.GetControlByName('pButton.btnCancel')
      btnCancel.Caption = '&Tutup'
      btnCancel.Default = 1

  except:
    raise
