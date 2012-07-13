import sys, time, string
#sys.path.append('c:/dafapp/dplk07/script_modules/')
#import moduleapi
#import rpdb2; rpdb2.start_embedded_debugger("000")

import com.ihsan.foundation.appserver as appserver
import com.ihsan.util.modman as modman

modman.loadStdModules(globals(),
  [
    "moduleapi"
  ]
)

def FormEndSetData(uideflist, auiname, apobjconst):
  config = uideflist.Config

  try:
    uiCalled = uideflist.GetPClassUIByName(auiname)
    rec = uiCalled.ActiveRecord
    if auiname == 'uipMaster':
      no_peserta = uiCalled.ActiveRecord.no_peserta
      no_rekening = uiCalled.ActiveRecord.no_rekening
    else:
      no_peserta = uiCalled.ActiveRecord.GetFieldByName('LNasabahDPLK.no_peserta')
      no_rekening = uiCalled.ActiveRecord.GetFieldByName('LRekeningDPLK.no_rekening')
      
      keyRekInvDPLK = "PObj:RekInvDPLK#no_rekening=%s" % no_rekening
      uideflist.SetData('uipMaster', keyRekInvDPLK)
    
    moduleapi.IsPesertaAktif(config, no_peserta)
    moduleapi.CheckRegCIFRestriction(uideflist, auiname, apobjconst)
    
    uipRegisterCIF = uideflist.GetPClassUIByName("uipRegisterCIF")
    if uipRegisterCIF.DataSet.RecordCount == 0:
      rec = uideflist.uipMaster.ActiveRecord
      moduleapi.CheckRegisterCIFUniq(config, rec.no_peserta, 'S', no_rekening)      
  except:
    raise Exception, str(sys.exc_info()[1])

def uipRegisterCIFApplyRow(sender, oData):
  uideflist = sender.UIDefList
  config = uideflist.Config

  if oData.no_referensi in ['', None]:
    raise Exception,'\n\nRegistrasi Error\nNomor referensi tidak terdefinisi.'

  oData.tanggal_register = config.Now()