class fUploadCorporate:
  def __init__(self, formObj, parentForm):
    #self.formObj, self.app = formObj, formObj.ClientApplication
    if parentForm != None:
      self.parentForm = parentForm
    else:
      self.parentForm = None
  #--

  def Show(self):
    app = self.FormObject.ClientApplication
    
    self.uipTrxSession.Edit()
    self.uipTrxSession.filename = ''
    
    self.FormContainer.Show()
          
  def BrowseClick(self,sender):
    app = self.FormObject.ClientApplication

    fileName = app.OpenFileDialog("Open file..", "Excel Files(*.xls)|*.xls")

    if fileName not in [None, ""]:
      self.uipTrxSession.Edit()
      self.uipTrxSession.filename = fileName

  def UploadClick(self,sender):
    formObj = self.FormObject
    app = formObj.ClientApplication
    
    uipTrxSession = self.uipTrxSession
    if uipTrxSession.upload_type in (None,0,'') :
      app.ShowMessage('Jenis upload belum ditentukan')
      return

    if not uipTrxSession.upload_type in ['P','K','W','I','A','R']:
      app.ShowMessage('PERINGATAN!\nJenis upload yang dipilih tidak terdaftar...')
      return

    if uipTrxSession.filename in (None,0,'') :
      app.ShowMessage('File tidak ada...')
      return
    
    formObj.CommitBuffer()
    filename=uipTrxSession.filename

    ph = formObj.GetDataPacket()
    sw = ph.Packet.AddStreamWrapper()
    sw.LoadFromFile(filename)
    
    resp = formObj.CallServerMethod('UploadData',ph)
    
    status = resp.FirstRecord
    if status.Is_Err : 
      app.ShowMessage(status.Err_Message)
      return
    
    app.ShowMessage('%d data telah dipindahkan ke database' % status.sucsess)
    
    uipTrxSession.Edit()
    uipTrxSession.filename = ''
    
    return
