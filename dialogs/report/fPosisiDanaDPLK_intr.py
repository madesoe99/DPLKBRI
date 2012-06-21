def FormShow(form, parameter):
  app = form.ClientApplication

  uipNoData = form.GetUIPartByName('uipNoData')
  uipNoData.Edit()
  uipNoData.tanggal_awal = app.ModDateTime.Now()
  uipNoData.tanggal_akhir = app.ModDateTime.Now()

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipNoData = form.GetUIPartByName('uipNoData')

  res = app.ExecuteScript('report/PosisiDanaDPLK',
    app.CreateValues(
      ['tanggal_akhir',uipNoData.tanggal_akhir]
    )
  )

  app.DownloadItem(res.FirstRecord.filename,'v')
  sender.ExitAction = 1
