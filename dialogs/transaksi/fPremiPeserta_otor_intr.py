class fPremiPeserta_otor:
  def __init__(self, formObj, parentForm, mode):
    self.FormObj = formObj
    self.App = formObj.ClientApplication
    self.Mode = mode
  #--
  
  def bSetujuiOnClick(self, sender):
   if self.App.ConfirmDialog('Anda yakin Otorisasi Iuran Pendaftaran Peserta DPLK %s %s?' \
      % (self.uipPeserta.no_peserta, self.uipPeserta.nama_lengkap)):
      # sETUJUI transaksi
      self.Otorisasi(sender,'A')

  def bTolakOnClick(self, sender):
    if self.App.ConfirmDialog('Anda yakin membatalkan Iuran Pendaftaran Peserta DPLK %s %s?' \
      % (self.uipPeserta.no_peserta, self.uipPeserta.nama_lengkap)):
      # reject transaksi
      self.Otorisasi(sender,'R')
    
  def Form_OnFormShow(self, form, parameter):
    #cek mode
    if self.Mode == 'view':
      #mode view, disable button Approve dan Reject
      self.pButton_bSetujui.Enabled = 0
      self.pButton_bSetujui.Default = 0
      self.pButton_bTolak.Enabled = 0
      self.pButton_bBatal.Caption = '&Tutup'
      self.pButton_bBatal.Default = 1
      form.Caption = 'Lihat Detil Titipan Premi Peserta DPLK'
  #--

  def Otorisasi(self, button, mode):
      ph = self.App.CreateValues(\
        ['id_transaksi',self.uipTransaksi.ID_Transaksi],\
        ['mode',mode]
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
