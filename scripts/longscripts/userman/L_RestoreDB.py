import os
import sys
import gzip

def DAFLongScriptMain(config, parameter, pid, monfilename):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # pid: Process ID of this script
  # monfilename: Monitor file name to store status

  rec = parameter.FirstRecord
  app = config.AppObject

  consoleID = 'stdprogress_' + str(pid)
  #app.CreateConsole(consoleID, 'progress')
  
  sJobName = 'Restore database. TaskID = ' + str(pid)
  #app.WriteConsole(sJobName + ': started\r\n')
  
  #fileLog = open(config.GetHomeDir()[:-1]+'trackedtasks/'+consoleID,'w')
  app.ConWriteln(sJobName + ': mulai berlangsung', monfilename)

  try:
    try:
      #app.SwitchDefaultConsole(consoleID)
      fileName = rec.serverFileName
      if not os.access(fileName, os.F_OK):
        raise ''
      
      #uncompressing file
      inF = gzip.GzipFile(fileName, 'rb')
      s = inF.read()
      inF.close()
      
      outF = open(fileName + '.tmp', 'wb')
      outF.write(s)
      outF.close()
      
      #progress = config.ProgressTracker
      config.RestoreDB(fileName + '.tmp')

      #deleting temporary file
      os.remove(fileName + '.tmp')

      #app.WriteConsole(sJobName + ': completed\r\n')
    
      app.ConWriteln(sJobName + ': selesai', monfilename)
    finally:
      #app.CloseConsole(consoleID)
      pass
  except:
    #app.WriteConsole(sJobName + ': error\r\n' + str(sys.exc_info()[1]) + '\r\n')
    raise


  #return 1

  
