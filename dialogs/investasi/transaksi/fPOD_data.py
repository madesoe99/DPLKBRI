def OnSetDataEx_POD (uideflist, parameter) :
  config = uideflist.config
  rec = uideflist.uipNoData.AddRecord()
  rec.TglPOD = config.Now()
  raise 'as'
