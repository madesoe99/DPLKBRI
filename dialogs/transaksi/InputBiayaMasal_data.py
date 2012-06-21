def FormGeneralSetData(uideflist, uiname, objdata):
  config = uideflist.config
  uipInput = uideflist.uipInput
  recInput = uipInput.Dataset.AddRecord()

  recInput.UserAdmin = config.SecurityContext.UserID
  recInput.TanggalHitung = config.ModLibUtils.Now()
  
  return 0
