import string, time, sys
sys.path.append('c:/dafapp/dplk07/script_modules')

import moduleapi

def FormGeneralSetData(uideflist, uiname, objdata):
  config = uideflist.Config
  uipUserInfo = uideflist.uipUserInfo
  uipInput = uideflist.uipInput

  userID = config.SecurityContext.UserID
  #groupID = config.SecurityContext.GetUserInfo()[2]
  #tglPakai = time.localtime()[:3]
  tglPakai = config.ModLibUtils.DecodeDate(config.ModLibUtils.Now())

  lsGroup = moduleapi.GetUserGroupList(config, userID)

  recUserInfo = uipUserInfo.Dataset.AddRecord()
  recInput = uipInput.Dataset.AddRecord()
  
  #inisialisasi, status awal untuk user ADMINISTRATOR
  recUserInfo.isTeller = 0
  recUserInfo.isBackOffice = 0
  recUserInfo.isBackOfficeCabang = 0
  recUserInfo.UserIDOwner = ''
  recUserInfo.BranchCode = ''

  config.SendDebugMsg('lsGroup: '+ str(lsGroup))
  #cek user apakah termasuk group teller, BOD atau admin
  if string.upper(userID) == 'ROOT' or \
    'ADMIN' in lsGroup:
    config.SendDebugMsg('is1')
    #string.upper(str(groupID)) == 'ADMIN':
    #user root or admin: nothing to do, value like inisialization before
    pass
  elif moduleapi.IsUserTeller(config, config.SecurityContext.userID):
    #user 'teller'
    config.SendDebugMsg('is2')
    recUserInfo.isTeller = 1
    recUserInfo.UserIDOwner = userID
  elif 'BO' in lsGroup:
  #elif string.upper(str(groupID)) == 'BO':
    #user 'Backoffice Cabang'
    config.SendDebugMsg('is3')
    recUserInfo.isBackOfficeCabang = 1
    recUserInfo.BranchCode = config.SecurityContext.GetUserInfo()[4]
  elif 'BOD' in lsGroup:
  #else:
    #bukan ROOT, BO atau TELLER, artinya BOD user
    
    # Sementara di tutup
    #config.SendDebugMsg('is4')
    #recUserInfo.isBackOffice = 1
    #recUserInfo.UserIDOwner = userID

    #find another SuperUser (NoLimitLocation = 'T') except me & add to uipSuperUser
    #for constructing Transaction Batch OQL restriction
    #SuperUsers = moduleapi.FindSuperUserExceptMe(config, userID)
    #uipSU = uideflist.uipSuperUser
    #for user in SuperUsers:
      #recSU = uipSU.Dataset.AddRecord()
      #recSU.UserID = user
     pass
    # By Ade
    
  recInput.TanggalPakai = '%s/%s/%d' % (string.zfill(str(tglPakai[1]),2), \
    string.zfill(str(tglPakai[2]),2),tglPakai[0])
  recInput.isNeedType = 1
  recInput.isNotNeedTanggalPakai = 1
  recInput.isOpenOnly = 1
  recInput.isManualTransaction = 0
  
  if uiname != 'x' and objdata != 'x':
    #set batch type dan batch sub type bila ada, didapetin dari uiname & objdata
    oTB = config.CreatePObjImplProxy('TransactionBatch')
    oTB.Key = objdata

    recInput.BatchType = oTB.batch_type
    recInput.BatchSubType = oTB.batch_sub_type
    recInput.SetFieldName('LTransactionBatch.no_batch', oTB.no_batch)
    recInput.SetFieldName('LTransactionBatch.ID_TransactionBatch', oTB.ID_TransactionBatch)
  #else:
    #berbentuk 'x' dan 'x', maka batch type dan batch sub type akan diset di FormShow

  #cek pengguna ialah TELLER
  if recUserInfo.isTeller:
    isNeedLoginCoreBanking = config.SysVarIntf.GetStringSysVar('LOGINCOREBANKING', \
      'NeedLoginCoreBanking')
      
    if isNeedLoginCoreBanking == 'T':
      #user sudah login ke core banking
      #cek dulu apakah sudah ada core banking batch untuk hari ini
      oCBB = config.CreatePObjImplProxy('CoreBankingBatch')
      oCBB.SetKey('User_ID',userID)
      oCBB.SetKey('Tanggal',tglPakai[2])
      oCBB.SetKey('Bulan',tglPakai[1])
      oCBB.SetKey('Tahun',tglPakai[0])

      if oCBB.IsNull:
        #tidak ada core banking batch
        raise Exception, '\nPERINGATAN' + 'Batch Core Banking Aplikasi DPLK untuk hari ini '\
          'belum dibuat. Mohon buat terlebih dahulu.'

    #set langsung batch transaksi(tanpa harus lookup)
    uipBD = uideflist.uipBatchDefined
    tglPakai = '%d/%d/%d' % (tglPakai[0],tglPakai[1],tglPakai[2])

    sSQL = 'select t.ID_TRANSACTIONBATCH, t.NO_BATCH, t.TGL_USED, ' \
           't.BRANCH_CODE, t.BATCH_TYPE from dbo.TRANSACTIONBATCH t ' \
           'where t.USER_ID_OWNER = \'%s\' and t.TGL_USED = \'%s\' and ' \
           't.BATCH_STATUS = \'O\'' % (userID, tglPakai)
    rSQL = config.CreateSQL(sSQL).RawResult
    
    if rSQL.Eof:
      #batch transaksi tidak ditemukan
      raise Exception, '\nPERINGATAN' + '\n\nBatch DPLK untuk hari ini belum ada / tidak ditemukan! '\
        '\nHubungi Administrator agar membuatkan batch DPLK.'
    else:
      #batch transaksi ditemukan, simpan ketiganya (batch type 'RTP')
      rSQL.First()
      while not rSQL.Eof:
        recBD = uipBD.Dataset.AddRecord()

        recBD.ID_TransactionBatch = rSQL.ID_TransactionBatch
        recBD.no_batch = rSQL.no_batch
        recBD.tgl_used = config.ModLibUtils.EncodeDate(rSQL.tgl_used[0], \
          rSQL.tgl_used[1],rSQL.tgl_used[2])
        recBD.branch_code = rSQL.branch_code
        recBD.batch_type = rSQL.batch_type
        
        rSQL.Next()

  return 0
