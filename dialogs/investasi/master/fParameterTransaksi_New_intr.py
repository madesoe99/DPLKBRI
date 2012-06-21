def btnOKClick(sender):
  form = sender.OwnerForm
  uip = form.GetUIPartByName('uip')


  form.CommitBuffer()
  try:
    uip.Edit()
    uip.__SYSFLAG = 'N'
    form.PostResult()
    sender.ExitAction = 1
  except:
    raise
