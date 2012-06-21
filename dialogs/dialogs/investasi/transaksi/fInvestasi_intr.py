def FormShow(form, parameter):
  uipInvestasi = form.GetUIPartByName('uipInvestasi')

  qTransPiutangInvestasi = form.GetPanelByName('qTransPiutangInvestasi')
  qTransPiutangInvestasi.SetParameter('id_investasi',uipInvestasi.id_investasi)
  qTransPiutangInvestasi.DisplayData()

  qTransPiutangLRInvestasi = form.GetPanelByName('qTransPiutangLRInvestasi')
  qTransPiutangLRInvestasi.SetParameter('id_investasi',uipInvestasi.id_investasi)
  qTransPiutangLRInvestasi.DisplayData()

  qTransLRInvestasi = form.GetPanelByName('qTransLRInvestasi')
  qTransLRInvestasi.SetParameter('id_investasi',uipInvestasi.id_investasi)
  qTransLRInvestasi.DisplayData()

