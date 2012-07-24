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

    oR = config.CreatePObjImplProxy('RekInvDPLK')
    oR.Key = noRekening
    hasPassbook = oR.has_passbook; oR.has_passbook = 'T'
    noBukuLama = oR.no_seri_buku; oR.no_seri_buku = noBuku
     
    oB = config.CreatePObjImplProxy('MASTERBUKUDPLK')
    oB.Key = noBuku
    oB.status_buku = 'T'
     
    if hasPassbook == 'T':
      oHistBuku = config.CreatePObjImplProxy('HistoriBukuDPLK')
      oHistBuku.Key = noBukuLama
      oHistBuku.status = 'F'
     
    oH = config.CreatePObject('HistoriBukuDPLK')
    oH.branch_code = kode_cabang
    oH.no_peserta = noPeserta
    oH.no_rekening = noRekening
    oH.no_seri_buku = noBuku
    oH.tgl_input =  config.Now()
    oH.status = 'T'
    oH.user_id = userid
     
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