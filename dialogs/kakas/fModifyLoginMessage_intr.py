def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def FormShow(form,parameter):
  form.GetControlByName('pData.IsiPesan').Text = \
    form.GetUIPartByName('uipNoData').PesanLogin

def IsiPesanChange(sender):
  form = sender.OwnerForm
  
  form.GetUIPartByName('uipNoData').Edit()
  form.GetUIPartByName('uipNoData').PesanLogin = \
    form.GetControlByName('pData.IsiPesan').Text
  form.GetUIPartByName('uipNoData').Post()

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipNoData = form.GetUIPartByName('uipNoData')

  form.CommitBuffer()
  isiPesan = form.GetControlByName('pData.IsiPesan').Text
  try:
    form.PostResult()
    sender.ExitAction = 1
  except:
    raise
