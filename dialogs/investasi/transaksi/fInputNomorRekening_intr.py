class fInputNomorRekening:
  def __init__(self, formObj, parentForm):
    self.app = formObj.ClientApplication

  def ShowForm(self):
    self.FormContainer.Show()
    #self.FormObject.CommitBuffer()
    #return self.uipNoData.GetFieldValue('LMasterGiro.no_giro')

  #def btnOKClick(self, sender):
  #  sender.ExitAction = 1

