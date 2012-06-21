def btnOKClick(sender):
  form = sender.OwnerForm
  uipPaketInvestasi = form.GetUIPartByName('uipPaketInvestasi')

  #cek rincian paket investasi
  if form.GetUIPartByName('uipRincianPaketInvestasi').RecordCount == 0:
    form.ShowMessage('Rincian Paket Investasi wajib diisi.')
    return

  form.CommitBuffer()
  try:
    uipPaketInvestasi.Edit()
    uipPaketInvestasi.__SYSFLAG = 'N'
    form.PostResult()
    sender.ExitAction = 1
  except:
    raise
  
def GridBeforePost(pclassui):
  if pclassui.maks_proporsi <= 0.0:
    raise 'PERINGATAN','Maksimal proporsi harus lebih besar dari 0!'

def GridAfterNewRecord(pclassui):
  #inisialisasi maksimal proporsi dengan nilai 0.0
  pclassui.maks_proporsi = 0.0
