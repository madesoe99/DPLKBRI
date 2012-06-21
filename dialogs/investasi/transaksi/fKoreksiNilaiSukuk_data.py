import sys, time, string
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi

mode = ''

def FormGeneralSetData(uideflist, auiname, apobjconst):
  global mode

  config = uideflist.Config
  uipPendapatanObligasi = uideflist.uipPendapatanObligasi
  uipObligasi = uideflist.uipObligasi

  rec_tpi = uipPendapatanObligasi.Dataset.AddRecord()
  if auiname in ['uipObligasi', 'new']:
    # new

    rec_tpi.tgl_transaksi = config.Now()
    rec_tpi.tgl_sistem = config.Now()
    rec_tpi.nominal = 0.0
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
  rec_tpi = uideflist.uipPendapatanObligasi.Dataset.GetRecord(0)

  oObligasi = config.CreatePObjImplProxy('Obligasi')
  oObligasi.Key = rec_inv.id_investasi

  moduleapi.CheckTransactionValidity(config, oObligasi, mode)

  rec_tpi.SetFieldByName('LObligasi.id_investasi', oObligasi.id_investasi)
  rec_tpi.SetFieldByName('LObligasi.nama_obligasi', oObligasi.nama_obligasi)
  rec_tpi.SetFieldByName('LObligasi.tgl_buka', oObligasi.tgl_buka)

  #rec_tpi.akum_LR = oObligasi.akum_LR
  #rec_tpi.akum_piutangLR = oObligasi.akum_piutangLR
  rec_inv.akum_nominal = oObligasi.Harga_pari
  rec_tpi.nominal_total = rec_tpi.nominal + rec_inv.akum_nominal
  rec_tpi.Nilai_Wajar = rec_tpi.nominal_total * 100 / rec_inv.akum_nominal

  rec_tpi.SetFieldByName('LPihakKetiga.kode_pihak_ketiga',oObligasi.LPihakKetiga.kode_pihak_ketiga)
  rec_tpi.SetFieldByName('LPihakKetiga.nama_pihak_ketiga',oObligasi.LPihakKetiga.nama_pihak_ketiga)

  rec_tpi.SetFieldByName('LPaketInvestasi.kode_paket_investasi',oObligasi.LRincianPaketInvestasi.LPaketInvestasi.kode_paket_investasi)
  rec_tpi.SetFieldByName('LPaketInvestasi.nama_paket_investasi',oObligasi.LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi)

def uipPendapatanObligasiApplyRow(uipPendapatanObligasi, oPendapatanObligasi):
  config = uipPendapatanObligasi.UIDefList.Config

  #if oPendapatanObligasi.nominal < moduleapi.zero_approx:
  #  raise 'Kesalahan Pendapatan Obligasi','Nilai pendapatan obligasi harus lebih dari nol.'

  if oPendapatanObligasi.nominal < moduleapi.zero_approx:
    oPendapatanObligasi.mutasi_kredit = 0.0
    oPendapatanObligasi.mutasi_debet = -oPendapatanObligasi.nominal
  else :
    oPendapatanObligasi.mutasi_kredit = oPendapatanObligasi.nominal
    oPendapatanObligasi.mutasi_debet = 0.0
  oObl = config.CreatePObjImplProxy('Obligasi')
  oObl.Key = oPendapatanObligasi.id_investasi

  oPendapatanObligasi.kode_jns_investasi = oObl.kode_jns_investasi#oPendapatanObligasi.LObligasi.kode_jns_investasi
  oPendapatanObligasi.kode_jenis_trinvestasi = 'N'
  oPendapatanObligasi.user_id = config.SecurityContext.userid
  oPendapatanObligasi.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oPendapatanObligasi.isCommitted = 'F'

def FormEndProcessData(uideflist, datapacket):
  config = uideflist.Config
  uidef = uideflist.GetPClassUIByName('uipPendapatanObligasi')
  rec = uidef.ActiveRecord

  id_investasi = rec.GetFieldByName('LObligasi.id_investasi')

  if rec.mode == 'new':
    #moduleapi.IsInvestasiAvail(config, id_investasi)
    moduleapi.CheckTransaksiInvestasiExclusive(config, id_investasi)

