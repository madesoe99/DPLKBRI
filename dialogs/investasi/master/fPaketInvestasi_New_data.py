def FormGeneralSetData(uideflist, auiname, apobjconst):
  config = uideflist.Config
  uipPaketInvestasi = uideflist.uipPaketInvestasi

  rec = uipPaketInvestasi.Dataset.AddRecord()
  rec.user_id = config.SecurityContext.userid
  rec.last_update = config.Now()

  return 0

