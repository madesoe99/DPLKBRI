def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def displayWithData(sender, context):
  app = context.OwnerForm.ClientApplication
  mode = sender.StringTag

  if mode == 'new':
    key = mode
    uipart = mode
    formid = 'fRegisterInvestasi'
  else:
    # mode == view
    key = context.KeyObjConst
    uipart = 'uipInvestasi'
    formid = 'fInvestasi'

  aform = app.GetFormWithData('investasi/transaksi/'+formid,formid,0,key,uipart)
  SetToCenterForm(context.OwnerForm, aform.FormObject)
  ea = aform.Show(app.CreateValues(['mode',mode]))

def mnuTransInvClick(sender, context):
  app = context.OwnerForm.ClientApplication

  key = context.KeyObjConst
  uipart = 'uipInvestasi'
  formid = sender.StringTag

  aform = app.GetFormWithData('investasi/transaksi/'+formid,formid,0,key,uipart)
  SetToCenterForm(context.OwnerForm, aform.FormObject)
  ea = aform.Show(app.CreateValues(['mode','new']))
