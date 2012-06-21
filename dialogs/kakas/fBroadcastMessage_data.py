import os

def FormGeneralSetData(uideflist, uiname, objdata):
  config = uideflist.config
  uipNoData = uideflist.uipNoData
  uipUserOnline = uideflist.uipUserOnline

  recNoData = uipNoData.Dataset.AddRecord()
  recNoData.isBroadcast = 0

  #ambil session dan user pemilik session tersebut
  sessionDir = config.SecurityContext.SessionDirectory
  oUser = config.CreatePObjImplProxy('UserApp')
  
  if os.path.exists(sessionDir):
    #ambil semua file yang ada di direktori session
    tSessionFile = os.listdir(sessionDir)
    
    for sessionFile in tSessionFile:
      user_id = sessionFile.split('_',1)[0]
      recUserOnline = uipUserOnline.Dataset.AddRecord()
      recUserOnline.SessionID = sessionFile

      if user_id == 'root':
        recUserOnline.LoginID = recUserOnline.NamaUser = \
          recUserOnline.BranchCode = recUserOnline.BranchName = user_id
      else:
        try:
          oUser.Key = user_id
          oBranch = oUser.LBranchLocation

          recUserOnline.LoginID = user_id
          recUserOnline.NamaUser = oUser.UserName
          recUserOnline.BranchCode = oBranch.branch_code
          recUserOnline.BranchName = oBranch.BranchName
        except:
          #os.remove(sessionDir + sessionFile)
          continue

  return 0

