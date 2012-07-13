import sys, string, time
import com.ihsan.util.modman as modman
import com.ihsan.foundation.appserver as appserver

moduleapi = modman.getModule(appserver.ActiveConfig, 'moduleapi')

#sys.path.append('c:/dafapp/dplk07/script_modules/')
#import moduleapi
                       
def FormEndSetData(uideflist, auiname, apobjconst):
  config = uideflist.Config

  try:
    #checking status dplk peserta
    uiCalled = uideflist.GetPClassUIByName(auiname)
    if auiname == 'uipMaster':
      no_peserta = uiCalled.ActiveRecord.no_peserta      
      no_rekening = uiCalled.ActiveRecord.no_rekening      
    else:
      no_peserta = uiCalled.ActiveRecord.GetFieldByName('LNasabahDPLK.no_peserta')
      no_rekening = uiCalled.ActiveRecord.GetFieldByName('LRekeningDPLK.no_rekening')
    moduleapi.IsPesertaAktif(config, no_peserta)

    #cek usia peserta
    oR = config.CreatePObjImplProxy('RekInvDPLK')
    oR.Key = no_rekening
    if oR.status_asuransi == 'F' and moduleapi.GetUsiaPeserta(config, no_peserta) > 55.0:
      #peserta wasiat ummat hanya boleh dibawah 55 tahun
      keepGoingProcess = 0
      raise Exception,'\n\nPERINGATAN\nUntuk pendaftaran baru Asuransi, '\
      'usia yang diperbolehkan harus dibawah 55 tahun.'

    #checking yang lain
    moduleapi.CheckRegCIFRestriction(uideflist, auiname, apobjconst)
    if uideflist.uipMaster.Dataset.RecordCount > 0:
      rec = uideflist.uipMaster.ActiveRecord
      moduleapi.CheckRegisterCIFUniq(config, rec.no_peserta, 'U')
  except:
    raise Exception, str(sys.exc_info()[1])

def uipRegisterCIFApplyRow(sender, oData):
  uideflist = sender.UIDefList
  config = uideflist.Config
  #mode = sender.ActiveRecord.mode

  if oData.no_referensi in ['', None]:
    raise Exception, 'Registrasi Error' + 'Nomor referensi tidak terdefinisi.'

  oData.tanggal_register = config.Now()

