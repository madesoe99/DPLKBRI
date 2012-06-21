def uipNasabahDPLKCorporateApplyRow(sender, oNasabahDPLKCorporate):
  config = sender.UIDefList.Config
  if (oNasabahDPLKCorporate.tgl_bayar_iuran < 1) or (oNasabahDPLKCorporate.tgl_bayar_iuran > 31):
    raise 'Kesalahan Nilai','Tanggal Bayar Iuran tidak valid'

  #raise str(config.SecurityContext.GetSessionID())
  #oNasabahDPLKCorporate.terminal_id

