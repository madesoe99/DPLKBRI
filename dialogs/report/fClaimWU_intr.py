def FormShow(form, parameter):
  app = form.ClientApplication

  #uipNasabah.SetFieldValue('DanaPk', \
    #uipNasabah.GetFieldValue('LRekeningDPLK.akum_dana_iuran_pk'))



  uipNoData = form.GetUIPartByName('uipNoData')
  uipNoData.Edit()
  #uipNoData.tanggal_lahir      = app.ModDateTime.Now()
  uipNoData.tanggal_registrasi = app.ModDateTime.Now()

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipNoData = form.GetUIPartByName('uipNoData')

  res = app.ExecuteScript('report/ClaimWu',
    app.CreateValues(
      ['nama_lengkap', uipNoData.nama_lengkap]
      ,['tanggal_registrasi',uipNoData.tanggal_registrasi]


    )
  )

  app.DownloadItem(res.FirstRecord.filename,'v')
  sender.ExitAction = 1
