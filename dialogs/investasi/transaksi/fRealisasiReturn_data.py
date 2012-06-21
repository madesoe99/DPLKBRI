import sys, time, string
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi

mode = ''

def FormGeneralSetData(uideflist, auiname, apobjconst):
  global mode

  config = uideflist.Config
  uipRealisasiReturn = uideflist.uipRealisasiReturn
  uipReksadana = uideflist.uipReksadana

  rec_tpi = uipRealisasiReturn.Dataset.AddRecord()
  if auiname in ['uipReksadana', 'new']:
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

def uipReksadanaSetData(uipReksadana):
  global mode

  uideflist = uipReksadana.UIDefList
  config = uideflist.Config

  rec_inv = uipReksadana.Dataset.GetRecord(0)
  rec_tpi = uideflist.uipRealisasiReturn.Dataset.GetRecord(0)

  oReksadana = config.CreatePObjImplProxy('Reksadana')
  oReksadana.Key = rec_inv.id_investasi

  moduleapi.CheckTransactionValidity(config, oReksadana, mode)

  rec_tpi.SetFieldByName('LReksadana.id_investasi', oReksadana.id_investasi)
  rec_tpi.SetFieldByName('LReksadana.nama_reksadana', oReksadana.nama_reksadana)
  rec_tpi.SetFieldByName('LReksadana.tgl_buka', oReksadana.tgl_buka)

  rec_tpi.SetFieldByName('LPihakKetiga.kode_pihak_ketiga',oReksadana.LPihakKetiga.kode_pihak_ketiga)
  rec_tpi.SetFieldByName('LPihakKetiga.nama_pihak_ketiga',oReksadana.LPihakKetiga.nama_pihak_ketiga)

  rec_tpi.SetFieldByName('LPaketInvestasi.kode_paket_investasi',oReksadana.LRincianPaketInvestasi.LPaketInvestasi.kode_paket_investasi)
  rec_tpi.SetFieldByName('LPaketInvestasi.nama_paket_investasi',oReksadana.LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi)

def uipRealisasiReturnApplyRow(uipRealisasiReturn, oRealisasiReturn):
  uideflist = uipRealisasiReturn.UIDefList
  config = uideflist.Config
  
  if oRealisasiReturn.NAB < moduleapi.zero_approx:
    raise 'Kesalahan Realisasi Return Reksadana','\nNilai NAB baru harus lebih dari nol.'

  #if oRealisasiReturn.nominal_jual > oRealisasiReturn.LReksadana.nominal_jual:
  #  raise 'Kesalahan Realisasi Return Reksadana','Nilai nominal jual baru tidak boleh lebih dari nilai sebelumnya.'

  oRealisasiReturn.unit_penyertaan = oRealisasiReturn.nominal_investasi / oRealisasiReturn.NAB
  oRealisasiReturn.profit = oRealisasiReturn.NAB * oRealisasiReturn.LReksadana.unit_penyertaan - oRealisasiReturn.nominal_investasi
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

  oRealisasiReturn.kode_jns_investasi = oRealisasiReturn.LReksadana.kode_jns_investasi
  oRealisasiReturn.kode_jenis_trinvestasi = 'U' # realisasi return reksadana
  oRealisasiReturn.user_id = config.SecurityContext.userid
  oRealisasiReturn.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oRealisasiReturn.isCommitted = 'F'

def FormEndProcessData(uideflist, datapacket):
  config = uideflist.Config
  uidef = uideflist.GetPClassUIByName('uipRealisasiReturn')
  rec = uidef.ActiveRecord

  id_investasi = rec.GetFieldByName('LReksadana.id_investasi')

  if rec.mode == 'new':
    #moduleapi.IsInvestasiAvail(config, id_investasi)
    moduleapi.CheckTransaksiInvestasiExclusive(config, id_investasi)

