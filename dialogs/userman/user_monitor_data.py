import sys
import com.ihsan.util.dbutil as dbutil

def removeSession(config, params, returns):
  mlu = config.ModLibUtils
  isErr = 0
  errMsg = ""
  config.BeginTransaction()
  try:
    fr = params.FirstRecord
    secCtx = config.SecurityContext
    oSession = config.CreatePObjImplProxy("UserLogin")
    oSession.Key = fr.login_id
    if oSession.session_id == secCtx.SessionID:
      raise Exception, "Cannot kill your own session"                                                                                              
    dbutil.runSQL(config, "DELETE FROM userlogin WHERE login_id = %d AND session_id <> %s" % (fr.login_id, mlu.QuotedStr(secCtx.SessionID))) 
    config.Commit()  
  except:
    isErr = 1
    errMsg = str(sys.exc_info()[1])    
    config.Rollback()
  #--
  
  returns.CreateValues(['isErr', isErr], ['errMsg', errMsg])

def removeAllSessions(config, params, returns):
  mlu = config.ModLibUtils
  isErr = 0
  errMsg = ""
  config.BeginTransaction()
  try:
    secCtx = config.SecurityContext                                                                                              
    dbutil.runSQL(config, "DELETE FROM userlogin WHERE session_id <> %s" % (mlu.QuotedStr(secCtx.SessionID))) 
    config.Commit()  
  except:
    isErr = 1
    errMsg = str(sys.exc_info()[1])    
    config.Rollback()
  #--
  
  returns.CreateValues(['isErr', isErr], ['errMsg', errMsg])
