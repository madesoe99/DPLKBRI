def FormShow(form, parameter):
  uipNoData = form.GetUIPartByName('uipNoData')
  uipNoData.Edit()
  uipNoData.bulan = 1
  uipNoData.jenis = parameter.FirstRecord.jenis
  
  if uipNoData.jenis == 'T':
    # tahunan
    form.GetControlByName('pData.bulan').Visible = 0
    form.GetControlByName('pData.bulan').ControlCaption = ''
    form.Caption = 'Rekapitulasi Transaksi Tahunan'

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipNoData = form.GetUIPartByName('uipNoData')

  if uipNoData.jenis == 'T':
    # tahunan
    bulan = -999
  else:
    bulan = uipNoData.bulan

  tahun = uipNoData.tahun

  res = app.ExecuteScript('report/rekap_transaksi',\
    app.CreateValues(['bulan',bulan]\
      ,['tahun',tahun]\
    )\
  )

  app.DownloadItem(res.FirstRecord.filename,'v')
  sender.ExitAction = 1

