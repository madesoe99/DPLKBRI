import sys, time, string
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi

mode = ''

def FormGeneralSetData(uideflist, auiname, apobjconst):
  global mode

  config = uideflist.Config
  uipTransPiutangLRInvestasi = uideflist.uipTransPiutangLRInvestasi
  uipInvestasi = uideflist.uipInvestasi

  rec_tpi = uipTransPiutangLRInvestasi.Dataset.AddRecord()
  if auiname == 'uipInvestasi':
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

  return 1

def uipInvestasiSetData(uipInvestasi):
  global mode

  uideflist = uipInvestasi.UIDefList
  config = uideflist.Config

  rec_inv = uipInvestasi.Dataset.GetRecord(0)
  rec_tpi = uideflist.uipTransPiutangLRInvestasi.Dataset.GetRecord(0)

  oInvestasi = config.CreatePObjImplProxy('Investasi')
  oInvestasi.Key = rec_inv.id_investasi

  moduleapi.CheckTransactionValidity(config, oInvestasi, mode)

  rec_tpi.SetFieldByName('LInvestasi.id_investasi',oInvestasi.id_investasi)
  rec_tpi.no_bilyet = oInvestasi.no_bilyet
  #rec_tpi.akum_piutangLR = oInvestasi.akum_piutangLR

  rec_tpi.SetFieldByName('LPihakKetiga.kode_pihak_ketiga',oInvestasi.LPihakKetiga.kode_pihak_ketiga)
  rec_tpi.SetFieldByName('LPihakKetiga.nama_pihak_ketiga',oInvestasi.LPihakKetiga.nama_pihak_ketiga)

  rec_tpi.SetFieldByName('LPaketInvestasi.kode_paket_investasi',oInvestasi.LRincianPaketInvestasi.LPaketInvestasi.kode_paket_investasi)
  rec_tpi.SetFieldByName('LPaketInvestasi.nama_paket_investasi',oInvestasi.LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi)

  rec_tpi.SetFieldByName('LJenisInvestasi.kode_jns_investasi',oInvestasi.LRincianPaketInvestasi.LJenisInvestasi.kode_jns_investasi)
  rec_tpi.SetFieldByName('LJenisInvestasi.nama_jns_investasi',oInvestasi.LRincianPaketInvestasi.LJenisInvestasi.nama_jns_investasi)

def uipTransPiutangLRInvestasiApplyRow(uipTransPiutangLRInvestasi, oTransPiutangLRInvestasi):
  config = uipTransPiutangLRInvestasi.UIDefList.Config

  if moduleapi.IsApproxZero(oTransPiutangLRInvestasi.mutasi_debet) and moduleapi.IsApproxZero(oTransPiutangLRInvestasi.mutasi_kredit):
    raise Exception, 'Kesalahan Piutang LR Manual' + '\nNilai mutasi debet dan mutasi kredit salah satunya harus lebih dari nol.'

  if oTransPiutangLRInvestasi.mutasi_debet < 0.0:
    raise Exception, 'Kesalahan Piutang LR Manual' + 'Nilai mutasi debet tidak boleh negatif.'

  if oTransPiutangLRInvestasi.mutasi_kredit < 0.0:
    raise Exception, 'Kesalahan Piutang LR Manual' + 'Nilai mutasi kredit tidak boleh negatif.'

  oTransPiutangLRInvestasi.kode_jenis_trinvestasi = 'H'
  oTransPiutangLRInvestasi.user_id = config.SecurityContext.userid
  oTransPiutangLRInvestasi.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oTransPiutangLRInvestasi.isCommitted = 'F'

