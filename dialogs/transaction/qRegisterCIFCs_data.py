import string

def FormGeneralSetData(uideflist, auiname, apobjconst):
  config = uideflist.Config

  oUserApp = config.CreatePObjImplProxy('UserApp')
  oUserApp.Key = config.SecurityContext.userid

  oBranch = config.CreatePObjImplProxy('BranchLocation')
  oBranch.Key = config.SecurityContext.GetUserInfo()[4]

  rec = uideflist.uipNoData.Dataset.AddRecord()

  #cek apakah user termasuk ROOT atau grup ADMINISTRATOR, lalu pasang flag
  rec.NoLimitLocation = oUserApp.NoLimitLocation
  groupID = config.SecurityContext.GetUserInfo()[2]
  if string.upper(oUserApp.user_id) == 'ROOT' or \
    string.upper(str(groupID)) == 'ADMIN' or rec.NoLimitLocation == 'T':
    rec.isAdmin = 1
  else:
    rec.isAdmin = 0
    rec.SetFieldByName('LBranchLocation.branch_code',oBranch.branch_code)
    rec.SetFieldByName('LBranchLocation.BranchName',oBranch.BranchName)

  return 0

