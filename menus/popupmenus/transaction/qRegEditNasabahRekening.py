def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def mnuNewClick(sender, context):
  app = context.OwnerForm.ClientApplication
  formid = 'fEditNasabahRekening_Intro'

  aform = app.GetForm('transaction/'+formid,formid,0)
  SetToCenterForm(context.OwnerForm, aform.FormObject)
  aform.Show(app.CreateValues(['mode','new']))

def displayWithData(sender, context):
  app = context.OwnerForm.ClientApplication
  key = context.KeyObjConst
  mode = sender.StringTag
  formid = 'fEditNasabahRekening'

  #aform = app.GetFormWithData('transaction/'+formid,formid,0,key,uipart)
  aform = app.GetFormWithData('transaction/'+formid,formid,0,key,'uipRegEditNasabahRekening')
  SetToCenterForm(context.OwnerForm, aform.FormObject)
  aform.Show(app.CreateValues(['mode',mode]))

def mnuDeleteClick(sender, context):
  app = context.OwnerForm.ClientApplication
  try:
    dlg = app.ConfirmDialog('Are you sure you want to delete this row?')
    if dlg:
      key = context.KeyObjConst

      app.DeletePObj(key)
      app.ShowMessage('Data was succesfully deleted')
      context.DeleteRow()
  finally:
    app = None

  return 1

def mnuAuthorizeClick(sender, context):
  app = context.OwnerForm.ClientApplication
  try:
    dlg = app.ConfirmDialog('Are you sure you want to authorize this row?')
    if dlg:
      id = context.GetFieldValue('RegEditNasabahRekening.ID')

      app.ExecuteScript('transaction/regeditnsbrek_auth',app.CreateValues(['id',id]))
      app.ShowMessage('Data was succesfully authorized')
      context.DeleteRow()
  finally:
    app = None

  return 1

