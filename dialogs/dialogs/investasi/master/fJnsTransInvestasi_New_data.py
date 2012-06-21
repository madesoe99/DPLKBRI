def FormGeneralSetData(uideflist, auiname, apobjconst):
  config = uideflist.Config
  uipJnsTransInvestasi = uideflist.uipJnsTransInvestasi

  rec = uipJnsTransInvestasi.Dataset.AddRecord()
  rec.user_id = config.SecurityContext.userid
  rec.last_update = config.Now()

  return 0

