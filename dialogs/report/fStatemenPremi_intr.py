def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipNoData = form.GetUIPartByName('uipNoData')

  y, m, d = uipNoData.dari_tanggal[:3]
  dari_tanggal = app.ModDateTime.EncodeDate(y, m, d)

  y, m, d = uipNoData.hingga_tanggal[:3]
  hingga_tanggal = app.ModDateTime.EncodeDate(y, m, d)

  res = form.CallServerMethod('CreateReport',\
    app.CreateValues(['no_peserta',uipNoData.GetFieldValue('LNasabahDPLK.no_peserta')]\
      ,['dari_tanggal',dari_tanggal]\
      ,['hingga_tanggal',hingga_tanggal]\
    )\
  )

  libDLClass = form.ClientApplication.GetClientClass("libDownload", "libDownload")
  libDL = libDLClass()
  libDL.previewStream(form.ClientApplication, res.Packet.GetStreamWrapper(0))

  sender.ExitAction = 1

