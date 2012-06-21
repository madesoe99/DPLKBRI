import sys

def FormGeneralSetData(uideflist, uiname, objdata):
  config = uideflist.Config
  recLogin = uideflist.uipLogin.Dataset.AddRecord()
  recGiro = uideflist.uipGiro.Dataset.AddRecord()
  dsGroup = uideflist.uipCBLoginGroups.Dataset
  
  #set parameter login
  recLogin.isConnected = \
    config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING','NeedLoginCoreBanking')
  recLogin.ServerName = \
    config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING','ServerName')
  recLogin.AppName = \
    config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING','AppNameAsli')
  #recLogin.AppNameAsli = \
  #  config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING','AppName')

  #set giro rekening
  recGiro.GiroPremi = \
    config.SysVarIntf.GetStringSysVar('GIROCOREBANKING','GiroPremi')
  recGiro.GiroPendaftaran = \
    config.SysVarIntf.GetStringSysVar('GIROCOREBANKING','GiroPendaftaran')
  recGiro.GiroReturnInvestasi = \
    config.SysVarIntf.GetStringSysVar('GIROCOREBANKING','GiroReturnInvestasi')

  #set user groups
  usergroups = config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING', 'UserGroups')
  usergroups = usergroups.split(';')
  for i in range(len(usergroups)):
    recGroup = dsGroup.AddRecord()
    recGroup.GroupID = usergroups[i]
    recGroup.__SYSFLAG = 'N'

  return 0

def FormGeneralProcessData(uideflist, data):
  config = uideflist.Config
  recLogin = data.uipLogin.GetRecord(0)
  recGiro = data.uipGiro.GetRecord(0)
  dsGroup = data.uipCBLoginGroups

  try:
    #set parameter login
    config.SysVarIntf.SetStringSysVar('LOGINCOREBANKING','NeedLoginCoreBanking',\
      recLogin.isConnected)
    config.SysVarIntf.SetStringSysVar('LOGINCOREBANKING','ServerName',recLogin.ServerName)
    config.SysVarIntf.SetStringSysVar('LOGINCOREBANKING','AppName',str(recLogin.AppName).split('.')[0])
    config.SysVarIntf.SetStringSysVar('LOGINCOREBANKING','AppNameAsli',recLogin.AppName)

    #set giro rekening
    config.SysVarIntf.SetStringSysVar('GIROCOREBANKING','GiroPremi',\
      recGiro.GiroPremi)
    config.SysVarIntf.SetStringSysVar('GIROCOREBANKING','GiroPendaftaran',\
      recGiro.GiroPendaftaran)
    config.SysVarIntf.SetStringSysVar('GIROCOREBANKING','GiroReturnInvestasi',\
      recGiro.GiroReturnInvestasi)
      
    n = dsGroup.RecordCount
    groups = ''
    for i in range(n):
      group_id = dsGroup.GetRecord(i).GroupID
      if i == 0:
        groups = group_id
      else:
        groups = groups + ';' + group_id
    config.SysVarIntf.SetStringSysVar('LOGINCOREBANKING', 'UserGroups', groups)

  except:
    raise
    #raise '\nProses Error','\nPenyimpanan Koneksitas Core Banking gagal!'

  return 0
