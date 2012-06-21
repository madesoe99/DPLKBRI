def bExeClick(sender) :
  form = sender.OwnerForm
  app = form.ClientApplication
  uip = form.GetUIPartByName('uipReksadana')
  if uip.TglAwal==None or uip.TglAkhir==None:
    app.ShowMessage('PERINGATAN : Tanggal Awal / Akhir belum diisi')
    return
  if uip.TglAwal > uip.TglAkhir:
    app.ShowMessage('Tanggal awal tidak boleh lebih dari tanggal akhir.')
    return

  y, m, d = uip.TglAwal[:3]
  dateFrom = '%s/%s/%s' % (str(m).zfill(2),str(d).zfill(2),str(y))

  y, m, d = uip.TglAkhir[:3]
  tomorrowEndDate = app.ModDateTime.EncodeDate(y, m, d) + 1
  y, m, d = app.ModDateTime.DecodeDate(tomorrowEndDate)
  tmrw_dateUntil = '%s/%s/%s' % (str(m).zfill(2),str(d).zfill(2),str(y))

  qHist = form.GetPanelByName('qHistNAB')
  qHist.SetParameter('dateFrom', dateFrom)
  qHist.SetParameter('dateUntil_tmrw', tmrw_dateUntil)
  qHist.SetParameter('id_investasi', uip.id_investasi)

  qHist.DisplayData()

  qHist = form.GetPanelByName('qHistSubscribe')
  qHist.SetParameter('dateFrom', dateFrom)
  qHist.SetParameter('dateUntil_tmrw', tmrw_dateUntil)
  qHist.SetParameter('id_investasi', uip.id_investasi)

  qHist.DisplayData()
  
  qHist = form.GetPanelByName('qHistRedempt')
  qHist.SetParameter('dateFrom', dateFrom)
  qHist.SetParameter('dateUntil_tmrw', tmrw_dateUntil)
  qHist.SetParameter('id_investasi', uip.id_investasi)

  qHist.DisplayData()
