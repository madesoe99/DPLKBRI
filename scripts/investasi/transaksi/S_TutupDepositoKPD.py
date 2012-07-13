import sys

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)
  config.BeginTransaction()
  try:
    oDeposito = config.AccessPObject(parameter.FirstRecord.key)
    oDeposito.status = 'F'
    oDeposito.tgl_tutup = config.Now()
    config.Commit()
  except:
    config.Rollback()
    raise Exception, str(sys.exc_info()[1])
