class fPengalihanDariDPPK:
  def __init__(self, formObj, parentForm):
    pass
  #--

  def bSimpanClick(self, button):
    form = self.FormObject
    
    #cek kode dplk dan nomor DPLK lain
    if self.uipTransaksi.GetFieldValue('LLDP.kode_dp') in (None,'') or \
      self.uipTransaksi.no_dplk_lain in (None,''):
      form.ShowMessage('Kode DPPK lain atau Nomor DPPK lain ' \
        'belum terisi, mohon diisi dahulu.')
      return

    #cek saldo pengalihan
    if (self.uipTransaksi.mutasi_iuran_pk in (None,'') or self.uipTransaksi.mutasi_iuran_pk < self.uipParameter.PRESISI_ANGKA_FLOAT) and \
      (self.uipTransaksi.mutasi_iuran_pst in (None,'') or self.uipTransaksi.mutasi_iuran_pst < self.uipParameter.PRESISI_ANGKA_FLOAT) and \
      (self.uipTransaksi.mutasi_iuran_tmb in (None,'') or self.uipTransaksi.mutasi_iuran_tmb < self.uipParameter.PRESISI_ANGKA_FLOAT) and \
      (self.uipTransaksi.mutasi_psl in (None,'') or self.uipTransaksi.mutasi_psl < self.uipParameter.PRESISI_ANGKA_FLOAT):
      form.ShowMessage('Semua saldo pengalihan tidak boleh kosong atau 0! Mohon untuk diisi')
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