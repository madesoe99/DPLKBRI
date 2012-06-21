def FormSetDataEx(uideflist, parameter):
  config = uideflist.Config
  key = parameter.FirstRecord.key
  if key[:12] == 'PObj:Rincian' :
    oRincian = config.AccessPObject(key)
    obj, field = key.split('#')

    oInv = config.CreatePObjImplProxy(obj[12:])
    oInv.key = oRincian.id_investasi
    key = oInv.PObjConst

  uideflist.SetData('uipInvestasi', key)

def uipInvestasiSetData(uipInvestasi):
  config = uipInvestasi.UIDefList.Config
  rec = uipInvestasi.Dataset.GetRecord(0)

  #oRincianPaketInvestasi = config.CreatePObjImplProxy('RincianPaketInvestasi')
  #oRincianPaketInvestasi.SetKey('kode_paket_investasi',rec.GetFieldByName('LRincianPaketInvestasi.kode_paket_investasi'))
  #oRincianPaketInvestasi.SetKey('kode_jns_investasi',rec.GetFieldByName('LRincianPaketInvestasi.kode_jns_investasi'))

  #oPaketInvestasi = oRincianPaketInvestasi.LPaketInvestasi
  #rec.SetFieldByName('LPaketInvestasi.kode_paket_investasi',oPaketInvestasi.kode_paket_investasi)
  #rec.SetFieldByName('LPaketInvestasi.nama_paket_investasi',oPaketInvestasi.nama_paket_investasi)

