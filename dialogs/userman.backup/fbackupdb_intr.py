def btnOKClick(btnOK):
  form = btnOK.OwnerForm
  app = form.ClientApplication
  
  backupName = form.GetControlByName('pnlInput.edInput').Text
  retval = app.ExecuteScript('userman/S_CheckBackup', app.CreateValues(['backupName', backupName]))

  if retval.FirstRecord.exist:
    bContinue = app.ConfirmDialog('This backup set already exists. Replace(Y/N)?')
  else:
    bContinue = 1
    
  bUseLongScript = 1
  if bContinue:
    if bUseLongScript:
      #pid = app.ExecuteScriptTrackable('userman/L_BackupDB', 
      param = app.CreateValues(['backupName', backupName],
        [execFile,'userman/L_BackupDB'])
        
      app.ExecuteScript('longscripts/ExecuteLongScript', param)
      #pcConsole.ConsoleFilterName = 'stdprogress_' + str(pid)
      btnOK.Enabled = 0
      btnCancel = form.GetControlByName('pnlButton.btnCancel')
      if(btnCancel):
        btnCancel.Caption = 'Close'
    else:
      #app.ShowConsoleOnRequest('stdprogress')
      btnOK.ExitAction = 1
      try:
        app.ExecuteScript('userman/L_BackupDB', app.CreateValues(['backupName', backupName]))
      finally:
        pass
        #app.HideConsoleOnRequest()
    

