
def Form_OnSetDataEx(uideflist, params):
  config = uideflist.config
  uipFilter = uideflist.uipFilter

  recFilter = uipFilter.Dataset.AddRecord()
  recFilter.cbAllCabang = 1
  recFilter.cbAllTransaksi = 0
  recFilter.cbStatusOtorisasi = 'A'
  recFilter.eAwalTanggal = config.ModLibUtils.Now()
  recFilter.eHinggaTanggal = config.ModLibUtils.Now()
    
  return 0
#--
