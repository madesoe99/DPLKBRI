
def mnuSuratAkseptasiClick(sender, context):
  app = context.OwnerForm.ClientApplication

  res = app.ExecuteScript('report/SuratAkseptasi',
    app.CreateValues(
      ['no_rekening',context.GetFieldValue('RekAsuransi.no_rekening')]
    )
  )

  app.DownloadItem(res.FirstRecord.filename,'v')

def mnuSuratTunggakanPremiClick(sender, context):
  app = context.OwnerForm.ClientApplication

  res = app.ExecuteScript('report/SuratTunggakanPremi',
    app.CreateValues(
      ['no_rekening',context.GetFieldValue('RekAsuransi.no_rekening')]
    )
  )

  app.DownloadItem(res.FirstRecord.filename,'v')

