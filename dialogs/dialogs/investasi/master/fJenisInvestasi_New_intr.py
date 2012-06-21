def btnOKClick(sender):
  form = sender.OwnerForm
  uipJenisInvestasi = form.GetUIPartByName('uipJenisInvestasi')
  
  form.CommitBuffer()
  uipJenisInvestasi.Edit()
  uipJenisInvestasi.__SYSFLAG = 'N'
  form.PostResult()

  sender.ExitAction = 1

