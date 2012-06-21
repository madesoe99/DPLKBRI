def UserGroupApp_AfterNewRow(sender, data):
  data.user_id = sender.UIDefList.UserApp.ActiveInstance.user_id
  data.group_id = sender.ActiveRecord.GetFieldByName("LUserGroup.group_id")
#--
