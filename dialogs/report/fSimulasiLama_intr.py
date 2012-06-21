def FormShow(form, parameter):
  app = form.ClientApplication

  #uipNasabah.SetFieldValue('DanaPk', \
    #uipNasabah.GetFieldValue('LRekeningDPLK.akum_dana_iuran_pk'))



  uipNoData = form.GetUIPartByName('uipNoData')
  uipNoData.Edit()
  #uipNoData.tanggal_lahir      = app.ModDateTime.Now()
  uipNoData.SetFieldValue('biaya_administrasi', \
    uipNoData.GetFieldValue(5000))
  uipNoData.tanggal_registrasi = app.ModDateTime.Now()
  #uipNoData.biaya_administrasi = 5000
  uipNoData.biaya_pengelolaan = 1
  uipNoData.tingkat_investasi = 8

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipNoData = form.GetUIPartByName('uipNoData')

  res = app.ExecuteScript('report/simulasi_dplk',
    app.CreateValues(
      ['nama_lengkap', uipNoData.nama_lengkap]
      ,['tanggal_registrasi',uipNoData.tanggal_registrasi]
      ,['iuran_bulanan',uipNoData.iuran_bulanan]
      ,['kenaikan_iuran',uipNoData.kenaikan_iuran]
      ,['paket_investasi',uipNoData.paket_investasi]


    )
  )

  app.DownloadItem(res.FirstRecord.filename,'v')
  sender.ExitAction = 1
