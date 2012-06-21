def UserGroupApp_AfterNewRow(sender, data):
  data.LUser = sender.UIDefList.UserApp.ActiveInstance

def UserGroupApp_AfterApplyRow(sender, data):
  userapp = sender.UIDefList.UserApp.ActiveInstance
  data.LUserGroup.AddUser(userapp.user_id)
  	
def Form_BeforeDeleteRow (data):
  userapp = data.LUser
  #data.LUserGroup.DeleteUser(userapp.user_id)

