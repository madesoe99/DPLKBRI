import sys

class frmBrowseFolder:
  def __init__(self, formObj, parentForm):
    self.LastFolderSelected = ""
    pass
    
  def selectFile(self):
    res = self.FormContainer.Show()
    if res == 1:
      return self.active_directory.actual_server_path + self.list_class.fd_name
    else:
      return None
    #-
  #--
    
  def reducepath(self, spath):
    if spath != "" and spath[-1] == "/": spath = spath[0:-1]
    slis = spath.split('/')
    rpath = slis[0]
    for i in range(1, len(slis) - 1):
      rpath = rpath + '/' + slis[i]
    rpath += "/"
    return rpath
    
  def extractFileFromPath(self, spath):
    elmts = spath.split('\\')
    return elmts[-1]
  
  def FormAfterProcessServerData(self, sender, operation_id, datapacket):
    part = sender.GetUIPartByName('list_class')
    part.First()
    sender.GetControlByName('button_panel.bUp').Enabled = self.active_directory.path_type == 1
    acpart = self.active_directory
    if acpart.isErr:
      self.FormObject.ClientApplication.ShowMessage(acpart.errMsg)
    #--
    return 1
    
  def bUp_Click (self, sender):
    form = sender.OwnerForm
    app = form.ClientApplication
    uipart = form.GetUIPartByName('list_class')

    acpart = form.GetUIPartByName('active_directory')
    if acpart.path_type == 0:
      sender.Enabled = 0
      return 0
    mask = acpart.mask or ""

    new_path = self.reducepath(acpart.actual_server_path)
    ph = app.CreateValues(['path', new_path], ['mask', mask])
    form.SetDataWithParameters(ph)
  #--
  
  def bOpen_Click (self, sender):
    form = sender.OwnerForm
    app = form.ClientApplication
    uipart = form.GetUIPartByName('list_class')
    if not (uipart.fd_type == 1):
      return 0

    fname = uipart.fd_name
    acpart = form.GetUIPartByName('active_directory')
    new_path = acpart.actual_server_path + fname + "/"
    mask = acpart.mask or ""
    ph = app.CreateValues(['path', new_path], ['mask', mask])
    form.SetDataWithParameters(ph)
  #--
  
  def bRefresh_Click (self, sender):
    form = sender.OwnerForm
    app = form.ClientApplication
    uipart = form.GetUIPartByName('list_class')

    acpart = form.GetUIPartByName('active_directory')
    new_path = acpart.actual_server_path
    mask = acpart.mask or ""
    ph = app.CreateValues(['path', new_path], ['mask', mask])
    form.SetDataWithParameters(ph)
  #--
  
  def bDownloadClick(self, sender):
    form = self.FormObject
    app = form.ClientApplication
    
    uipart = form.GetUIPartByName('list_class')
    if uipart.fd_type == 1:
      return 0

    fname = uipart.fd_name
    acpart = form.GetUIPartByName('active_directory')
    new_path = acpart.actual_server_path + fname

    ph = form.CallServerMethod('download_file', app.CreateValues(['path', new_path]))
    sw = ph.packet.GetStreamWrapper(0)
    extension = app.GetExtensionFromMIMEType(sw.MIMEType)
    fileName = app.SaveFileDialog("Save as...", "*.*")
    if fileName != None and fileName != "":
      sw.SaveToFile(fileName)
  #--
  
  def bUploadClick(self, sender):
    form = self.FormObject
    app = form.ClientApplication
    
    acpart = form.GetUIPartByName('active_directory')
    target_path = acpart.actual_server_path
    
    fName = app.OpenFileDialog("Select file to upload", "*.*")
    if fName == None or fName == "":
      return
    
    fileName = self.extractFileFromPath(fName) 
    ph = app.CreateValues(["path", target_path], ["file_name", fileName])
    sw = ph.Packet.AddStreamWrapper()
    sw.LoadFromFile(fName)
                                         
    form.CallServerMethod('upload_file', ph)
  #--
#--
