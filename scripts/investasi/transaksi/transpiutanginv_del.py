import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi

# hapus transaksi piutang investasi

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  id = parameter.FirstRecord.id

  oTransPiutangInvestasi = config.CreatePObjImplProxy('TransPiutangInvestasi')
  oTransPiutangInvestasi.Key = id

  config.BeginTransaction()
  try:
    oTransPiutangInvestasi.Delete()

    config.Commit()
  except:
    config.Rollback()
    raise

  return 1

