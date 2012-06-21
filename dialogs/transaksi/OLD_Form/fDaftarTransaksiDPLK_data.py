import string

def FormGeneralSetData(uideflist, uiname, objdata):
  config = uideflist.config
  uipUserInfo = uideflist.uipUserInfo
  uipFilter = uideflist.uipFilter
  
  oUser = config.CreatePObjImplProxy('UserApp')
  oUser.Key = config.SecurityContext.UserID

  userID = oUser.user_id
  groupID = config.SecurityContext.GetUserInfo()[2]
  
  recUserInfo = uipUserInfo.Dataset.AddRecord()
  recFilter = uipFilter.Dataset.AddRecord()

  #inisialisasi, status awal untuk user 'root'
  recUserInfo.isBackOffice = 0
  recUserInfo.BranchCode = ''

  #cek user apakah termasuk group teller, BO, BOD, atau Admin
  if string.upper(userID) == 'ROOT' or \
    string.upper(str(groupID)) == 'ADMIN' or oUser.NoLimitLocation == 'T':
    #user root, admin, BOD: nothing to do, value like inisialization before
    pass
  else:
    #bukan root, admin, BOD artinya BO user
    recUserInfo.isBackOffice = 1
    recUserInfo.BranchCode = config.SecurityContext.GetUserInfo()[4]
    recFilter.SetFieldByName('LBranch.branch_code',recUserInfo.BranchCode)
    recFilter.SetFieldByName('LBranch.BranchName', \
      config.SecurityContext.GetUserInfo()[5])
    
  #set filter tanggal
  recFilter.AwalTanggal = recFilter.AkhirTanggal = config.ModDateTime.Now()
  
  return 0
