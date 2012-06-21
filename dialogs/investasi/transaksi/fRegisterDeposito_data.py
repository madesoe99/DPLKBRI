import sys, time, string
sys.path.append('c:/dafapp/dplk07/script_modules')
sys.path.append('c:/dafapp/dplk07/scripts/investasi/transaksi')
import moduleapi, paketinvinfo

def FormGeneralSetData(uideflist, auiname, apobjconst):
  config = uideflist.Config
  uipRegisterDeposito = uideflist.uipRegisterDeposito
  uipParameter = uideflist.uipParameter

  recP = uipParameter.Dataset.AddRecord()
  #set parameter nowDate
  tglPakai = time.localtime()[:3]
  recP.nowDate = '%s/%s/%d' % (string.zfill(str(tglPakai[1]),2), \
    string.zfill(str(tglPakai[2]),2),tglPakai[0])

  if auiname == 'new':
    #uipRegisterDeposito = uideflist.uipRegisterDeposito
    rec = uipRegisterDeposito.Dataset.AddRecord()
    #uipRegisterDeposito = uideflist.uipRegisterDeposito
    rec.tgl_buka = config.Now()
    rec.nominal = 0.0
    rec.tanggal_register = config.Now()
    rec.jenisJatuhTempo = 1
    rec.nisbah = 0.0
    rec.biaya = 0.0
    rec.treatmentPokok = 'A'
    rec.kapitalisir_rollover = 'F'
    rec.mode = auiname
    
    oMasterGiro = moduleapi.GetGiroBagiHasil(config)
    if oMasterGiro and not oMasterGiro.IsNull:
      rec.SetFieldByName('LMasterGiro.acc_giro', oMasterGiro.acc_giro)
      rec.SetFieldByName('LMasterGiro.no_giro', oMasterGiro.no_giro)

    rec.user_id = config.SecurityContext.userid
    rec.terminal_id = config.SecurityContext.GetSessionInfo()[1]
    
    KodeJnsInv = 'D'
    resSQLRPI = moduleapi.resSQLRPI(config, KodeJnsInv)
    if resSQLRPI.RecordCount == 1:
      # rincian paket investasi langsung diisi
      #rec.SetFieldByName('LRincianPaketInvestasi.kode_jns_investasi', 'A')
      #rec.SetFieldByName('LRincianPaketInvestasi.kode_paket_investasi', resSQLRPI.kode_paket_investasi)
      #rec.dpkPaket, rec.dpkTersedia, rec.nilaiMaksProporsi, rec.nominalGiro = paketinvinfo.getPaketInfo(config, resSQLRPI.kode_paket_investasi, 'A')
      #rec.nominal = min(rec.dpkTersedia, rec.nilaiMaksProporsi, rec.nominalGiro)

      uipRincianRegisterDeposito = uideflist.uipRincianRegisterDeposito
      rec = uipRincianRegisterDeposito.Dataset.AddRecord()
      rec.SetFieldByName('LRincianPaketInvestasi.kode_jns_investasi', KodeJnsInv)
      rec.SetFieldByName('LRincianPaketInvestasi.kode_paket_investasi', resSQLRPI.kode_paket_investasi)
      rec.SetFieldByName('LRincianPaketInvestasi.maks_proporsi', resSQLRPI.maks_proporsi or 0.0)
      rec.dpkPaket, rec.dpkInvExisting, rec.dpkTersedia, rec.nilaiMaksProporsi, rec.nominalGiro = paketinvinfo.getPaketInfo(config, resSQLRPI.kode_paket_investasi, KodeJnsInv)
      rec.nominal = min(rec.dpkTersedia, rec.nilaiMaksProporsi, rec.nominalGiro)

    retval = 0
  else:
    retval = 1

  return retval

def uipRegisterDepositoApplyRow(uipRegisterDeposito, oRegisterDeposito):
  config = uipRegisterDeposito.UIDefList.Config
  
  if oRegisterDeposito.kapitalisir_rollover == 'F' and oRegisterDeposito.LMasterGiro.IsNull :
     raise 'PERINGATAN','Nomor Rekening Pindah Buku belum dimasukkan'

  #if oRegisterDeposito.no_bilyet in [None, '']:
  #  raise 'Kesalahan Register Deposito','Nomor bilyet tidak terdefinisi.'

  #moduleapi.CheckNoBilyetAvl(config, oRegisterDeposito.no_bilyet)

  if oRegisterDeposito.nominal < moduleapi.zero_approx:
    raise 'Kesalahan Register Deposito','Nilai nominal harus lebih besar dari nol.'

  #if oRegisterDeposito.nominal > min(oRegisterDeposito.dpkTersedia, oRegisterDeposito.nilaiMaksProporsi):
  #  raise 'Kesalahan Register Deposito','\nNilai nominal tidak boleh lebih dari dpk yang tersedia dan nilai maksimum proprsi.'

  if (oRegisterDeposito.nisbah < 0.0) or (oRegisterDeposito.nisbah >= 100.0):
    raise 'Kesalahan Register Deposito','Nilai nisbah harus lebih besar dari nol dan kurang dari 100.'

  #if oRegisterDeposito.biaya < moduleapi.zero_approx:
  #  raise 'Kesalahan Register Deposito','Biaya tidak boleh kurang dari nol.'

  if oRegisterDeposito.jenisJatuhTempo != 0:
    # bukan deposito on call
    oRegisterDeposito.tgl_jatuh_tempo = moduleapi.HitungJatuhTempo(config, oRegisterDeposito.tgl_buka, oRegisterDeposito.jenisJatuhTempo)
  else:
    if oRegisterDeposito.jmlHariOnCall <= 0:
      raise 'Kesalahan Register Deposito','Jumlah hari jatuh tempo on call harus lebih besar dari nol.'
    # deposito on call
    oRegisterDeposito.tgl_jatuh_tempo = moduleapi.HitungJatuhTempo(config, oRegisterDeposito.tgl_buka, oRegisterDeposito.jenisJatuhTempo, oRegisterDeposito.jmlHariOnCall)

  oRegisterDeposito.user_id = config.SecurityContext.userid
  oRegisterDeposito.terminal_id = config.SecurityContext.GetSessionInfo()[1]

