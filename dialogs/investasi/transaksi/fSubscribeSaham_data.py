import sys, time, string
sys.path.append('c:/dafapp/dplk/script_modules')
import moduleapi

mode = ''

def FormGeneralSetData(uideflist, auiname, apobjconst):
  global mode

  config = uideflist.Config
  uipSubscribeSaham = uideflist.uipSubscribeSaham
  uipSaham = uideflist.uipSaham

  rec_tpi = uipSubscribeSaham.Dataset.AddRecord()
  if auiname in ['uipSaham', 'new']:
    # new

    rec_tpi.tgl_transaksi = config.Now()
    rec_tpi.tgl_sistem = config.Now()
    rec_tpi.mutasi_debet = 0.0
    rec_tpi.unit_penyertaan = 0
    rec_tpi.subscription_fee = 0.0
    rec_tpi.mode = auiname
    mode = auiname

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
  rec_tpi = uideflist.uipSubscribeSaham.Dataset.GetRecord(0)

  oSaham = config.CreatePObjImplProxy('Saham')
  oSaham.Key = rec_inv.id_investasi
  
  moduleapi.CheckTransactionValidity(config, oSaham, mode)

  rec_tpi.SetFieldByName('LSaham.id_investasi', oSaham.id_investasi)
  rec_tpi.SetFieldByName('LSaham.nama_Saham', oSaham.nama_Saham)
  rec_tpi.SetFieldByName('LSaham.tgl_buka', oSaham.tgl_buka)

  #rec_tpi.akum_nominal = oSaham.akum_nominal

  rec_tpi.SetFieldByName('LPihakKetiga.kode_pihak_ketiga', oSaham.LPihakKetiga.kode_pihak_ketiga)
  rec_tpi.SetFieldByName('LPihakKetiga.nama_pihak_ketiga', oSaham.LPihakKetiga.nama_pihak_ketiga)

  rec_tpi.SetFieldByName('LPaketInvestasi.kode_paket_investasi', oSaham.LRincianPaketInvestasi.LPaketInvestasi.kode_paket_investasi)
  rec_tpi.SetFieldByName('LPaketInvestasi.nama_paket_investasi', oSaham.LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi)

def uipSubscribeSahamApplyRow(uipSubscribeSaham, oSubscribeSaham):
  config = uipSubscribeSaham.UIDefList.Config

  #oSaham = oSubscribeSaham.LInvestasi
  #oSaham = oSaham.CastAs('Saham')
  oSaham = config.CreatePObjImplProxy('Saham')
  oSaham.Key = oSubscribeSaham.id_investasi

  oSubscribeSaham.mutasi_debet = oSubscribeSaham.nilai_subscribe
  if oSubscribeSaham.mutasi_debet <= 0.0:
    raise Exception, 'Kesalahan Subscribe Saham Tambahan' + 'Nilai alokasi tambahan harus lebih dari nol.'

  oSubscribeSaham.mutasi_kredit = 0.0
  # nilai kode_jns_investasi diisi lagi jika belum ada
  oSubscribeSaham.kode_jns_investasi = oSaham.kode_jns_investasi#oSubscribeSaham.LSaham.kode_jns_investasi
  oSubscribeSaham.kode_jenis_trinvestasi = 'SS'
  oSubscribeSaham.user_id = config.SecurityContext.userid
  oSubscribeSaham.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oSubscribeSaham.isCommitted = 'F'


def FormEndProcessData(uideflist, datapacket):
  config = uideflist.Config
  uidef = uideflist.GetPClassUIByName('uipSubscribeSaham')
  rec = uidef.ActiveRecord

  id_investasi = rec.GetFieldByName('LSaham.id_investasi')

  if rec.mode == 'new':
    #moduleapi.IsInvestasiAvail(config, id_investasi)
    moduleapi.CheckTransaksiInvestasiExclusive(config, id_investasi)

