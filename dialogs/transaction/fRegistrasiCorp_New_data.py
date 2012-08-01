dictRiskFlag = {'L' : 'Low', 'H' : 'High' , 'M' : 'Moderate' , '' : ''}

def FormOnSetDataEx(uideflist, params):
  config = uideflist.Config
  uipRegEditNasabahDPLKCorporate = uideflist.uipRegEditNasabahDPLKCorporate

  rec = uipRegEditNasabahDPLKCorporate.Dataset.AddRecord()
  rec.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  rec.tanggal_register = config.Now()
  rec.tgl_bergabung = config.Now()
  rec.user_id = config.SecurityContext.userid
  rec.tgl_bayar_iuran = 1
  
  #set biaya daftar anggota sesuai default
  oP = config.CreatePObjImplProxy('Parameter')
  oP.Key = 'BESAR_BIAYA_DAFTAR'
  rec.biaya_daftar_anggota = oP.Numeric_Value

  #set parameter presisi angka float
  oP.Key = 'PRESISI_ANGKA_FLOAT'
  recP = uideflist.uipParameter.Dataset.AddRecord()
  recP.PRESISI_ANGKA_FLOAT = oP.Numeric_Value

  #set biaya daftar anggota sesuai default
  oP.Key = 'DEFAULT_NEGARA'
  rec.SetFieldByName("LNegara.kode_negara", oP.Numeric_Value)
  rec.SetFieldByName("LNegara.nama_negara", oP.Varchar_Value)
  
  # set risk flag negara
  oNegara = config.CreatePObjImplProxy('Negara')
  oNegara.key = oP.Numeric_Value  
  rec.SetFieldByName("LNegara.risk_flag", dictRiskFlag[oNegara.Risk_Flag or ''])

def uipRegEditNasabahDPLKCorporateApplyRow(sender, oData):
  uideflist = sender.UIDefList
  config = uideflist.Config
  #mode = sender.ActiveRecord.mode
  
  #if oData.no_referensi in ['', None]:
  #  raise Exception, 'Registrasi Error' + 'Nomor referensi tidak terdefinisi.'

  if (oData.tgl_bayar_iuran < 1) or (oData.tgl_bayar_iuran > 31):
    raise Exception, 'Kesalahan Nilai' + 'Tanggal Bayar Iuran tidak valid'

  oData.tanggal_register = config.Now()

  if sender.ActiveRecord.mode == 'new':
    oData.operation_code = 'N'
  elif sender.ActiveRecord.mode == 'editdoc':
    # edit
    oData.operation_code = 'E'