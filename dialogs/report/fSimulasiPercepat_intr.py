def FormShow(form, parameter):
  app = form.ClientApplication

  uipNoData = form.GetUIPartByName('uipNoData')
  uipNoData.Edit()
  uipNoData.tanggal_lahir      = app.ModDateTime.Now()
  uipNoData.tanggal_registrasi = app.ModDateTime.Now()
  uipNoData.biaya_administrasi = 5000
  uipNoData.biaya_pengelolaan = 1


def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipNoData = form.GetUIPartByName('uipNoData')

  res = app.ExecuteScript('report/simulasi_percepat',
    app.CreateValues(
      ['tanggal_lahir',uipNoData.tanggal_lahir]
      ,['tanggal_registrasi',uipNoData.tanggal_registrasi]
      ,['nama_lengkap',uipNoData.nama_lengkap]
      ,['iuran_bulanan',uipNoData.iuran_bulanan]
      ,['pengalihan_dana',uipNoData.pengalihan_dana]
      ,['kenaikan_iuran',uipNoData.kenaikan_iuran]
      ,['paket_investasi',uipNoData.paket_investasi]

      
    )
  )

  app.DownloadItem(res.FirstRecord.filename,'v')
  sender.ExitAction = 1
