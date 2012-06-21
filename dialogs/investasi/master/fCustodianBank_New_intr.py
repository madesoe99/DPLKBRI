def btnOKClick(sender):
  form = sender.OwnerForm
  uipCustodianBank = form.GetUIPartByName('uipCustodianBank')

  #cek isian field yang harus diisi
  if (uipCustodianBank.BankCode and uipCustodianBank.BankName) in [None,'']:
    form.ShowMessage('Kode dan Nama Custodian Bank wajib diisi!')
    return
    
  form.CommitBuffer()
  try:
    uipCustodianBank.Edit()
    uipCustodianBank.__SYSFLAG = 'N'
    form.PostResult()
    sender.ExitAction = 1
  except:
    raise
