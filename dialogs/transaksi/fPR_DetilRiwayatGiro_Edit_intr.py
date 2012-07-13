class fPR_DetilRiwayatGiro_Edit:
  def __init__(self, formObj, parentForm):
    self.app = formObj.ClientApplication
  
  def Show(self) :
    self.FormContainer.Show()
    if self.uipart1.proses == 1 :
      return self.uipart1.nominal

  def is_validOnClick(self, checkbox):
    if self.panel1_is_valid.Checked:
      self.uipart1.keterangan= ''  
    else:
      self.uipart1.keterangan = self.uipart1.ket
  #--
  def bSimpanOnClick(self, sender):
    self.FormObject.CommitBuffer()
    param = self.FormObject.GetDataPacket()
    resp = self.FormObject.CallServerMethod('Simpan',param)

    status = resp.FirstRecord
    if status.IsErr :
      self.app.ShowMessage(status.ErrMessage)
      return
    self.uipart1.Edit()
    self.uipart1.proses = 1
    sender.ExitAction = 2
    self.FormObject.Close(2)

