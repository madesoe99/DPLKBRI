def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipNoData = form.GetUIPartByName('uipNoData')

  no_peserta_awal = uipNoData.GetFieldValue('LNasabahDPLK_awal.no_peserta')
  no_peserta_akhir = uipNoData.GetFieldValue('LNasabahDPLK_akhir.no_peserta')

  res = app.ExecuteScript('report/saldo_iuran_pst',\
    app.CreateValues(\
      ['no_peserta_awal',no_peserta_awal]\
      ,['no_peserta_akhir',no_peserta_akhir]\
    )\
  )

  app.DownloadItem(res.FirstRecord.filename,'v')
  sender.ExitAction = 1

