import sys, string, time
import com.ihsan.util.modman as modman
import com.ihsan.foundation.appserver as appserver

moduleapi = modman.getModule(appserver.ActiveConfig, 'moduleapi')

#sys.path.append('c:/dafapp/dplk07/script_modules/')
#import moduleapi

def SetNasabahKorporatFlag(uideflist):
  config = uideflist.Config
  dsRegisterCIF = uideflist.uipRegisterCIF.Dataset
  if dsRegisterCIF.RecordCount > 0:
    recCIF = dsRegisterCIF.GetRecord(0)
    no_peserta = recCIF.GetFieldByName('LNasabahDPLK.no_peserta')
  else:
    recCIF = dsRegisterCIF.AddRecord()
    recmaster = uideflist.uipMaster.Dataset.GetRecord(0)
    no_peserta = recmaster.no_peserta

  oNasabahDPLK = config.CreatePObjImplProxy('NasabahDPLK')
  oNasabahDPLK.Key = no_peserta
  if oNasabahDPLK.LNasabahDPLKCorporate.IsNull:
    recCIF.nasabah_korporat = 0
  else:
    recCIF.nasabah_korporat = 1

def FormEndSetData(uideflist, auiname, apobjconst):
  config = uideflist.Config

  try:
    #checking status dplk peserta
    uiCalled = uideflist.GetPClassUIByName(auiname)
    if auiname == 'uipMaster':
      no_peserta = uiCalled.ActiveRecord.no_peserta
    else:
      no_peserta = uiCalled.ActiveRecord.GetFieldByName('LNasabahDPLK.no_peserta')
    moduleapi.IsPesertaAktif(config, no_peserta)

    moduleapi.CheckRegCIFRestriction(uideflist, auiname, apobjconst)
    if uideflist.uipMaster.Dataset.RecordCount > 0:
      rec = uideflist.uipMaster.ActiveRecord
      moduleapi.CheckRegisterCIFUniq(config, rec.no_peserta, 'A')
  except:
    raise

  SetNasabahKorporatFlag(uideflist)

def uipRegisterCIFApplyRow(sender, oData):
  uideflist = sender.UIDefList
  config = uideflist.Config
  #mode = sender.ActiveRecord.mode

  if oData.no_referensi in ['', None]:
    raise '\n\nRegistrasi Error','Nomor referensi tidak terdefinisi!'

  oData.tanggal_register = config.Now()

