# event handler on save

def FormAfterProcessServerData (sender, operation_id, datapacket):
  part = sender.GetUIPartByName('menuitems')
  part.First()
  
  return 1

def bSave_Click (sender):
  try:
    formobj = sender.OwnerForm
    formobj.CommitBuffer()
    app = formobj.ClientApplication
    datapacket = formobj.GetDataPacket()

    returnpacket = app.ExecuteScript('S_UpdateMenuSecurity', datapacket)
    app.ShowMessage('update successful')
    sender.ExitAction = 1
  finally:
    formobj = None
    app = None
