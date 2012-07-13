import time, string

def FormGeneralSetData(uideflist, auiname, apobjconst):
  config = uideflist.Config
  uipRegisterInvestasi = uideflist.uipRegisterInvestasi
  uipParameter = uideflist.uipParameter

  recP = uipParameter.Dataset.AddRecord()
  #set parameter nowDate
  tglPakai = time.localtime()[:3]
  recP.nowDate = '%s/%s/%d' % (string.zfill(str(tglPakai[1]),2), \
    string.zfill(str(tglPakai[2]),2),tglPakai[0])

  if auiname == 'new':
    rec = uipRegisterInvestasi.Dataset.AddRecord()
    uipRegisterInvestasi = uideflist.uipRegisterInvestasi
    rec.tgl_buka = config.Now()
    rec.nominal = 0.0
    rec.tanggal_register = config.Now()
    rec.mode = auiname

    rec.user_id = config.SecurityContext.userid
    rec.terminal_id = config.SecurityContext.GetSessionInfo()[1]
      
    retval = 0
  else:
    retval = 1

  return retval

#def uipRegisterInvestasiSetData(uipRegisterInvestasi):
#  config = uipRegisterInvestasi.UIDefList.Config
#  rec = uipRegisterInvestasi.Dataset.GetRecord(0)
#
#  oRincianPaketInvestasi = config.CreatePObjImplProxy('RincianPaketInvestasi')
#  oRincianPaketInvestasi.SetKey('kode_paket_investasi',rec.GetFieldByName('LRincianPaketInvestasi.kode_paket_investasi'))
#  oRincianPaketInvestasi.SetKey('kode_jns_investasi',rec.GetFieldByName('LRincianPaketInvestasi.kode_jns_investasi'))
#
#  oPaketInvestasi = oRincianPaketInvestasi.LPaketInvestasi
#  rec.SetFieldByName('LPaketInvestasi.kode_paket_investasi',oPaketInvestasi.kode_paket_investasi)
#  rec.SetFieldByName('LPaketInvestasi.nama_paket_investasi',oPaketInvestasi.nama_paket_investasi)

def uipRegisterInvestasiApplyRow(uipRegisterInvestasi, oRegisterInvestasi):
  config = uipRegisterInvestasi.UIDefList.Config

  if oRegisterInvestasi.no_bilyet in [None, '']:
    raise Exception, 'Kesalahan Register Investasi' + 'Nomor bilyet tidak terdefinisi.'

  if oRegisterInvestasi.nominal <= 0.0:
    raise Exception, 'Kesalahan Register Investasi' + 'Nilai nominal harus lebih besar dari nol.'

  oRegisterInvestasi.user_id = config.SecurityContext.userid
  oRegisterInvestasi.terminal_id = config.SecurityContext.GetSessionInfo()[1]

