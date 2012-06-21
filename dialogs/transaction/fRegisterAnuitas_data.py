import sys
sys.path.append('c:/dafapp/dplk07/script_modules/')
import moduleapi

def FormEndSetData(uideflist, auiname, apobjconst):
  config = uideflist.Config

  moduleapi.CheckRegCIFRestriction(uideflist, auiname, apobjconst)
  if uideflist.uipMaster.Dataset.RecordCount > 0:
    rec = uideflist.uipMaster.ActiveRecord
    moduleapi.CheckRegisterCIFUniq(config, rec.no_peserta, 'N')

def uipRegisterCIFApplyRow(sender, oData):
  uideflist = sender.UIDefList
  config = uideflist.Config
  #mode = sender.ActiveRecord.mode

  if oData.no_referensi in ['', None]:
    raise 'Registrasi Error','Nomor referensi tidak terdefinisi.'
