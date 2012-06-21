class fHistoriNasabahRekening:
  def __init__(self, formObj, parentForm):
    if parentForm != None:
      self.parentForm = parentForm
    else:
      self.parentForm = None

  def Show(self):
    app = self.FormObject.ClientApplication
    
    #self.FormShow(self.FormObject, mode)
    self.FormContainer.Show()