mode = ''

def FormShow(form, parameter):
  global mode
  app = form.ClientApplication
  mode = parameter.FirstRecord.mode

  uipNoData = form.GetUIPartByName('uipNoData')
  uipNoData.Edit()
  uipNoData.dateFrom = app.ModDateTime.Now()
  uipNoData.dateUntil = app.ModDateTime.Now()

def btnOKClick(sender):
  global mode
  dictScript = {'mnuHasilInv':'hasilinv', 'mnuHasilInvPeriode':'hasilinvperiode'}
  form = sender.OwnerForm
  app = form.ClientApplication
  uipNoData = form.GetUIPartByName('uipNoData')

  form.CommitBuffer()

  scriptname = dictScript[mode] 
  
  res = app.ExecuteScript('investasi/report/%s' % scriptname 
    , app.CreateValues(
      ['dateFrom', uipNoData.dateFrom]
      , ['dateUntil', uipNoData.dateUntil]
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

