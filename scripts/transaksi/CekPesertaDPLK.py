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
    sSQL = "select * from rekinvdplk\
    where no_peserta = '%s'" % oN.no_peserta
    rSQL = config.CreateSQL(sSQL).RawResult
    #oR = config.CreatePObjImplProxy('RekeningDPLK')
    #oR.Key = oN.no_peserta
    #while not rSQL.Eof:
    tgl_pensiun = rSQL.tgl_pensiun
    if rSQL.status_DPLK == 'N':
      #status rekening non aktif
      config.SendDebugMsg('Non Aktif')
      NoPesertaExist = 2
    elif rSQL.status_DPLK == 'S':
      #status rekening suspend
      config.SendDebugMsg('Suspend')
      NoPesertaExist = 3
    elif rSQL.Status_Biaya_Daftar == 'F':
      #peserta belum membayar biaya pendaftaran
      config.SendDebugMsg('Belum membayar biaya pendaftaran')
      NoPesertaExist = 4
    elif config.ModLibUtils.Now() > config.ModLibUtils.EncodeDate(tgl_pensiun[0],\
      tgl_pensiun[1],tgl_pensiun[2]): 
      #tgl pensiun peserta sudah lewat
      config.SendDebugMsg('tgl pensiun sudah lewat')
      NoPesertaExist = 5
    elif rSQL.Is_Boleh_Debet == 'F':
      NoPesertaExist = 6
    elif rSQL.Is_Boleh_Debet == 'S': #boleh didebet dengan syarat tertentu
      NoPesertaExist = 7
  
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
  
  '''
  returnpacket.CreateValues(
    ['status', succeedStatus]
    , ['nbOfTrans', moduleapi.CountUnAuthTransaksiPeserta(config, noPeserta)]
    , ['persyaratan', GetPersyaratan(config, succeedStatus, noPeserta)]
  )
  '''
  
  returnpacket.CreateValues(
    ['status', succeedStatus]
    , ['nbOfTrans', 0]
    , ['persyaratan', '']
  )
  
  return 1