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
  if auiname == 'uipInvestasi':
    # new
    rec_tpi.tgl_transaksi = config.Now()
    rec_tpi.tgl_sistem = config.Now()
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
  rec_tpi = uideflist.uipTransPiutangInvestasi.Dataset.GetRecord(0)

  oInvestasi = config.CreatePObjImplProxy('Investasi')
  oInvestasi.Key = rec_inv.id_investasi
  
  moduleapi.CheckTransactionValidity(config, oInvestasi, mode)

  rec_tpi.SetFieldByName('LInvestasi.id_investasi',oInvestasi.id_investasi)
  rec_tpi.no_bilyet = oInvestasi.no_bilyet
  #rec_tpi.akum_nominal = oInvestasi.akum_nominal

  rec_tpi.SetFieldByName('LPihakKetiga.kode_pihak_ketiga',oInvestasi.LPihakKetiga.kode_pihak_ketiga)
  rec_tpi.SetFieldByName('LPihakKetiga.nama_pihak_ketiga',oInvestasi.LPihakKetiga.nama_pihak_ketiga)

  rec_tpi.SetFieldByName('LPaketInvestasi.kode_paket_investasi',oInvestasi.LRincianPaketInvestasi.LPaketInvestasi.kode_paket_investasi)
  rec_tpi.SetFieldByName('LPaketInvestasi.nama_paket_investasi',oInvestasi.LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi)

  rec_tpi.SetFieldByName('LJenisInvestasi.kode_jns_investasi',oInvestasi.LRincianPaketInvestasi.LJenisInvestasi.kode_jns_investasi)
  rec_tpi.SetFieldByName('LJenisInvestasi.nama_jns_investasi',oInvestasi.LRincianPaketInvestasi.LJenisInvestasi.nama_jns_investasi)

def uipTransPiutangInvestasiApplyRow(uipTransPiutangInvestasi, oTransPiutangInvestasi):
  config = uipTransPiutangInvestasi.UIDefList.Config

  oTransPiutangInvestasi.mutasi_debet = 0.0
  oTransPiutangInvestasi.mutasi_kredit = oTransPiutangInvestasi.LInvestasi.akum_nominal
  oTransPiutangInvestasi.kode_jenis_trinvestasi = 'C'
  oTransPiutangInvestasi.user_id = config.SecurityContext.userid
  oTransPiutangInvestasi.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oTransPiutangInvestasi.isCommitted = 'F'

