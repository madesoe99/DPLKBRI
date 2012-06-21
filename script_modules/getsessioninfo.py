def GetSessionInfo(config, id):
  if (id >= 0) and (id <= 3):
    return config.SecurityContext.GetSessionInfo()[id]

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  sessioninfo = GetSessionInfo(config, parameter.FirstRecord.id)
  
  returnpacket.CreateValues(['sessioninfo',sessioninfo])

  return 1
