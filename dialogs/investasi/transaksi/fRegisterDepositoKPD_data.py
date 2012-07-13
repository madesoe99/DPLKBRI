import sys, time, string
sys.path.append('c:/dafapp/dplk/script_modules')
sys.path.append('c:/dafapp/dplk/scripts/investasi/transaksi')
import moduleapi

def FormGeneralSetData(uideflist, auiname, apobjconst):
  config = uideflist.Config
  uipRegisterDeposito = uideflist.uipRegisterDeposito

  rec = uipRegisterDeposito.Dataset.AddRecord()
  rec.tgl_buka = config.Now()
  rec.nominal_pembukaan = 0.0
  rec.tanggal_register = config.Now()
  rec.jenisJatuhTempo = 1
  rec.nisbah = 0.0
  rec.biaya = 0.0
  rec.treatmentPokok = 'A'
  rec.kapitalisir_rollover = 'F'

  rec.user_id = config.SecurityContext.userid
  rec.terminal_id = config.SecurityContext.GetSessionInfo()[1]


  return retval

def uipRegisterDepositoApplyRow(uipRegisterDeposito, oRegisterDeposito):
  config = uipRegisterDeposito.UIDefList.Config

  if oRegisterDeposito.nominal_deposito < moduleapi.zero_approx:
    raise Exception, 'Kesalahan Register Deposito KPD' + 'Nilai nominal harus lebih besar dari nol.'

  if (oRegisterDeposito.nisbah < 0.0) or (oRegisterDeposito.nisbah >= 100.0):
    raise Exception, 'Kesalahan Register Deposito KPD' + 'Nilai nisbah harus lebih besar dari nol dan kurang dari 100.'

  if oRegisterDeposito.jenisJatuhTempo != 0:
    # bukan deposito on call
    oRegisterDeposito.tgl_jatuh_tempo = moduleapi.HitungJatuhTempo(config, oRegisterDeposito.tgl_buka, oRegisterDeposito.jenisJatuhTempo)
  else:
    if oRegisterDeposito.jmlHariOnCall <= 0:
      raise Exception, 'Kesalahan Register Deposito KPD' + 'Jumlah hari jatuh tempo on call harus lebih besar dari nol.'
    # deposito on call
    oRegisterDeposito.tgl_jatuh_tempo = moduleapi.HitungJatuhTempo(config, oRegisterDeposito.tgl_buka, oRegisterDeposito.jenisJatuhTempo, oRegisterDeposito.jmlHariOnCall)

  oRegisterDeposito.status = 'T'
  oRegisterDeposito.tanggal_register = config.Now()
  oRegisterDeposito.user_id = config.SecurityContext.userid
  oRegisterDeposito.terminal_id = config.SecurityContext.GetSessionInfo()[1]

