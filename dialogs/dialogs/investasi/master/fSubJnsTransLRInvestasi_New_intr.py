def btnOKClick(sender):
  form = sender.OwnerForm
  uipSubJnsTransLRInvestasi = form.GetUIPartByName('uipSubJnsTransLRInvestasi')

  form.CommitBuffer()
  uipSubJnsTransLRInvestasi.Edit()
  uipSubJnsTransLRInvestasi.__SYSFLAG = 'N'
  form.PostResult()

  sender.ExitAction = 1

