import sys, time, string
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi

mode = ''

def FormGeneralSetData(uideflist, auiname, apobjconst):
  global mode

  config = uideflist.Config
  uipTransPiutangInvestasi = uideflist.uipTransPiutangInvestasi
  uipInvestasi = uideflist.uipInvestasi

  rec_tpi = uipTransPiutangInvestasi.Dataset.AddRecord()
  if auiname in ['uipInvestasi', 'new']:
    # new

    rec_tpi.tgl_transaksi = config.Now()
    rec_tpi.tgl_sistem = config.Now()
    rec_tpi.mutasi_debet = 0.0
    rec_tpi.mutasi_kredit = 0.0
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

def uipInvestasiSetData(uipInvestasi):
  global mode

  uideflist = uipInvestasi.UIDefList
  config = uideflist.Config

  rec_inv = uipInvestasi.Dataset.GetRecord(0)
  rec_tpi = uideflist.uipTransPiutangInvestasi.Dataset.GetRecord(0)

  oInvestasi = config.CreatePObjImplProxy('Investasi')
  oInvestasi.Key = rec_inv.id_investasi

  moduleapi.CheckTransactionValidity(config, oInvestasi, mode, 'I')

  rec_tpi.SetFieldByName('LInvestasi.id_investasi', oInvestasi.id_investasi)
  #rec_tpi.SetFieldByName('LInvestasi.no_bilyet', oInvestasi.no_bilyet)
  rec_tpi.SetFieldByName('LInvestasi.tgl_buka', oInvestasi.tgl_buka)

  #rec_tpi.no_bilyet = oInvestasi.no_bilyet
  #rec_tpi.akum_nominal = oInvestasi.akum_nominal

  rec_tpi.SetFieldByName('LPihakKetiga.kode_pihak_ketiga',oInvestasi.LPihakKetiga.kode_pihak_ketiga)
  rec_tpi.SetFieldByName('LPihakKetiga.nama_pihak_ketiga',oInvestasi.LPihakKetiga.nama_pihak_ketiga)

  rec_tpi.SetFieldByName('LPaketInvestasi.kode_paket_investasi',oInvestasi.LRincianPaketInvestasi.LPaketInvestasi.kode_paket_investasi)
  rec_tpi.SetFieldByName('LPaketInvestasi.nama_paket_investasi',oInvestasi.LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi)

def uipTransPiutangInvestasiApplyRow(uipTransPiutangInvestasi, oTransPiutangInvestasi):
  config = uipTransPiutangInvestasi.UIDefList.Config

  if moduleapi.IsApproxZero(oTransPiutangInvestasi.mutasi_debet) and moduleapi.IsApproxZero(oTransPiutangInvestasi.mutasi_kredit):
    raise Exception, 'Kesalahan Investasi Manual' + '\nNilai mutasi debet dan mutasi kredit salah satunya harus lebih dari nol.'

  if oTransPiutangInvestasi.mutasi_debet < 0.0:
    raise Exception, 'Kesalahan Investasi Manual' + 'Nilai mutasi debet tidak boleh negatif.'

  if oTransPiutangInvestasi.mutasi_kredit < 0.0:
    raise Exception, 'Kesalahan Investasi Manual' + 'Nilai mutasi kredit tidak boleh negatif.'

  oTransPiutangInvestasi.kode_jns_investasi = oTransPiutangInvestasi.LInvestasi.kode_jns_investasi
  oTransPiutangInvestasi.kode_jenis_trinvestasi = 'I'
  oTransPiutangInvestasi.user_id = config.SecurityContext.userid
  oTransPiutangInvestasi.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oTransPiutangInvestasi.isCommitted = 'F'

def FormEndProcessData(uideflist, datapacket):
  config = uideflist.Config
  uidef = uideflist.GetPClassUIByName('uipTransPiutangInvestasi')
  rec = uidef.ActiveRecord

  id_investasi = rec.GetFieldByName('LInvestasi.id_investasi')

  if rec.mode == 'new':
    #moduleapi.IsInvestasiAvail(config, id_investasi)
    moduleapi.CheckTransaksiInvestasiExclusive(config, id_investasi)

