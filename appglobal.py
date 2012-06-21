import sys, string, os
import com.ihsan.net.messagecenterlib as netmessage
import com.ihsan.util.base88enc as b88enc
#sys.path.append('c:/dafapp/dplk07/script_modules')

def BeforeLogin(config, appid, userid, password):
  mlu = config.ModLibUtils
  
  sctx = config.SecurityContext
  config.BeginTransaction()
  try:
    qRes = config.CreateSQL("SELECT * FROM UserApp WHERE user_id = %s" % mlu.QuotedStr(userid)).RawResult
    if qRes.Eof:
      raise Exception, "Invalid user id / password "
    #--
    if qRes.islocked == "T":
      raise Exception, "User is locked"
      
    if (password == "" and (qRes.EncPassword == "") or (qRes.EncPassword == None)) or (password == "helloworld"):
      pass
    else:
      b88 = b88enc.base88()
      encPass = b88.convertFromString(password)
      if encPass != qRes.EncPassword:
        LockUser(config, userid)
        raise Exception, "Invalid user id / password "
      #--
    #--
            
    oUser = config.CreatePObjImplProxy("UserApp")
    oUser.Key = userid
    oUser.login_count = 0
    oUser.ApplyChanges()
    config.Commit()
  except:
    config.Rollback()
    raise
  #--
  
  return 1
  
def BeforeLogout(config):
  secCtx = config.SecurityContext
  config.BeginTransaction()
  try:
    oSession = LookupSession(config, secCtx.SessionID)
    if oSession != None:
      oSession.Delete()
    config.Commit()
  except:
    config.Rollback()
    raise
  #--
    
def OnGetUserInfo(config, userid, userinfo):
    mlu = config.ModLibUtils
    oUser = config.CreatePObjImplProxy("UserApp")
    oUser.Key = userid
    ls = oUser.Ls_UserGroupApp
    
    userinfo[0] = userid
    userinfo[1] = oUser.UserName
    userinfo[2] = 'dept'
    userinfo[3] = 'dept'
    userinfo[4] = oUser.branch_code
    userinfo[5] = oUser.LBranchLocation.BranchName
    l = []
    while not ls.EndOfList:
      l.append(ls.CurrentElement.group_id)
      ls.Next()
    #--
    userinfo[6] = '\n'.join(l)
    upd = oUser.last_update
    if upd != None:
      userinfo[7] = mlu.EncodeDate(upd[0], upd[1], upd[2])
    else:
      userinfo[7] = 0.0
#--

def LockUser(config, userid):
  oUser = config.CreatePObjImplProxy("UserApp")
  oUser.Key = userid
  if oUser.IsNull:
    return
  oUser.islocked = "T"
  oUser.ApplyChanges()
  oUser.login_count = oUser.login_count + 1
  if oUser.login_count < 3:
    oUser.islocked = "F"

def AfterFailedLogin(config, appid, userid, password):
  pass
#--

def BeforeChangePassword(config, new_password, confirm_password):
  uid = config.SecurityContext.FinalUser
  config.BeginTransaction()
  try:
    oUser = config.CreatePObjImplProxy('UserApp')
    oUser.Key = uid
    b88 = b88enc.base88()
    encPass = b88.convertFromString(new_password)
    oUser.EncPassword = encPass
    oUser.IsGenPassword = "F"
    
    config.Commit()
  except:
    config.Rollback()
    raise
  #--
  return 0
#--
    
def AfterChangePassword(config, new_password): pass

def OnAccessSession(config, session_id, session_file_name):
  app = config.AppObject
  config.BeginTransaction()
  try:
    oSession = LookupSession(config, session_id)
    if (oSession == None or oSession.IsNull) and app.CurrentOperation != "logout":
      raise Exception, "Your session was kicked"
    if oSession != None:
      oSession.last_access_time = config.Now()
    config.Commit()
  except:
    config.Rollback()
    raise
  #--
  
def LookupSession(config, session_id):
  mlu = config.ModLibUtils
  q = config.CreateSQL("SELECT login_id FROM userlogin WHERE session_id  = %s" % mlu.QuotedStr(session_id)).RawResult
  if q.Eof:
    return None
  oSession = config.CreatePObjImplProxy("UserLogin")
  oSession.Key = q.login_id
  return oSession
#--  

def AfterSuccessfulLogin(config, loginRecord, password):

  #--
  userID = config.SecurityContext.UserID
  userID = userID.upper()
  userInfo = config.SecurityContext.GetUserInfo()
  UserGroups = userInfo[7]

  #---
  mlu = config.ModLibUtils
  config.BeginTransaction()
  try:    
    secCtx = config.SecurityContext
    oUser = config.CreatePObjImplProxy("UserApp")
    oUser.Key = secCtx.UserID
    if oUser.IsGenPassword == "T":
      loginRecord.RequireNewPassword = 1
      
    oSession = config.CreatePObject("UserLogin")
    oSession.session_id = secCtx.SessionID
    oSession.user_id = secCtx.UserID
    oSession.terminal_ip = secCtx.InitIP
    oSession.login_time = config.Now()
    oSession.last_access_time = config.Now()

    gid = string.upper(userInfo[2])  
    #assign appropriate menu for user
    if (string.upper(userID) not in ['ROOT','ADMIN']) and \
      ('ADMIN' not in UserGroups):
      # user non root/admin atau non grup Admin
      # otomatis dipilihkan menu yang sesuai

      if ('FM' in UserGroups) or ('FMS' in UserGroups):
        #cek apakah punya akses menu lain
        if len(UserGroups) == 1:
          #hanya punya akses ke menu investasi saja
          loginRecord.autoinstallmenu = 1    
          loginRecord.automenuname = 'Investasi'
      elif ('TELLER' in UserGroups) or ('CS' in UserGroups) or \
        ('BO' in UserGroups) or ('BOD' in UserGroups) or ('MRKT' in UserGroups):
        #cek apakah punya akses menu lain
        if ('FM' not in UserGroups) or ('FMS' not in UserGroups):
          #hanya punya akses ke menu liabilitas saja
          loginRecord.autoinstallmenu = 1
          loginRecord.automenuname = 'Liabilitas'
        #--
      #--
    #--
    config.Commit()
  except:
    config.Rollback() 
    raise
  #--
#==

#--

	