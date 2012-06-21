def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def ShowForm(sender, context):
  app = context.OwnerForm.ClientApplication
  key = context.KeyObjConst
  mode = sender.StringTag
  
  if mode == 'new':
    aform = app.CreateForm('transaction/fRegistrasiCorp_New', 'fRegistrasiCorp_New', 0, None, None)
    ea = aform.Show(app.CreateValues(['mode','new']))

  else:
    # mode edit, view, auth
    aform = app.GetFormWithData('transaction/fRegistrasiCorp','fRegistrasiCorp',\
      0,key,'uipRegEditNasabahDPLKCorporate')

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
