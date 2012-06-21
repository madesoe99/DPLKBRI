def btnOKClick(sender):
  form = sender.OwnerForm
  uipSektoral = form.GetUIPartByName('uipSektoral')

  #cek isian field yang harus diisi
  if (uipSektoral.kode_sektoral and uipSektoral.nama_sektoral) in [None,'']:
    form.ShowMessage('Kode dan Nama Sektoral wajib diisi!')
    return
    
  form.CommitBuffer()
  try:
    uipSektoral.Edit()
    uipSektoral.__SYSFLAG = 'N'
    form.PostResult()
    sender.ExitAction = 1
  except:
    raise
