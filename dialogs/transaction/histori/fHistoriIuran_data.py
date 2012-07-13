#def FormEndSetData(uideflist, auiname, apobjconst):
#  config = uideflist.Config
#  uipRegisterCIF = uideflist.uipRegisterCIF
#
#  rec = uipRegisterCIF.Dataset.GetRecord(0)
#  if rec.mode == 'new':
#    rec.terminal_id = config.SecurityContext.GetSessionInfo()[1]

def uipRegisterCIFApplyRow(sender, oData):
  uideflist = sender.UIDefList
  config = uideflist.Config
  #mode = sender.ActiveRecord.mode

  #if oData.no_referensi in ['', None]:
  #  raise Exception, 'Registrasi Error' + 'Nomor referensi tidak terdefinisi.'

  oData.tanggal_register = config.Now()

