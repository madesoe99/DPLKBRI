def uipReksadanaSetData(uipReksadana):
  uideflist = uipReksadana.UIDefList
  config = uideflist.Config

  rec_inv = uipReksadana.Dataset.GetRecord(0)
  rec_tpi = uideflist.uipPendapatanReksadana.Dataset.GetRecord(0)

  oReksadana = config.CreatePObjImplProxy('Reksadana')
  oReksadana.Key = rec_inv.id_investasi

  rec_tpi.SetFieldByName('LReksadana.id_investasi', oReksadana.id_investasi)
  rec_tpi.SetFieldByName('LReksadana.nama_reksadana', oReksadana.nama_reksadana)
  rec_tpi.SetFieldByName('LReksadana.tgl_buka', oReksadana.tgl_buka)

  #rec_tpi.akum_LR = oReksadana.akum_LR
  #rec_tpi.akum_piutangLR = oReksadana.akum_piutangLR

  rec_tpi.SetFieldByName('LPihakKetiga.kode_pihak_ketiga',oReksadana.LPihakKetiga.kode_pihak_ketiga)
  rec_tpi.SetFieldByName('LPihakKetiga.nama_pihak_ketiga',oReksadana.LPihakKetiga.nama_pihak_ketiga)

  rec_tpi.SetFieldByName('LPaketInvestasi.kode_paket_investasi',oReksadana.LRincianPaketInvestasi.LPaketInvestasi.kode_paket_investasi)
  rec_tpi.SetFieldByName('LPaketInvestasi.nama_paket_investasi',oReksadana.LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi)

