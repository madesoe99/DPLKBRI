def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def mnuNewClick(sender, context):
  app = context.OwnerForm.ClientApplication
  formid = sender.StringTag

  aform = app.GetForm('transaction/fRegisterWasiatUmmat_Intro',\
    'fRegisterWasiatUmmat_Intro',0)
  #SetToCenterForm(context.OwnerForm, aform.FormObject)
  aform.Show()

def displayWithData(sender, context):
  app = context.OwnerForm.ClientApplication
  keyvalue = context.GetFieldValue('RegisterAsuransi.ID')

  keyobjconst = 'PObj:RegisterAsuransi#REGISTERCIF_ID=%d' % (keyvalue)

  mode = sender.StringTag
  formid = 'fRegisterWasiatUmmat'
  aform = app.GetFormWithData('transaction/'+formid,formid,0,keyobjconst,'uipRegisterCIF')
  #SetToCenterForm(context.OwnerForm, aform.FormObject)
  ea = aform.Show(app.CreateValues(['mode',mode]))

  if mode == 'auth':
    if ea == 1:
      # otorisasi berhasil
      #app.ShowMessage('Otorisasi berhasil.')
      context.DeleteRow()
    elif ea <> 2:
      # penghapusan berhasil
      #app.ShowMessage('Penolakan register berhasil.')
      context.DeleteRow()
