import sys
sys.path.append('c:/dafapp/dplk07/script_modules')

import moduleapi

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  nbOfTrans = moduleapi.CountUnAuthTransaksiPeserta(
    config
    , parameter.FirstRecord.no_peserta
    , parameter.FirstRecord.excludeIDTrans
  )
  returnpacket.CreateValues(
    ['nbOfTrans', nbOfTrans]
  )

  return 1

