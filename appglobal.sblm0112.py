import sys, string, os
import com.ihsan.net.messagecenterlib as netmessage
sys.path.append('c:/dafapp/dplk07/script_modules')

import moduleapi

def AfterSuccessfulLogin(config, reclogin, password):
  userID = config.SecurityContext.UserID
  userID = userID.upper()
  UserGroups = moduleapi.GetUserGroupList(config, userID)

  #cek kebutuhan koneksi CoreBanking
  isNeedLoginCoreBanking = config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING', \
    'NeedLoginCoreBanking')
    
  if isNeedLoginCoreBanking == 'F':
    if string.upper(userID) != 'ROOT': 
      try:
        #baca dari file login.message
        homeDir = config.GetHomeDir()
        warningMessageTextFile = config.SysVarIntf.GetStringSysVar('MESSAGING','WarningCoreBankingTextFile')
        warningMessageFile = homeDir + warningMessageTextFile
    
        isiPesanWarning = ''
        if os.access(warningMessageFile, os.F_OK):
          file = open(warningMessageFile,'r')
          isiPesanWarning = file.read()
          file.close()    
      except:
        isiPesanWarning = ''      
      reclogin.WarnUserLevel = 2
    else:
      #userid == ROOT
      reclogin.WarnUserLevel = 1
      isiPesanWarning = '\n\nSEGERA KONEKSIKAN KEMBALI DENGAN CORE BANKING!'
      
    reclogin.WarnUserMessage = isiPesanWarning

  gid = string.upper(config.SecurityContext.GetUserInfo()[2])  
  if isNeedLoginCoreBanking == 'T':
    CBLoginGroups = config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING', 'UserGroups')
    CBLoginGroups = CBLoginGroups.split(';')
    try:
      idx = CBLoginGroups.index(gid)
    except:
      idx = -1
      
    if idx >= 0:
      #langsung login ke Core Banking
      ServerName = config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING', 'ServerName')
      AppName = config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING', 'AppNameAsli')
      SessionID = AppName.split('.')[0] + userID
      try:
        config.AppObject.rlogin(ServerName, AppName, userID, password, SessionID)
      except:
        reclogin.WarnUserLevel = 2
        reclogin.WarnUserMessage = '\nAplikasi Liablilitas DPLK 2007 tidak bisa '\
          'terkoneksi dengan CoreBanking!\n\nSEGERA HUBUNGI ADMINISTRATOR DPLK dan JANGAN '\
          'LAKUKAN TRANSAKSI APAPUN!\n' \
          'Error info: ' + str(sys.exc_info()[1])
        return
      
  #assign appropriate menu for user
  if (string.upper(userID) not in ['ROOT','ADMIN']) and \
    ('ADMIN' not in UserGroups):
    # user non root/admin atau non grup Admin
    # otomatis dipilihkan menu yang sesuai

    if 'FM' in UserGroups:
      #cek apakah punya akses menu lain
      if len(UserGroups) == 1:
        #hanya punya akses ke menu investasi saja
        reclogin.autoinstallmenu = 1    
        reclogin.automenuname = 'Investasi'
    elif ('TELLER' in UserGroups) or ('CS' in UserGroups) or \
      ('BO' in UserGroups) or ('BOD' in UserGroups) or ('MRKT' in UserGroups):
      #cek apakah punya akses menu lain
      if 'FM' not in UserGroups:
        #hanya punya akses ke menu liabilitas saja
        reclogin.autoinstallmenu = 1
        reclogin.automenuname = 'Liabilitas'
  else:
    # user root/admin atau grup admin
    reclogin.MonServerIsAdmin = 1
        
  #register console untuk GLOBALMESSAGECENTER
  if gid in ['CS', 'TELLER']:
    reclogin.MONSERVERADDRESS = ''
  else: 
    netmessage.RegisterMessageCenter(config)

def BeforeLogout(config):
  #Clear SessionBLOB table for this session
  sessionID = config.SecurityContext.SessionID
  config.SendDebugMsg(str(sessionID))
  oqlstat = config.OQLEngine.CreateOQL('SELECT FROM SessionBLOB [SessionID=:SessionID] (Self);')
  oqlstat.SetParameterValueByName('SessionID', sessionID)
  oqlstat.ApplyParamValues()

  gid = string.upper(config.SecurityContext.GetUserInfo()[2])  
  config.BeginTransaction()
  try:
    oqlstat.Active = 1
    oqlres = oqlstat.RawResult
    while not oqlres.Eof:
      oSessionBLOB = oqlstat.SessionBLOB
      oBLOBData = oSessionBLOB.LBLOBData
      try:
        if not oBLOBData.IsNull:
          oBLOBData.DeleteData()
          oBLOBData.Delete()
      finally:
        oSessionBLOB.Delete()
      oqlres.Next()
    config.Commit()
  except:
    config.Rollback()
    raise
    
  #unregister console untuk GLOBALMESSAGECENTER
  if gid not in ['CS', 'TELLER']:
   netmessage.UnregisterMessageCenter(config)
