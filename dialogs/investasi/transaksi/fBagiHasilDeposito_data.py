import sys, time, string
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi

mode = ''

def FormGeneralSetData(uideflist, auiname, apobjconst):
  global mode

  config = uideflist.Config
  uipBagiHasilDeposito = uideflist.uipBagiHasilDeposito
  uipDeposito = uideflist.uipDeposito

  rec_tpi = uipBagiHasilDeposito.Dataset.AddRecord()
  if auiname in ['uipDeposito', 'new']:
    # new

    rec_tpi.tgl_transaksi = config.Now()
    rec_tpi.tgl_sistem = config.Now()
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

def uipDepositoSetData(uipDeposito):
  global mode

  uideflist = uipDeposito.UIDefList
  config = uideflist.Config

  rec_inv = uipDeposito.Dataset.GetRecord(0)
  rec_tpi = uideflist.uipBagiHasilDeposito.Dataset.GetRecord(0)

  oDeposito = config.CreatePObjImplProxy('Deposito')
  oDeposito.Key = rec_inv.id_investasi

  oInvestasi = config.CreatePObjImplProxy('Investasi')
  oInvestasi.Key = rec_inv.id_investasi

  moduleapi.CheckTransactionValidity(config, oDeposito, mode)

  rec_tpi.SetFieldByName('LDeposito.id_investasi', oDeposito.id_investasi)
  rec_tpi.SetFieldByName('LDeposito.no_bilyet', oDeposito.no_bilyet)
  rec_tpi.SetFieldByName('LDeposito.tgl_buka', oDeposito.tgl_buka)
  rec_tpi.SetFieldByName('LDeposito.rekening_deposito', oDeposito.rekening_deposito)
  rec_tpi.SetFieldByName('nomrek_baghas', oDeposito.no_rekening)
  rec_tpi.SetFieldByName('nominal_pembukaan', oInvestasi.nominal_pembukaan)

  rec_tpi.no_bilyet = oDeposito.no_bilyet
  #rec_tpi.akum_LR = oDeposito.akum_LR
  #rec_tpi.akum_piutangLR = oDeposito.akum_piutangLR

  rec_tpi.SetFieldByName('LPihakKetiga.kode_pihak_ketiga',oDeposito.LPihakKetiga.kode_pihak_ketiga)
  rec_tpi.SetFieldByName('LPihakKetiga.nama_pihak_ketiga',oDeposito.LPihakKetiga.nama_pihak_ketiga)

  #rec_tpi.SetFieldByName('LPaketInvestasi.kode_paket_investasi',oDeposito.LRincianPaketInvestasi.LPaketInvestasi.kode_paket_investasi)
  #rec_tpi.SetFieldByName('LPaketInvestasi.nama_paket_investasi',oDeposito.LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi)

  #rec_tpi.SetFieldByName('LJenisInvestasi.kode_jns_investasi',oDeposito.LRincianPaketInvestasi.LJenisInvestasi.kode_jns_investasi)
  #rec_tpi.SetFieldByName('LJenisInvestasi.nama_jns_investasi',oDeposito.LRincianPaketInvestasi.LJenisInvestasi.nama_jns_investasi)

def uipBagiHasilDepositoApplyRow(uipBagiHasilDeposito, oBagiHasilDeposito):
  config = uipBagiHasilDeposito.UIDefList.Config

  if oBagiHasilDeposito.mutasi_kredit <= moduleapi.zero_approx:
    raise 'Kesalahan Bagi Hasil Deposito','Nilai bagi hasil harus lebih dari nol.'

  oBagiHasilDeposito.nominal = oBagiHasilDeposito.mutasi_kredit
  oBagiHasilDeposito.mutasi_debet = 0.0
  oBagiHasilDeposito.kode_jns_investasi = oBagiHasilDeposito.LDeposito.kode_jns_investasi
  oBagiHasilDeposito.kode_jenis_trinvestasi = 'E'
  oBagiHasilDeposito.user_id = config.SecurityContext.userid
  oBagiHasilDeposito.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oBagiHasilDeposito.isCommitted = 'F'

def FormEndProcessData(uideflist, datapacket):
  config = uideflist.Config
  uidef = uideflist.GetPClassUIByName('uipBagiHasilDeposito')
  rec = uidef.ActiveRecord

  id_investasi = rec.GetFieldByName('LDeposito.id_investasi')

  if rec.mode == 'new':
    #moduleapi.IsInvestasiAvail(config, id_investasi)
    moduleapi.CheckTransaksiInvestasiExclusive(config, id_investasi)

