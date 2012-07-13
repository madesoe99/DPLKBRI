#def FormEndSetData(uideflist, auiname, apobjconst):
#  config = uideflist.Config
#  uipRegisterCIF = uideflist.uipRegisterCIF
#  uipMaster = uideflist.uipMaster
#
#  rec = uipMaster.Dataset.GetRecord(0)
#  oRekeningDPLK = config.CreatePObjImplProxy('RekeningDPLK')
#  oRekeningDPLK.Key = rec.no_peserta
#  if oRekeningDPLK.status_autodebet == 'F':


def uipRegisterCIFApplyRow(sender, oData):
  uideflist = sender.UIDefList
  config = uideflist.Config
  #mode = sender.ActiveRecord.mode

  #if oData.no_referensi in ['', None]:
  #  raise Exception, 'Registrasi Error' + 'Nomor referensi tidak terdefinisi.'

  oData.tanggal_register = config.Now()

