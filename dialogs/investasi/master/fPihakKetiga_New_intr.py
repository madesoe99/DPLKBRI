import sys

def btnOKClick(sender):
  form = sender.OwnerForm
  uipPihakKetiga = form.GetUIPartByName('uipPihakKetiga')

  #cek isian field yang harus diisi
  if (uipPihakKetiga.kode_pihak_ketiga and uipPihakKetiga.nama_pihak_ketiga) in [None,'']:
    form.ShowMessage('Kode dan Nama Pihak Ketiga wajib diisi!')
    return

  form.CommitBuffer()
  try:
    uipPihakKetiga.Edit()
    uipPihakKetiga.__SYSFLAG = 'N'
    form.PostResult()
    sender.ExitAction = 1
  except:
    #raise Exception, str(sys.exc_info()[1])
    form.ShowMessage(str(sys.exc_info()[1]))
    return 
