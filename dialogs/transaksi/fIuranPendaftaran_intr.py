class fIuranPendaftaran:
  def __init__(self, formObj, parentForm):
    self.app = formObj.ClientApplication
  #--
  
  def bSimpanClick(self, button):

    form = self.FormObject    
    form.CommitBuffer()
    phForm = form.GetDataPacket()
    phReturn = form.CallServerMethod("SimpanTransaksi", phForm)

    status = phReturn.FirstRecord
    if status.IsErr :
      self.app.ShowMessage(status.ErrMessage)
      return
    button.ExitAction = 2
    self.FormObject.Close(2)
  #--
  
  