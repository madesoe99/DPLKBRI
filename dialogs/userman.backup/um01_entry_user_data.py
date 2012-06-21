def UserApp_AfterApplyRow(sender, data):
  data.RegisterData()

def UserGroupApp_AfterNewRow(sender, data):
  usergroupapp = sender.ActiveInstance
  userapp = sender.UIDefList.UserApp.ActiveInstance 
  usergroupapp.Create(userapp, sender.GetLink('LUserGroup'))
