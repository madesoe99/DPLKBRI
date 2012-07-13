def uipRegisterCIFApplyRow(sender, oData):
  uideflist = sender.UIDefList
  config = uideflist.Config
  #mode = sender.ActiveRecord.mode

  #if oData.no_referensi in ['', None]:
  #  raise Exception, 'Registrasi Error' + 'Nomor referensi tidak terdefinisi.'

  oData.tanggal_register = config.Now()

