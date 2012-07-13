import sys, time, string
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi

mode = ''

def FormGeneralSetData(uideflist, auiname, apobjconst):
  global mode

  config = uideflist.Config
  uipBeliObligasi = uideflist.uipBeliObligasi
  uipObligasi = uideflist.uipObligasi

  rec_tpi = uipBeliObligasi.Dataset.AddRecord()
  if auiname in ['uipObligasi', 'new']:
    # new

    rec_tpi.tgl_transaksi = config.Now()
    rec_tpi.tgl_sistem = config.Now()
    rec_tpi.mutasi_debet = 0.0
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

def uipObligasiSetData(uipObligasi):
  global mode

  uideflist = uipObligasi.UIDefList
  config = uideflist.Config

  rec_inv = uipObligasi.Dataset.GetRecord(0)
  rec_tpi = uideflist.uipBeliObligasi.Dataset.GetRecord(0)

  oObligasi = config.CreatePObjImplProxy('Obligasi')
  oObligasi.Key = rec_inv.id_investasi
  
  moduleapi.CheckTransactionValidity(config, oObligasi, mode)

  rec_tpi.SetFieldByName('LObligasi.id_investasi', oObligasi.id_investasi)
  rec_tpi.SetFieldByName('LObligasi.nama_obligasi', oObligasi.nama_obligasi)
  rec_tpi.SetFieldByName('LObligasi.tgl_buka', oObligasi.tgl_buka)

  #rec_tpi.no_bilyet = oObligasi.no_bilyet
  #rec_tpi.akum_nominal = oObligasi.akum_nominal

  rec_tpi.SetFieldByName('LPihakKetiga.kode_pihak_ketiga',oObligasi.LPihakKetiga.kode_pihak_ketiga)
  rec_tpi.SetFieldByName('LPihakKetiga.nama_pihak_ketiga',oObligasi.LPihakKetiga.nama_pihak_ketiga)

  rec_tpi.SetFieldByName('LPaketInvestasi.kode_paket_investasi',oObligasi.LRincianPaketInvestasi.LPaketInvestasi.kode_paket_investasi)
  rec_tpi.SetFieldByName('LPaketInvestasi.nama_paket_investasi',oObligasi.LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi)

def uipBeliObligasiApplyRow(uipBeliObligasi, oBeliObligasi):
  config = uipBeliObligasi.UIDefList.Config

  if oBeliObligasi.mutasi_debet <= 0.0:
    raise Exception, 'Kesalahan Beli Obligasi' +  'Nilai beli obligasi harus lebih dari nol.'

  oBeliObligasi.mutasi_kredit = 0.0
  # nilai kode_jns_investasi diisi lagi jika belum ada
  oBeliObligasi.kode_jns_investasi = oBeliObligasi.LObligasi.kode_jns_investasi
  oBeliObligasi.kode_jenis_trinvestasi = 'O' # O = Beli Obligasi
  oBeliObligasi.user_id = config.SecurityContext.userid
  oBeliObligasi.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oBeliObligasi.isCommitted = 'F'

def FormEndProcessData(uideflist, datapacket):
  config = uideflist.Config
  uidef = uideflist.GetPClassUIByName('uipBeliObligasi')
  rec = uidef.ActiveRecord

  id_investasi = rec.GetFieldByName('LObligasi.id_investasi')

  if rec.mode == 'new':
    #moduleapi.IsInvestasiAvail(config, id_investasi)
    moduleapi.CheckTransaksiInvestasiExclusive(config, id_investasi)

