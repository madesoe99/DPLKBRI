import os

def FormGeneralSetData(uideflist, uiname, objdata):
  config = uideflist.config
  uipNoData = uideflist.uipNoData

  recNoData = uipNoData.Dataset.AddRecord()
  try:
    #baca dari file login.message
    homeDir = config.GetHomeDir()
    loginMessageTextFile = config.SysVarIntf.GetStringSysVar('MESSAGING','LoginMessageTextFile')
    loginMessageFile = homeDir + loginMessageTextFile

    isiPesanLogin = ''
    if os.access(loginMessageFile, os.F_OK):
      file = open(loginMessageFile,'r')
      isiPesanLogin = file.read()
      file.close()

  except:
    isiPesanLogin = ''

  if isiPesanLogin:
    #isi global variabel tidak kosong
    recNoData.PesanLogin = isiPesanLogin

  return 0
  
def FormGeneralProcessData(uideflist, data):
  config = uideflist.Config
  uipNoData = uideflist.uipNoData
  
  try:
    rec = data.uipNoData.GetRecord(0)
    if rec.__SYSFLAG == 'M':
      #pesan login dimodifikasi, simpan pesan tersebut
      homeDir = config.GetHomeDir()
      loginMessageTextFile = config.SysVarIntf.GetStringSysVar('MESSAGING','LoginMessageTextFile')
      loginMessageFile = homeDir + loginMessageTextFile

      if os.access(loginMessageFile, os.F_OK):
        file = open(loginMessageFile,'w')
        file.write(rec.PesanLogin)
        file.close()

  except:
    raise Exception, '\nProses Error' + 'Penyimpanan Pesan Login Aplikasi gagal!'

  return 0
