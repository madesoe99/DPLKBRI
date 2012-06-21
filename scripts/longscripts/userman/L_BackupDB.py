import os
import sys
import gzip

def Main(config, parameter, consoleID):
  pid = config.SecurityContext.pid
  rec = parameter.FirstRecord
  app = config.AppObject

  sJobName = 'Backup database to set name \"' + rec.backupName + '\". TaskID = ' + str(pid)
  #app.WriteConsole(sJobName + ': started\r\n')
  
  #fileLog = open(config.GetHomeDir()[:-1]+'trackedtasks/'+consoleID,'w')
  app.ConWriteln(sJobName + ': mulai berlangsung', monfilename)
  try:
    #app.CreateConsole(consoleID, 'progress')
    try:
      #app.SwitchDefaultConsole(consoleID)

      homeDir = config.GetHomeDir()
      listFile = homeDir + 'backup.lst'
      if not os.access(listFile, os.F_OK):
        raise 'Backup table list is not defined'
      tempFile = homeDir + 'database\\backups\\' + rec.backupName + '.tmp'
      targetFile = homeDir + 'database\\backups\\' + rec.backupName + '.backup'

      #progress = config.ProgressTracker
      #progress.ProgressLevel1()

      config.BackupDB(listFile, tempFile)
            
      #compressing file
      inF = open(tempFile, 'rb')
      s = inF.read()
      inF.close()      
            
      f = gzip.GzipFile(targetFile, 'wb')
      f.write(s)
      f.close()
      
      #deleting temporary file
      os.remove(tempFile)
             
      app.WriteConsole(sJobName + ': completed\r\n')
    finally:
      app.CloseConsole(consoleID)
  except:
    app.WriteConsole(sJobName + ': error\r\n' + str(sys.exc_info()[1]) + '\r\n')
    raise

  
def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)
  consoleID = 'stdprogress'
  Main(config, parameter, consoleID)


  return 1
  
def DAFLongScriptMain(config, parameter, pid, monfilename):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # pid: Process ID of this script
  # monfilename: Monitor file name to store status
  consoleID = 'stdprogress_' + str(pid)
  Main(config, parameter, consoleID)


  #return 1
