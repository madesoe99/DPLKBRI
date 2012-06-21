class fIuranPeserta:
  def __init__(self, formObj, parentForm):
    pass
  #--

  def bSimpanClick(self, button):
    form = self.FormObject
    
    #cek nominal iuran peserta
    if self.uipTransaksi.mutasi_iuran_pst in (None,'') or \
      self.uipTransaksi.mutasi_iuran_pst < self.uipParameter.PRESISI_ANGKA_FLOAT:
      form.ShowMessage('Nominal Iuran Peserta masih kosong atau 0! Mohon untuk diisi.')
      return
    
    form.CommitBuffer()
    phForm = form.GetDataPacket()
    phReturn = form.CallServerMethod("SimpanTransaksi", phForm)

    #process return
    dsStatus = phReturn.Packet.status
    rec = dsStatus.GetRecord(0)
    if rec.error_status:
      # show error message
      form.ShowMessage(rec.error_message)
      return
    else:
      #KODE LAIN BILA MEMERLUKAN PRINT SLIP
      button.ExitAction = 1
  #--