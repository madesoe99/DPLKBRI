def MyZFill(strinput, maxlen):
  while len(strinput) < maxlen:
    strinput = '0' + strinput
  return strinput

def FormShow(form, parameter):
  app = form.ClientApplication

  uipNoData = form.GetUIPartByName('uipNoData')
  uipNoData.Edit()
  uipNoData.date_ltd = 0
  #uipNoData.dateFrom = app.ModDateTime.Now()
  #uipNoData.dateUntil = app.ModDateTime.Now()
  uipNoData.status = 'A'

  btnShowClick(form.GetControlByName('pFilter.btnShow'))

def date_ltdClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication

  uipNoData = form.GetUIPartByName('uipNoData')
  uipNoData.Edit()

  dateFrom = form.GetControlByName('pFilter.dateFrom')
  dateUntil = form.GetControlByName('pFilter.dateUntil')

  if sender.Checked:
    dateFrom.Visible = 1
    dateUntil.Visible = 1
    uipNoData.SetFieldValue('dateFrom', app.ModDateTime.Now())
    uipNoData.SetFieldValue('dateUntil', app.ModDateTime.Now())
  else:
    uipNoData.SetFieldValue('dateFrom', None)
    uipNoData.SetFieldValue('dateUntil', None)
    dateFrom.Visible = 0
    dateUntil.Visible = 0

def btnShowClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipNoData = form.GetUIPartByName('uipNoData')
  qDeposito = form.GetPanelByName('qDeposito')
  qIssuerDeposito = form.GetPanelByName('qIssuerDeposito')
  date_ltdCtrl = form.GetControlByName('pFilter.date_ltd')
  
  date_ltd = date_ltdCtrl.Checked
  if date_ltdCtrl.Checked:
    date_ltd = 1
  qDeposito.SetParameter('date_ltd', date_ltd)

  if uipNoData.dateFrom > uipNoData.dateUntil:
    #raise Exception, 'Kesalahan Interval Tanggal' + 'Tanggal awal tidak boleh lebih dari tanggal akhir.'
    app.ShowMessage('Tanggal awal tidak boleh lebih dari tanggal akhir.')
    return

  if date_ltd:
    y, m, d = uipNoData.dateFrom[:3]
    dateFrom = '%s/%s/%s' % (MyZFill(str(m), 2),MyZFill(str(d), 2),str(y))

    y, m, d = uipNoData.dateUntil[:3]
    tomorrowEndDate = app.ModDateTime.EncodeDate(y, m, d) + 1
    y, m, d = app.ModDateTime.DecodeDate(tomorrowEndDate)
    tmrw_dateUntil = '%s/%s/%s' % (MyZFill(str(m), 2),MyZFill(str(d), 2),str(y))

    uipNoData.Edit()
    uipNoData.dateUntil_tmrw = tomorrowEndDate

    qDeposito.SetParameter('dateFrom', dateFrom)
    qDeposito.SetParameter('dateUntil_tmrw', tmrw_dateUntil)
    
  status_ltd = 0
  status = 'T'
  if uipNoData.status == 'A':
    status_ltd = 1
    status = 'T'
  elif uipNoData.status == 'T':
    status_ltd = 1
    status = 'F'
  #else:
  #  # uipNoData.status == 'S'

  qDeposito.SetParameter('status_ltd', status_ltd)
  qDeposito.SetParameter('status', status)
  qDeposito.SetParameter('pihak_ketiga',qIssuerDeposito.GetFieldValue('Deposito.pihak_ketiga'))

  if uipNoData.isDisplay == 1:
    qDeposito.Refresh()
  else:
    # uipNoData.isDisplay == 0
    qDeposito.DisplayData()
    uipNoData.isDisplay = 1