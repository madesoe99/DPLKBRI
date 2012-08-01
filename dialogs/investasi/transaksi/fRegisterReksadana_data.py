import sys, time, string

'''sys.path.append('c:/dafapp/dplk07/script_modules')
sys.path.append('c:/dafapp/dplk07/scripts/investasi/transaksi')
import moduleapi, paketinvinfo'''
import com.ihsan.util.modman as modman
modman.loadStdModules(globals(), 
  [
    "moduleapi",
    "scripts#investasi.transaksi.paketinvinfo"
  ]
)

def FormGeneralSetData(uideflist, auiname, apobjconst):
  config = uideflist.Config
  uipRegisterReksadana = uideflist.uipRegisterReksadana
  uipParameter = uideflist.uipParameter

  recP = uipParameter.Dataset.AddRecord()
  #set parameter nowDate
  tglPakai = time.localtime()[:3]
  recP.nowDate = '%s/%s/%d' % (string.zfill(str(tglPakai[1]),2), \
    string.zfill(str(tglPakai[2]),2),tglPakai[0])

  if auiname == 'new':
    rec = uipRegisterReksadana.Dataset.AddRecord()
    uipRegisterReksadana = uideflist.uipRegisterReksadana
    rec.tgl_buka = config.Now()
    rec.nominal = 0.0
    rec.tanggal_register = config.Now()
    rec.mode = auiname
    
    rec.SetFieldByName('LSubJenisInv.kode_subjns_LRInvestasi', 'RKS')
    rec.SetFieldByName('LSubJenisInv.deskripsi', 'Reksadana')
    
    rec.biaya = 0.0
    rec.unit_penyertaan = 0.0
    rec.NAB_awal = 0.0

    rec.user_id = config.SecurityContext.userid
    rec.terminal_id = config.SecurityContext.GetSessionInfo()[1]
    
    '''KodeJnsInv= 'R'
    resSQLRPI = moduleapi.resSQLRPI(config, KodeJnsInv)
    if resSQLRPI.RecordCount == 1 :
      # rincian paket investasi langsung diisi
      rec.SetFieldByName('LRincianPaketInvestasi.kode_jns_investasi', KodeJnsInv)
      rec.SetFieldByName('LRincianPaketInvestasi.kode_paket_investasi', resSQLRPI.kode_paket_investasi)
      rec.maks_proporsi = resSQLRPI.maks_proporsi or 0.0
      rec.dpkPaket, rec.dpkInvExisting, rec.dpkTersedia, rec.nilaiMaksProporsi, rec.nominalGiro = paketinvinfo.getPaketInfo(config, resSQLRPI.kode_paket_investasi, KodeJnsInv)
      rec.nominal = min(rec.dpkTersedia, rec.nilaiMaksProporsi)'''

    retval = 0
  else:
    retval = 1

  return retval

def uipRegisterReksadanaSetData(uipRegisterReksadana):
  config = uipRegisterReksadana.UIDefList.Config
  rec = uipRegisterReksadana.Dataset.GetRecord(0)
#
  if rec.GetFieldByName('LRincianPaketInvestasi.kode_paket_investasi') not in (None, '') :
    oRincianPaketInvestasi = config.CreatePObjImplProxy('RincianPaketInvestasi')
    oRincianPaketInvestasi.SetKey('kode_paket_investasi',rec.GetFieldByName('LRincianPaketInvestasi.kode_paket_investasi'))
    oRincianPaketInvestasi.SetKey('kode_jns_investasi',rec.GetFieldByName('LRincianPaketInvestasi.kode_jns_investasi'))
    rec.maks_proporsi = oRincianPaketInvestasi.maks_proporsi
#
#  oPaketInvestasi = oRincianPaketInvestasi.LPaketInvestasi
#  rec.SetFieldByName('LPaketInvestasi.kode_paket_investasi',oPaketInvestasi.kode_paket_investasi)
#  rec.SetFieldByName('LPaketInvestasi.nama_paket_investasi',oPaketInvestasi.nama_paket_investasi)

def uipRegisterReksadanaApplyRow(uipRegisterReksadana, oRegisterReksadana):
  config = uipRegisterReksadana.UIDefList.Config

  if oRegisterReksadana.nama_reksadana in [None, '']:
    raise Exception, 'Kesalahan Register Reksadana' + 'Nama reksadana tidak terdefinisi.'

  if oRegisterReksadana.nominal < 0.000001:
    raise Exception, 'Kesalahan Register Reksadana' + 'Nilai investasi harus lebih besar dari nol.'
  '''
  if oRegisterReksadana.nominal > min(oRegisterReksadana.dpkTersedia, oRegisterReksadana.nilaiMaksProporsi):
  #if oRegisterReksadana.nominal > min(oRegisterReksadana.dpkTersedia, oRegisterReksadana.nilaiMaksProporsi, oRegisterReksadana.nominalGiro):
    raise Exception, 'Kesalahan Register Reksadana' + '\nDana paket investasi tidak tersedia.'
  '''
  if oRegisterReksadana.NAB_awal <= 0.0:
    pass#raise Exception, 'Kesalahan Register Reksadana' + 'Nilai harga beli harus lebih besar dari nol.'

  oRegisterReksadana.NAB = oRegisterReksadana.NAB_awal
  oRegisterReksadana.user_id = config.SecurityContext.userid
  oRegisterReksadana.terminal_id = config.SecurityContext.GetSessionInfo()[1]

