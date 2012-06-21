import sys, time, string
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi

mode = ''

def FormGeneralSetData(uideflist, auiname, apobjconst):
  global mode

  config = uideflist.Config
  uipBagiHasilReksadana = uideflist.uipBagiHasilReksadana
  uipReksadana = uideflist.uipReksadana

  rec_tpi = uipBagiHasilReksadana.Dataset.AddRecord()
  if auiname in ['uipReksadana', 'new']:
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

def uipReksadanaSetData(uipReksadana):
  global mode

  uideflist = uipReksadana.UIDefList
  config = uideflist.Config

  rec_inv = uipReksadana.Dataset.GetRecord(0)
  rec_tpi = uideflist.uipBagiHasilReksadana.Dataset.GetRecord(0)

  oReksadana = config.CreatePObjImplProxy('Reksadana')
  oReksadana.Key = rec_inv.id_investasi

  moduleapi.CheckTransactionValidity(config, oReksadana, mode)

  rec_tpi.SetFieldByName('LReksadana.id_investasi', oReksadana.id_investasi)
  rec_tpi.SetFieldByName('LReksadana.no_bilyet', oReksadana.no_bilyet)
  rec_tpi.SetFieldByName('LReksadana.tgl_buka', oReksadana.tgl_buka)

  rec_tpi.no_bilyet = oReksadana.no_bilyet
  #rec_tpi.akum_LR = oReksadana.akum_LR

  rec_tpi.SetFieldByName('LPihakKetiga.kode_pihak_ketiga',oReksadana.LPihakKetiga.kode_pihak_ketiga)
  rec_tpi.SetFieldByName('LPihakKetiga.nama_pihak_ketiga',oReksadana.LPihakKetiga.nama_pihak_ketiga)

  rec_tpi.SetFieldByName('LPaketInvestasi.kode_paket_investasi',oReksadana.LRincianPaketInvestasi.LPaketInvestasi.kode_paket_investasi)
  rec_tpi.SetFieldByName('LPaketInvestasi.nama_paket_investasi',oReksadana.LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi)

  rec_tpi.SetFieldByName('LJenisInvestasi.kode_jns_investasi',oReksadana.LRincianPaketInvestasi.LJenisInvestasi.kode_jns_investasi)
  rec_tpi.SetFieldByName('LJenisInvestasi.nama_jns_investasi',oReksadana.LRincianPaketInvestasi.LJenisInvestasi.nama_jns_investasi)

def uipBagiHasilReksadanaApplyRow(uipBagiHasilReksadana, oBagiHasilReksadana):
  config = uipBagiHasilReksadana.UIDefList.Config

  if oBagiHasilReksadana.NAB > oBagiHasilReksadana.LReksadana.NAB:
    raise 'Kesalahan Bagi Hasil Reksadana','Nilai NAB baru tidak boleh lebih dari nilai sebelumnya.'

  #if oBagiHasilReksadana.nominal_jual > oBagiHasilReksadana.LReksadana.nominal_jual:
  #  raise 'Kesalahan Bagi Hasil Reksadana','Nilai nominal jual baru tidak boleh lebih dari nilai sebelumnya.'

  if oBagiHasilReksadana.nominal_bagi_hasil >= 0.0:
    # bagi hasil (pendapatan reksadana)
    oBagiHasilReksadana.kode_subjns_LRInvestasi = 'C1'
    oBagiHasilReksadana.mutasi_kredit = oBagiHasilReksadana.nominal_bagi_hasil
    oBagiHasilReksadana.mutasi_debet = 0.0
  else:
    # bagi hasil (biaya reksadana)
    oBagiHasilReksadana.kode_subjns_LRInvestasi = 'C2'
    oBagiHasilReksadana.mutasi_kredit = 0.0
    oBagiHasilReksadana.mutasi_debet = -oBagiHasilReksadana.nominal_bagi_hasil

  oBagiHasilReksadana.kode_jns_investasi = oBagiHasilReksadana.LReksadana.kode_jns_investasi
  oBagiHasilReksadana.kode_jenis_trinvestasi = 'L'
  oBagiHasilReksadana.user_id = config.SecurityContext.userid
  oBagiHasilReksadana.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oBagiHasilReksadana.isCommitted = 'F'

def FormEndProcessData(uideflist, datapacket):
  config = uideflist.Config
  uidef = uideflist.GetPClassUIByName('uipBagiHasilReksadana')
  rec = uidef.ActiveRecord

  id_investasi = rec.GetFieldByName('LReksadana.id_investasi')

  if rec.mode == 'new':
    #moduleapi.IsInvestasiAvail(config, id_investasi)
    moduleapi.CheckTransaksiInvestasiExclusive(config, id_investasi)

