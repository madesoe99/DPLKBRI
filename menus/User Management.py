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
    
def userMonitorClick(sender, context):
  app = context
  user_mon = app.FindForm('user_monitor')
  if user_mon != None:
    user_mon.Show()
  else:
    frm = app.CreateForm('userman/user_monitor', 'user_monitor', 2, None, None)
    frm.FormContainer.Show()
  #--
#--

def browseDirClick(sender, context):
  app = context
  frm = app.FindForm('browse_appdir')
  if frm != None:
    frm.Show()
  else:
    oForm = app.CreateForm('userman/browse_appdir', 'browse_appdir', 2, app.CreateValues(['path', '/']), None)
    oForm.FormContainer.Show()
  #--    

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

def excelImportClick(sender, app):
  frm = app.CreateForm("ximport/fProcessImport", "fProcessImport", 0, None, None)
  frm.FormContainer.Show()
#--
    