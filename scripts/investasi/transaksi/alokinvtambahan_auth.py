import com.ihsan.util.modman as modman
import transpiutanginv_auth

#moduleapi = modman.getModule(config, 'moduleapi')

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  id = parameter.FirstRecord.id

  config.BeginTransaction()
  try:
    transpiutanginv_auth.otorTransPiutangInvestasi(config, id)

    config.Commit()
  except:
    config.Rollback()
    raise

  return 1

