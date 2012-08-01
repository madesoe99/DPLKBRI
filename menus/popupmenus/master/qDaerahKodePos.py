def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def mnuNewClick(sender, context):
  app = context.OwnerForm.ClientApplication
  formid = sender.StringTag

  aform = app.CreateForm('master/'+formid,formid,0 ,None ,None)
  #SetToCenterForm(context.OwnerForm, aform.FormObject)
  aform.FormContainer.Show()

def displayWithData(sender, context):
  app = context.OwnerForm.ClientApplication
  key = context.KeyObjConst
  formid = sender.StringTag
  aform = app.GetFormWithData('master/'+formid,formid,0,key,'uipDaerahKodePos')
  SetToCenterForm(context.OwnerForm, aform.FormObject)
  aform.Show()

def mnuDeleteClick(sender, context):
  app = context.OwnerForm.ClientApplication
  try:
    dlg = app.ConfirmDialog('Anda yakin menghapus Data Kode Pos ini?')
    if dlg:
      key = context.KeyObjConst

      app.DeletePObj(key)
      #app.ShowMessage('Data was succesfully deleted')
      context.DeleteRow()
  finally:
    app = None

  return 1
