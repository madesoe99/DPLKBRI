def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def displayWithData(sender, context):
  app = context.OwnerForm.ClientApplication
  uipTL = context.OwnerForm.GetUIPartByName('uipTemplateList')
  parameter = app.CreateValues(['namaTemplate',uipTL.NamaTemplate],\
    ['mode',sender.StringTag])
  
  formid = sender.Name
  aform = app.GetFormWithParameters('kakas/'+formid,formid,0,parameter)
  #SetToCenterForm(context.OwnerForm, aform.FormObject)
  aform.Show(app.CreateValues(['mode',sender.StringTag]))
