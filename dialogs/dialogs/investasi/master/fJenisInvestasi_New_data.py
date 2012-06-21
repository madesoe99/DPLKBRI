def FormGeneralSetData(uideflist, auiname, apobjconst):
  config = uideflist.Config
  uipJenisInvestasi = uideflist.uipJenisInvestasi

  rec = uipJenisInvestasi.Dataset.AddRecord()
  rec.user_id = config.SecurityContext.userid
  rec.last_update = config.Now()

  return 0

