import sys, string
sys.path.append('c:/dafapp/dplk07/script_modules')

import moduleapi

def CekNomorPeserta(config, noPeserta, Keterangan):

  userid = config.SecurityContext.userid
  kode_cabang = config.SecurityContext.GetUserInfo()[4]
  
  config.BeginTransaction()
  try:

     NoPesertaExist = 1

     oPending = config.CreatePObject('PendingAlkhairat')
     oPending.no_peserta = noPeserta
     oPending.keterangan = Keterangan
     oPending.tgl_input =  config.Now()
     oPending.flag = 'F'
     oPending.user_id = userid
     oPending.branch_code = kode_cabang

     config.Commit()
  except:
     config.Rollback()
     NoPesertaExist = 2
     raise

  config.SendDebugMsg('Selesai......')
  return NoPesertaExist

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  noPeserta = parameter.FirstRecord.nopeserta
  keterangan = parameter.FirstRecord.keterangan


  try:
    succeedStatus = CekNomorPeserta(config, noPeserta, keterangan)
      
  except:
    raise
  
  returnpacket.CreateValues(
    ['status', succeedStatus]
    , ['nbOfTrans', moduleapi.CountUnAuthTransaksiPeserta(config, noPeserta)]
  )

  return 1
