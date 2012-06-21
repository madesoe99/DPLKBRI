import sys, time, string
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi

mode = ''

def FormGeneralSetData(uideflist, auiname, apobjconst):
  global mode

  config = uideflist.Config
  uipRealisasiReturnSaham = uideflist.uipRealisasiReturnSaham
  uipSaham = uideflist.uipSaham

  rec_tpi = uipRealisasiReturnSaham.Dataset.AddRecord()
  if auiname in ['uipSaham', 'new']:
    # new

    rec_tpi.tgl_transaksi = config.Now()
    rec_tpi.tgl_sistem = config.Now()
    rec_tpi.NAB = 0.0
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
  rec_tpi = uideflist.uipRealisasiReturnSaham.Dataset.GetRecord(0)

  oSaham = config.CreatePObjImplProxy('Saham')
  oSaham.Key = rec_inv.id_investasi

  moduleapi.CheckTransactionValidity(config, oSaham, mode)

  rec_tpi.SetFieldByName('LSaham.id_investasi', oSaham.id_investasi)
  rec_tpi.SetFieldByName('LSaham.nama_Saham', oSaham.nama_Saham)
  rec_tpi.SetFieldByName('LSaham.tgl_buka', oSaham.tgl_buka)

  rec_tpi.SetFieldByName('LPihakKetiga.kode_pihak_ketiga',oSaham.LPihakKetiga.kode_pihak_ketiga)
  rec_tpi.SetFieldByName('LPihakKetiga.nama_pihak_ketiga',oSaham.LPihakKetiga.nama_pihak_ketiga)

  rec_tpi.SetFieldByName('LPaketInvestasi.kode_paket_investasi',oSaham.LRincianPaketInvestasi.LPaketInvestasi.kode_paket_investasi)
  rec_tpi.SetFieldByName('LPaketInvestasi.nama_paket_investasi',oSaham.LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi)

def uipRealisasiReturnApplyRow(uipRealisasiReturnSaham, oRealisasiReturn):
  uideflist = uipRealisasiReturnSaham.UIDefList
  config = uideflist.Config
  
  if oRealisasiReturn.NAB < moduleapi.zero_approx:
    raise 'Kesalahan Realisasi Return Saham','\nNilai NAB baru harus lebih dari nol.'

  #if oRealisasiReturn.nominal_jual > oRealisasiReturn.LSaham.nominal_jual:
  #  raise 'Kesalahan Realisasi Return Saham','Nilai nominal jual baru tidak boleh lebih dari nilai sebelumnya.'

  oRealisasiReturn.unit_penyertaan = oRealisasiReturn.nominal_investasi / oRealisasiReturn.NAB
  oRealisasiReturn.profit = oRealisasiReturn.NAB * oRealisasiReturn.LSaham.unit_penyertaan - oRealisasiReturn.nominal_investasi
  if oRealisasiReturn.profit >= 0.0:
    # profit
    oRealisasiReturn.kode_subjns_LRInvestasi = 'C-PROF'
    oRealisasiReturn.mutasi_debet = 0.0
    oRealisasiReturn.mutasi_kredit = oRealisasiReturn.profit
  else:
    # loss
    oRealisasiReturn.kode_subjns_LRInvestasi = 'C-COST'
    oRealisasiReturn.mutasi_debet = -oRealisasiReturn.profit
    oRealisasiReturn.mutasi_kredit = 0.0

  oRealisasiReturn.kode_jns_investasi = oRealisasiReturn.LSaham.kode_jns_investasi
  oRealisasiReturn.kode_jenis_trinvestasi = 'U' # realisasi return Saham
  oRealisasiReturn.user_id = config.SecurityContext.userid
  oRealisasiReturn.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oRealisasiReturn.isCommitted = 'F'

def FormEndProcessData(uideflist, datapacket):
  config = uideflist.Config
  uidef = uideflist.GetPClassUIByName('uipRealisasiReturnSaham')
  rec = uidef.ActiveRecord

  id_investasi = rec.GetFieldByName('LSaham.id_investasi')

  if rec.mode == 'new':
    #moduleapi.IsInvestasiAvail(config, id_investasi)
    moduleapi.CheckTransaksiInvestasiExclusive(config, id_investasi)

