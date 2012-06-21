def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  sBaseFileName = 'report1.htm'
  sFileName = config.UserHomeDirectory + sBaseFileName
  oFile = open(sFileName, 'w')

  oFile.write('<html>')
  oFile.write('</html>')
  oFile.close()

  recRes = returnpacket.CreateDataPacketStructure('filename:string')
  recRes.filename = sBaseFileName

  return 1

