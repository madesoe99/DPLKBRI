def FormGeneralSetDataEx(uideflist, parameter):
  config = uideflist.config
  recFilter = uideflist.uipFilter.Dataset.AddRecord()

  #set filter tanggal mulai dan hingga
  recFilter.AwalTanggal = recFilter.AkhirTanggal = config.ModLibUtils.Now()

  return 0
