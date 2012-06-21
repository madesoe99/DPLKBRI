class frmUserMonitor:
  def __init__(self, formObj, parentForm):
    pass
    
  def bKickClick(self, sender):
    formObj = self.FormObject
    clientApp = formObj.ClientApplication
    
    session_id = self.qLogins.GetFieldValue("userlogin.login_id")
    if session_id == None:
      clientApp.ShowMessage("No session is selected")
      return
    #--
      
    res = formObj.CallServerMethod("removeSession", clientApp.CreateValues(["login_id", session_id]))
    fr = res.FirstRecord
    if fr.isErr == 1:
      clientApp.ShowMessage("Remove session error:\r\n%s" % fr.errMsg)
    else:
      clientApp.ShowMessage("Session was kicked successfully")
      self.qLogins.DeleteRow()
    #--
  #--
  
  def bKickAllClick(self, sender):
    formObj = self.FormObject
    clientApp = formObj.ClientApplication
    
    res = formObj.CallServerMethod("removeAllSessions", clientApp.CreatePacket())
    fr = res.FirstRecord
    if fr.isErr == 1:
      clientApp.ShowMessage("Server error:\r\n%s" % fr.errMsg)
    else:
      clientApp.ShowMessage("Successful")
      self.qLogins.Refresh()
    #--
  #--
  
#_-
      
    
    