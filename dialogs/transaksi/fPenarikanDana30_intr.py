class fPenarikanDana30:
  def __init__(self, formObj, parentForm):
    pass
  #--

  def JenisBiaya_OnChange(self, cbJenisBiaya):
    index = self.pDataTransaksi_jenis_biaya.ItemIndex
    self.uipTransaksi.Edit()
    if index == 0:
      self.uipTransaksi.biaya_lain = self.uipParameter.BiayaSKN
    elif index == 1:
      self.uipTransaksi.biaya_lain = self.uipParameter.BiayaRTGS
  #--
  
  def JumlahTarik_OnExit(self, dbEdit):
    #cek masing-masing nominal penarikan iuran pekerja
    if self.uipTransaksi.jml_tarik_iuran_pk > self.uipTransaksi.batas_penarikan_pk:
      self.FormObject.ShowMessage('Input jumlah penarikan iuran pekerja melebihi batas penarikan iuran pekerja')
      return

    #cek masing-masing nominal penarikan iuran peserta
    if self.uipTransaksi.jml_tarik_iuran_pst > self.uipTransaksi.batas_penarikan_pst:
      self.FormObject.ShowMessage('Input jumlah penarikan iuran peserta melebihi batas penarikan iuran peserta')
      return

    #cek masing-masing nominal penarikan iuran tambahan
    if self.uipTransaksi.jml_tarik_iuran_tmb > self.uipTransaksi.batas_penarikan_tmb:
      self.FormObject.ShowMessage('Input jumlah penarikan iuran tambahan melebihi batas penarikan iuran tambahan')
      return

    self.uipTransaksi.Edit()
    self.uipTransaksi.jml_tarik = self.uipTransaksi.jml_tarik_iuran_pk + \
      self.uipTransaksi.jml_tarik_iuran_pst + self.uipTransaksi.jml_tarik_iuran_tmb
  #--
  
  def bHitungClick(self, button):
    form = self.FormObject
    app = form.ClientApplication
    
    #cek masing-masing nominal penarikan iuran pekerja
    if self.uipTransaksi.jml_tarik_iuran_pk > self.uipTransaksi.batas_penarikan_pk:
      self.FormObject.ShowMessage('Input jumlah penarikan iuran pekerja melebihi batas penarikan iuran pekerja')
      return

    #cek masing-masing nominal penarikan iuran peserta
    if self.uipTransaksi.jml_tarik_iuran_pst > self.uipTransaksi.batas_penarikan_pst:
      self.FormObject.ShowMessage('Input jumlah penarikan iuran peserta melebihi batas penarikan iuran peserta')
      return

    #cek masing-masing nominal penarikan iuran tambahan
    if self.uipTransaksi.jml_tarik_iuran_tmb > self.uipTransaksi.batas_penarikan_tmb:
      self.FormObject.ShowMessage('Input jumlah penarikan iuran tambahan melebihi batas penarikan iuran tambahan')
      return

    #cek masing-masing nominal penarikan total
    if self.uipTransaksi.jml_tarik < self.uipParameter.PRESISI_ANGKA_FLOAT:
      self.FormObject.ShowMessage('Silahkan isi nominal jumlah penarikan!')
      return

    # do hitung versi client
    self.uipHitung.saldo_iuran_pk = self.uipRekening.akum_iuran_pk
    self.uipHitung.saldo_iuran_pst = self.uipRekening.akum_iuran_pst
    self.uipHitung.saldo_iuran_tmb = self.uipRekening.akum_iuran_tmb
    self.uipHitung.saldo_pmb = self.uipRekening.akum_pmb_pk + \
      self.uipRekening.akum_pmb_pst + self.uipRekening.akum_pmb_tmb + \
      self.uipRekening.akum_pmb_psl
    self.uipHitung.saldo_psl = self.uipRekening.akum_psl
    
    self.uipHitung.saldo_jml_dana = self.uipHitung.saldo_iuran_pk + \
      self.uipHitung.saldo_iuran_pst + self.uipHitung.saldo_iuran_tmb + \
      self.uipHitung.saldo_pmb + self.uipHitung.saldo_psl
    
    self.uipHitung.saldo_iuran_awal = self.uipHitung.saldo_iuran_pk + \
      self.uipHitung.saldo_iuran_pst + self.uipHitung.saldo_iuran_tmb
    self.uipHitung.jml_tarik = self.uipTransaksi.jml_tarik
    
    self.uipHitung.biaya_tarik = self.uipParameter.PERSEN_BIAYA_TARIK_NORMAL / 100 * \
      self.uipHitung.saldo_pmb
    if self.uipHitung.biaya_tarik < self.uipParameter.MIN_BIAYA_TARIK:
      self.uipHitung.biaya_tarik = self.uipParameter.MIN_BIAYA_TARIK
    
    self.uipHitung.saldo_iuran_akhir = self.uipHitung.saldo_iuran_awal -\
      self.uipHitung.jml_tarik
      
    #get informasi pajak
    ph = form.CallServerMethod("GetNominalPajak", \
      app.CreateValues(['tglTransaksi', self.uipTransaksi.tgl_transaksi], \
      ['nomorRekening', self.uipRekening.no_rekening], \
      ['nomorPeserta', self.uipPeserta.no_peserta], \
      ['jumlahTarik', self.uipHitung.jml_tarik]))
    dsStatus = ph.packet.status
    recStatus = dsStatus.GetRecord(0)
    if recStatus.error_status:
      # show error message
      formObj.ShowMessage(recStatus.error_message)
    else:
      dsPajak = ph.Packet.pajak
      recPajak = dsPajak.GetRecord(0)
      self.uipHitung.pajak = recPajak.nominal_pajak

    self.uipHitung.jenis_biaya_lain = self.uipTransaksi.jenis_biaya
    self.uipHitung.nominal_biaya_lain = self.uipTransaksi.biaya_lain
    
    self.uipHitung.dana_diterima = self.uipHitung.jml_tarik - \
      self.uipHitung.pajak - self.uipHitung.nominal_biaya_lain  
    
    #set readonly all control page perhitungan
    self.pHitung.SetAllControlsReadOnly()
  
    #aktifkan button Simpan
    self.pButton_bSimpan.Enabled = 1
    
    #notify user
    form.ShowMessage('Silahkan lihat di Info Perhitungan.')
  #--
  
  def bSimpanClick(self, button):
    form = self.FormObject
    
    #cek masing-masing nominal penarikan iuran pekerja
    if self.uipTransaksi.jml_tarik_iuran_pk > self.uipTransaksi.batas_penarikan_pk:
      self.FormObject.ShowMessage('Input jumlah penarikan iuran pekerja melebihi batas penarikan iuran pekerja')
      return

    #cek masing-masing nominal penarikan iuran peserta
    if self.uipTransaksi.jml_tarik_iuran_pst > self.uipTransaksi.batas_penarikan_pst:
      self.FormObject.ShowMessage('Input jumlah penarikan iuran peserta melebihi batas penarikan iuran peserta')
      return

    #cek masing-masing nominal penarikan iuran tambahan
    if self.uipTransaksi.jml_tarik_iuran_tmb > self.uipTransaksi.batas_penarikan_tmb:
      self.FormObject.ShowMessage('Input jumlah penarikan iuran tambahan melebihi batas penarikan iuran tambahan')
      return

    #cek masing-masing nominal penarikan total
    if self.uipTransaksi.jml_tarik < self.uipParameter.PRESISI_ANGKA_FLOAT:
      self.FormObject.ShowMessage('Silahkan isi nominal jumlah penarikan!')
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