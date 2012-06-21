def FormShow(form, parameter):
  app = form.ClientApplication

  uipNoData = form.GetUIPartByName('uipNoData')
  uipNoData.Edit()


def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipNoData = form.GetUIPartByName('uipNoData')

  res = app.ExecuteScript('report/SuratAkseptasi',
        app.CreateValues(
          ['no_peserta',uipNoData.no_peserta]
        )
  )
  app.DownloadItem(res.FirstRecord.filename,'v')
  sender.ExitAction = 1


