class fPengalihanDariDPLK:
  def __init__(self, formObj, parentForm):
    self.app = formObj.ClientApplication
    self.Input = self.app.GetClientClass("Inputan", "Inputan")()
  #--

  def bSimpanClick(self, button):
    form = self.FormObject
    
    #cek kode dplk dan nomor DPLK lain
    if self.uipTransaksi.GetFieldValue('LLDP.kode_dp') in (None,'') or \
      self.uipTransaksi.no_dplk_lain in (None,''):
      form.ShowMessage('Kode DPLK lain atau Nomor DPLK lain ' \
        'belum terisi, mohon diisi dahulu.')
      return

    #cek saldo pengalihan
    if (self.uipTransaksi.mutasi_iuran_pk in (None,'') or self.uipTransaksi.mutasi_iuran_pk < self.uipParameter.PRESISI_ANGKA_FLOAT) and \
      (self.uipTransaksi.mutasi_iuran_pst in (None,'') or self.uipTransaksi.mutasi_iuran_pst < self.uipParameter.PRESISI_ANGKA_FLOAT) and \
      (self.uipTransaksi.mutasi_iuran_tmb in (None,'') or self.uipTransaksi.mutasi_iuran_tmb < self.uipParameter.PRESISI_ANGKA_FLOAT) and \
      (self.uipTransaksi.mutasi_psl in (None,'') or self.uipTransaksi.mutasi_psl < self.uipParameter.PRESISI_ANGKA_FLOAT) and \
      (self.uipTransaksi.mutasi_pmb_pk in (None,'') or self.uipTransaksi.mutasi_pmb_pk < self.uipParameter.PRESISI_ANGKA_FLOAT) and \
      (self.uipTransaksi.mutasi_pmb_pst in (None,'') or self.uipTransaksi.mutasi_pmb_pst < self.uipParameter.PRESISI_ANGKA_FLOAT) and \
      (self.uipTransaksi.mutasi_pmb_tmb in (None,'') or self.uipTransaksi.mutasi_pmb_tmb < self.uipParameter.PRESISI_ANGKA_FLOAT) and \
      (self.uipTransaksi.mutasi_pmb_psl in (None,'') or self.uipTransaksi.mutasi_pmb_psl < self.uipParameter.PRESISI_ANGKA_FLOAT):
      form.ShowMessage('Semua saldo pengalihan tidak boleh kosong atau 0! Mohon untuk diisi')
      return
    #if self.Input.CekKet(form,self.uipTransaksi.keterangan) == 0:return
    
    if self.app.ConfirmDialog('Anda yakin Simpan transaksi Pengalihan Dari DPLK Lain peserta %s %s?' % (self.uipPeserta.no_peserta, self.uipPeserta.nama_lengkap)):
      pass
    else:
      return 0
    
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

  def OnEnter(self, sender):
    uip = self.uipTransaksi
    self.Input.OnEnter(sender,uip)

  def OnExit(self, sender):
    uip = self.uipTransaksi
    self.Input.OnExit(sender,uip)

