import time, sys

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)
  pathscripts = config.GetHomeDir()[:-1]+'scripts/longscripts/'
  
  #raise parameter.FirstRecord.execFile
  addpath, module= (parameter.FirstRecord.execFile).split('/')
  sys.path.append(pathscripts+addpath+'/')
  lib = __import__(module)

  app = config.AppObject
  app.ConCreate('status')
  lib.DAFLongScriptMain(config, parameter, config.SecurityContext.pid, module)

  return 1
