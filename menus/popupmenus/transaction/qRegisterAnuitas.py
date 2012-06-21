def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

#fungsi ini mungkin akan dibuang
def mnuNewClick(sender, context):
  app = context.OwnerForm.ClientApplication
  formid = sender.StringTag

  aform = app.GetForm('transaction/fRegisterAnuitas_Intro',\
    'fRegisterAnuitas_Intro',0)
  #SetToCenterForm(context.OwnerForm, aform.FormObject)
  aform.Show()

def displayWithData(sender, context):
  app = context.OwnerForm.ClientApplication
  keyvalue = context.GetFieldValue('RegisterAnuitas.ID')
  if not keyvalue in [None]:
    keyobjconst = 'PObj:RegisterAnuitas#REGISTERCIF_ID=%d' % (keyvalue)
  
    mode = sender.StringTag
    formid = 'fRegisterAnuitas'
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
