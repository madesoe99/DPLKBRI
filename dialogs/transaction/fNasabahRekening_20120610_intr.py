class fNasabahRekening:
  def __init__(self, formObj, parentForm):
    if parentForm != None:
      self.parentForm = parentForm
    else:
      self.parentForm = None

  def Show(self, mode):
    app = self.FormObject.ClientApplication
    
    #self.FormShow(self.FormObject, mode)
    #param = form.GetDataPacket()    
    #form.CallServerMethod('namascript',param)
    
    self.FormContainer.Show()