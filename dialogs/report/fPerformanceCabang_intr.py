def FormShow(form, parameter):
  app = form.ClientApplication

  uipNoData = form.GetUIPartByName('uipNoData')
  uipNoData.Edit()
  uipNoData.dateFrom = app.ModDateTime.Now()
  uipNoData.dateUntil = app.ModDateTime.Now()

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipNoData = form.GetUIPartByName('uipNoData')


  res = app.ExecuteScript('report/PerformanceCabang',
     app.CreateValues(
      ['dateFrom', uipNoData.dateFrom]
      , ['dateUntil', uipNoData.dateUntil]
      )
  )

  app.DownloadItem(res.FirstRecord.filename,'v')
  sender.ExitAction = 1
