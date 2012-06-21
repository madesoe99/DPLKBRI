def Action1Click(sender, context):
  dialogname = sender.StringTag
  aform = context.FindForm(dialogname)
  if aform == None:  
    aform = context.GetForm('userman/' + dialogname, dialogname, 2)
  try:
    aform.Show()
  finally:
    aform = None

def Action2Click (sender, context):
  dialogname = sender.Name
  objname = sender.StringTag
  try:
    aform = context.GetFormWithData('userman/' + dialogname, dialogname, 0, 'x:', objname)
    aform.Show()
  finally:
    aform = None

def stdExecScript(sender, context):
  script_file = sender.Name
  message = sender.StringTag
  if context.ConfirmDialog(message) != 0:
    rdp = context.ExecuteScript('userman/' + script_file, None)

    ds = rdp.packet.GetDataset(0)
    record = ds.GetRecord(0)
    if record.IsErr:
      raise record.ErrMessage

    context.ShowMessage('Eksekusi berhasil')

def browseDirClick(sender, context):
  dialogname = 'browse_appdir'
  try:
    aform = context.GetFormWithData('userman/' + dialogname, dialogname, 0, '', 'list_class')
    aform.Show()
  finally:
    aform = None

def backupdataClick(sender, context):
  iForm = context.GetForm('userman/fbackupdb', 'fbackupdb', 0)
  iForm.Show()

def restoredata(sender, context):
  app = context
  dialogname = 'browse_appdir'
  try:
    aform = context.GetFormWithData('userman/' + dialogname, dialogname, 0, 'BACKUP_ROOT', 'list_class')
    iRes = aform.Show()
    if iRes == 1:
      formObject = aform.FormObject
      serverFilePath = formObject.GetUIPartByName('active_directory').actual_server_path
      uipListClass = formObject.GetUIPartByName('list_class')
      if uipListClass.Eof:
        return
        
      serverFileName = serverFilePath + '\\' + uipListClass.fd_name
      app.ExecuteScriptTrackable('userman/L_RestoreDB', app.CreateValues(['serverFileName', serverFileName]))
      app.ShowMessage('Restore process started. See console monitor for progress report')
  finally:
    aform = None

