def mnuCetakAdvisClick(sender, context):
  app = context.OwnerForm.ClientApplication
  uipH = context.OwnerForm.GetUIPartByName('uipHistoriPindahPaketInvestasi')

  #cetak advis
  if app.ConfirmDialog('Anda bermaksud membuat Advis Biaya Transaksi Pindah Paket?'):
    idTransaksi = uipH.GetFieldValue('historippi_id')

    try:
      sysContext = ''
      if context.OwnerForm.SystemContext != '':
        sysContext = context.OwnerForm.SystemContext + '://'

      res = app.ExecuteScript(sysContext + 'report/AdvisTransaksiPindahPaket', \
        app.CreateValues(['classtransaksi','BiayaAdmTransaksi'],\
        ['idHistori',uipH.historippi_id]))
      app.DownloadItem(res.FirstRecord.filename,'v')
    except:
      app = None
      raise
