class frmStatemenIndividu:
  def __init__(self, formObject, parentForm):
    pass

  def btnOKClick(self, sender):
    form = self.FormObject
    app = form.ClientApplication
    uipNoData = form.GetUIPartByName('uipNoData')

    if uipNoData.dari_tanggal in ['', None]:
      app.ShowMessage('Dari Tanggal mohon untuk diisi...')
      return
      
    if uipNoData.hingga_tanggal in ['', None]:
      app.ShowMessage('Hingga Tanggal mohon untuk diisi...')
      return
      
    y, m, d = uipNoData.dari_tanggal[:3]
    dari_tanggal = app.ModDateTime.EncodeDate(y, m, d)

    y, m, d = uipNoData.hingga_tanggal[:3]
    hingga_tanggal = app.ModDateTime.EncodeDate(y, m, d)

    res = form.CallServerMethod('CreateReport',\
      app.CreateValues(['no_rekening',uipNoData.GetFieldValue('no_rekening')]\
        ,['dari_tanggal',dari_tanggal]\
        ,['hingga_tanggal',hingga_tanggal]\
      )\
    )

    libDLClass = form.ClientApplication.GetClientClass("libDownload", "libDownload")
    libDL = libDLClass()
    libDL.previewStream(form.ClientApplication, res.Packet.GetStreamWrapper(0))

    sender.ExitAction = 1

