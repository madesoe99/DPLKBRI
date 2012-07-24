def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def displayWithData(sender, context):
  app = context.OwnerForm.ClientApplication
  key = context.KeyObjConst
  mode = sender.StringTag
  ph = app.CreateValues(['key', key])

  form = app.CreateForm('transaction/fRekeningAnuitas', 'fRekeningAnuitas', 0, ph, None)
  SetToCenterForm(context.OwnerForm, form.FormObject)
  form.Show()
