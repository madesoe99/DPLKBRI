def FormShow(form, parameter):
  app = form.ClientApplication

  tahun = app.ModDateTime.DecodeDate(app.ModDateTime.Now())[0]

  uipNoData = form.GetUIPartByName('uipNoData')
  uipNoData.Edit()
  uipNoData.tahun = tahun

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipNoData = form.GetUIPartByName('uipNoData')

  form.CommitBuffer()

  res = app.ExecuteScript('investasi/report/hasiltahunan'
    , app.CreateValues(
      ['year', uipNoData.tahun]
      )
  )

  Exef = '.htm'
  #app.DownloadItem(res.FirstRecord.filename,'v')
  streamWrapper = res.Packet.GetStreamWrapper(0)
  fileName = form.OpenFileDialog("Select file to save..",
      "Format Save Files(*%s)|*%s"%(Exef,Exef))
  if fileName != "":
     if fileName[-4:] != Exef :
        fileName = fileName + Exef
     streamWrapper.SaveToFile(fileName)
     if app.ConfirmDialog('Apakah file akan ditampilkan ?') :
        app.ShellExecuteFile(fileName)
     sender.ExitAction = 1

