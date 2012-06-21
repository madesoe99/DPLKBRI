def bExeClick(sender) :
  form = sender.OwnerForm
  app = form.ClientApplication
  uipDepo = form.GetUIPartByName('uipDeposito')
  qHist = form.GetPanelByName('qHistori')
  if uipDepo.TglAwal==None or uipDepo.TglAkhir==None:
    app.ShowMessage('PERINGATAN : Tanggal Awal / Akhir belum diisi')
    return
  if uipDepo.TglAwal > uipDepo.TglAkhir:
    app.ShowMessage('Tanggal awal tidak boleh lebih dari tanggal akhir.')
    return

  y, m, d = uipDepo.TglAwal[:3]
  dateFrom = '%s/%s/%s' % (str(m).zfill(2),str(d).zfill(2),str(y))

  y, m, d = uipDepo.TglAkhir[:3]
  tomorrowEndDate = app.ModDateTime.EncodeDate(y, m, d) + 1
  y, m, d = app.ModDateTime.DecodeDate(tomorrowEndDate)
  tmrw_dateUntil = '%s/%s/%s' % (str(m).zfill(2),str(d).zfill(2),str(y))

  qHist.SetParameter('dateFrom', dateFrom)
  qHist.SetParameter('dateUntil_tmrw', tmrw_dateUntil)
  qHist.SetParameter('id_investasi', uipDepo.id_investasi)

  qHist.DisplayData()
