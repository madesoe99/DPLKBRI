def uipSahamSetData(uipSaham):
  uideflist = uipSaham.UIDefList
  config = uideflist.Config

  rec_inv = uipSaham.Dataset.GetRecord(0)
  rec_tpi = uideflist.uipPendapatanSaham.Dataset.GetRecord(0)

  oSaham = config.CreatePObjImplProxy('Saham')
  oSaham.Key = rec_inv.id_investasi

  rec_tpi.SetFieldByName('LSaham.id_investasi', oSaham.id_investasi)
  rec_tpi.SetFieldByName('LSaham.nama_Saham', oSaham.nama_Saham)
  rec_tpi.SetFieldByName('LSaham.tgl_buka', oSaham.tgl_buka)

  #rec_tpi.akum_LR = oSaham.akum_LR
  #rec_tpi.akum_piutangLR = oSaham.akum_piutangLR

  rec_tpi.SetFieldByName('LPihakKetiga.kode_pihak_ketiga',oSaham.LPihakKetiga.kode_pihak_ketiga)
  rec_tpi.SetFieldByName('LPihakKetiga.nama_pihak_ketiga',oSaham.LPihakKetiga.nama_pihak_ketiga)

  rec_tpi.SetFieldByName('LPaketInvestasi.kode_paket_investasi',oSaham.LRincianPaketInvestasi.LPaketInvestasi.kode_paket_investasi)
  rec_tpi.SetFieldByName('LPaketInvestasi.nama_paket_investasi',oSaham.LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi)

