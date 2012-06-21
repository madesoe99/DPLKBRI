def FormShow(form, parameter):
  uipNoData = form.GetUIPartByName('uipNoData')
  uipNoData.Edit()
  uipNoData.klasifikasi = 'J'

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipNoData = form.GetUIPartByName('uipNoData')

  res = app.ExecuteScript('report/profil_peserta',\
    app.CreateValues(['klasifikasi',uipNoData.klasifikasi]\
    )\
  )

  app.DownloadItem(res.FirstRecord.filename,'v')
  sender.ExitAction = 1

