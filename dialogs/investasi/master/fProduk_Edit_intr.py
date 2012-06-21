def btnOKClick(sender):
  form = sender.OwnerForm
  uipProduk = form.GetUIPartByName('uipProduk')

  #cek isian field yang harus diisi
  if (uipProduk.kode_produk and uipProduk.nama_produk) in [None,'']:
    form.ShowMessage('Kode dan Nama Produk wajib diisi!')
    return
    
  form.CommitBuffer()
  try:
    uipCustodianBank.Edit()
    uipCustodianBank.__SYSFLAG = 'N'
    form.PostResult()
    sender.ExitAction = 1
  except:
    raise
