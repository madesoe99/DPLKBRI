def MyZFill(strinput, maxlen):
  while len(strinput) < maxlen:
    strinput = '0' + strinput
  return strinput

def FormShow(form, parameter):
  app = form.ClientApplication

  uipNoData = form.GetUIPartByName('uipNoData')
  uipNoData.Edit()
  uipNoData.dateFrom = app.ModDateTime.Now()
  uipNoData.dateUntil = app.ModDateTime.Now()
  
  btnShowClick(form.GetControlByName('pFilter.btnShow'))

def btnShowClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipNoData = form.GetUIPartByName('uipNoData')
  qRegisterDeposito = form.GetPanelByName('qRegisterDeposito')

  if uipNoData.dateFrom > uipNoData.dateUntil:
    #raise 'Kesalahan Interval Tanggal','Tanggal awal tidak boleh lebih dari tanggal akhir.'
    app.ShowMessage('Tanggal awal tidak boleh lebih dari tanggal akhir.')
    return

  y, m, d = uipNoData.dateFrom[:3]
  dateFrom = '%s/%s/%s' % (MyZFill(str(m), 2),MyZFill(str(d), 2),str(y))

  y, m, d = uipNoData.dateUntil[:3]
  tomorrowEndDate = app.ModDateTime.EncodeDate(y, m, d) + 1
  y, m, d = app.ModDateTime.DecodeDate(tomorrowEndDate)
  tmrw_dateUntil = '%s/%s/%s' % (MyZFill(str(m), 2),MyZFill(str(d), 2),str(y))

  uipNoData.Edit()
  uipNoData.dateUntil_tmrw = tomorrowEndDate

  qRegisterDeposito.SetParameter('dateFrom',dateFrom)
  qRegisterDeposito.SetParameter('dateUntil_tmrw',tmrw_dateUntil)

  uipNoData.isDisplay
  if uipNoData.isDisplay == 1:
    qRegisterDeposito.Refresh()
  else:
    # uipNoData.isDisplay == 0
    qRegisterDeposito.DisplayData()
    uipNoData.isDisplay = 1

