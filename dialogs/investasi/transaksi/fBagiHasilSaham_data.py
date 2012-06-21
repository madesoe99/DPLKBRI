import sys, time, string
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi

mode = ''

def FormGeneralSetData(uideflist, auiname, apobjconst):
  global mode

  config = uideflist.Config
  uipBagiHasilSaham = uideflist.uipBagiHasilSaham
  uipSaham = uideflist.uipSaham

  rec_tpi = uipBagiHasilSaham.Dataset.AddRecord()
  if auiname in ['uipSaham', 'new']:
    # new

    rec_tpi.tgl_transaksi = config.Now()
    rec_tpi.tgl_sistem = config.Now()
    rec_tpi.NAB = 0.0
    rec_tpi.nominal_jual = 0.0
    rec_tpi.nominal_bagi_hasil = 0.0
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
  rec_tpi = uideflist.uipBagiHasilSaham.Dataset.GetRecord(0)

  oSaham = config.CreatePObjImplProxy('Saham')
  oSaham.Key = rec_inv.id_investasi

  moduleapi.CheckTransactionValidity(config, oSaham, mode)

  rec_tpi.SetFieldByName('LSaham.id_investasi', oSaham.id_investasi)
  rec_tpi.SetFieldByName('LSaham.no_bilyet', oSaham.no_bilyet)
  rec_tpi.SetFieldByName('LSaham.tgl_buka', oSaham.tgl_buka)

  rec_tpi.no_bilyet = oSaham.no_bilyet
  #rec_tpi.akum_LR = oSaham.akum_LR

  rec_tpi.SetFieldByName('LPihakKetiga.kode_pihak_ketiga',oSaham.LPihakKetiga.kode_pihak_ketiga)
  rec_tpi.SetFieldByName('LPihakKetiga.nama_pihak_ketiga',oSaham.LPihakKetiga.nama_pihak_ketiga)

  rec_tpi.SetFieldByName('LPaketInvestasi.kode_paket_investasi',oSaham.LRincianPaketInvestasi.LPaketInvestasi.kode_paket_investasi)
  rec_tpi.SetFieldByName('LPaketInvestasi.nama_paket_investasi',oSaham.LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi)

  rec_tpi.SetFieldByName('LJenisInvestasi.kode_jns_investasi',oSaham.LRincianPaketInvestasi.LJenisInvestasi.kode_jns_investasi)
  rec_tpi.SetFieldByName('LJenisInvestasi.nama_jns_investasi',oSaham.LRincianPaketInvestasi.LJenisInvestasi.nama_jns_investasi)

def uipBagiHasilSahamApplyRow(uipBagiHasilSaham, oBagiHasilSaham):
  config = uipBagiHasilSaham.UIDefList.Config

  if oBagiHasilSaham.NAB > oBagiHasilSaham.LSaham.NAB:
    raise 'Kesalahan Bagi Hasil Saham','Nilai NAB baru tidak boleh lebih dari nilai sebelumnya.'

  #if oBagiHasilSaham.nominal_jual > oBagiHasilSaham.LSaham.nominal_jual:
  #  raise 'Kesalahan Bagi Hasil Saham','Nilai nominal jual baru tidak boleh lebih dari nilai sebelumnya.'

  if oBagiHasilSaham.nominal_bagi_hasil >= 0.0:
    # bagi hasil (pendapatan Saham)
    oBagiHasilSaham.kode_subjns_LRInvestasi = 'C1'
    oBagiHasilSaham.mutasi_kredit = oBagiHasilSaham.nominal_bagi_hasil
    oBagiHasilSaham.mutasi_debet = 0.0
  else:
    # bagi hasil (biaya Saham)
    oBagiHasilSaham.kode_subjns_LRInvestasi = 'C2'
    oBagiHasilSaham.mutasi_kredit = 0.0
    oBagiHasilSaham.mutasi_debet = -oBagiHasilSaham.nominal_bagi_hasil

  oBagiHasilSaham.kode_jns_investasi = oBagiHasilSaham.LSaham.kode_jns_investasi
  oBagiHasilSaham.kode_jenis_trinvestasi = 'L'
  oBagiHasilSaham.user_id = config.SecurityContext.userid
  oBagiHasilSaham.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oBagiHasilSaham.isCommitted = 'F'

def FormEndProcessData(uideflist, datapacket):
  config = uideflist.Config
  uidef = uideflist.GetPClassUIByName('uipBagiHasilSaham')
  rec = uidef.ActiveRecord

  id_investasi = rec.GetFieldByName('LSaham.id_investasi')

  if rec.mode == 'new':
    #moduleapi.IsInvestasiAvail(config, id_investasi)
    moduleapi.CheckTransaksiInvestasiExclusive(config, id_investasi)

