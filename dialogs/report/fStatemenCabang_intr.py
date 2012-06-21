class frmStatemenCabang:
  def __init__(self, formObject, parentForm):
    pass

  def btnOKClick(self, sender):
    form = self.FormObject
    app = form.ClientApplication
    uipNoData = form.GetUIPartByName('uipNoData')

#    y, m, d = uipNoData.dari_tanggal[:3]
#    dari_tanggal = app.ModDateTime.EncodeDate(y, m, d)

#    y, m, d = uipNoData.hingga_tanggal[:3]
#    hingga_tanggal = app.ModDateTime.EncodeDate(y, m, d)

    res = form.CallServerMethod('CreateReport',\
      app.CreateValues(['branch_code', uipNoData.GetFieldValue('LBranchLocation.branch_code')]\
        ,['periode', uipNoData.periode]\
        ,['tahun', uipNoData.tahun]\
        ,['tepi_atas', uipNoData.tepi_atas]\
        ,['tepi_bawah', uipNoData.tepi_bawah]\
        ,['tepi_kiri', uipNoData.tepi_kiri]\
        ,['baris_per_halaman', uipNoData.baris_per_halaman]\
        ,['isNasabahCorporateIncl', uipNoData.isNasabahCorporateIncl]\
      )\
    )
#        ,['dari_tanggal',dari_tanggal]\
#        ,['hingga_tanggal',hingga_tanggal]\
#      )\
#    )

    nbOfFiles = res.Packet.StreamWrapperCount
    if nbOfFiles > 1:
      app.ShowMessage('Statemen telah dibuat dalam %d file terpisah.' % (nbOfFiles))

    libDLClass = form.ClientApplication.GetClientClass("libDownload", "libDownload")
    libDL = libDLClass()
    for i in range(res.Packet.StreamWrapperCount):
      libDL.previewStream(form.ClientApplication, res.Packet.GetStreamWrapper(i))

    sender.ExitAction = 1

