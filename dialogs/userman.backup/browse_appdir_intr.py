def reducepath(spath):
  slis = spath.split('\\')
  rpath = slis[0]
  for i in range(1, len(slis) - 1):
    rpath = rpath + '\\' + slis[i]

  return rpath

def FormAfterProcessServerData (sender, operation_id, datapacket):
  part = sender.GetUIPartByName('list_class')
  part.First()
  
  sender.GetControlByName('button_panel.bUp').Enabled = 0

  return 1

def bUp_Click (sender):
  try:
    form = sender.OwnerForm
    app = form.ClientApplication
    uipart = form.GetUIPartByName('list_class')

    acpart = form.GetUIPartByName('active_directory')
    if acpart.path_type == 0:
      sender.Enabled = 0
      return 0

    new_actual_path = reducepath(acpart.actual_server_path)
    new_display_path = reducepath(reducepath(acpart.display_path))
    
    datapacket = app.CreateUIDataPacketHolder()
    record = datapacket.packet.CreateSimpleDataPacket()
    record.data = new_actual_path

    r_result = app.ExecuteScript('userman/S_GetListOfDir', datapacket)
    dataset = r_result.packet.GetDataset(0)

    uipart.ClearData()
    n = dataset.RecordCount
    for i in range(n):
      record = dataset.GetRecord(i)
      uipart.Append()
      uipart.fd_name = record.fd_name
      uipart.fd_size = record.fd_size
      uipart.fd_type = record.fd_type
      uipart.fd_type_char = record.fd_type_char
      uipart.fd_mdate = record.fd_mdate
      uipart.Post()
    
    uipart.First()

    acpart.Edit()
    acpart.actual_server_path = new_actual_path
    acpart.display_path = new_display_path + '\\'
    if new_display_path == 'SERVER':
      acpart.path_type = 0
      sender.Enabled = 0
    acpart.Post()

  finally:
    form = None
    app = None

def bOpen_Click (sender):
  try:
    form = sender.OwnerForm
    app = form.ClientApplication
    uipart = form.GetUIPartByName('list_class')
    if not (uipart.fd_type == 1):
      sender.ExitAction = 1
      return 0

    fname = uipart.fd_name
    acpart = form.GetUIPartByName('active_directory')

    new_actual_path = acpart.actual_server_path + '\\' + fname
    new_display_path = acpart.display_path + fname + '\\'
    
    datapacket = app.CreateUIDataPacketHolder()
    record = datapacket.packet.CreateSimpleDataPacket()
    record.data = new_actual_path

    r_result = app.ExecuteScript('userman/S_GetListOfDir', datapacket)
    dataset = r_result.packet.GetDataset(0)

    uipart.ClearData()
    n = dataset.RecordCount
    for i in range(n):
      record = dataset.GetRecord(i)
      uipart.Append()
      uipart.fd_name = record.fd_name
      uipart.fd_size = record.fd_size
      uipart.fd_type = record.fd_type
      uipart.fd_type_char = record.fd_type_char
      uipart.fd_mdate = record.fd_mdate
      uipart.Post()
    
    uipart.First()

    acpart.Edit()
    acpart.actual_server_path = new_actual_path
    acpart.display_path = new_display_path
    acpart.path_type = 1
    acpart.Post()
    form.GetControlByName('button_panel.bUp').Enabled = 1
  finally:
    form = None
    app = None

def bRefresh_Click (sender):
  try:
    form = sender.OwnerForm
    app = form.ClientApplication
    uipart = form.GetUIPartByName('list_class')

    acpart = form.GetUIPartByName('active_directory')
        
    datapacket = app.CreateUIDataPacketHolder()
    record = datapacket.packet.CreateSimpleDataPacket()
    record.data = acpart.actual_server_path

    r_result = app.ExecuteScript('userman/S_GetListOfDir', datapacket)
    dataset = r_result.packet.GetDataset(0)

    uipart.ClearData()
    n = dataset.RecordCount
    for i in range(n):
      record = dataset.GetRecord(i)
      uipart.Append()
      uipart.fd_name = record.fd_name
      uipart.fd_size = record.fd_size
      uipart.fd_type = record.fd_type
      uipart.fd_type_char = record.fd_type_char
      uipart.fd_mdate = record.fd_mdate
      uipart.Post()
    
    uipart.First()
  finally:
    form = None
    app = None
