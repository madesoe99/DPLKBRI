def FormBeginProcessData(uideflist, datapacket):
  config = uideflist.Config
  rec = datapacket.uipProduk.GetRecord(0)

  #update field user_id dan last_update
  rec.user_id = config.SecurityContext.UserID
  rec.last_update = config.ModLibUtils.Now()

  return 1

