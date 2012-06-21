class fPengalihanKeDPLK:
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
    
    #cek kode dplk lain
    if self.uipTransaksi.GetFieldValue('LLDP.kode_dp') in (None,''):
      form.ShowMessage('Kode DPLK lain atau Nomor DPLK lain ' \
        'belum terisi, mohon diisi dahulu.')
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
    
    self.uipHitung.biaya_pengelolaan = 0.0
    self.uipHitung.biaya_administrasi = self.uipParameter.BiayaADM
    self.uipHitung.biaya_pengalihan = (self.uipParameter.BiayaPindah / 100) * \
      self.uipHitung.saldo_jml_dana
      
    self.uipHitung.saldo_dana_dialihkan = self.uipHitung.saldo_jml_dana - \
      self.uipHitung.biaya_pengelolaan - self.uipHitung.biaya_administrasi - \
      self.uipHitung.biaya_pengalihan
    
    self.uipHitung.jenis_biaya_lain = self.uipTransaksi.jenis_biaya
    self.uipHitung.nominal_biaya_lain = self.uipTransaksi.biaya_lain
    
    self.uipHitung.dana_dialihkan = self.uipHitung.saldo_dana_dialihkan - \
      self.uipHitung.nominal_biaya_lain 
    
    
    #set readonly all control page perhitungan
    self.pHitung.SetAllControlsReadOnly()
  
    #aktifkan button Simpan
    self.pButton_bSimpan.Enabled = 1
    
    #notify user
    form.ShowMessage('Silahkan lihat di Info Perhitungan.')
  #--
  
  def bSimpanClick(self, button):
    form = self.FormObject
    
    #cek kode dplk lain
    if self.uipTransaksi.GetFieldValue('LLDP.kode_dp') in (None,''):
      form.ShowMessage('Kode DPLK lain atau Nomor DPLK lain ' \
        'belum terisi, mohon diisi dahulu.')
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