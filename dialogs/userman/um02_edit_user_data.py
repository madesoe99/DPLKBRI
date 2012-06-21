def UserApp_AfterApplyRow(sender, data):
  uideflist = sender.uideflist
  config = uideflist.config
  data.mod_user_id = config.SecurityContext.UserID
  data.last_update = config.Now()
  if data.home_directory == None or data.home_directory == "":
    data.home_directory = "$(USERHOME)"
#--
