import os

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)
  
  app = config.AppObject
  app.WriteConsole('Cek file upload...\r\n')
  
  rec = parameter.FirstRecord
  homeDir = config.GetHomeDir()
  try:
    if str(rec.uploadFileName) == '':
      raise '','Nama file upload invalid!'
  
    returnpacket.CreateValues(['exist', os.access(rec.uploadFileName, os.F_OK)])
  except:
    raise

  return 1
