import sys, string
import com.ihsan.util.modman as modman
import com.ihsan.foundation.appserver as appserver

modman.loadStdModules(globals(),
  [
    "moduleapi"
  ]
)

#sys.path.append('c:/dafapp/dplk07/script_modules')
#import moduleapi

def CekNomorPeserta(config, noPeserta, noRekening, noBuku):

  userid = config.SecurityContext.userid
  kode_cabang = config.SecurityContext.GetUserInfo()[4]
  
  config.BeginTransaction()
  try:

     config.SendDebugMsg('no buku :'+ str(noBuku))
     NoPesertaExist = 1
     oN = config.CreatePObjImplProxy('NasabahDPLK')
     oN.Key = noPeserta

     config.SendDebugMsg('Ubah Status Ambil Buku')

     oR = config.CreatePObjImplProxy('RekInvDPLK')
     oR.Key = noRekening
     oR.no_seri_buku = noBuku

     oHistBuku = config.CreatePObjImplProxy('HistoriBukuDPLK')
     oHistBuku.key = oN.no_peserta
     oHistBuku.status = 'F'
     noBukuHist = oHistBuku.no_seri_buku
     
     oH = config.CreatePObject('HistoriBukuDPLK')
     oH.no_peserta = noPeserta
     oH.no_rekening = noRekening
     oH.no_seri_buku = noBuku
     oH.status = 'T'
     oH.tgl_input =  config.Now()
     oH.user_id = userid
     oH.branch_code = kode_cabang

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
  noRekening = parameter.FirstRecord.norekening
  noBuku = parameter.FirstRecord.nobuku


  try:
    succeedStatus = CekNomorPeserta(config, noPeserta, noRekening, noBuku)
      
  except:
    raise
  
  returnpacket.CreateValues(
    ['status', succeedStatus]
    , ['nbOfTrans', moduleapi.CountUnAuthTransaksiPeserta(config, noRekening)]
  )

  return 1