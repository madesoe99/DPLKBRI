def FormShow(form, parameter):
  uipPI = form.GetUIPartByName('uipPaketInvestasi')
  uipPI.Edit()
  
  uipPI.isAktif = 'T'

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
  form = pclassui.OwnerForm
  pclassui.kode_paket_investasi = form.GetUIPartByName('uipPaketInvestasi').kode_paket_investasi
  if pclassui.maks_proporsi <= 0.0 or pclassui.maks_proporsi > 100.0:
    raise Exception, 'PERINGATAN' + 'Maksimal proporsi harus lebih besar dari 0 dan kurang dari sama dengan 100!'

def GridAfterNewRecord(pclassui):
  #inisialisasi maksimal proporsi dengan nilai 0.0
  pclassui.maks_proporsi = 0.0

def LJenisInvAfterLookup(sender, linkui):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRincianPaketInvestasi = form.GetUIPartByName('uipRincianPaketInvestasi')
  uipRincianPaketInvestasi.Edit()
  uipRincianPaketInvestasi.kode_jns_investasi = uipRincianPaketInvestasi.GetFieldValue('LJenisInvestasi.kode_jns_investasi')