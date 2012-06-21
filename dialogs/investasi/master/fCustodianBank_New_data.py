def FormGeneralSetData(uideflist, auiname, apobjconst):
  config = uideflist.Config
  uipCustodianBank = uideflist.uipCustodianBank

  rec = uipCustodianBank.Dataset.AddRecord()
  #rec.self_investment = 'F'
  rec.user_id = config.SecurityContext.userid
  rec.last_update = config.Now()

  return 0

