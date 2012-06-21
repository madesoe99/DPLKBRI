import sys, time, string
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi

mode = ''

def FormGeneralSetData(uideflist, auiname, apobjconst):
  global mode

  config = uideflist.Config
  uipTutupDeposito = uideflist.uipTutupDeposito
  uipDeposito = uideflist.uipDeposito

  rec_tpi = uipTutupDeposito.Dataset.AddRecord()
  if auiname in ['uipDeposito', 'new']:
    # new

    rec_tpi.tgl_transaksi = config.Now()
    rec_tpi.tgl_sistem = config.Now()
    rec_tpi.mode = auiname
    mode = auiname

    rec_tpi.penalti = 0.0
    #rec_tpi.akom_bagi_hasil = 0.0

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
  rec_tpi = uideflist.uipTutupDeposito.Dataset.GetRecord(0)

  oDeposito = config.CreatePObjImplProxy('Deposito')
  oDeposito.Key = rec_inv.id_investasi
  
  moduleapi.CheckTransactionValidity(config, oDeposito, mode)

  rec_tpi.SetFieldByName('LDeposito.id_investasi', oDeposito.id_investasi)
  rec_tpi.SetFieldByName('LDeposito.no_bilyet', oDeposito.no_bilyet)
  rec_tpi.SetFieldByName('LDeposito.tgl_buka', oDeposito.tgl_buka)
  rec_tpi.SetFieldByName('LDeposito.rekening_deposito', oDeposito.rekening_deposito)

  rec_tpi.no_bilyet = oDeposito.no_bilyet
  #rec_tpi.akum_nominal = oDeposito.akum_nominal

  rec_tpi.SetFieldByName('LPihakKetiga.kode_pihak_ketiga',oDeposito.LPihakKetiga.kode_pihak_ketiga)
  rec_tpi.SetFieldByName('LPihakKetiga.nama_pihak_ketiga',oDeposito.LPihakKetiga.nama_pihak_ketiga)
  if rec_tpi.no_rekening == '' :
    rec_tpi.SetFieldByName('LMasterGiro.no_giro',oDeposito.no_rekening)
  else :
    rec_tpi.SetFieldByName('LMasterGiro.no_giro',rec_tpi.no_rekening)
  #rec_tpi.SetFieldByName('LPaketInvestasi.kode_paket_investasi',oDeposito.LRincianPaketInvestasi.LPaketInvestasi.kode_paket_investasi)
  #rec_tpi.SetFieldByName('LPaketInvestasi.nama_paket_investasi',oDeposito.LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi)

def uipTutupDepositoApplyRow(uipTutupDeposito, oTutupDeposito):
  config = uipTutupDeposito.UIDefList.Config

  oTutupDeposito.mutasi_debet = 0.0
  oTutupDeposito.mutasi_kredit = oTutupDeposito.LDeposito.akum_nominal
  # nilai kode_jns_investasi diisi lagi jika belum ada
  oTutupDeposito.kode_jns_investasi = oTutupDeposito.LDeposito.kode_jns_investasi
  oTutupDeposito.kode_jenis_trinvestasi = 'C'
  oTutupDeposito.user_id = config.SecurityContext.userid
  oTutupDeposito.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oTutupDeposito.isCommitted = 'F'

def FormEndProcessData(uideflist, datapacket):
  config = uideflist.Config
  uidef = uideflist.GetPClassUIByName('uipTutupDeposito')
  rec = uidef.ActiveRecord

  id_investasi = rec.GetFieldByName('LDeposito.id_investasi')

  if rec.mode == 'new':
    #moduleapi.IsInvestasiAvail(config, id_investasi)
    moduleapi.CheckTransaksiInvestasiExclusive(config, id_investasi)

