# Get login message from Global Variabel
import os

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  try:
    #baca dari file login.message
    homeDir = config.GetHomeDir()
    loginMessageTextFile = config.SysVarIntf.GetStringSysVar('MESSAGING','LoginMessageTextFile')
    loginMessageFile = homeDir + loginMessageTextFile
    
    message = ''
    if os.access(loginMessageFile, os.F_OK):
      file = open(loginMessageFile,'r')
      message = file.read()
      file.close()
    
    returnpacket.CreateValues(['loginMessage',message])
  except:
    returnpacket.CreateValues(['loginMessage',''])

  return 1
