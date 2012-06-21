import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  id = parameter.FirstRecord.id

  oTransLRInvestasi = config.CreatePObjImplProxy('TransLRInvestasi')
  oTransLRInvestasi.Key = id
  oInvestasi = oTransLRInvestasi.LInvestasi

  config.BeginTransaction()
  try:
    oTransLRInvestasi.isCommitted = 'T'
    oTransLRInvestasi.tgl_otorisasi = config.Now()
    oTransLRInvestasi.user_id_auth = config.SecurityContext.userid
    oTransLRInvestasi.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]
    oTransLRInvestasi.no_bilyet = oInvestasi.no_bilyet

    oInvestasi.akum_LR = oInvestasi.akum_LR + oTransLRInvestasi.mutasi_kredit
    oInvestasi.last_update = config.Now()

    config.Commit()
  except:
    config.Rollback()
    raise

  return 1

