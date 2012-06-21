def MyZFill(strinput, maxlen):
  while len(strinput) < maxlen:
    strinput = '0' + strinput
  return strinput

def FormShow(form, paramter):
  qTransaksiInvestasi = form.GetPanelByName('qTransaksiInvestasi')
  qTransaksiInvestasi.DisplayData()

def btnShowClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipNoData = form.GetUIPartByName('uipNoData')
  qTransaksiInvestasi = form.GetPanelByName('qTransaksiInvestasi')

  if uipNoData.dari_tanggal > uipNoData.hingga_tanggal:
    raise 'Kesalahan Rentang Tanggal','Tanggal batas awal melebihi tanggal batas akhir.'

  y, m, d = uipNoData.dari_tanggal[:3]
  dari_tanggal = '%s/%s/%s' %(MyZFill(str(m), 2),MyZFill(str(d), 2),str(y))

  y, m, d = uipNoData.hingga_tanggal[:3]

  trueHinggaTanggalDT = app.ModDateTime.EncodeDate(y, m, d) + 1
  y, m, d = app.ModDateTime.DecodeDate(trueHinggaTanggalDT)
  true_hingga_tanggal = '%s/%s/%s' %(MyZFill(str(m), 2),MyZFill(str(d), 2),str(y))

  uipNoData.Edit()
  uipNoData.true_hingga_tanggal = trueHinggaTanggalDT

  qTransaksiInvestasi.SetParameter('dari_tanggal',dari_tanggal)
  qTransaksiInvestasi.SetParameter('true_hingga_tanggal',true_hingga_tanggal)
  #qTransaksiInvestasi.DisplayData()
  qTransaksiInvestasi.Refresh()

