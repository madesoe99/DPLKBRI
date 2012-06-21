import sys, time, string
sys.path.append('c:/dafapp/dplk/script_modules')
sys.path.append('c:/dafapp/dplk/scripts/investasi/transaksi')
import moduleapi, paketinvinfo

def FormGeneralSetData(uideflist, auiname, apobjconst):
  config = uideflist.Config
  uipRegisterSaham = uideflist.uipRegisterSaham
  uipParameter = uideflist.uipParameter

  recP = uipParameter.Dataset.AddRecord()
  #set parameter nowDate
  tglPakai = time.localtime()[:3]
  recP.nowDate = '%s/%s/%d' % (string.zfill(str(tglPakai[1]),2), \
    string.zfill(str(tglPakai[2]),2),tglPakai[0])

  if auiname == 'new':
    rec = uipRegisterSaham.Dataset.AddRecord()
    uipRegisterSaham = uideflist.uipRegisterSaham
    rec.tgl_buka = config.Now()
    rec.nominal = 0.0
    rec.tanggal_register = config.Now()
    rec.mode = auiname

    rec.biaya = 0.0
    rec.unit_penyertaan = 0.0
    rec.NAB_awal = 0.0

    rec.user_id = config.SecurityContext.userid
    rec.terminal_id = config.SecurityContext.GetSessionInfo()[1]
    
    KodeJnsInv= 'S'
    resSQLRPI = moduleapi.resSQLRPI(config, KodeJnsInv)
    if resSQLRPI.RecordCount == 1 :
      # rincian paket investasi langsung diisi
      rec.SetFieldByName('LRincianPaketInvestasi.kode_jns_investasi', KodeJnsInv)
      rec.SetFieldByName('LRincianPaketInvestasi.kode_paket_investasi', resSQLRPI.kode_paket_investasi)
      rec.maks_proporsi = resSQLRPI.maks_proporsi or 0.0
      rec.dpkPaket, rec.dpkInvExisting, rec.dpkTersedia, rec.nilaiMaksProporsi, rec.nominalGiro = paketinvinfo.getPaketInfo(config, resSQLRPI.kode_paket_investasi, KodeJnsInv)
#       rec.nominal = min(rec.dpkTersedia, rec.nilaiMaksProporsi, rec.nominalGiro)
      rec.nominal = min(rec.dpkTersedia, rec.nilaiMaksProporsi)

      #uipRincianRegisterDeposito = uideflist.uipRincianRegisterDeposito
      #rec = uipRincianRegisterDeposito.Dataset.AddRecord()
      #rec.SetFieldByName('LRincianPaketInvestasi.kode_jns_investasi', 'C')
      #rec.SetFieldByName('LRincianPaketInvestasi.kode_paket_investasi', resSQLRPI.kode_paket_investasi)
      #rec.SetFieldByName('LRincianPaketInvestasi.maks_proporsi', resSQLRPI.maks_proporsi or 0.0)
      #rec.dpkPaket, rec.dpkInvExisting, rec.dpkTersedia, rec.nilaiMaksProporsi, rec.nominalGiro = paketinvinfo.getPaketInfo(config, resSQLRPI.kode_paket_investasi, 'C')
      #rec.nominal = min(rec.dpkTersedia, rec.nilaiMaksProporsi, rec.nominalGiro)

    retval = 0
  else:
    retval = 1

  return retval

def uipRegisterSahamSetData(uipRegisterSaham):
  config = uipRegisterSaham.UIDefList.Config
  rec = uipRegisterSaham.Dataset.GetRecord(0)
#
  if rec.GetFieldByName('LRincianPaketInvestasi.kode_paket_investasi') not in (None, '') :
    oRincianPaketInvestasi = config.CreatePObjImplProxy('RincianPaketInvestasi')
    oRincianPaketInvestasi.SetKey('kode_paket_investasi',rec.GetFieldByName('LRincianPaketInvestasi.kode_paket_investasi'))
    oRincianPaketInvestasi.SetKey('kode_jns_investasi',rec.GetFieldByName('LRincianPaketInvestasi.kode_jns_investasi'))
    rec.maks_proporsi = oRincianPaketInvestasi.maks_proporsi
#
#  oPaketInvestasi = oRincianPaketInvestasi.LPaketInvestasi
#  rec.SetFieldByName('LPaketInvestasi.kode_paket_investasi',oPaketInvestasi.kode_paket_investasi)
#  rec.SetFieldByName('LPaketInvestasi.nama_paket_investasi',oPaketInvestasi.nama_paket_investasi)

def uipRegisterSahamApplyRow(uipRegisterSaham, oRegisterSaham):
  config = uipRegisterSaham.UIDefList.Config

  if oRegisterSaham.nama_Saham in [None, '']:
    raise 'Kesalahan Register Saham','Nama Saham tidak terdefinisi.'

  if oRegisterSaham.nominal < 0.000001:
    raise 'Kesalahan Register Saham','Nilai investasi harus lebih besar dari nol.'

  if oRegisterSaham.nominal > min(oRegisterSaham.dpkTersedia, oRegisterSaham.nilaiMaksProporsi):
  #if oRegisterSaham.nominal > min(oRegisterSaham.dpkTersedia, oRegisterSaham.nilaiMaksProporsi, oRegisterSaham.nominalGiro):
    raise 'Kesalahan Register Saham','\nDana paket investasi tidak tersedia.'

  if oRegisterSaham.NAB_awal <= 0.0:
    pass#raise 'Kesalahan Register Saham','Nilai harga beli harus lebih besar dari nol.'

  oRegisterSaham.NAB = oRegisterSaham.NAB_awal
  oRegisterSaham.user_id = config.SecurityContext.userid
  oRegisterSaham.terminal_id = config.SecurityContext.GetSessionInfo()[1]

