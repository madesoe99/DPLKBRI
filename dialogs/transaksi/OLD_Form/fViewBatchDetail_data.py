import string, sys
sys.path.append('c:/dafapp/dplk07/script_modules')

import moduleapi


def FormEndSetData(uideflist, uiname, objdata):
  config = uideflist.config
  uipUserInfo = uideflist.uipUserInfo
  userID = config.SecurityContext.UserID
  groupID = config.SecurityContext.GetUserInfo()[2]
  
  recUserInfo = uipUserInfo.Dataset.AddRecord()

  #inisialisasi, status awal untuk user 'ADMINISTRATOR
  recUserInfo.isTeller = 0
  recUserInfo.isBackOffice = 0
  recUserInfo.BranchCode = ''
  recUserInfo.UserIDOwner = ''

  #cek user apakah termasuk group teller, backoffice atau admin
  if string.upper(userID) == 'ROOT' or \
    string.upper(str(groupID)) == 'ADMIN':
    #user 'root' or 'admin': nothing to do, value like inisialization before
    pass
  elif moduleapi.IsUserTeller(config, userID):
    #user 'teller'
    recUserInfo.isTeller = 1
    recUserInfo.UserIDOwner = userID
    recUserInfo.BranchCode = config.SecurityContext.GetUserInfo()[4]
  else:
    #bukan 'root' dan 'teller', artinya 'backoffice' user
    recUserInfo.isBackOffice = 1
    recUserInfo.BranchCode = config.SecurityContext.GetUserInfo()[4]

  return 0
