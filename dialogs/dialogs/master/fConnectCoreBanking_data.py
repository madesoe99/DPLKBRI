import sys

def FormGeneralSetData(uideflist, uiname, objdata):
  config = uideflist.Config
  recLogin = uideflist.uipLogin.Dataset.AddRecord()
  recGiro = uideflist.uipGiro.Dataset.AddRecord()
  
  #set parameter login
  recLogin.isConnected = \
    config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING','NeedLoginCoreBanking')
  recLogin.ServerName = \
    config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING','ServerName')
  recLogin.AppName = \
    config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING','AppName')
  recLogin.LoginName = \
    config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING','LoginName')

  #set giro rekening
  recGiro.GiroPremi = \
    config.SysVarIntf.GetStringSysVar('GIROCOREBANKING','GiroPremi')
  recGiro.GiroPendaftaran = \
    config.SysVarIntf.GetStringSysVar('GIROCOREBANKING','GiroPendaftaran')
  recGiro.GiroReturnInvestasi = \
    config.SysVarIntf.GetStringSysVar('GIROCOREBANKING','GiroReturnInvestasi')

  return 0

def FormGeneralProcessData(uideflist, data):
  config = uideflist.Config
  recLogin = data.uipLogin.GetRecord(0)
  recGiro = data.uipGiro.GetRecord(0)

  try:
    #set parameter login
    config.SysVarIntf.SetStringSysVar('LOGINCOREBANKING','NeedLoginCoreBanking',\
      recLogin.isConnected)
    config.SysVarIntf.SetStringSysVar('LOGINCOREBANKING','ServerName',recLogin.ServerName)
    config.SysVarIntf.SetStringSysVar('LOGINCOREBANKING','AppName',recLogin.AppName)
    config.SysVarIntf.SetStringSysVar('LOGINCOREBANKING','LoginName',recLogin.LoginName)

    #set giro rekening
    config.SysVarIntf.SetStringSysVar('GIROCOREBANKING','GiroPremi',\
      recGiro.GiroPremi)
    config.SysVarIntf.SetStringSysVar('GIROCOREBANKING','GiroPendaftaran',\
      recGiro.GiroPendaftaran)
    config.SysVarIntf.SetStringSysVar('GIROCOREBANKING','GiroReturnInvestasi',\
      recGiro.GiroReturnInvestasi)

  except:
    raise Exception, '\nProses Error' + '\nPenyimpanan Koneksitas Core Banking gagal!'

  return 0
