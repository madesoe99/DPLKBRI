import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi,TransactInv

def SetRealisasiReturn(config, oRealisasiReturn):
  # set nilai2 transaksi realisasi return

  oRealisasiReturn.isCommitted = 'T'
  oRealisasiReturn.tgl_otorisasi = config.Now()
  oRealisasiReturn.user_id_auth = config.SecurityContext.userid
  oRealisasiReturn.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]
  oRealisasiReturn.nama_investasi = oRealisasiReturn.LReksadana.nama_reksadana

def SetReksadanaValues(config, oRealisasiReturn):
  # set nilai2 reksadana
  
  oReksadana = oRealisasiReturn.LReksadana
  oReksadana.NAB_awal = oRealisasiReturn.NAB
  oReksadana.NAB = oRealisasiReturn.NAB
  oReksadana.unit_penyertaan = oRealisasiReturn.unit_penyertaan
  oReksadana.akum_LR += oRealisasiReturn.profit

  TransactInv.CreateRincianBagiHasil(config, oReksadana, oRealisasiReturn.profit)

def CreateHistNABReksadana(config, oRealisasiReturn):
  oHistNABReksadana = config.CreatePObject('HistNABReksadana')
  oHistNABReksadana.NAB = oRealisasiReturn.NAB
  oHistNABReksadana.tgl_penetapan = config.Now()
  oHistNABReksadana.LReksadana = oRealisasiReturn.LReksadana
  oHistNABReksadana.UserOto = config.SecurityContext.UserID
  oHistNABReksadana.TerminalOto = config.SecurityContext.InitIP


def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  id = parameter.FirstRecord.id

  oRealisasiReturn = config.CreatePObjImplProxy('RealisasiReturn')
  oRealisasiReturn.Key = id

  config.BeginTransaction()
  try:
    SetRealisasiReturn(config, oRealisasiReturn)
    SetReksadanaValues(config, oRealisasiReturn)
    CreateHistNABReksadana(config, oRealisasiReturn)

    config.Commit()
  except:
    config.Rollback()
    raise

  return 1

