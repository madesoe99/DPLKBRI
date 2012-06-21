import sys
sys.path.append('c:/dafapp/dplk07/script_modules')

import moduleapi

def GetPersyaratan(config, status, no_peserta):
  if status == 7:
      oN = config.CreatePObjImplProxy('NasabahDPLK')
      oN.Key = no_peserta
      persyaratan = oN.LNasabahDPLKCorporate.persyaratan
  else:
      persyaratan = ''

  return persyaratan

def CekNomorPeserta(config, noPeserta):
  oN = config.CreatePObjImplProxy('NasabahDPLK')
  oN.Key = noPeserta

  config.SendDebugMsg('masukkkkkkk')
  NoPesertaExist = 1
  if oN.IsNull:
    #objek Peserta DPLK tidak ditemukan: tidak terdaftar
    NoPesertaExist = 0
  else:
    #objek Peserta DPLK ada, cek status rekening
    oR = config.CreatePObjImplProxy('MasterBukuDPLK')
    oR.Key = oN.no_peserta
    if oR.has_pasbook == 'T':
      #status rekening non aktif
      config.SendDebugMsg('Sudah Ambil Buku')
      NoPesertaExist = 2

  config.SendDebugMsg('Selesai......')
  return NoPesertaExist

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  noPeserta = parameter.FirstRecord.nopeserta


  try:
    succeedStatus = CekNomorPeserta(config, noPeserta)
      
  except:
    raise
  
  returnpacket.CreateValues(
    ['status', succeedStatus]
  )

  return 1
