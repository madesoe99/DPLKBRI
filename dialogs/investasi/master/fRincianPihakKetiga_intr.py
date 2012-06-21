def OnClick_OK (sender) :
  form = sender.OwnerForm
  app = form.ClientApplication
  if app.ConfirmDialog('Apakah anda akan menyimpan perubahan ini?') :
    form.CommitBuffer()
    form.PostResult()
    sender.ExitAction = 1
