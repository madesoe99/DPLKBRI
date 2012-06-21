import time, sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import batchutils
import com.ihsan.lib.trace as trace

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  try:
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
      succeedStatus = 1
      config.BeginTransaction()
      try:
        #masukkan Core Banking Batch yang baru ke dalam CoreBankingBatch
        oCBB = batchutils.GetBatch(config)

        config.Commit()
      except:
        config.Rollback()
        raise

  except:
    raise

  returnpacket.CreateValues(['status',succeedStatus])

  return 1
