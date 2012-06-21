import sys
sys.path.append('c:/dafapp/dplk07/script_modules/')
import moduleapi

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  kode_paket_investasi = parameter.FirstRecord.kode_paket_investasi
  kode_jns_investasi = moduleapi.GetSingleRPI(config, kode_paket_investasi)
  if kode_jns_investasi == None:
    returnpacket.CreateValues(['kode_jns_investasi',''])
    return 1

  oRincianPaketInvestasi = config.CreatePObjImplProxy('RincianPaketInvestasi')
  oRincianPaketInvestasi.SetKey('kode_paket_investasi',kode_paket_investasi)
  oRincianPaketInvestasi.SetKey('kode_jns_investasi',kode_jns_investasi)

  returnpacket.CreateValues(\
    ['kode_jns_investasi',kode_jns_investasi],\
    ['nama_jns_investasi',oRincianPaketInvestasi.LJenisInvestasi.nama_jns_investasi]\
  )

  return 1

