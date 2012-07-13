def FormGeneralSetData(uideflist, auiname, apobjconst):
  config = uideflist.Config
  uipPihakKetiga = uideflist.uipPihakKetiga

  rec = uipPihakKetiga.Dataset.AddRecord()
  rec.self_investment = 'F'
  rec.is_level_detil = 'T'
  rec.user_id = config.SecurityContext.userid
  rec.last_update = config.Now()

  return 0

