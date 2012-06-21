import os

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)
  
  app = config.AppObject
  app.WriteConsole('Script S_CheckBackup begins\r\n')
  
  rec = parameter.FirstRecord
  homeDir = config.GetHomeDir()
  if str(rec.backupName) == '':
    raise 'Invalid backup name'
  fileName = homeDir + 'database\\backups\\' + rec.backupName + '.backup'
  returnpacket.CreateValues(['exist', os.access(fileName, os.F_OK)])
  
  app.WriteConsole('Script S_CheckBackup stopped\r\n')

  return 1
