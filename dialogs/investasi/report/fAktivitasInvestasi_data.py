def FormSetDataEx(uideflist, parameter):
  config = uideflist.Config
  #uideflist.SetData('uipInvestasi', parameter.FirstRecord.key)
  uipInv = uideflist.uipInvestasi.Dataset.AddRecord()
  uipInv.kode_jns_investasi = parameter.FirstRecord.kode_jns_investasi

def uipInvestasiSetData(uipInvestasi):
  config = uipInvestasi.UIDefList.Config
  rec = uipInvestasi.Dataset.GetRecord(0)

  #oRincianPaketInvestasi = config.CreatePObjImplProxy('RincianPaketInvestasi')
  #oRincianPaketInvestasi.SetKey('kode_paket_investasi',rec.GetFieldByName('LRincianPaketInvestasi.kode_paket_investasi'))
  #oRincianPaketInvestasi.SetKey('kode_jns_investasi',rec.GetFieldByName('LRincianPaketInvestasi.kode_jns_investasi'))

  #oPaketInvestasi = oRincianPaketInvestasi.LPaketInvestasi
  #rec.SetFieldByName('LPaketInvestasi.kode_paket_investasi',oPaketInvestasi.kode_paket_investasi)
  #rec.SetFieldByName('LPaketInvestasi.nama_paket_investasi',oPaketInvestasi.nama_paket_investasi)

