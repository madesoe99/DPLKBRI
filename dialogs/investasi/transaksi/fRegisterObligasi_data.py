import sys, time, string
sys.path.append('c:/dafapp/dplk07/script_modules')
sys.path.append('c:/dafapp/dplk07/scripts/investasi/transaksi')
import moduleapi, paketinvinfo

def FormGeneralSetData(uideflist, auiname, apobjconst):
  config = uideflist.Config
  uipRegisterObligasi = uideflist.uipRegisterObligasi
  uipParameter = uideflist.uipParameter

  recP = uipParameter.Dataset.AddRecord()
  #set parameter nowDate
  tglPakai = time.localtime()[:3]
  recP.nowDate = '%s/%s/%d' % (string.zfill(str(tglPakai[1]),2), \
    string.zfill(str(tglPakai[2]),2),tglPakai[0])

  if auiname == 'new':
    rec = uipRegisterObligasi.Dataset.AddRecord()
    uipRegisterObligasi = uideflist.uipRegisterObligasi
    rec.tgl_buka = config.Now()
    rec.tgl_jatuh_tempo = rec.tgl_buka
    rec.nominal = 0.0
    rec.tanggal_register = config.Now()
    rec.mode = auiname

    rec.harga_pari = 0.0
    rec.harga_beli = 0.0
    rec.harga_beli_val = 0.0
    rec.nilai_wajar = 0.0
    rec.nilai_wajar_val = 0.0
    #rec.biaya = 0.0

    rec.jenisKupon = 3
    rec.jenis_obligasi = 'R'

    rec.user_id = config.SecurityContext.userid
    rec.terminal_id = config.SecurityContext.GetSessionInfo()[1]
    
    '''KodeJnsInv = 'O'
    resSQLRPI = moduleapi.resSQLRPI(config, KodeJnsInv)
    if resSQLRPI.RecordCount == 1:
      rec.SetFieldByName('LRincianPaketInvestasi.kode_jns_investasi', KodeJnsInv)
      rec.SetFieldByName('LRincianPaketInvestasi.kode_paket_investasi', resSQLRPI.kode_paket_investasi)
      rec.maks_proporsi = resSQLRPI.maks_proporsi or 0.0
      rec.dpkPaket, rec.dpkInvExisting, rec.dpkTersedia, rec.nilaiMaksProporsi, rec.nominalGiro = paketinvinfo.getPaketInfo(config, resSQLRPI.kode_paket_investasi, KodeJnsInv)
      rec.nominal = min(rec.dpkTersedia, rec.nilaiMaksProporsi)'''

    retval = 0
  else:
    retval = 1

  return retval

def uipRegisterObligasiSetData(uipRegisterObligasi):
  config = uipRegisterObligasi.UIDefList.Config
  rec = uipRegisterObligasi.Dataset.GetRecord(0)
  rec.SetFieldByName('LMasterGiro.no_giro',rec.no_rekening)

def uipRegisterObligasiApplyRow(uipRegisterObligasi, oRegisterObligasi):
  config = uipRegisterObligasi.UIDefList.Config

  if oRegisterObligasi.nama_obligasi in [None, '']:
    raise 'Kesalahan Register Obligasi','\nNama obligasi tidak terdefinisi.'

  nominal_beli = oRegisterObligasi.harga_pari * oRegisterObligasi.harga_beli / 100.0
  #if nominal_beli > min(oRegisterObligasi.dpkTersedia, oRegisterObligasi.nilaiMaksProporsi, oRegisterObligasi.nominalGiro):
  '''
  if nominal_beli > min(oRegisterObligasi.dpkTersedia, oRegisterObligasi.nilaiMaksProporsi):
    raise 'Kesalahan Register Obligasi','\nDana paket investasi tidak tersedia.'
  '''
  if oRegisterObligasi.harga_beli <= 0.0:
    raise 'Kesalahan Register Obligasi','\nHarga beli harus lebih besar dari nol.'

  if oRegisterObligasi.harga_pari <= 0.0:
    raise 'Kesalahan Register Obligasi','\nNilai pari harus lebih besar dari nol.'

  oRegisterObligasi.nominal = oRegisterObligasi.harga_pari
  oRegisterObligasi.user_id = config.SecurityContext.userid
  oRegisterObligasi.terminal_id = config.SecurityContext.GetSessionInfo()[1]

