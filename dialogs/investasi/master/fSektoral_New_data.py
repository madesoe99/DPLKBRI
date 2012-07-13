def FormGeneralSetData(uideflist, auiname, apobjconst):
  config = uideflist.Config
  uipSektoral = uideflist.uipSektoral

  rec = uipSektoral.Dataset.AddRecord()
  rec.is_level_detil = 'F'
  rec.user_id = config.SecurityContext.userid
  rec.last_update = config.Now()

  return 0

