class fCreateTransaksiHistoriGiro:

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

    if not res.FirstRecord.isExist:
      #belum ada HistoriGiroHarian untuk hari ini
      self.FormObject.ShowMessage('Histori Giro Harian tidak ditemukan! '\
        'Tidak diperkenankan membuat transaksi DPLK untuk riwayat transaksi Giro DPLK '\
        'untuk tanggal %d-%d-%d.' % (self.uipFilter.TanggalTransaksi[2],\
        self.uipFilter.TanggalTransaksi[1],self.uipFilter.TanggalTransaksi[0]))
      return
    elif res.FirstRecord.isAllTransactionProceed:
      #HistoriGiroHarian hari ini sudah dibuatkan transaksinya
      self.FormObject.ShowMessage('Histori Giro Harian sudah dibuat menjadi transaksi DPLK! '\
        'Tidak diperkenankan membuat ulang transaksi DPLK untuk riwayat transaksi Giro DPLK '\
        'untuk tanggal %d-%d-%d.' % (self.uipFilter.TanggalTransaksi[2],\
        self.uipFilter.TanggalTransaksi[1],self.uipFilter.TanggalTransaksi[0]))
      return

    try:
      if app.ConfirmDialog('Anda yakin akan membuat transaksi DPLK untuk riwayat transaksi Giro '\
        'DPLK tanggal %d-%d-%d?' % (self.uipFilter.TanggalTransaksi[2],\
        self.uipFilter.TanggalTransaksi[1],self.uipFilter.TanggalTransaksi[0])):

        #pid = app.ExecuteScriptTrackable('transaksi/L_CreateTransaksiHistoriGiro',\
        param =  app.CreateValues(['tglTransaksi',dtTanggalTransaksi],
          ['execFile','transaksi/L_CreateTransaksiHistoriGiro'])
        app.ExecuteScript('longscripts/ExecuteLongScript', param)
          
        #pcConsole.ConsoleFilterName = 'BuatTransaksiHistoriGiro_' + str(pid)
        sender.Enabled = sender.Default = 0
        sender.OwnerForm.GetControlByName('pButton.bCancel').Caption = '&Tutup'
        sender.OwnerForm.GetControlByName('pButton.bCancel').Default = 1

    finally:
      app = None
