class fSendPeserta:

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

    #cek HistoriKirimPeserta hari ini sudah ada atau belum
    res = app.ExecuteScript('transaksi/CekHistoriKirimPeserta',\
      app.CreateValues(['tglTransaksi',dtTanggalTransaksi]))

    if res.FirstRecord.isExist:
      #sudah ada HistoriKirimPeserta untuk hari ini

      #self.FormObject.ShowMessage('Histori Kirim Peserta sudah ada! '\
      #  'Tidak diperkenankan mengirim ulang data peserta yang terdaftar '\
      #  'tanggal %d-%d-%d.' % (self.uipFilter.TanggalTransaksi[2],\
      #  self.uipFilter.TanggalTransaksi[1],self.uipFilter.TanggalTransaksi[0]))

      if not app.ConfirmDialog(
        'PERHATIAN:\nHistori Kirim Peserta tanggal %d-%d-%d sudah ada!\n'\
        'Kirim ulang data peserta?'\
        % (
           self.uipFilter.TanggalTransaksi[2]
           , self.uipFilter.TanggalTransaksi[1]
           , self.uipFilter.TanggalTransaksi[0]
        )
      ):
        return
    elif not app.ConfirmDialog('Anda yakin akan mengirim data peserta yang terdaftar tanggal '\
      '%d-%d-%d ke Core Banking?' % (self.uipFilter.TanggalTransaksi[2],\
      self.uipFilter.TanggalTransaksi[1],self.uipFilter.TanggalTransaksi[0])):
      return

    #pid = app.ExecuteScriptTrackable('transaksi/L_SendPeserta',\
    param =  app.CreateValues(['tglTransaksi',dtTanggalTransaksi],
      [execFile,'transaksi/L_SendPeserta'])
        
    app.ExecuteScript('longscripts/ExecuteLongScript', param)
    #pcConsole.ConsoleFilterName = 'SendPeserta_' + str(pid)
    sender.Enabled = sender.Default = 0
    sender.OwnerForm.GetControlByName('pButton.bCancel').Caption = '&Tutup'
    sender.OwnerForm.GetControlByName('pButton.bCancel').Default = 1

