import sys, time, string
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi

mode = ''

def FormGeneralSetData(uideflist, auiname, apobjconst):
  global mode

  config = uideflist.Config
  uipSubscribeReksadana = uideflist.uipSubscribeReksadana
  uipReksadana = uideflist.uipReksadana

  rec_tpi = uipSubscribeReksadana.Dataset.AddRecord()
  if auiname in ['uipReksadana', 'new']:
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

def uipReksadanaSetData(uipReksadana):
  global mode

  uideflist = uipReksadana.UIDefList
  config = uideflist.Config

  rec_inv = uipReksadana.Dataset.GetRecord(0)
  rec_tpi = uideflist.uipSubscribeReksadana.Dataset.GetRecord(0)

  oReksadana = config.CreatePObjImplProxy('Reksadana')
  oReksadana.Key = rec_inv.id_investasi
  
  moduleapi.CheckTransactionValidity(config, oReksadana, mode)

  rec_tpi.SetFieldByName('LReksadana.id_investasi', oReksadana.id_investasi)
  rec_tpi.SetFieldByName('LReksadana.nama_reksadana', oReksadana.nama_reksadana)
  rec_tpi.SetFieldByName('LReksadana.tgl_buka', oReksadana.tgl_buka)

  #rec_tpi.akum_nominal = oReksadana.akum_nominal

  rec_tpi.SetFieldByName('LPihakKetiga.kode_pihak_ketiga', oReksadana.LPihakKetiga.kode_pihak_ketiga)
  rec_tpi.SetFieldByName('LPihakKetiga.nama_pihak_ketiga', oReksadana.LPihakKetiga.nama_pihak_ketiga)

  rec_tpi.SetFieldByName('LPaketInvestasi.kode_paket_investasi', oReksadana.LRincianPaketInvestasi.LPaketInvestasi.kode_paket_investasi)
  rec_tpi.SetFieldByName('LPaketInvestasi.nama_paket_investasi', oReksadana.LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi)

def uipSubscribeReksadanaApplyRow(uipSubscribeReksadana, oSubscribeReksadana):
  config = uipSubscribeReksadana.UIDefList.Config

  #oReksadana = oSubscribeReksadana.LInvestasi
  #oReksadana = oReksadana.CastAs('Reksadana')
  oReksadana = config.CreatePObjImplProxy('Reksadana')
  oReksadana.Key = oSubscribeReksadana.id_investasi

  oSubscribeReksadana.mutasi_debet = oSubscribeReksadana.nilai_subscribe
  if oSubscribeReksadana.mutasi_debet <= 0.0:
    raise Exception, 'Kesalahan Subscribe Reksadana Tambahan' + 'Nilai alokasi tambahan harus lebih dari nol.'

  oSubscribeReksadana.mutasi_kredit = 0.0
  # nilai kode_jns_investasi diisi lagi jika belum ada
  oSubscribeReksadana.kode_jns_investasi = oReksadana.kode_jns_investasi#oSubscribeReksadana.LReksadana.kode_jns_investasi
  oSubscribeReksadana.kode_jenis_trinvestasi = 'S'
  oSubscribeReksadana.user_id = config.SecurityContext.userid
  oSubscribeReksadana.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oSubscribeReksadana.isCommitted = 'F'


def FormEndProcessData(uideflist, datapacket):
  config = uideflist.Config
  uidef = uideflist.GetPClassUIByName('uipSubscribeReksadana')
  rec = uidef.ActiveRecord

  id_investasi = rec.GetFieldByName('LReksadana.id_investasi')

  if rec.mode == 'new':
    #moduleapi.IsInvestasiAvail(config, id_investasi)
    moduleapi.CheckTransaksiInvestasiExclusive(config, id_investasi)

