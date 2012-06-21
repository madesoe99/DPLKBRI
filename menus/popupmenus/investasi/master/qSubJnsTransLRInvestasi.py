def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def mnuNewClick(sender, context):
  app = context.OwnerForm.ClientApplication
  formid = sender.StringTag

  #aform = app.GetForm('investasi/master/'+formid,formid,0)
  aform = app.GetFormWithData('investasi/master/'+formid,formid,0,'x','x')
  SetToCenterForm(context.OwnerForm, aform.FormObject)
  aform.Show()

def displayWithData(sender, context):
  app = context.OwnerForm.ClientApplication
  key = context.KeyObjConst
  formid = sender.StringTag
  aform = app.GetFormWithData('investasi/master/'+formid,formid,0,key,'uipSubJnsTransLRInvestasi')
  SetToCenterForm(context.OwnerForm, aform.FormObject)
  aform.Show()

def mnuDeleteClick(sender, context):
  app = context.OwnerForm.ClientApplication
  try:
    dlg = app.ConfirmDialog('Anda yakin menghapus kode sub jenis investasi %s?' \
      % (context.GetFieldValue('SubJnsTransLRInvestasi.kode_subjns_LRInvestasi')))
    if dlg:
      key = context.KeyObjConst
      app.DeletePObj(key)
      context.DeleteRow()
  finally:
    app = None

  return 1

