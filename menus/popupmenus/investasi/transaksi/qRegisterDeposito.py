def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def displayWithData(sender, context):
  app = context.OwnerForm.ClientApplication
  mode = sender.StringTag
  formid = 'fRegisterDeposito'

  if mode == 'new':
    key = mode
    uipart = mode
  else:
    key = context.KeyObjConst
    uipart = 'uipRegisterDeposito'

  aform = app.GetFormWithData('investasi/transaksi/'+formid,formid,0,key,uipart)
  SetToCenterForm(context.OwnerForm, aform.FormObject)
  ea = aform.Show(
    app.CreateValues(
      ['mode',mode]
      , ['inv','A']
      , ['caption',sender.Caption.replace('...','')]
    )
  )

  if mode == 'auth':
    if ea == 1:
      # otorisasi berhasil
      #app.ShowMessage('Otorisasi berhasil.')
      context.DeleteRow()
    elif ea <> 2:
      # penghapusan berhasil
      #app.ShowMessage('Penolakan register berhasil.')
      context.DeleteRow()

