class frmRenameFile:
  def __init__(self, formObj, parentForm):
    pass
    
  def getRenameFile(self, path, oldName):
    formObj = self.FormObject
    
    self.uipInput.ClearData()
    self.uipInput.Append()
    self.uipInput.path = path
    self.uipInput.original_name = oldName
    self.uipInput.new_name = oldName
    
    res = self.FormContainer.Show()
    if res == 1:
      return self.uipInput.new_name
    else:
      return None
    #--
  #--
#--