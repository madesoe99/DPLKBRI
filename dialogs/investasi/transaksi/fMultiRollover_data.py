import sys, time, string
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi

def FormGeneralSetData(uideflist, auiname, apobjconst):
  config = uideflist.Config
  uipNoData = uideflist.uipNoData

  nowDateTime = config.Now()

  rec = uipNoData.Dataset.AddRecord()
  rec.dateFrom = nowDateTime
  rec.dateUntil = nowDateTime
  rec.dateUntil_tmrw = nowDateTime + 1

  rec.user_id = config.SecurityContext.userid
  rec.terminal_id = config.SecurityContext.GetSessionInfo()[1]

  nowDateTup = config.ModDateTime.DecodeDate(nowDateTime)
  rec.nowDate = '%s/%s/%d' % (string.zfill(str(nowDateTup[1]),2), \
    string.zfill(str(nowDateTup[2]),2),nowDateTup[0])

  return 0

def uipRolloverDepositoApplyRow(uipRolloverDeposito, oRolloverDeposito):
  config = uipRolloverDeposito.UIDefList.Config
  uideflist = uipRolloverDeposito.UIDefList

  rec = uipRolloverDeposito.ActiveRecord

  if rec.proses in ['K', 'R']:
    if rec.proses == 'K':
      oRolloverDeposito.lakukan_kapitalisir = 'T'
      oRolloverDeposito.mutasi_debet = oRolloverDeposito.LDeposito.akum_piutangLR
    else:
      # rec.proses == 'R'
      oRolloverDeposito.lakukan_kapitalisir = 'F'
      oRolloverDeposito.mutasi_debet = 0.0

    oRolloverDeposito.mutasi_kredit = 0.0
    oRolloverDeposito.no_bilyet = oRolloverDeposito.LDeposito.no_bilyet
    oRolloverDeposito.mutasi_debet = oRolloverDeposito.LDeposito.akum_piutangLR
    oRolloverDeposito.mutasi_kredit = 0.0
    oRolloverDeposito.kode_jns_investasi = oRolloverDeposito.LDeposito.kode_jns_investasi
    oRolloverDeposito.kode_jenis_trinvestasi = 'F'
    oRolloverDeposito.user_id = config.SecurityContext.userid
    oRolloverDeposito.terminal_id = config.SecurityContext.GetSessionInfo()[1]
    oRolloverDeposito.isCommitted = 'F'
    
    moduleapi.CheckTransaksiInvestasiExclusive(config, oRolloverDeposito.id_investasi)

