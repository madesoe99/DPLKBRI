def FormShow(form, parameter):
  app = form.ClientApplication

  uipNoData = form.GetUIPartByName('uipNoData')
  uipNoData.Edit()
  uipNoData.tanggal_awal = app.ModDateTime.Now()
  uipNoData.tanggal_akhir = app.ModDateTime.Now()

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipNoData = form.GetUIPartByName('uipNoData')

  res = app.ExecuteScript('report/peserta_corporate',
    app.CreateValues(['kode_nasabah_corporate', uipNoData.GetFieldValue('LNasabahDPLKCorporate.kode_nasabah_corporate')]\
      ,['tanggal_awal',uipNoData.tanggal_awal]
      ,['tanggal_akhir',uipNoData.tanggal_akhir]
    )
  )

  app.DownloadItem(res.FirstRecord.filename,'v')
  sender.ExitAction = 1
