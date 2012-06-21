def FormShow(form, parameter):
  app = form.ClientApplication

  uipNoData = form.GetUIPartByName('uipNoData')
  uipNoData.Edit()
  uipNoData.dateFrom = app.ModDateTime.Now()
  uipNoData.dateUntil = app.ModDateTime.Now()

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  Exef = '.htm'
  uipNoData = form.GetUIPartByName('uipNoData')

  form.CommitBuffer()

  res = app.ExecuteScript('investasi/report/roijenisinv'
    , app.CreateValues(
      ['dateFrom', uipNoData.dateFrom]
      , ['dateUntil', uipNoData.dateUntil]
      )
  )

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

