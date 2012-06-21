import time

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  try:
    #appCode berisi M (Ihsan Solusi) dan DP (aplikasi DPLK)
    appCode = 'MDP'
    userID = config.SecurityContext.UserID
    branchNo = config.SecurityContext.GetUserInfo()[4]
    y,m,d = time.localtime()[:3]
    
    #cek dulu apakah sudah ada core banking batch untuk hari ini
    oCBB = config.CreatePObjImplProxy('CoreBankingBatch')
    oCBB.SetKey('User_ID',userID)
    oCBB.SetKey('Tanggal',d)
    oCBB.SetKey('Bulan',m)
    oCBB.SetKey('Tahun',y)
    
    succeedStatus = -999
    if oCBB.IsNull:
      #core banking batch hari ini belum tersedia dalam CoreBankingBatch
      param = config.AppObject.CreateValues(['Code', appCode], ['BranchNo', branchNo], \
        ['UserID', userID])      
      sessionID = config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING', 'AppName') + \
        userID
  
      #remote eksekusi creating core banking batch
      ph = config.AppObject.rexecscript(sessionID,'remote/CreateBatch',param,1)
      
      succeedStatus = 1
      #raise str(ph.FirstRecord.ErrMessage)
      if not ph.FirstRecord.IsErr:
        config.BeginTransaction()
        try:
          #masukkan Core Banking Batch yang baru ke dalam CoreBankingBatch
          oCBB = config.CreatePObject('CoreBankingBatch')
          oCBB.User_ID = userID
          oCBB.Tanggal = d
          oCBB.Bulan = m
          oCBB.Tahun = y
          oCBB.No_Batch = ph.FirstRecord.BatchNo
          
          config.Commit()
        except:
          config.Rollback()
          raise
      else:
        succeedStatus = 0
      
  except:
    raise
  
  returnpacket.CreateValues(['status',succeedStatus])

  return 1
