class fOtorisasiPenarikanDana30:
  def __init__(self, formObj, parentForm, mode):
    self.FormObj = formObj
    self.App = formObj.ClientApplication
    self.Mode = mode
    self.ket={'A':'Approve', 'R':'Tolak'}
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
      form.Caption = 'Lihat Detil Penarikan Dana Sebagian'
  #--

  def bReject_Click(self, button):
      phReturn = self.Proses_Click(button,'R')
      #process return

  def bApprove_Click(self, button):
      phReturn = self.Proses_Click(button,'A')
      #process return

  def Proses_Click(self, button,jenis):
    if self.App.ConfirmDialog('Anda yakin %s transaksi Penarikan peserta %s %s?' \
      % (self.ket[jenis], self.uipPeserta.no_peserta, self.uipPeserta.nama_lengkap)):
      # reject transaksi
      ph = self.App.CreateValues(\
        ['id_transaksi',self.uipTransaksi.ID_Transaksi],['mode',jenis])
      phReturn = self.App.ExecuteScript('transaksi/OtorisasiTransaksi', ph)

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