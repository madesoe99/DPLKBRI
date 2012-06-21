def uipInvestasiSetData(uipInvestasi):
  uideflist = uipInvestasi.UIDefList
  config = uideflist.Config

  rec_inv = uipInvestasi.Dataset.GetRecord(0)
  rec_tpi = uideflist.uipTransPiutangLRInvestasi.Dataset.GetRecord(0)

  oInvestasi = config.CreatePObjImplProxy('Investasi')
  oInvestasi.Key = rec_inv.id_investasi

  rec_tpi.SetFieldByName('LInvestasi.id_investasi',oInvestasi.id_investasi)
  rec_tpi.no_bilyet = oInvestasi.no_bilyet
  #rec_tpi.akum_LR = oInvestasi.akum_LR
  #rec_tpi.akum_piutangLR = oInvestasi.akum_piutangLR

  rec_tpi.SetFieldByName('LPihakKetiga.kode_pihak_ketiga',oInvestasi.LPihakKetiga.kode_pihak_ketiga)
  rec_tpi.SetFieldByName('LPihakKetiga.nama_pihak_ketiga',oInvestasi.LPihakKetiga.nama_pihak_ketiga)

  rec_tpi.SetFieldByName('LPaketInvestasi.kode_paket_investasi',oInvestasi.LRincianPaketInvestasi.LPaketInvestasi.kode_paket_investasi)
  rec_tpi.SetFieldByName('LPaketInvestasi.nama_paket_investasi',oInvestasi.LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi)

  rec_tpi.SetFieldByName('LJenisInvestasi.kode_jns_investasi',oInvestasi.LRincianPaketInvestasi.LJenisInvestasi.kode_jns_investasi)
  rec_tpi.SetFieldByName('LJenisInvestasi.nama_jns_investasi',oInvestasi.LRincianPaketInvestasi.LJenisInvestasi.nama_jns_investasi)

