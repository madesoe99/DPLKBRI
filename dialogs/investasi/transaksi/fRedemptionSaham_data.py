import sys, time, string
sys.path.append('c:/dafapp/dplk/script_modules')
import moduleapi, TransactInv

mode = ''

def FormGeneralSetData(uideflist, auiname, apobjconst):
  global mode

  config = uideflist.Config
  uipRedemptionSaham = uideflist.uipRedemptionSaham
  uipSaham = uideflist.uipSaham

  rec_tpi = uipRedemptionSaham.Dataset.AddRecord()
  if auiname in ['uipSaham', 'new']:
    # new

    rec_tpi.tgl_transaksi = config.Now()
    rec_tpi.tgl_sistem = config.Now()
    rec_tpi.mode = auiname
    mode = auiname

    #rec_tpi.biaya_redempt = 0.0

    rec_tpi.user_id = config.SecurityContext.userid
    rec_tpi.terminal_id = config.SecurityContext.GetSessionInfo()[1]

  #set parameter nowDate
  recP = uideflist.uipParameter.Dataset.AddRecord()
  tglPakai = time.localtime()[:3]
  recP.nowDate = '%s/%s/%d' % (string.zfill(str(tglPakai[1]),2), \
    string.zfill(str(tglPakai[2]),2),tglPakai[0])

  if auiname == 'new':
    return 0

  return 1

def uipSahamSetData(uipSaham):
  global mode

  uideflist = uipSaham.UIDefList
  config = uideflist.Config

  rec_inv = uipSaham.Dataset.GetRecord(0)
  rec_tpi = uideflist.uipRedemptionSaham.Dataset.GetRecord(0)

  oSaham = config.CreatePObjImplProxy('Saham')
  oSaham.Key = rec_inv.id_investasi
  
  moduleapi.CheckTransactionValidity(config, oSaham, mode)


  rec_tpi.SetFieldByName('LSaham.id_investasi', oSaham.id_investasi)
  rec_tpi.SetFieldByName('LSaham.nama_Saham', oSaham.nama_Saham)
  rec_tpi.SetFieldByName('LSaham.tgl_buka', oSaham.tgl_buka)

  #rec_tpi.akum_nominal = oSaham.akum_nominal

  rec_tpi.SetFieldByName('LPihakKetiga.kode_pihak_ketiga',oSaham.LPihakKetiga.kode_pihak_ketiga)
  rec_tpi.SetFieldByName('LPihakKetiga.nama_pihak_ketiga',oSaham.LPihakKetiga.nama_pihak_ketiga)

  rec_tpi.SetFieldByName('LPaketInvestasi.kode_paket_investasi',oSaham.LRincianPaketInvestasi.LPaketInvestasi.kode_paket_investasi)
  rec_tpi.SetFieldByName('LPaketInvestasi.nama_paket_investasi',oSaham.LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi)
  '''if rec_tpi.biaya_redempt != 0.0 :
    oReksaSwitch = config.CreatePObjImplProxy('Saham')
    oReksaSwitch.Key = int(rec_tpi.no_rekening)
    rec_tpi.SetFieldByName('LSahamSwitch.id_investasi',oReksaSwitch.id_investasi)
    rec_tpi.SetFieldByName('LSahamSwitch.nama_Saham',oReksaSwitch.nama_Saham)
  else :'''

  rec_tpi.SetFieldByName('LMasterGiro.no_giro',rec_tpi.no_rekening)

def uipRedemptionSahamApplyRow(uipRedemptionSaham, oRedemptionSaham):
  config = uipRedemptionSaham.UIDefList.Config

  oSaham = oRedemptionSaham.LSaham

  if oRedemptionSaham.nilai_redempt <= 0 and oRedemptionSaham.unit_penyertaan == 0.0 :
    pass#raise 'Kesalahan Redemption Saham','Nilai redemption harus lebih dari nol.'

  #if (oRedemptionSaham.nilai_redempt - oSaham.unit_penyertaan * oSaham.NAB) > moduleapi.zero_approx:
  if (oRedemptionSaham.nilai_redempt - oSaham.akum_nominal) > moduleapi.zero_approx:
    pass#raise 'Kesalahan Redemption Saham','\nNilai redemption tidak boleh lebih dari unit penyertaan dikali NAB sekarang.'

  #totPiutInv = oSaham.NAB_awal * oRedemptionSaham.unit_penyertaan
  totPiutInv = oRedemptionSaham.nilai_redempt
  
  oRedemptionSaham.mutasi_debet = 0.0
  oRedemptionSaham.mutasi_kredit = totPiutInv

  # nilai kode_jns_investasi diisi lagi jika belum ada
  oRedemptionSaham.kode_jns_investasi = oRedemptionSaham.LSaham.kode_jns_investasi
  oRedemptionSaham.kode_jenis_trinvestasi = 'RS'
  oRedemptionSaham.user_id = config.SecurityContext.userid
  oRedemptionSaham.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oRedemptionSaham.isCommitted = 'F'

  if oRedemptionSaham.no_rekening == '' :
    raise 'PERINGATAN','Tujuan redempt harus diisi'


def FormEndProcessData(uideflist, datapacket):
  config = uideflist.Config
  uidef = uideflist.GetPClassUIByName('uipRedemptionSaham')
  rec = uidef.ActiveRecord

  id_investasi = rec.GetFieldByName('LSaham.id_investasi')

  if rec.mode == 'new':
    #moduleapi.IsInvestasiAvail(config, id_investasi)
    moduleapi.CheckTransaksiInvestasiExclusive(config, id_investasi)

