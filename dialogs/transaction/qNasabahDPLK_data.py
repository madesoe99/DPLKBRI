def FormGeneralSetData(uideflist, auiname, apobjconst):
  config = uideflist.Config

  oUserApp = config.CreatePObjImplProxy('UserApp')
  oUserApp.Key = config.SecurityContext.userid
  
  oBranch = config.CreatePObjImplProxy('BranchLocation')
  oBranch.Key = config.SecurityContext.GetUserInfo()[4]

  rec = uideflist.uipNoData.Dataset.AddRecord()

  return 0

