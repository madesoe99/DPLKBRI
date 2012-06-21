import sys
import com.ihsan.util.base88enc as b88enc
import random

gLastGenPassword = ""

def UserApp_AfterApplyRow(sender, data):
  
  global gLastGenPassword
  
  uideflist = sender.uideflist
  config = uideflist.config
  secCtx = config.SecurityContext
  
  data.last_update = config.Now()
  data.mod_user_id = secCtx.UserID
  data.login_count = 0
  data.islocked = "F"
  data.isgenpassword = "T"
  if data.home_directory == None or data.home_directory == "":
    data.home_directory = "$(USERHOME)"
  
  b88 = b88enc.base88()
  pwd = genPassword()
  data.encpassword = b88.convertFromString(pwd)
  gLastGenPassword = pwd
#--

def UserGroupApp_AfterNewRow(sender, data):
  usergroupapp = sender.ActiveInstance
  userapp = sender.UIDefList.UserApp.ActiveInstance
  usergroupapp.group_id = sender.ActiveRecord.GetFieldByName('LUserGroup.group_id')
  usergroupapp.user_id = userapp.user_id
#--

def EndProcessServerData(uideflist, datapacket):
  
  global gLastGenPassword
  
  uideflist.PostReturnMessage = "User created. Password is %s" % gLastGenPassword
  return 3 

def genPassword():
  s = ""
  for i in range(4):
    s = s + chr(random.randint(ord('a'), ord('z')))
  s = s + str(random.randint(11, 99))
  return s
#--
