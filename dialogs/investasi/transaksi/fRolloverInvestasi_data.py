import sys, time, string
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi

mode = ''
prevMode = ''

def FormGeneralSetData(uideflist, auiname, apobjconst):
  global mode, prevMode

  config = uideflist.Config
  uipRolloverDeposito = uideflist.uipRolloverDeposito
  uipDeposito = uideflist.uipDeposito

  rec_tpi = uipRolloverDeposito.Dataset.AddRecord()
  if auiname in ['uipDeposito', 'new']:
    # new

    rec_tpi.tgl_transaksi = config.Now()
    rec_tpi.tgl_sistem = config.Now()
    rec_tpi.mode = auiname
    prevMode = rec_tpi.mode
    mode = auiname

    rec_tpi.user_id = config.SecurityContext.userid
    rec_tpi.terminal_id = config.SecurityContext.GetSessionInfo()[1]

  #set parameter nowDate
  recP = uideflist.uipParameter.Dataset.AddRecord()
  tglPakai = time.localtime()[:3]
  recP.nowDate = '%s/%s/%d' % (string.zfill(str(tglPakai[1]),2), \
    string.zfill(str(tglPakai[2]),2), tglPakai[0])

  if auiname == 'new':
    return 0

  return 1

def uipDepositoSetData(uipDeposito):
  global mode, prevMode

  uideflist = uipDeposito.UIDefList
  config = uideflist.Config

  rec_inv = uipDeposito.Dataset.GetRecord(0)
  rec_tpi = uideflist.uipRolloverDeposito.Dataset.GetRecord(0)

  oInvestasi = config.CreatePObjImplProxy('Investasi')
  oInvestasi.Key = rec_inv.id_investasi
  oDeposito = oInvestasi.CastAs('Deposito')

  moduleapi.CheckTransactionValidity(config, oInvestasi, mode)
  if (prevMode in ['new', 'edit', 'view', 'viewdoc', 'auth']) and not moduleapi.IsJatuhTempo(config, oDeposito):
    raise Exception, 'Kesalahan Rollover Deposito' +  'Deposito belum jatuh tempo.'

  rec_tpi.SetFieldByName('LDeposito.id_investasi', oInvestasi.id_investasi)
  rec_tpi.SetFieldByName('LDeposito.no_bilyet', oInvestasi.no_bilyet)
  rec_tpi.SetFieldByName('LDeposito.tgl_buka', oInvestasi.tgl_buka)

  rec_tpi.no_bilyet = oInvestasi.no_bilyet
  #rec_tpi.akum_piutangLR = oInvestasi.akum_piutangLR
  rec_tpi.rollover_counter = oInvestasi.rollover_counter
  rec_tpi.no_rekening = oDeposito.no_rekening

  rec_tpi.SetFieldByName('LPihakKetiga.kode_pihak_ketiga', oInvestasi.LPihakKetiga.kode_pihak_ketiga)
  rec_tpi.SetFieldByName('LPihakKetiga.nama_pihak_ketiga', oInvestasi.LPihakKetiga.nama_pihak_ketiga)

  #rec_tpi.SetFieldByName('LPaketInvestasi.kode_paket_investasi', oInvestasi.LRincianPaketInvestasi.LPaketInvestasi.kode_paket_investasi)
  #rec_tpi.SetFieldByName('LPaketInvestasi.nama_paket_investasi', oInvestasi.LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi)

  rec_tpi.treatmentPokok = oDeposito.treatmentPokok
  rec_tpi.kapitalisir_rollover = oDeposito.kapitalisir_rollover
  #rec_tpi.lakukan_kapitalisir = oDeposito.kapitalisir_rollover

def uipRolloverDepositoApplyRow(uipRolloverDeposito, oRolloverDeposito):
  config = uipRolloverDeposito.UIDefList.Config
  rec_tpi = uipRolloverDeposito.ActiveRecord

  if not moduleapi.IsJatuhTempo(config, oRolloverDeposito.LDeposito):
    pass#raise Exception, 'Kesalahan Rollover Deposito' +  'Deposito belum jatuh tempo.'

  if rec_tpi.lakukan_kapitalisir == 'T':
    oRolloverDeposito.mutasi_debet = oRolloverDeposito.LDeposito.akum_piutangLR
  else:
    oRolloverDeposito.mutasi_debet = 0.0

  oRolloverDeposito.mutasi_kredit = 0.0
  oRolloverDeposito.kode_jns_investasi = oRolloverDeposito.LDeposito.kode_jns_investasi
  oRolloverDeposito.kode_jenis_trinvestasi = 'F'
  oRolloverDeposito.user_id = config.SecurityContext.userid
  oRolloverDeposito.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oRolloverDeposito.isCommitted = 'F'

def FormEndProcessData(uideflist, datapacket):
  config = uideflist.Config
  uidef = uideflist.GetPClassUIByName('uipRolloverDeposito')
  rec = uidef.ActiveRecord

  id_investasi = rec.GetFieldByName('LDeposito.id_investasi')

  if rec.mode == 'new':
    #moduleapi.IsInvestasiAvail(config, id_investasi)
    moduleapi.CheckTransaksiInvestasiExclusive(config, id_investasi)

