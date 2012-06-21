import time

def CekAllowTransaction(config, userID):
  #cek global variabel apakah perlu cek user time zone
  isTimeZoneUsed = config.SysVarIntf.GetStringSysVar('TIMEZONE','UseTimeZone')
  if isTimeZoneUsed == 'T':
    #perlu cek user timezone
    #get user timezone from its branch location
    oUser = config.CreatePObjImplProxy('UserApp')
    oUser.Key = userID
    
    userTimeZone = oUser.LBranchLocation.Branch_Time_Zone    
    serverTimeZone = config.SysVarIntf.GetStringSysVar('TIMEZONE','TimeZoneServer')
    
    #ambil selisih waktu standar dari variabel global
    SelisihWIBWITA = config.SysVarIntf.GetIntSysVar('TIMEZONE','SelisihMenitBaratTengah')
    SelisihWIBWIT = config.SysVarIntf.GetIntSysVar('TIMEZONE','SelisihMenitBaratTimur')
    SelisihWITAWIT = config.SysVarIntf.GetIntSysVar('TIMEZONE','SelisihMenitTengahTimur')
    
    #ambil rentang waktu resmi di variabel global
    AwalJamKerja = config.SysVarIntf.GetIntSysVar('TIMEZONE','AwalJamKerja')
    AwalMenitKerja = config.SysVarIntf.GetIntSysVar('TIMEZONE','AwalMenitKerja')
    AkhirJamKerja = config.SysVarIntf.GetIntSysVar('TIMEZONE','AkhirJamKerja')
    AkhirMenitKerja = config.SysVarIntf.GetIntSysVar('TIMEZONE','AkhirMenitKerja')

    SelisihMenitWaktu = 0
    if userTimeZone != serverTimeZone:
      #berbeda zona waktu dengan server, cek selisih waktu dari global variable
      if serverTimeZone == 'B':
        if userTimeZone == 'TA':
          SelisihMenitWaktu = SelisihWIBWITA
        elif userTimeZone == 'T':
          SelisihMenitWaktu = SelisihWIBWIT
      elif serverTimeZone == 'TA':
        if userTimeZone == 'B':
          SelisihMenitWaktu = -SelisihWIBWITA
        elif userTimeZone == 'T':
          SelisihMenitWaktu = SelisihWITAWIT
      elif serverTimeZone == 'T':
        if userTimeZone == 'B':
          SelisihMenitWaktu = -SelisihWIBWIT
        elif userTimeZone == 'TA':
          SelisihMenitWaktu = -SelisihWITAWIT
          
    #konversi selisih menit ke dalam detik
    SelisihDetikWaktu = SelisihMenitWaktu * 60.0
    
    #dapatkan waktu user sekarang berbasis zona waktu user berada (format float)
    fUserTime = time.time() + SelisihDetikWaktu
    y,m,d,H,M,S,ms0,ms1,ms2 = time.localtime(fUserTime)
    
    #buat waktu jam resmi berbasis float
    fAwalWaktuKerja = time.mktime([y,m,d,AwalJamKerja,AwalMenitKerja,S,ms0,ms1,ms2])
    fAkhirWaktuKerja = time.mktime([y,m,d,AkhirJamKerja,AkhirMenitKerja,S,ms0,ms1,ms2])
    
    #config.SendDebugMsg('Selisih detik: '+str(SelisihDetikWaktu))
    #config.SendDebugMsg('Waktu server: '+str(time.asctime()))
    #config.SendDebugMsg('Waktu user: '+str(time.ctime(fUserTime)))
    #config.SendDebugMsg('Awal kerja: '+str(time.ctime(fAwalWaktuKerja)))
    #config.SendDebugMsg('Akhir kerja: '+str(time.ctime(fAkhirWaktuKerja)))
    
    #bandingkan float usertime dengan float waktu resmi
    if (fUserTime < fAwalWaktuKerja) or (fUserTime > fAkhirWaktuKerja):
      #user time menunjukkan diluar jam kerja resmi
      allowTransaction = 0
    else:
      #user time menunjukkan masih berada dalam rentang jam kerja resmi
      allowTransaction = 1
    
  else:
    #tidak perlu cek user timezone
    allowTransaction = 1
    
  return allowTransaction

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  userID = parameter.FirstRecord.userid
  
  try:
    allowTransaction = CekAllowTransaction(config, userID)      
  except:
    raise
  
  returnpacket.CreateValues(['allowtransaction',allowTransaction])

  return 1
