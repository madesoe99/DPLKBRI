def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def FormShow(form,parameter):
  form.GetUIPartByName('uipUserOnline').First()

def btnRefreshClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipUserOnline = form.GetUIPartByName('uipUserOnline')
  datapacket = None

  try:
    res = app.ExecuteScript('userman/S_GetCurrentSession', datapacket)
    dataset = res.packet.GetDataset(0)

    uipUserOnline.ClearData()
    for i in range(dataset.RecordCount):
      record = dataset.GetRecord(i)
      uipUserOnline.Append()
      
      uipUserOnline.SessionID = record.session_id
      uipUserOnline.LoginID = record.user_id
      uipUserOnline.NamaUser = record.UserName
      uipUserOnline.BranchCode = record.branch_code
      uipUserOnline.BranchName = record.BranchName
      
      uipUserOnline.Post()

    uipUserOnline.First()
  finally:
    form = None
    app = None

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipNoData = form.GetUIPartByName('uipNoData')
  uipUserOnline = form.GetUIPartByName('uipUserOnline')

  form.CommitBuffer()
  isiPesan = form.GetControlByName('pData.IsiPesan').Text
  
  #cek pesan kosong
  if isiPesan in [None,'']:
    form.ShowMessage('Pesan yang akan dikirim masih kosong! Mohon untuk diisi.')
    return
  
  try:
    if uipNoData.isBroadcast and \
      app.ConfirmDialog('Anda yakin mem-Broadcast pesan ini ke seluruh '\
      'pengguna yang sedang online?'):
      #broadcast pesan
      app.ExecuteScript('MessagePush', app.CreateValues(['message',isiPesan],\
        ['isBroadcast',uipNoData.isBroadcast]))
    elif not uipNoData.isBroadcast and \
      app.ConfirmDialog('Anda yakin mengirim pesan ini ke %s [%s]?'\
      % (uipUserOnline.LoginID,uipUserOnline.NamaUser)):
        #tidak perlu broadcast, hanya ke user tertentu
        app.ExecuteScript('MessagePush', app.CreateValues(['message',isiPesan],\
          ['isBroadcast',uipNoData.isBroadcast],['userID',uipUserOnline.LoginID]))
  except:
    raise
