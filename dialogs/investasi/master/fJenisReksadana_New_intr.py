def btnOKClick(sender):
  form = sender.OwnerForm
  uipJenisReksadana = form.GetUIPartByName('uipJenisReksadana')

  #cek isian field yang harus diisi
  if (uipJenisReksadana.kode_jns_reksadana) in [None,'']:
    form.ShowMessage('Kode Jenis Reksadana wajib diisi!')
    return
    
  form.CommitBuffer()
  try:
    uipJenisReksadana.Edit()
    uipJenisReksadana.__SYSFLAG = 'N'
    form.PostResult()
    sender.ExitAction = 1
  except:
    raise
