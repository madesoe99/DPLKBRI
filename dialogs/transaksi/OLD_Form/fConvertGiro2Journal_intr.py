class fConvertGiro2Journal:

  def __init__(self, formObj, parentForm):
    pass

  def FormAfterProcessServerData(self, form, opID, datapacket):
    #set form initialization value dengan hari kemarin
    self.uipFilter.TanggalTransaksi = \
      form.ClientApplication.ModDateTime.Now() - 1

    return 1

  def FormShow(self):
    rShow = self.FormContainer.Show()
    
  def bProsesClick(self, sender):
    app = self.FormObject.ClientApplication
    
    dtTanggalTransaksi = app.ModDateTime.EncodeDate(self.uipFilter.TanggalTransaksi[0],\
      self.uipFilter.TanggalTransaksi[1],self.uipFilter.TanggalTransaksi[2])

    #cek HistoriGiroHarian hari ini sudah ada atau belum
    res = app.ExecuteScript('transaksi/CekHistoriGiroHarian',\
      app.CreateValues(['tglTransaksi',dtTanggalTransaksi]))

    if res.FirstRecord.isExist:
      #sudah ada HistoriGiroHarian untuk hari ini
      self.FormObject.ShowMessage('Histori Giro Harian tanggal %d-%d-%d sudah ada! '\
        'Tidak diperkenankan membuat Histori Giro Harian lagi.' \
        % (self.uipFilter.TanggalTransaksi[2],self.uipFilter.TanggalTransaksi[1],\
        self.uipFilter.TanggalTransaksi[0]))
      return

    try:
      if app.ConfirmDialog('Anda yakin akan mengambil riwayat transaksi semua '\
        'Giro DPLK di Core Banking tanggal %d-%d-%d?' % (self.uipFilter.TanggalTransaksi[2],\
        self.uipFilter.TanggalTransaksi[1],self.uipFilter.TanggalTransaksi[0])):

        #pid = app.ExecuteScriptTrackable('transaksi/L_ConvertGiro2Journal',\
        param = app.CreateValues(['tglTransaksi',dtTanggalTransaksi],
          ['execFile','transaksi/L_ConvertGiro2Journal'])
        app.ExecuteScript('longscripts/ExecuteLongScript', param)  
        #pcConsole.ConsoleFilterName = 'GetHistoriGiro_' + str(pid)
        sender.Enabled = sender.Default = 0
        sender.OwnerForm.GetControlByName('pButton.bCancel').Caption = '&Tutup'
        sender.OwnerForm.GetControlByName('pButton.bCancel').Default = 1

    finally:
      app = None
