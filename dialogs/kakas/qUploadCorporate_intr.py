class qUploadCorporate:
  def __init__(self, formObj, parentForm):
    pass
  #--
  
  def Show(self):
    self.ResetFilter()
    self.DisplayList()
    self.FormContainer.Show()
  #--
  
  def ResetFilter(self):
    form = self.FormObject
    app = form.ClientApplication
    uipNoData = form.GetUIPartByName('uipNoData')
    
    uipNoData.SetFieldValue('upload_type', 'ALL')
  
  def DisplayList(self):
    form = self.FormObject
    app = form.ClientApplication
    uipNoData = form.GetUIPartByName('uipNoData')
    qList = self.qList
    
    qList.SetParameter('all_upload_type', uipNoData.upload_type)
    qList.SetParameter('upload_type', uipNoData.upload_type)
  
    qList.DisplayData()
  #--
    
  def bFilterOnClick(self, sender):
    # procedure(sender: TrtfButton)
    self.DisplayList()
    pass
  #--  

  def bResetOnClick(self, sender):
    # procedure(sender: TrtfButton)
    self.ResetFilter()
    self.DisplayList()
    pass