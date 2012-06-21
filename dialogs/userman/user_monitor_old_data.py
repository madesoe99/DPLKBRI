import ConfigParser, os, string

def FormGeneralSetData(uideflist, uiname, pobjconst):
  config = uideflist.config
  dataset = uideflist.userlist.Dataset
  userobj = config.CreatePObjImplProxy('UserApp')
  sessionpath = config.SecurityContext.SessionDirectory
  
  sessionlist = os.listdir(sessionpath)

  for session in sessionlist:
    session_part = session.split('_')
    user_id = session_part[0]
    if user_id == 'root':
      Record = dataset.AddRecord()
      Record.session_id = session
      Record.user_id = user_id
      Record.UserName = user_id
      Record.branch_code = user_id
      Record.BranchName = user_id
    else:
      try:
        userobj.Key = user_id
        branch = userobj.LBranchLocation
        Record = dataset.AddRecord()
        Record.session_id = session
        Record.user_id = user_id
        Record.UserName = userobj.UserName
        Record.branch_code = branch.branch_code
        Record.BranchName = branch.BranchName
      except:
        os.remove(sessionpath + session)
        continue
      
  # stop further processing
  return 0
