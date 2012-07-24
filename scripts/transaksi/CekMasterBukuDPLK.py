import sys
import com.ihsan.util.modman as modman
import com.ihsan.foundation.appserver as appserver

modman.loadStdModules(globals(),
  [
    "moduleapi"
  ]
)

#sys.path.append('c:/dafapp/dplk07/script_modules')
#import moduleapi

def CekNomorBuku(config, noBuku):

  userid = config.SecurityContext.userid
  
  config.SendDebugMsg('no buku :'+ str(noBuku))
  NoBukuExist = 1

  oR = config.CreatePObjImplProxy('MasterBukuDPLK')
  oR.Key = noBuku

  if oR.IsNull:
    #objek buku DPLK tidak ditemukan: tidak terdaftar
    NoBukuExist = 0
  elif oR.status_buku == 'T':
    NoBukuExist = 2    

  return NoBukuExist

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  noBuku = parameter.FirstRecord.nobuku

  try:
    succeedStatus = CekNomorBuku(config, noBuku)
      
  except:
    raise
  
  returnpacket.CreateValues(
    ['status', succeedStatus]
    , ['nbOfTrans', moduleapi.CountUnAuthTransaksiPeserta(config, noBuku)]
  )

  return 1