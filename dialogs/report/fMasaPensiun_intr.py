def FormShow(form, parameter):
  app = form.ClientApplication

  uipNoData = form.GetUIPartByName('uipNoData')
  uipNoData.Edit()
  uipNoData.tanggal_pensiun_awal = app.ModDateTime.Now()
  uipNoData.tanggal_pensiun_akhir = app.ModDateTime.Now()
  uipNoData.isDipercepat = parameter.FirstRecord.isDipercepat == 'T'

  if uipNoData.isDipercepat:
    form.Caption == form.Caption + ' Dipercepat'

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipNoData = form.GetUIPartByName('uipNoData')

  res = app.ExecuteScript('report/masa_pensiun',\
    app.CreateValues(\
      ['tanggal_pensiun_awal',uipNoData.tanggal_pensiun_awal]\
      ,['tanggal_pensiun_akhir',uipNoData.tanggal_pensiun_akhir]\
      ,['isDipercepat',uipNoData.isDipercepat]\
    )\
  )

  app.DownloadItem(res.FirstRecord.filename,'v')
  sender.ExitAction = 1

