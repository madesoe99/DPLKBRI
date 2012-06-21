import sys, time, string
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi, TransactInv

mode = ''

def FormGeneralSetData(uideflist, auiname, apobjconst):
  global mode

  config = uideflist.Config
  uipRedemptionReksadana = uideflist.uipRedemptionReksadana
  uipReksadana = uideflist.uipReksadana

  rec_tpi = uipRedemptionReksadana.Dataset.AddRecord()
  if auiname in ['uipReksadana', 'new']:
    # new

    rec_tpi.tgl_transaksi = config.Now()
    rec_tpi.tgl_sistem = config.Now()
    rec_tpi.mode = auiname
    mode = auiname

    rec_tpi.biaya_redempt = 0.0

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

def uipReksadanaSetData(uipReksadana):
  global mode

  uideflist = uipReksadana.UIDefList
  config = uideflist.Config

  rec_inv = uipReksadana.Dataset.GetRecord(0)
  rec_tpi = uideflist.uipRedemptionReksadana.Dataset.GetRecord(0)

  oReksadana = config.CreatePObjImplProxy('Reksadana')
  oReksadana.Key = rec_inv.id_investasi
  
  moduleapi.CheckTransactionValidity(config, oReksadana, mode)


  rec_tpi.SetFieldByName('LReksadana.id_investasi', oReksadana.id_investasi)
  rec_tpi.SetFieldByName('LReksadana.nama_reksadana', oReksadana.nama_reksadana)
  rec_tpi.SetFieldByName('LReksadana.tgl_buka', oReksadana.tgl_buka)

  #rec_tpi.akum_nominal = oReksadana.akum_nominal

  rec_tpi.SetFieldByName('LPihakKetiga.kode_pihak_ketiga',oReksadana.LPihakKetiga.kode_pihak_ketiga)
  rec_tpi.SetFieldByName('LPihakKetiga.nama_pihak_ketiga',oReksadana.LPihakKetiga.nama_pihak_ketiga)

  rec_tpi.SetFieldByName('LPaketInvestasi.kode_paket_investasi',oReksadana.LRincianPaketInvestasi.LPaketInvestasi.kode_paket_investasi)
  rec_tpi.SetFieldByName('LPaketInvestasi.nama_paket_investasi',oReksadana.LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi)
  if rec_tpi.biaya_redempt != 0.0 :
    oReksaSwitch = config.CreatePObjImplProxy('Reksadana')
    oReksaSwitch.Key = int(rec_tpi.no_rekening)
    rec_tpi.SetFieldByName('LReksadanaSwitch.id_investasi',oReksaSwitch.id_investasi)
    rec_tpi.SetFieldByName('LReksadanaSwitch.nama_reksadana',oReksaSwitch.nama_reksadana)
  else :
    rec_tpi.SetFieldByName('LMasterGiro.no_giro',rec_tpi.no_rekening)

def uipRedemptionReksadanaApplyRow(uipRedemptionReksadana, oRedemptionReksadana):
  config = uipRedemptionReksadana.UIDefList.Config

  oReksadana = oRedemptionReksadana.LReksadana

  if oRedemptionReksadana.nilai_redempt <= 0 and oRedemptionReksadana.unit_penyertaan == 0.0 :
    pass#raise 'Kesalahan Redemption Reksadana','Nilai redemption harus lebih dari nol.'

  #if (oRedemptionReksadana.nilai_redempt - oReksadana.unit_penyertaan * oReksadana.NAB) > moduleapi.zero_approx:
  if (oRedemptionReksadana.nilai_redempt - oReksadana.akum_nominal) > moduleapi.zero_approx:
    pass#raise 'Kesalahan Redemption Reksadana','\nNilai redemption tidak boleh lebih dari unit penyertaan dikali NAB sekarang.'

  #totPiutInv = oReksadana.NAB_awal * oRedemptionReksadana.unit_penyertaan
  totPiutInv = oRedemptionReksadana.nilai_redempt
  
  oRedemptionReksadana.mutasi_debet = 0.0
  oRedemptionReksadana.mutasi_kredit = totPiutInv

  # nilai kode_jns_investasi diisi lagi jika belum ada
  oRedemptionReksadana.kode_jns_investasi = oRedemptionReksadana.LReksadana.kode_jns_investasi
  oRedemptionReksadana.kode_jenis_trinvestasi = 'R'
  oRedemptionReksadana.user_id = config.SecurityContext.userid
  oRedemptionReksadana.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oRedemptionReksadana.isCommitted = 'F'

  if oRedemptionReksadana.no_rekening == '' :
    raise 'PERINGATAN','Tujuan redempt harus diisi'


def FormEndProcessData(uideflist, datapacket):
  config = uideflist.Config
  uidef = uideflist.GetPClassUIByName('uipRedemptionReksadana')
  rec = uidef.ActiveRecord

  id_investasi = rec.GetFieldByName('LReksadana.id_investasi')

  if rec.mode == 'new':
    #moduleapi.IsInvestasiAvail(config, id_investasi)
    moduleapi.CheckTransaksiInvestasiExclusive(config, id_investasi)

