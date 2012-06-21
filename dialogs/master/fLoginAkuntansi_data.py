import sys, rotor

def FormGeneralSetData(uideflist, uiname, objdata):
  config = uideflist.Config
  recLogin = uideflist.uipLogin.Dataset.AddRecord()
  recSetting = uideflist.uipSetting.Dataset.AddRecord()

  #set parameter login
  recLogin.ServerName = config.SysVarIntf.GetStringSysVar('LOGINAKUNTANSI','ServerName')
  recLogin.AppName = config.SysVarIntf.GetStringSysVar('LOGINAKUNTANSI','AppName')
  recLogin.Session_Name = config.SysVarIntf.GetStringSysVar('LOGINAKUNTANSI','Session_Name')
  recLogin.UserID = config.SysVarIntf.GetStringSysVar('LOGINAKUNTANSI','UserID')

  #decrypt password sebelum assign ke recLogin
  cryptedPasswd = config.SysVarIntf.GetStringSysVar('LOGINAKUNTANSI','Password')
  rt = rotor.newrotor(recLogin.UserID, 19)
  recLogin.Password = rt.decrypt(cryptedPasswd)
  
  #set setting akuntansi
  recSetting.DefaultCurrency = \
    config.SysVarIntf.GetStringSysVar('SETTINGAKUNTANSI','DefaultCurrency')
  recSetting.BranchCodeTransaksi = \
    config.SysVarIntf.GetStringSysVar('SETTINGAKUNTANSI','BranchCodeTransaksi')
  recSetting.BranchCodePremi = \
    config.SysVarIntf.GetStringSysVar('SETTINGAKUNTANSI','BranchCodePremi')

  return 0

def FormGeneralProcessData(uideflist, data):
  config = uideflist.Config
  rec = data.uipLogin.GetRecord(0)
  recSetting = data.uipSetting.GetRecord(0)

  try:
    #set parameter login
    config.SysVarIntf.SetStringSysVar('LOGINAKUNTANSI','ServerName',rec.ServerName)
    config.SysVarIntf.SetStringSysVar('LOGINAKUNTANSI','AppName',rec.AppName)
    config.SysVarIntf.SetStringSysVar('LOGINAKUNTANSI','Session_Name',rec.Session_Name)
    config.SysVarIntf.SetStringSysVar('LOGINAKUNTANSI','UserID',rec.UserID)
    
    #encrypt password sebelum assign ke global variabel
    rt = rotor.newrotor(rec.UserID, 19)
    cryptedPasswd = rt.encrypt(rec.Password)
    config.SysVarIntf.SetStringSysVar('LOGINAKUNTANSI','Password',cryptedPasswd)
    
    #set setting akuntansi
    config.SysVarIntf.SetStringSysVar('SETTINGAKUNTANSI','DefaultCurrency',\
      recSetting.DefaultCurrency)
    config.SysVarIntf.SetStringSysVar('SETTINGAKUNTANSI','BranchCodeTransaksi',\
      recSetting.BranchCodeTransaksi)
    config.SysVarIntf.SetStringSysVar('SETTINGAKUNTANSI','BranchCodePremi',\
      recSetting.BranchCodePremi)

  except:
    raise '\nProses Error','Penyimpanan Login Aplikasi Akuntansi gagal!'

  return 0
