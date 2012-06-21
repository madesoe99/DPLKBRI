import sys, string, time
import com.ihsan.util.modman as modman
import com.ihsan.foundation.appserver as appserver

#sys.path.append('c:/dafapp/dplk/script_modules/')
#import moduleapi

moduleapi = modman.getModule(appserver.ActiveConfig, 'moduleapi')
#import rpdb2; rpdb2.start_embedded_debugger("000")

def FormEndSetData(uideflist, auiname, apobjconst):
  config = uideflist.Config

  try:
    #checking status dplk peserta
    uiCalled = uideflist.GetPClassUIByName(auiname)
    rec = uiCalled.ActiveRecord
    if auiname == 'uipMaster':
      no_peserta = uiCalled.ActiveRecord.no_peserta
    else:
      no_peserta = uiCalled.ActiveRecord.GetFieldByName('LNasabahDPLK.no_peserta')
      
    moduleapi.IsPesertaAktif(config, no_peserta)

    moduleapi.CheckRegCIFRestriction(uideflist, auiname, apobjconst)
    if uideflist.uipMaster.Dataset.RecordCount > 0:
      rec = uideflist.uipMaster.ActiveRecord
      moduleapi.CheckRegisterCIFUniq(config, rec.no_peserta, 'I')
  except:
    raise Exception, str(sys.exc_info()[1])

  #set parameter PRESISI_ANGKA_FLOAT
  recP = uideflist.uipParameter.Dataset.AddRecord()
  oP = config.CreatePObjImplProxy('Parameter')
  oP.Key = 'PRESISI_ANGKA_FLOAT'
  recP.PRESISI_ANGKA_FLOAT = oP.Numeric_Value

  oP.Key = 'MIN_JML_IURAN_PST'
  recP.MIN_JML_IURAN_PST = oP.Numeric_Value

  oP.Key = 'MIN_JML_IURAN_PK'
  recP.MIN_JML_IURAN_PK = oP.Numeric_Value

  oP.Key = 'IS_ONLY_MIN_JML_IURAN_PST'
  recP.IS_ONLY_MIN_JML_IURAN_PST = int(oP.Numeric_Value)

def uipRegisterCIFApplyRow(sender, oData):
  uideflist = sender.UIDefList
  config = uideflist.Config
  #mode = sender.ActiveRecord.mode

  if oData.no_referensi in ['', None]:
    raise 'Registrasi Error','Nomor referensi tidak terdefinisi.'

  oData.tanggal_register = config.Now()

