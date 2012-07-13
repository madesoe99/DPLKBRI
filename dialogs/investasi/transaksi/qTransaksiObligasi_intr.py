isShowed = 0

def MyZFill(strinput, maxlen):
  while len(strinput) < maxlen:
    strinput = '0' + strinput
  return strinput

def FormShow(form, paramter):
  qTransaksiObligasi = form.GetPanelByName('qTransaksiObligasi')
  qTransaksiObligasi.DisplayData()

  btnShowClick(form.GetControlByName('pFilter.btnShow'))

def btnShowClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipNoData = form.GetUIPartByName('uipNoData')
  qTransaksiObligasi = form.GetPanelByName('qTransaksiObligasi')

  if uipNoData.dari_tanggal > uipNoData.hingga_tanggal:
    raise Exception, 'Kesalahan Rentang Tanggal' + 'Tanggal batas awal melebihi tanggal batas akhir.'

  y, m, d = uipNoData.dari_tanggal[:3]
  dari_tanggal = '%s/%s/%s' %(MyZFill(str(m), 2),MyZFill(str(d), 2),str(y))

  y, m, d = uipNoData.hingga_tanggal[:3]

  trueHinggaTanggalDT = app.ModDateTime.EncodeDate(y, m, d) + 1
  y, m, d = app.ModDateTime.DecodeDate(trueHinggaTanggalDT)
  true_hingga_tanggal = '%s/%s/%s' %(MyZFill(str(m), 2),MyZFill(str(d), 2),str(y))

  uipNoData.Edit()
  uipNoData.true_hingga_tanggal = trueHinggaTanggalDT

  qTransaksiObligasi.SetParameter('dari_tanggal',dari_tanggal)
  qTransaksiObligasi.SetParameter('true_hingga_tanggal',true_hingga_tanggal)

  global isShowed
  if isShowed:
    qTransaksiObligasi.Refresh()
  else:
    qTransaksiObligasi.DisplayData()
    isShowed = 1

