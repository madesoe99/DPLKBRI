def FormAfterProcessServerData (sender, operation_id, datapacket):
  part = sender.GetUIPartByName('userlist')
  part.First()
  
  return 1

def bKick_Click (sender):
  try:
    form = sender.OwnerForm
    app = form.ClientApplication
    uipart = form.GetUIPartByName('userlist')
    session = uipart.session_id
    datapacket = app.CreateUIDataPacketHolder()
    record = datapacket.packet.CreateSimpleDataPacket()
    record.data = session

    r_result = app.ExecuteScript('userman/S_RemoveSession', datapacket)
    dataset = r_result.packet.GetDataset(0)
    record = dataset.GetRecord(0)

    if record.IsErr:
      raise record.ErrMessage
    else:
      app.ShowMessage('User kicked successfully')
      uipart.Delete()
  finally:
    form = None
    app = None

def bKickAll_Click (sender):
  try:
    form = sender.OwnerForm
    app = form.ClientApplication
    datapacket = None

    r_result = app.ExecuteScript('userman/S_RemoveAllSession', datapacket)
    dataset = r_result.packet.GetDataset(0)
    record = dataset.GetRecord(0)

    if record.IsErr:
      raise record.ErrMessage
    else:
      app.ShowMessage('All User kicked successfully')
      bRefresh_Click(sender)
  finally:
    form = None
    app = None

def bRefresh_Click (sender):
  try:
    form = sender.OwnerForm
    app = form.ClientApplication
    uipart = form.GetUIPartByName('userlist')
    datapacket = None

    r_result = app.ExecuteScript('userman/S_GetCurrentSession', datapacket)
    dataset = r_result.packet.GetDataset(0)

    form.ResetAndClearData()
    n = dataset.RecordCount
    for i in range(n):
      record = dataset.GetRecord(i)
      uipart.Append()
      uipart.session_id = record.session_id
      uipart.user_id = record.user_id
      uipart.UserName = record.UserName
      uipart.branch_code = record.branch_code
      uipart.BranchName = record.BranchName
      uipart.Post()
    
    uipart.First()
  finally:
    form = None
    app = None
