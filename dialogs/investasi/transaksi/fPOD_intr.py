def MyZFill(strinput, maxlen):
  while len(strinput) < maxlen:
    strinput = '0' + strinput
  return strinput

def FormShow(form, parameter):
  app = form.ClientApplication
  uipNoData = form.GetUIPartByName('uipNoData')

  #set parameter nowDate
  uipNoData.Edit()
  uipNoData.TglPOD = app.ModDateTime.Now()
  y, m, d = app.ModDateTime.DecodeDate(app.ModDateTime.Now())
  uipNoData.nowDate = '%s/%s/%d' % (
    MyZFill(str(m), 2)
    , MyZFill(str(d), 2)
    , y
  )

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipNoData = form.GetUIPartByName('uipNoData')

  if app.ConfirmDialog('Lakukan POD hari ini?'):
    #tID = app.ExecuteScriptTrackable(
    #  'investasi/transaksi/pod_l'
    #  , app.CreateValues(['ID_TransactionBatch', uipNoData.GetFieldValue('LTransactionBatch.ID_TransactionBatch')])
    #)
    #app.ShowTaskProgress(tID)
    app.ExecuteScript('investasi/transaksi/pod_inv', app.CreateValues(['execFile','investasi/transaksi/pod_l']))
    sender.ExitAction = 1

def btnCancelClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication

  sender.ExitAction = 2

