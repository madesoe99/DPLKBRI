def FormGeneralSetData(uideflist, auiname, apobjconst):
  config = uideflist.Config
  uipSubJnsTransLRInvestasi = uideflist.uipSubJnsTransLRInvestasi

  rec = uipSubJnsTransLRInvestasi.Dataset.AddRecord()
  rec.user_id = config.SecurityContext.userid
  rec.last_update = config.Now()

  return 0

