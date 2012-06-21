class frmRepHistoriGiro:
  def __init__(self, formObject, parentForm):
    pass

  def bProsesClick(self, button):
    f = self.FormObject
    f.CommitBuffer()
    p = f.GetDataPacket()
    repres = f.CallServerMethod("createReport", p)

    libDLClass = f.ClientApplication.GetClientClass("libDownload", "libDownload")
    libDL = libDLClass()
    libDL.previewStream(f.ClientApplication, repres.Packet.GetStreamWrapper(0))
    
    button.ExitAction = 1
    pass
