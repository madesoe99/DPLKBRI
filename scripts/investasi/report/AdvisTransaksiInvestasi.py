import sys, time, os, string

def ConstructReport(config, nama_advis, sHeader, sData, inputer, oFile):
  nowDate = '%s-%s-%d' % (string.zfill(str(time.localtime()[2]),2),\
    string.zfill(str(time.localtime()[1]),2),time.localtime()[0])
  nowTime = '%s:%s:%s' % (string.zfill(str(time.localtime()[3]),2),\
    string.zfill(str(time.localtime()[4]),2),\
    string.zfill(str(time.localtime()[5]),2))

  #write file
  oFile.write('DPLK Bank Rakyat Indonesia')
  oFile.write('\nLembar Advis %s' % (nama_advis))
  oFile.write('\n========================================================================\n')
  lHeader = sHeader.split('|')
  lData = sData.split('|')
  for i in range(len(lHeader)):
    oFile.write('%-30s: %s\n' % (lHeader[i], lData[i]))
  #write file
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('\n         Inputer data           Checker           Approver')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('\n         %s' % inputer)
  oFile.write('\n')
  oFile.write('\n----------')
  oFile.write('\nTanggal pembuatan advis : %s %s' % (nowDate, nowTime))
  oFile.write('\nUser pembuat advis      : %s' % (config.SecurityContext.GetUserInfo()[1]))

def CreateAdvis(config, nama_advis, sHeader, sData, inputer):
  sBaseFileName = 'Advis_%s_%s.txt' % (nama_advis, str(config.Now()))
  sFileName = config.UserHomeDirectory + sBaseFileName
  oFile = open(sFileName, 'w')
  ConstructReport(config, nama_advis, sHeader, sData, inputer, oFile)
  oFile.close()
  
  #set file read-only
  os.chmod(sFileName,333)

  return sBaseFileName

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  rec = parameter.FirstRecord  
  sBaseFileName = CreateAdvis(config, rec.nama_advis, rec.sHeader, rec.sData, rec.inputer)
  
  #return packet
  recRes = returnpacket.CreateDataPacketStructure('filename:string')
  recRes.filename = sBaseFileName

  return 1
