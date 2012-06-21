import sys, string
sys.path.append('c:/dafapp/dplk07/script_modules')

import moduleapi

def CekNomorPeserta(config, noBuku):

  userid = config.SecurityContext.userid
  
  config.SendDebugMsg('no buku :'+ str(noBuku))
  NoPesertaExist = 1

  oR = config.CreatePObjImplProxy('MasterBukuDPLK')
  oR.Key = noBuku

  if oR.IsNull:
    #objek Peserta DPLK tidak ditemukan: tidak terdaftar
     NoPesertaExist = 0

  return NoPesertaExist

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  noBuku = parameter.FirstRecord.nobuku

  try:
    succeedStatus = CekNomorPeserta(config, noBuku)
      
  except:
    raise
  
  returnpacket.CreateValues(
    ['status', succeedStatus]
    , ['nbOfTrans', moduleapi.CountUnAuthTransaksiPeserta(config, noBuku)]
  )

  return 1
