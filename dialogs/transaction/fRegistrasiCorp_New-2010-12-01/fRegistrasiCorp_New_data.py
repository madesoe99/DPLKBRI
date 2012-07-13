def FormGeneralSetData(uideflist, auiname, apobjconst):
  config = uideflist.Config
  uipRegEditNasabahDPLKCorporate = uideflist.uipRegEditNasabahDPLKCorporate

  rec = uipRegEditNasabahDPLKCorporate.Dataset.AddRecord()
  rec.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  rec.tanggal_register = config.Now()
  rec.user_id = config.SecurityContext.userid
  
  #set biaya daftar anggota sesuai default
  oP = config.CreatePObjImplProxy('Parameter')
  oP.Key = 'BESAR_BIAYA_DAFTAR'
  rec.biaya_daftar_anggota = oP.Numeric_Value

  #set parameter presisi angka float
  oP.Key = 'PRESISI_ANGKA_FLOAT'
  recP = uideflist.uipParameter.Dataset.AddRecord()
  recP.PRESISI_ANGKA_FLOAT = oP.Numeric_Value

  return 0

def uipRegEditNasabahDPLKCorporateApplyRow(sender, oData):
  uideflist = sender.UIDefList
  config = uideflist.Config
  #mode = sender.ActiveRecord.mode
  
  if oData.no_referensi in ['', None]:
    raise Exception, 'Registrasi Error' + 'Nomor referensi tidak terdefinisi.'

  if (oData.tgl_bayar_iuran < 1) or (oData.tgl_bayar_iuran > 31):
    raise Exception, 'Kesalahan Nilai' + 'Tanggal Bayar Iuran tidak valid'

  oData.tanggal_register = config.Now()

  if sender.ActiveRecord.mode == 'new':
    oData.operation_code = 'N'
  elif sender.ActiveRecord.mode == 'editdoc':
    # edit
    oData.operation_code = 'E'

