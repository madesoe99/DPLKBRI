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
  aform = app.GetFormWithData('master/'+formid,formid,0,key,'uipJenisPenerimaanManfaat')
  SetToCenterForm(context.OwnerForm, aform.FormObject)
  aform.Show()

def mnuDeleteClick(sender, context):
  app = context.OwnerForm.ClientApplication
  try:
    dlg = app.ConfirmDialog('Anda yakin menghapus Jenis Penerimaan Manfaat ini?')
    if dlg:
      key = context.KeyObjConst

      app.DeletePObj(key)
      #app.ShowMessage('Data was succesfully deleted')
      context.DeleteRow()
  finally:
    app = None

  return 1

