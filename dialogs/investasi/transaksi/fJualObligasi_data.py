import sys, time, string
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi

mode = ''

def FormGeneralSetData(uideflist, auiname, apobjconst):
  global mode

  config = uideflist.Config
  uipJualObligasi = uideflist.uipJualObligasi
  uipObligasi = uideflist.uipObligasi

  rec_tpi = uipJualObligasi.Dataset.AddRecord()
  if auiname in ['uipObligasi', 'new']:
    # new

    rec_tpi.tgl_transaksi = config.Now()
    rec_tpi.tgl_sistem = config.Now()
    rec_tpi.mode = auiname
    mode = auiname

    rec_tpi.nominal_jual = 0.0
    rec_tpi.profit = 0.0
    rec_tpi.biaya = 0.0

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
  rec_tpi = uideflist.uipJualObligasi.Dataset.GetRecord(0)

  oObligasi = config.CreatePObjImplProxy('Obligasi')
  oObligasi.Key = rec_inv.id_investasi
  
  moduleapi.CheckTransactionValidity(config, oObligasi, mode)

  rec_tpi.SetFieldByName('LObligasi.id_investasi', oObligasi.id_investasi)
  rec_tpi.SetFieldByName('LObligasi.nama_obligasi', oObligasi.nama_obligasi)
  rec_tpi.SetFieldByName('LObligasi.tgl_buka', oObligasi.tgl_buka)

  rec_inv.akum_nominal = oObligasi.harga_pari
  rec_tpi.PersenJual = (rec_tpi.nominal_jual / rec_inv.akum_nominal) * 100
  #rec_tpi.nominal_jual = oObligasi.akum_nominal
  rec_tpi.nama_obligasi = oObligasi.nama_obligasi
  #rec_tpi.akum_nominal = oObligasi.akum_nominal

  rec_tpi.SetFieldByName('LPihakKetiga.kode_pihak_ketiga',oObligasi.LPihakKetiga.kode_pihak_ketiga)
  rec_tpi.SetFieldByName('LPihakKetiga.nama_pihak_ketiga',oObligasi.LPihakKetiga.nama_pihak_ketiga)

  rec_tpi.SetFieldByName('LPaketInvestasi.kode_paket_investasi',oObligasi.LRincianPaketInvestasi.LPaketInvestasi.kode_paket_investasi)
  rec_tpi.SetFieldByName('LPaketInvestasi.nama_paket_investasi',oObligasi.LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi)

def uipJualObligasiApplyRow(uipJualObligasi, oJualObligasi):
  config = uipJualObligasi.UIDefList.Config

  oObl = config.CreatePObjImplProxy('Obligasi')
  oObl.Key = oJualObligasi.id_investasi
  y,m,d = oJualObligasi.tgl_transaksi[:3]
  tglt = config.ModDateTime.EncodeDate(y,m,d)
  y,m,d = oObl.tgl_jatuh_tempo[:3]
  tgljt = config.ModDateTime.EncodeDate(y,m,d)
  if oObl.TreatmentObligasi == 'H' :
    if oJualObligasi.nominal_jual != oObl.harga_pari :
      raise Exception, '\nPERINGATAN' + 'Untuk HTM harus dijual 100% '
    if tglt < (tgljt - 10) :
      raise Exception, '\nPERINGATAN' + 'Obligasi HTM tidak bisa dijual sebelum jatuh tempo'
  oJualObligasi.mutasi_debet = 0.0
  oJualObligasi.mutasi_kredit = oJualObligasi.nominal_jual#oJualObligasi.LObligasi.akum_nominal
  oJualObligasi.profit = oJualObligasi.nominal_jual - oObl.nominal_pembukaan
  # nilai kode_jns_investasi diisi lagi jika belum ada
  oJualObligasi.kode_jns_investasi = oObl.kode_jns_investasi#oJualObligasi.LObligasi.kode_jns_investasi
  oJualObligasi.kode_jenis_trinvestasi = 'J'
  oJualObligasi.user_id = config.SecurityContext.userid
  oJualObligasi.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oJualObligasi.isCommitted = 'F'

def FormEndProcessData(uideflist, datapacket):
  config = uideflist.Config
  uidef = uideflist.GetPClassUIByName('uipJualObligasi')
  rec = uidef.ActiveRecord

  id_investasi = rec.GetFieldByName('LObligasi.id_investasi')

  if rec.mode == 'new':
    #moduleapi.IsInvestasiAvail(config, id_investasi)
    moduleapi.CheckTransaksiInvestasiExclusive(config, id_investasi)

