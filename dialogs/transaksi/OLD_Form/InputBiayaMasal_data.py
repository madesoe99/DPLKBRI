def FormGeneralSetData(uideflist, uiname, objdata):
  config = uideflist.config
  uipInput = uideflist.uipInput
  recInput = uipInput.Dataset.AddRecord()

  recInput.UserAdmin = config.SecurityContext.UserID
  recInput.TanggalHitung = config.Now()
  
  return 0
