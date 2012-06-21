class fOtorisasiIuranPeserta:
  def __init__(self, formObj, parentForm, mode):
    self.FormObj = formObj
    self.App = formObj.ClientApplication
    self.Mode = mode
  #--

  def Form_OnFormShow(self, form, parameter):
    #cek mode
    if self.Mode == 'view':
      #mode view, disable button Approve dan Reject
      self.pButton_bApprove.Enabled = 0
      self.pButton_bApprove.Default = 0
      self.pButton_bReject.Enabled = 0
      self.pButton_bCancel.Caption = '&Tutup'
      self.pButton_bCancel.Default = 1
      form.Caption = 'Lihat Detil Pembayaran Iuran Peserta'
  #--

  def bReject_Click(self, button):
    if self.App.ConfirmDialog('Anda yakin membatalkan transaksi Iuran Peserta %s %s?' \
      % (self.uipPeserta.no_peserta, self.uipPeserta.nama_lengkap)):
      # reject transaksi
      ph = self.App.CreateValues(\
        ['id_transaksi',self.uipTransaksi.ID_Transaksi],\
        ['mode','R']
      )
      phReturn = self.App.ExecuteScript('transaksi/OtorisasiTransaksi', ph)

      #process return
      dsStatus = phReturn.Packet.status
      rec = dsStatus.GetRecord(0)
      if rec.error_status:
        # show error message
        self.FormObj.ShowMessage(rec.error_message)
        return
      else:
        button.OwnerForm.ResetAndClearData()
        button.ExitAction = 1
  #--