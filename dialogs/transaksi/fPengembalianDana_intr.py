class fPengembalianDana:
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
  
  def bHitungClick(self, button):
    form = self.FormObject
    app = form.ClientApplication
    
    #cek total dana pengambilan manfaat
    if self.uipTransaksi.total_dana < self.uipParameter.PRESISI_ANGKA_FLOAT:
      self.FormObject.ShowMessage('Total Dana Peserta ialah 0! Untuk itu, tidak ada dana yang bisa ditarik')
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
    
    # biaya pencairan
    persenBiayaKembali = self.uipParameter.PERSEN_CAIR_KEMBALI_DANA
    self.uipHitung.biaya_pencairan = (persenBiayaKembali / 100) * self.uipHitung.saldo_jml_dana 
    
    # biaya pengelolaan dan biaya administrasi dihitung berdasarkan proporsi
    self.uipHitung.biaya_pengelolaan = self.uipParameter.proporsiBiaya * \
      (self.uipParameter.PERSEN_BIAYA_PENGELOLAAN / 100) * self.uipHitung.saldo_jml_dana
    self.uipHitung.biaya_administrasi = self.uipParameter.proporsiBiaya * \
      self.uipParameter.BIAYA_ADM_TAHUNAN 
    
    self.uipHitung.saldo_pengembalian = self.uipHitung.saldo_jml_dana - \
      self.uipHitung.biaya_pencairan - \
      self.uipHitung.biaya_pengelolaan - \
      self.uipHitung.biaya_administrasi
    
    #get informasi pajak
    #ph = form.CallServerMethod("GetNominalPajak", \
    #  app.CreateValues(['saldoPengembalian', self.uipHitung.saldo_pengembalian]))
    ph = form.CallServerMethod("GetNominalPajak", \
      app.CreateValues(['tglTransaksi', self.uipTransaksi.tgl_transaksi], \
      ['nomorRekening', self.uipRekening.no_rekening], \
      ['nomorPeserta', self.uipPeserta.no_peserta], \
      ['jumlahDanaKembali', self.uipHitung.saldo_pengembalian]))
    dsStatus = ph.packet.status
    recStatus = dsStatus.GetRecord(0)
    if recStatus.error_status:
      # show error message
      formObj.ShowMessage(recStatus.error_message)
    else:
      dsPajak = ph.Packet.pajak
      recPajak = dsPajak.GetRecord(0)
      self.uipHitung.pajak = recPajak.nominal_pajak

    self.uipHitung.dana_setelah_pajak = \
      self.uipHitung.saldo_pengembalian - self.uipHitung.pajak

    self.uipHitung.jenis_biaya_lain = self.uipTransaksi.jenis_biaya
    self.uipHitung.nominal_biaya_lain = self.uipTransaksi.biaya_lain
    
    self.uipHitung.dana_dikembalikan = self.uipHitung.dana_setelah_pajak - \
      self.uipHitung.nominal_biaya_lain  
    
    #set readonly all control page perhitungan
    self.pHitung.SetAllControlsReadOnly()
  
    #aktifkan button Simpan
    self.pButton_bSimpan.Enabled = 1
    
    #notify user atau pindah tab info perhitungan
    #form.ShowMessage('Silahkan lihat di Info Perhitungan.')
    self.MultiPages.ActivePageIndex = 2
  #--
  
  def bSimpanClick(self, button):
    form = self.FormObject
    
    #cek total dana pengambilan manfaat
    if self.uipTransaksi.total_dana < self.uipParameter.PRESISI_ANGKA_FLOAT:
      self.FormObject.ShowMessage('Total Dana Peserta ialah 0! Untuk itu, tidak ada dana yang bisa ditarik')
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