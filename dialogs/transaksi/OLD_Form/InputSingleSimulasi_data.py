import string, time, sys
sys.path.append('c:/dafapp/dplk07/script_modules')

import moduleapi

def FormGeneralSetData(uideflist, uiname, objdata):
  config = uideflist.Config
  uipUserInfo = uideflist.uipUserInfo
  uipInput = uideflist.uipInput

  userID = config.SecurityContext.UserID
  #groupID = config.SecurityContext.GetUserInfo()[2]
  #tglPakai = time.localtime()[:3]
  tglPakai = config.ModLibUtils.DecodeDate(config.ModLibUtils.Now())

  lsGroup = moduleapi.GetUserGroupList(config, userID)

  recUserInfo = uipUserInfo.Dataset.AddRecord()
  recInput = uipInput.Dataset.AddRecord()
  
  #inisialisasi, status awal untuk user ADMINISTRATOR
  recUserInfo.isTeller = 0
  recUserInfo.isBackOffice = 0
  recUserInfo.isBackOfficeCabang = 0
  recUserInfo.UserIDOwner = ''
  recUserInfo.BranchCode = ''

  config.SendDebugMsg('lsGroup: '+ str(lsGroup))
  #cek user apakah termasuk group teller, BOD atau admin
  if string.upper(userID) == 'ROOT' or \
    'ADMIN' in lsGroup:
    config.SendDebugMsg('is1')
    #string.upper(str(groupID)) == 'ADMIN':
    #user root or admin: nothing to do, value like inisialization before
    pass
  elif moduleapi.IsUserTeller(config, config.SecurityContext.userID):
    #user 'teller'
    config.SendDebugMsg('is2')
    recUserInfo.isTeller = 1
    recUserInfo.UserIDOwner = userID
  elif 'BO' in lsGroup:
  #elif string.upper(str(groupID)) == 'BO':
    #user 'Backoffice Cabang'
    config.SendDebugMsg('is3')
    recUserInfo.isBackOfficeCabang = 1
    recUserInfo.BranchCode = config.SecurityContext.GetUserInfo()[4]
  elif 'BOD' in lsGroup:
  #else:
    #bukan ROOT, BO atau TELLER, artinya BOD user
    
    # Sementara di tutup
    #config.SendDebugMsg('is4')
    #recUserInfo.isBackOffice = 1
    #recUserInfo.UserIDOwner = userID

    #find another SuperUser (NoLimitLocation = 'T') except me & add to uipSuperUser
    #for constructing Transaction Batch OQL restriction
    #SuperUsers = moduleapi.FindSuperUserExceptMe(config, userID)
    #uipSU = uideflist.uipSuperUser
    #for user in SuperUsers:
      #recSU = uipSU.Dataset.AddRecord()
      #recSU.UserID = user
     pass
    # By Ade


  return 0
