class fPengambilanManfaatPensiun:
  def __init__(self, formObj, parentForm):
    self.app = formObj.ClientApplication
    self.Input = self.app.GetClientClass("Inputan", "Inputan")()
  #--

  def JenisBiaya_OnChange(self, cbJenisBiaya):
    index = self.pDataTransaksi_jenis_biaya.ItemIndex
    self.uipTransaksi.Edit()
    if index == 0:
      self.uipTransaksi.biaya_lain = self.uipParameter.BiayaSKN
    elif index == 1:
      self.uipTransaksi.biaya_lain = self.uipParameter.BiayaRTGS
    elif index == 2:
      self.uipTransaksi.biaya_lain = self.uipParameter.BiayaPindahBuku
  #--
  
  def JenisPenerimaanManfaatBeforeLookup(self, sender, linkui):
    self.uipTransaksi.Edit()
  
    #bersihkan dulu lookup LAhliWaris
    self.uipTransaksi.ClearLink('LAhliWaris')
  
    return 1
  #--
  def OnEnter(self, sender):
    uip = self.uipTransaksi
    self.Input.OnEnter(sender,uip)

  def OnExit(self, sender):
    uip = self.uipTransaksi
    self.Input.OnExit(sender,uip)
  
  def JenisPenerimaanManfaatAfterLookup(self, sender, linkui):
    #cek jenis penerimaan manfaat pensiun janda / anak
    if self.uipTransaksi.GetFieldValue('Ljenis_penerimaan_manfaat.kode_jns_manfaat') == 'J':
      self.pDataTransaksi.GetControlByName('LAhliWaris').Enabled = 1
    else:
      self.pDataTransaksi.GetControlByName('LAhliWaris').Enabled = 0
  #--
  
  def bHitungClick(self, button):
    form = self.FormObject
    app = form.ClientApplication
    
    #cek total dana pengambilan manfaat
    if self.uipTransaksi.total_dana < self.uipParameter.PRESISI_ANGKA_FLOAT:
      self.FormObject.ShowMessage('Total Dana Peserta ialah 0! Untuk itu, tidak ada dana yang bisa dicairkan')
      return

    #cek jenis penerimaan manfaat
    if self.uipTransaksi.GetFieldValue('Ljenis_penerimaan_manfaat.kode_jns_manfaat') in [None,'']:
      self.FormObject.ShowMessage('Mohon isi terlebih dahulu Jenis Penerimaan Manfaat')
      return

    #cek tanggal pensiun dipercepat dan jenis manfaat pensiun dipilih
    if self.uipTransaksi.tgl_transaksi < self.uipRekening.tgl_pensiun_dipercepat and \
      self.uipTransaksi.GetFieldValue('Ljenis_penerimaan_manfaat.kode_jns_manfaat') in ('B','D'):
      self.FormObject.ShowMessage('Peserta belum mencapai tanggal pensiun dipercepat')
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
    
    self.uipHitung.pengalihan_bwh1th = 0.0
    
    # biaya pencairan
    if self.uipTransaksi.isPengalihanKurangSetahun:
      #ada pengalihan dana mengendap kurang 1 tahun
      persenBiayaCair = self.uipParameter.PERSEN_CAIR_MANFAAT_KURANG_SETAHUN
    else:
      persenBiayaCair = self.uipParameter.PERSEN_CAIR_MANFAAT_UMUM
    self.uipHitung.biaya_pencairan = (persenBiayaCair / 100) * self.uipHitung.saldo_jml_dana 
    
    # biaya pengelolaan dan biaya administrasi dihitung berdasarkan proporsi
    self.uipHitung.biaya_pengelolaan = self.uipParameter.proporsiHari * \
      (self.uipParameter.PERSEN_BIAYA_PENGELOLAAN / 100 / 12) * self.uipHitung.saldo_jml_dana
    self.uipHitung.biaya_administrasi = self.uipParameter.BIAYA_ADM_TAHUNAN / 12 
    
    self.uipHitung.saldo_manfaat = self.uipHitung.saldo_jml_dana - \
      self.uipHitung.biaya_pencairan - \
      self.uipHitung.biaya_pengelolaan - \
      self.uipHitung.biaya_administrasi
    
    #get informasi pajak
    if self.uipTransaksi.isSkipPPh:
      self.uipHitung.pajak = 0.0
    else:
      ph = form.CallServerMethod("GetNominalPajak", \
        app.CreateValues(['saldoManfaat', self.uipHitung.saldo_manfaat]))
      dsStatus = ph.packet.status
      recStatus = dsStatus.GetRecord(0)
      if recStatus.error_status:
        # show error message
        formObj.ShowMessage(recStatus.error_message)
      else:
        dsPajak = ph.Packet.pajak
        recPajak = dsPajak.GetRecord(0)
        self.uipHitung.pajak = recPajak.nominal_pajak

    self.uipHitung.manfaat_setelah_pajak = \
      self.uipHitung.saldo_manfaat - self.uipHitung.pajak

    #PENENTUAN BESAR MANFAAT TUNAI DAN MANFAAT ANUITAS
    if self.uipTransaksi.isCekAturanMenkeu and \
      self.uipHitung.manfaat_setelah_pajak >= self.uipParameter.BATAS_MANFAAT_KENA_ANUITAS and \
      self.uipTransaksi.GetFieldValue('Ljenis_penerimaan_manfaat.kode_jns_manfaat') != 'J': 
      self.uipHitung.manfaat_tunai = self.uipHitung.manfaat_setelah_pajak * \
        (self.uipParameter.PERSEN_BATAS_TUNAI_MANFAAT / 100)  
      self.uipHitung.manfaat_anuitas = self.uipHitung.manfaat_setelah_pajak - \
        self.uipHitung.manfaat_tunai
    else: 
      self.uipHitung.manfaat_tunai = self.uipHitung.manfaat_setelah_pajak
      self.uipHitung.manfaat_anuitas = 0.0
    
    #cek % anuitas pilihan peserta jika semua dana diterima tunai
    if self.uipHitung.manfaat_anuitas < self.uipParameter.PRESISI_ANGKA_FLOAT:
      #semua dana diterima tunai, lihat % anuitas pilihan peserta
      self.uipHitung.manfaat_anuitas = (self.uipTransaksi.persen_anuitas_pilihan_peserta / 100) * \
        self.uipHitung.manfaat_tunai
      self.uipHitung.manfaat_tunai = self.uipHitung.manfaat_setelah_pajak - \
         self.uipHitung.manfaat_anuitas
    
    self.uipHitung.jenis_biaya_lain = self.uipTransaksi.jenis_biaya
    self.uipHitung.nominal_biaya_lain = self.uipTransaksi.biaya_lain
    
    self.uipHitung.manfaat_tunai_diterima = self.uipHitung.manfaat_tunai - \
      self.uipHitung.nominal_biaya_lain  
    
    #set readonly all control page perhitungan
    self.pHitung.SetAllControlsReadOnly()
  
    #aktifkan isian nama anuitas jika ada manfaat anuitas hasil hitung
    self.pDataTransaksi_nama_anuitas.ReadOnly = \
      self.uipHitung.manfaat_anuitas < self.uipParameter.PRESISI_ANGKA_FLOAT
    
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
      self.FormObject.ShowMessage('Total Dana Peserta ialah 0! Untuk itu, tidak ada dana yang bisa dicairkan')
      return

    #cek jenis penerimaan manfaat
    if self.uipTransaksi.GetFieldValue('Ljenis_penerimaan_manfaat.kode_jns_manfaat') in [None,'']:
      self.FormObject.ShowMessage('Mohon isi terlebih dahulu Jenis Penerimaan Manfaat')
      return

    #cek tanggal pensiun dipercepat dan jenis manfaat pensiun dipilih
    if self.uipTransaksi.tgl_transaksi < self.uipRekening.tgl_pensiun_dipercepat and \
      self.uipTransaksi.GetFieldValue('Ljenis_penerimaan_manfaat.kode_jns_manfaat') in ('B','D'):
      self.FormObject.ShowMessage('Peserta belum mencapai tanggal pensiun dipercepat')
      return

    #cek nama anuitas
    if self.uipHitung.manfaat_anuitas > self.uipParameter.PRESISI_ANGKA_FLOAT and \
      self.uipTransaksi.nama_anuitas in (None,''):
      self.FormObject.ShowMessage('Peserta ikut anuitas, mohon isi nama anuitas yang dipilih peserta')
      return

    if self.app.ConfirmDialog('Anda yakin Simpan transaksi pengambilan Manfaat Pensiun %s %s?' % (self.uipPeserta.no_peserta, self.uipPeserta.nama_lengkap)):
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