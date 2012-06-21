def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def mnuNewClick(sender, context):
  app = context.OwnerForm.ClientApplication
  formid = sender.StringTag

  aform = app.GetForm('master/'+formid,formid,0)
  SetToCenterForm(context.OwnerForm, aform.FormObject)
  aform.Show()

def displayWithData(sender, context):
  app = context.OwnerForm.ClientApplication
  key = context.KeyObjConst
  formid = sender.StringTag
  aform = app.GetFormWithData('master/'+formid,formid,0,key,'uipJenisPekerjaan')
  SetToCenterForm(context.OwnerForm, aform.FormObject)
  aform.Show()

def mnuDeleteClick(sender, context):
  app = context.OwnerForm.ClientApplication
  try:
    dlg = app.ConfirmDialog('Anda yakin menghapus Jenis Pekerjaan ini?')
    if dlg:
      key = context.KeyObjConst
      resp = app.ExecuteScript('deleteJenisPekerjaan',app.CreateValues(['key',key]))

      status = resp.FirstRecord
      if status.Is_Err :
        app.ShowMessage(status.Err_Message)
        return
        
      context.DeleteRow()
  finally:
    app = None

  return 1

