# File ini berisi API yang digunakan sebagai kakas untuk berbagai macam keperluan
# Isi yang sekarang tersedia:
# 1. LogFile - digunakan untuk membuat file .log

import os, time

def Logging(config, namaFile, pesanLog):
  logF = LogFile(config, namaFile)
  try:
    logF.WriteLog(pesanLog)  
  finally:
    logF.Close()

#
# LogFile: membuat file .log di folder dafapp/log 
#
class LogFile:

  def __init__(self, config, namaFile):
    self.Config = config
    self.LogFile = None
    
    #cek direktori log
    logDir = self.Config.GetHomeDir() + 'log\\'
    
    if not os.path.exists(logDir):
      #direktori log tidak ada, maka buatkan direktori log
      os.mkdir(logDir)

    pLogFile = logDir + namaFile + '.log'
  
    isAddLog = 0
    if os.access(pLogFile, os.F_OK):
      #TAMBAHKAN LOG-NYA SAJA
      isAddLog = 1
      
    if isAddLog:
      #tambahin isi log
      self.LogFile = open(pLogFile,'a')
      self.LogFile.write('\n\n-- %s --\n\n' % (time.asctime(time.localtime())))
    else:
      #buat file log baru
      self.LogFile = open(pLogFile,'w')

  ''' PRIVATE
  '''
  
  ''' PUBLIC
  '''   
  def WriteLog(self, stringLog):
    self.LogFile.write(stringLog)
    
  def Close(self):
    self.LogFile.close()
