def FormEndSetData(uideflist, auiname, apobjconst):
  config = uideflist.Config
  uipRegEditNasabahDPLKCorporate = uideflist.uipRegEditNasabahDPLKCorporate
  uipNasabahDPLKCorporate = uideflist.uipNasabahDPLKCorporate

  if uipNasabahDPLKCorporate.Dataset.RecordCount > 0:
    # mode editdoc, inisialisasi data register
    recOrig = uipNasabahDPLKCorporate.Dataset.GetRecord(0)

    # cek operation_code data asal
    oNasabahDPLKCorporate = config.CreatePObjImplProxy('NasabahDPLKCorporate')
    oNasabahDPLKCorporate.Key = recOrig.kode_nasabah_corporate
    if oNasabahDPLKCorporate.operation_code == 'E':
      raise Exception, 'Peringatan' + '\nPerusahaan tersebut sedang dikoreksi.'

    rec = uipRegEditNasabahDPLKCorporate.Dataset.AddRecord()
    rec.user_id = config.SecurityContext.userid
    rec.terminal_id = config.SecurityContext.GetSessionInfo()[1]
    rec.tanggal_register = config.Now()
  elif (uipNasabahDPLKCorporate.Dataset.RecordCount <= 0) \
    and (uipRegEditNasabahDPLKCorporate.Dataset.RecordCount <= 0):
    # kemungkinan mode editdoc, tapi key yang dimasukan tidak valid
    raise Exception, 'Peringatan' + 'Data perusahaan tidak ditemukan.'

  #set parameter presisi angka float
  oP = config.CreatePObjImplProxy('Parameter')
  oP.Key = 'PRESISI_ANGKA_FLOAT'
  recP = uideflist.uipParameter.Dataset.AddRecord()
  recP.PRESISI_ANGKA_FLOAT = oP.Numeric_Value
    
def uipRegEditNasabahDPLKCorporateApplyRow(sender, oData):
  uideflist = sender.UIDefList
  config = uideflist.Config
  #mode = sender.ActiveRecord.mode
  
  if (oData.tgl_bayar_iuran < 1) or (oData.tgl_bayar_iuran > 31):
    raise Exception, 'Kesalahan Nilai' + 'Tanggal Bayar Iuran tidak valid'

  oData.tanggal_register = config.Now()

  if sender.ActiveRecord.mode == 'new':
    oData.operation_code = 'N'
  elif sender.ActiveRecord.mode == 'editdoc':
    # edit
    oData.operation_code = 'E'
    oOrigData = oData.LNasabahDPLKCorporate
    oOrigData.operation_code = 'E'

