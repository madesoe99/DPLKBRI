class fRegistrasi:
  def __init__(self, formObj, parentForm):
    #self.formObj, self.app = formObj, formObj.ClientApplication
    self.gReady = 0
    if parentForm != None:
      self.parentForm = parentForm
    else:
      self.parentForm = None
  #--

  def Show(self, mode):
    app = self.FormObject.ClientApplication
    
    self.FormShow(self.FormObject, mode)
    self.FormContainer.Show()

  def ResetAlamatSuratValue(self, uipart):
    uipart.alamat_surat_jalan = \
    uipart.alamat_surat_jalan2 = \
    uipart.alamat_surat_rtrw = \
    uipart.alamat_surat_kelurahan = \
    uipart.alamat_surat_kecamatan = \
    uipart.alamat_surat_kota = \
    uipart.alamat_surat_propinsi = \
    uipart.alamat_surat_kode_pos = \
    uipart.alamat_surat_telepon = \
    uipart.alamat_surat_telepon2 = None

    uipart.SetFieldValue('LASPropinsi.kode_propinsi', None)
    uipart.SetFieldValue('LASPropinsi.nama_propinsi', None)
    uipart.SetFieldValue('LASKota.kode_kota', None)
    uipart.SetFieldValue('LASKota.nama_kota', None)
    uipart.SetFieldValue('LASKecamatan.kode_kecamatan', None)
    uipart.SetFieldValue('LASKecamatan.nama_kecamatan', None)
    
  def ResetAlamatKantorValue(self, uipart):
    uipart.nama_perusahaan = None
    uipart.alamat_kantor_jalan = None
    uipart.alamat_kantor_kode_pos = None
    uipart.alamat_kantor_kelurahan = None
    uipart.alamat_kantor_kecamatan = None
    uipart.alamat_kantor_kota = None
    uipart.alamat_kantor_propinsi = None
    uipart.alamat_kantor_telepon = None
    uipart.alamat_kantor_telepon2 = None
  
    uipart.SetFieldValue('LAKPropinsi.kode_propinsi', None)
    uipart.SetFieldValue('LAKPropinsi.nama_propinsi', None)
    uipart.SetFieldValue('LAKKota.kode_kota', None)
    uipart.SetFieldValue('LAKKota.nama_kota', None)
    uipart.SetFieldValue('LAKKecamatan.kode_kecamatan', None)
    uipart.SetFieldValue('LAKKecamatan.nama_kecamatan', None)
  
    uipart.SetFieldValue('LKepemilikan.kode_pemilikan',None)
    uipart.SetFieldValue('LKepemilikan.keterangan',None)

    uipart.SetFieldValue('LJenisUsaha.kode_jenis_usaha',None)
    uipart.SetFieldValue('LJenisUsaha.nama_jenis_usaha',None)

    uipart.SetFieldValue('LNasabahDPLKCorporate.kode_nasabah_corporate',None)
    uipart.SetFieldValue('LNasabahDPLKCorporate.nama_perusahaan',None)

  def SetControlsForView(self, form):
    form.GetPanelByName('pNasabah').SetAllControlsReadOnly()
    form.GetPanelByName('pNasabahRight').SetAllControlsReadOnly()
    form.GetPanelByName('pAlamat').SetAllControlsReadOnly()
    #form.GetPanelByName('pAlamatKantor').SetAllControlsReadOnly()
    form.GetPanelByName('pAlamatSurat').SetAllControlsReadOnly()
    form.GetPanelByName('pRekening').SetAllControlsReadOnly()
    form.GetPanelByName('pRekening2').SetAllControlsReadOnly()
    form.GetPanelByName('pPekerjaan').SetAllControlsReadOnly()
    form.GetPanelByName('pKantor').SetAllControlsReadOnly()
    form.GetPanelByName('pKelengkapan').SetAllControlsReadOnly()
    form.GetPanelByName('pRegister').SetAllControlsReadOnly()
    form.GetPanelByName('gAhliWaris').SetAllControlsReadOnly()
    form.GetPanelByName('gAhliWaris').RowSelect = 1
    form.GetPanelByName('gAhliWaris').SuppressHelpLine = 1
    form.GetPanelByName('gPaket').SetAllControlsReadOnly()
    form.GetPanelByName('gPaket').RowSelect = 1
    form.GetPanelByName('gPaket').SuppressHelpLine = 1
    form.GetPanelByName('pPaketInvestasi').SetAllControlsReadOnly()
    form.GetPanelByName('gRekSumber').SetAllControlsReadOnly()
    form.GetPanelByName('gRekSumber').RowSelect = 1
    form.GetPanelByName('gRekSumber').SuppressHelpLine = 1
    
    pButton = form.GetPanelByName('pButton')
    pButton.GetControlByName('btnOK').Caption = '&Setujui'
    pButton.GetControlByName('btnOK').Enabled = 0
    pButton.GetControlByName('btnOK').Default = 0
    pButton.GetControlByName('btnCancel').Caption = '&Tolak'
    pButton.GetControlByName('btnCancel').Enabled = 0
    pButton.GetControlByName('btnCancel').Cancel = 0
    pButton.GetControlByName('btnClose').Caption = '&Tutup'
    pButton.GetControlByName('btnClose').Default = 1
    pButton.GetControlByName('btnClose').Visible = 1
    pButton.GetControlByName('btnClose').Cancel = 1
    form.Caption = 'Lihat Detil Hasil ' + form.Caption
  
  def SetControlsForAuth(self, form):
    form.GetPanelByName('pNasabah').SetAllControlsReadOnly()
    form.GetPanelByName('pNasabahRight').SetAllControlsReadOnly()
    form.GetPanelByName('pAlamat').SetAllControlsReadOnly()
    #form.GetPanelByName('pAlamatKantor').SetAllControlsReadOnly()
    form.GetPanelByName('pAlamatSurat').SetAllControlsReadOnly()
    form.GetPanelByName('pRekening').SetAllControlsReadOnly()
    form.GetPanelByName('pRekening2').SetAllControlsReadOnly()
    form.GetPanelByName('pPekerjaan').SetAllControlsReadOnly()
    form.GetPanelByName('pKantor').SetAllControlsReadOnly()
    form.GetPanelByName('pKelengkapan').SetAllControlsReadOnly()
    form.GetPanelByName('pRegister').SetAllControlsReadOnly()
    form.GetPanelByName('gAhliWaris').SetAllControlsReadOnly()
    form.GetPanelByName('gAhliWaris').RowSelect = 1
    form.GetPanelByName('gAhliWaris').SuppressHelpLine = 1
    form.GetPanelByName('gPaket').SetAllControlsReadOnly()
    form.GetPanelByName('gPaket').RowSelect = 1
    form.GetPanelByName('gPaket').SuppressHelpLine = 1
    form.GetPanelByName('pPaketInvestasi').SetAllControlsReadOnly()
    form.GetPanelByName('gRekSumber').SetAllControlsReadOnly()
    form.GetPanelByName('gRekSumber').RowSelect = 1
    form.GetPanelByName('gRekSumber').SuppressHelpLine = 1
    
    pButton = form.GetPanelByName('pButton')
    pButton.GetControlByName('btnOK').Caption = '&Setujui'
    pButton.GetControlByName('btnCancel').Caption = '&Tolak'
    pButton.GetControlByName('btnCancel').Cancel = 0
    pButton.GetControlByName('btnClose').Visible = 1
    pButton.GetControlByName('btnClose').Cancel = 1
    form.Caption = 'Otorisasi Hasil ' + form.Caption
  
  def FormShow(self, form, parameter):
    app = form.ClientApplication
    
    uipRegisterNasabahRekening = form.GetUIPartByName('uipRegisterNasabahRekening')
    uipRegisterNasabahRekening.Edit()
    
    pPekerjaan = form.GetPanelByName('pPekerjaan')
    pKantor = form.GetPanelByName('pKantor')
    formMode = parameter.FirstRecord.mode
    #if formMode == "new_pesertaexisting":
    if uipRegisterNasabahRekening.no_peserta_existing not in [0, '', None]:
      #formMode = "new"
      self.pNasabah.SetAllControlsReadOnly(1)
      self.pNasabahRight.SetAllControlsReadOnly(1)
      self.pAlamat.SetAllControlsReadOnly(1)
      self.pAlamatSurat.SetAllControlsReadOnly(1)
      self.pPekerjaan.SetAllControlsReadOnly(1)
      self.pKantor.SetAllControlsReadOnly(1)
      self.pKelengkapan.SetAllControlsReadOnly(1)
      self.gAhliWaris.ReadOnly = 1
    
    uipRegisterNasabahRekening.mode = formMode
    uipRegisterNasabahRekening.isSamaAlamat = 0
    
    if uipRegisterNasabahRekening.mode == 'view':
      self.SetControlsForView(form)
    elif uipRegisterNasabahRekening.mode == 'auth':
      self.SetControlsForAuth(form)
    else:
      #mode edit
      form.Caption = 'Koreksi ' + form.Caption
      uipRegisterNasabahRekening.tanggal_register = app.ModDateTime.Now()
      uipRegisterNasabahRekening.user_id = app.UserID
  
      pRekening2 = form.GetPanelByName('pRekening2')
      pNasabah = form.GetPanelByName('pNasabah')
      if uipRegisterNasabahRekening.nolimitlocation == 'F':
        pNasabah.GetControlByName('LBranchLocation').Enabled = 0
  
      if uipRegisterNasabahRekening.GetFieldValue('LNasabahDPLKCorporate.kode_nasabah_corporate') \
        not in [None,'']:
        #termasuk anggota peserta korporat
        uipRegisterNasabahRekening.nasabah_korporat = 1
        #SetControlsEnability(form.GetPanelByName('pAlamatKantor'), 0, -2147483624)
      else:
        #tidak termasuk peserta korporat
        uipRegisterNasabahRekening.nasabah_korporat = 0
        #SetControlsEnability(form.GetPanelByName('pAlamatKantor'), -1, 0)
        pKantor.GetControlByName('LNasabahDPLKCorporate').Enabled = 0
        pRekening2.GetControlByName('iuran_pk').Enabled = 0
    
    uipRegisterNasabahRekening.cbKombinasiPaket = 0
    #self.LJenisPekerjaanOnAfterLookup(pPekerjaan.GetControlByName('LJenisPekerjaan'), self.uipRegisterNasabahRekening)
    self.gReady = 1
  
  def isSamaAlamatClick(self, sender):
    if self.gReady != 0:
      form = sender.OwnerForm
      pAlamatSurat = form.GetPanelByName('pAlamatSurat')
      uipRNR = form.GetUIPartByName('uipRegisterNasabahRekening')
      uipRNR.Edit()
    
      if sender.Checked:
        #copy isi Alamat ke Alamat Surat
        uipRNR.alamat_surat_jalan = uipRNR.alamat_jalan
        uipRNR.alamat_surat_jalan2 = uipRNR.alamat_jalan2
        uipRNR.alamat_surat_rtrw = uipRNR.alamat_rtrw
        uipRNR.alamat_surat_kelurahan = uipRNR.alamat_kelurahan
        uipRNR.alamat_surat_kecamatan = uipRNR.alamat_kecamatan
        uipRNR.alamat_surat_kota = uipRNR.alamat_kota
        uipRNR.alamat_surat_propinsi = uipRNR.alamat_propinsi
        uipRNR.alamat_surat_kode_pos = uipRNR.alamat_kode_pos
        uipRNR.alamat_surat_telepon = uipRNR.alamat_telepon
        uipRNR.alamat_surat_telepon2 = uipRNR.alamat_telepon2

        uipRNR.SetFieldValue('LASPropinsi.kode_propinsi', uipRNR.GetFieldValue('LATPropinsi.kode_propinsi'))
        uipRNR.SetFieldValue('LASPropinsi.nama_propinsi', uipRNR.GetFieldValue('LATPropinsi.nama_propinsi'))
        uipRNR.SetFieldValue('LASKota.kode_kota', uipRNR.GetFieldValue('LATKota.kode_kota'))
        uipRNR.SetFieldValue('LASKota.nama_kota', uipRNR.GetFieldValue('LATKota.nama_kota'))
        uipRNR.SetFieldValue('LASKecamatan.kode_kecamatan', uipRNR.GetFieldValue('LATKecamatan.kode_kecamatan'))
        uipRNR.SetFieldValue('LASKecamatan.nama_kecamatan', uipRNR.GetFieldValue('LATKecamatan.nama_kecamatan'))
    
      else:
        #reset isi Alamat Surat
        self.ResetAlamatSuratValue(uipRNR)  
  
  def LJenisPekerjaanOnAfterLookup(self, sender, linkui):
    # procedure(sender: TrtfDBLookupEdit; linkui: TrtfLinkUIElmtSetting)
    form = sender.OwnerForm
    pKantor = form.GetPanelByName('pKantor')
    uipPekerjaan = form.GetUIPartByName('uipRegisterNasabahRekening')
    uipPekerjaan.Edit()
  
    #Jika pekerjaan Pelajar/Mahasiswa dan Ibu Rumah Tangga
    kode_jenis_pekerjaan = uipPekerjaan.GetFieldValue("LJenisPekerjaan.kode_jenis_pekerjaan")
    if kode_jenis_pekerjaan in ['05','08'] :
      self.pKantor.SetAllControlsReadOnly(1)
      #self.pKelengkapan.SetAllControlsReadOnly(0, "RF_JenisPekerjaanOrtu")
    else:
      self.pKantor.SetAllControlsReadOnly(0, "RF_JenisUsaha")
      #self.pKelengkapan.SetAllControlsReadOnly(1)
  
  def nasabah_korporatClick(self, sender):
    if self.gReady != 0:
      form = sender.OwnerForm
      pNasabah = form.GetPanelByName('pNasabah')
      pPekerjaan = form.GetPanelByName('pPekerjaan')
      pKantor = form.GetPanelByName('pKantor')
      pRekening2 = form.GetPanelByName('pRekening2')
      
      uipRegisterNasabahRekening = form.GetUIPartByName('uipRegisterNasabahRekening')
      uipRegisterNasabahRekening.Edit()
      if sender.Checked:
        pKantor.GetControlByName('LNasabahDPLKCorporate').Enabled = 1
        pKantor.GetControlByName('LKepemilikan').Enabled = \
        pKantor.GetControlByName('LJenisUsaha').Enabled = \
        pKantor.GetControlByName('nama_perusahaan').Enabled = 0
  
        #SetControlsEnability(form.GetPanelByName('pAlamatKantor'), 0, -2147483624)
        self.ResetAlamatKantorValue(uipRegisterNasabahRekening)
        
        #enable juga iuran pk
        pRekening2.GetControlByName('iuran_pk').Enabled = 1
      else:
        pKantor.GetControlByName('LNasabahDPLKCorporate').Enabled = 0
  
        pKantor.GetControlByName('LKepemilikan').Enabled = 1
        uipRegisterNasabahRekening.SetFieldValue('LKepemilikan.kode_pemilikan',None)
        uipRegisterNasabahRekening.SetFieldValue('LKepemilikan.keterangan',None)
  
        pKantor.GetControlByName('LJenisUsaha').Enabled = 1
        uipRegisterNasabahRekening.SetFieldValue('LJenisUsaha.kode_jenis_usaha',None)
        uipRegisterNasabahRekening.SetFieldValue('LJenisUsaha.nama_jenis_usaha',None)
        
        pKantor.GetControlByName('nama_perusahaan').Enabled = 1
        uipRegisterNasabahRekening.SetFieldValue('nama_perusahaan',None)
  
        uipRegisterNasabahRekening.SetFieldValue('LNasabahDPLKCorporate.kode_nasabah_corporate',None)
        uipRegisterNasabahRekening.SetFieldValue('LNasabahDPLKCorporate.nama_perusahaan',None)
        #SetControlsEnability(form.GetPanelByName('pAlamatKantor'), -1, 0)
        
        #disable juga iuran pk
        pRekening2.GetControlByName('iuran_pk').Enabled = 0
  
  def LNasabahDPLKCorporateAfterLookup(self, sender, linkui):
    form = sender.OwnerForm
    uipRegisterNasabahRekening = form.GetUIPartByName('uipRegisterNasabahRekening')
  
    NamaPerusahaan = uipRegisterNasabahRekening.GetFieldValue('LNasabahDPLKCorporate.nama_perusahaan')
    kode_pemilikan = uipRegisterNasabahRekening.GetFieldValue('LNasabahDPLKCorporate.kode_pemilikan')
    keterangan = uipRegisterNasabahRekening.GetFieldValue('LNasabahDPLKCorporate.LKepemilikan.keterangan')
    kode_jenis_usaha = uipRegisterNasabahRekening.GetFieldValue('LNasabahDPLKCorporate.kode_jenis_usaha')
    nama_jenis_usaha = uipRegisterNasabahRekening.GetFieldValue('LNasabahDPLKCorporate.LJenisUsaha.nama_jenis_usaha')
  
    uipRegisterNasabahRekening.Edit()
    uipRegisterNasabahRekening.SetFieldValue('LKepemilikan.kode_pemilikan',kode_pemilikan)
    uipRegisterNasabahRekening.SetFieldValue('LKepemilikan.keterangan',keterangan)
    uipRegisterNasabahRekening.SetFieldValue('LJenisUsaha.kode_jenis_usaha',kode_jenis_usaha)
    uipRegisterNasabahRekening.SetFieldValue('LJenisUsaha.nama_jenis_usaha',nama_jenis_usaha)
    uipRegisterNasabahRekening.SetFieldValue('nama_perusahaan',NamaPerusahaan)
  
  def DaerahAsalAfterLookup(self, sender, linkui):
    form = sender.OwnerForm
    uipRegisterNasabahRekening = form.GetUIPartByName('uipRegisterNasabahRekening')
    uipRegisterNasabahRekening.Edit()
    
    uipRegisterNasabahRekening.SetFieldValue('LATPropinsi.kode_propinsi', uipRegisterNasabahRekening.GetFieldValue('LDaerahAsal.kode_propinsi'))
    uipRegisterNasabahRekening.SetFieldValue('LATPropinsi.nama_propinsi', uipRegisterNasabahRekening.GetFieldValue('LDaerahAsal.nama_propinsi'))
  
  def RAWBeforePost(self, uipRegNRAhliWaris):
    app = uipRegNRAhliWaris.OwnerForm.ClientApplication
  
    if uipRegNRAhliWaris.tanggal_lahir != None and \
      uipRegNRAhliWaris.tanggal_lahir[:3] > \
      app.ModDateTime.DecodeDate(app.ModDateTime.Now())[:3]:
      raise Exception, 'Pesan Kesalahan' + 'Tanggal lahir ahli waris tidak boleh melebihi tanggal hari ini!'
  
  def UsiaPensiunExit(self, sender):
    app = sender.OwnerForm.ClientApplication
    uipT = sender.OwnerForm.GetUIPartByName('uipRegisterNasabahRekening')
    uipT.Edit()
  
    #cek tanggal lahir
    if uipT.tanggal_lahir in [None,[]]:
      #tanggal lahir masih kosong
      app.ShowMessage('Tanggal Lahir masih kosong, tidak bisa menentukan tanggal pensiun dan tanggal pensiun dipercepat.')
      uipT.tgl_pensiun = uipT.tgl_pensiun_dipercepat = None
      return
  
    y, m, d = uipT.tanggal_lahir[:3]
    y += uipT.usia_pensiun
    if (m == 2) and (d == 29) and (not app.ModDateTime.IsLeapYear(y)):
      # tanggal 29 februari, tetapi tahun yang akan datang bukan tahun kabisat
      # dibulatkan menjadi tanggal 28 februari
      d = 28
  
    uipT.tgl_pensiun = app.ModDateTime.EncodeDate(y,m,d)
    uipT.tgl_pensiun_dipercepat = app.ModDateTime.EncodeDate(y-10,m,d)
  
  def validateForm(self):
    form = self.FormObject
    app = form.ClientApplication
    uipRegisterNasabahRekening = form.GetUIPartByName('uipRegisterNasabahRekening')
    uipParam = form.GetUIPartByName('uipParameter')
    uipRegNRAhliWaris = form.GetUIPartByName('uipRegNRAhliWaris')
    
    """nama ibu kandung"""
    if uipRegisterNasabahRekening.ibu_kandung in ["", None]:
      app.ShowMessage('Ibu Kandung masih kosong')
      return False
    
    """nama lengkap peserta"""
    if uipRegisterNasabahRekening.nama_lengkap in ["", None]:
      app.ShowMessage('Nama Lengkap masih kosong')
      return False
    
    """tempat lahir"""
    if uipRegisterNasabahRekening.tempat_lahir in ["", None]:
      app.ShowMessage('Tempat Lahir masih kosong')
      return False
    
    """tanggal lahir"""
    if uipRegisterNasabahRekening.tanggal_lahir in [[], None]:
      app.ShowMessage('Tanggal Lahir masih kosong, proses tidak dapat dilanjutkan...')
      return False
    
    """jenis kelamin"""
    if uipRegisterNasabahRekening.jenis_kelamin in ["", None]:
      app.ShowMessage('Jenis Kelamin masih kosong')
      return False
    
    """nomor referensi"""
    if uipRegisterNasabahRekening.no_referensi in ["", None]:
      app.ShowMessage('Nomor Referensi masih kosong')
      return False
    
    """alamat: jalan, rt/rw, kota, provinsi, kode pos, telp rumah (+kode area), handphone"""
    if uipRegisterNasabahRekening.alamat_jalan in ["", None]\
      or uipRegisterNasabahRekening.alamat_rtrw in ["", None]\
      or uipRegisterNasabahRekening.GetFieldValue('LATKota.kode_kota') in ["", None]\
      or uipRegisterNasabahRekening.GetFieldValue('LATPropinsi.kode_propinsi') in ["", None]\
      or uipRegisterNasabahRekening.alamat_kode_pos in ["", None]\
      or uipRegisterNasabahRekening.alamat_telepon in ["", None]\
      or uipRegisterNasabahRekening.alamat_telepon2 in ["", None]:
      app.ShowMessage("""Alamat Tempat Tinggal yang harus diisi:\n
        - Jalan
        - RT / RW
        - Kota
        - Propinsi
        - Kode Pos
        - Telp. Rumah
        - Handphone""")
      return False

    if uipRegisterNasabahRekening.alamat_surat_jalan in ["", None]\
      or uipRegisterNasabahRekening.alamat_surat_rtrw in ["", None]\
      or uipRegisterNasabahRekening.GetFieldValue('LASKota.kode_kota') in ["", None]\
      or uipRegisterNasabahRekening.GetFieldValue('LASPropinsi.kode_propinsi') in ["", None]\
      or uipRegisterNasabahRekening.alamat_surat_kode_pos in ["", None]\
      or uipRegisterNasabahRekening.alamat_surat_telepon in ["", None]\
      or uipRegisterNasabahRekening.alamat_surat_telepon2 in ["", None]:
      app.ShowMessage("""Alamat Surat yang harus diisi:\n
        - Jalan
        - RT / RW
        - Kota
        - Propinsi
        - Kode Pos
        - Telp. Rumah
        - Handphone""")
      return False

    """sumber dana"""
    if uipRegisterNasabahRekening.GetFieldValue("LSumberDana.sumber_dana") in ['', 0, None]:
      app.ShowMessage('Sumber Dana masih kosong')
      return False
            
    """usia pensiun"""
    if uipRegisterNasabahRekening.usia_pensiun in ['', 0, None]:
      app.ShowMessage('Usia Pensiun masih kosong, proses tidak dapat dilanjutkan...')
      return False
            
    """cek kiriman statemen"""
    if uipRegisterNasabahRekening.kirim_statemen == 'K' and \
      not uipRegisterNasabahRekening.nasabah_korporat:
      #bukan nasabah korporat tapi statemen minta dikirim ke alamat kantor
      form.ShowMessage('Peserta mendaftar tidak sebagai anggota peserta korporat manapun. '\
        'Untuk itu, Statemen tidak bisa dikirim ke alamat Kantor (Korporat)!')
      return False
    
    if uipRegisterNasabahRekening.kirim_statemen == 'R' and \
      uipRegisterNasabahRekening.alamat_surat_jalan == None:
      #kirim statemen ke rumah, tetapi alamat surat masih kosong
      form.ShowMessage('Alamat Surat masih kosong. '\
        'Untuk itu, Statemen tidak bisa dikirim ke alamat Rumah (Alamat Surat)!')
      return False
      
    """setoran awal"""
    if uipRegisterNasabahRekening.setoran_awal in ['', 0, None]:
      app.ShowMessage('Setoran Awal masih kosong')
      return False
            
    if uipRegisterNasabahRekening.sistem_pembayaran_iuran == "R":
      """iuran peserta"""
      if uipRegisterNasabahRekening.iuran_pst in ['', 0, None]:
        app.ShowMessage('Iuran Rutin Peserta masih kosong')
        return False
              
      """tgl penarikan iuran rutin"""
      if uipRegisterNasabahRekening.tgl_penarikan_iuran in ['', 0, None]:
        app.ShowMessage('Tanggal Penarikan Iuran Rutin masih kosong')
        return False
              
      """nomor akun rekening sumber"""
      if uipRegisterNasabahRekening.REKSUMBER_NO in ['', 0, None]:
        app.ShowMessage('No. Akun Rekening Sumber masih kosong')
        return False
              
      """nama pemilik rekening sumber"""
      if uipRegisterNasabahRekening.REKSUMBER_NAMA in ['', 0, None]:
        app.ShowMessage('Nama Pemilik Rekening Sumber masih kosong')
        return False
              
      """iuran peserta dan iuran pemberi kerja"""
      if uipParam.IS_ONLY_MIN_JML_IURAN_PST:
        #cek minimal iuran masing-masing
        if uipRegisterNasabahRekening.iuran_pst < uipParam.MIN_JML_IURAN_PST:
          form.ShowMessage('Iuran Peserta tidak boleh kurang dari Minimum Iuran '\
            'Peserta Default, yaitu Rp %.2f' % (uipParam.MIN_JML_IURAN_PST))
          return False
        
        if uipRegisterNasabahRekening.iuran_pk < uipParam.MIN_JML_IURAN_PK:
          form.ShowMessage('Iuran Pemberi Kerja tidak boleh kurang dari Minimum Iuran '\
            'Pemberi Kerja Default, yaitu Rp %.2f' % (uipParam.MIN_JML_IURAN_PST))
          return False
      else:
        #cek minimal iuran akumulasi
        if (uipRegisterNasabahRekening.iuran_pst + uipRegisterNasabahRekening.iuran_pk) < uipParam.MIN_JML_IURAN_PST:
          form.ShowMessage('Gabungan Iuran Peserta dan Iuran Pemberi Kerja tidak boleh '\
            'kurang dari Minimum Iuran Default,\nyaitu Rp %.2f' % (uipParam.MIN_JML_IURAN_PST))
          return False
    
    """cek tanggal: tanggal lahir, tanggal pensiun (usia pensiun terkait tanggal lahir)"""
    floatTglNow = app.ModDateTime.Now()
    y,m,d = uipRegisterNasabahRekening.tanggal_lahir[:3]
    floatTglPensiun = \
      app.ModDateTime.EncodeDate(y + uipRegisterNasabahRekening.usia_pensiun, m, d)
    
    """cek usia peserta"""
    usiaPeserta = (floatTglNow - app.ModDateTime.EncodeDate(y,m,d))/365
    if usiaPeserta < 18:
      form.ShowMessage('Usia peserta belum 18 Tahun!')
      return False

    if uipRegisterNasabahRekening.tanggal_lahir[:3] > \
      app.ModDateTime.DecodeDate(floatTglNow)[:3]:
      form.ShowMessage('Tanggal lahir peserta tidak boleh melebihi tanggal hari ini!')
      return False
    
    if app.ModDateTime.DecodeDate(floatTglPensiun)[:3] < \
      app.ModDateTime.DecodeDate(floatTglNow)[:3]:
      form.ShowMessage('Tanggal saat peserta akan pensiun telah terlewati. '\
        'Usia pensiun yang diinputkan tidak valid!')
      return False
    
    if (floatTglPensiun - floatTglNow) < uipParam.MIN_SELISIH_TGL_DAFTAR_PENSIUN:
      form.ShowMessage('Selisih hari antara tanggal saat peserta akan pensiun dan '\
        'tanggal hari ini minimal %d hari. \nMohon perbesar usia pensiun yang diinputkan.' \
        % (int(uipParam.MIN_SELISIH_TGL_DAFTAR_PENSIUN)))
      return False
   
    """cek proporsi paket"""
    remProp = 100
    self.uipPaket.First()
    while not self.uipPaket.Eof:
      remProp = remProp - self.uipPaket.proporsi
      self.uipPaket.Next()
    
    if remProp != 0:
      form.ShowMessage('Proporsi pembagian paket investasi belum tepat mencapai 100%')
      return False
      
    """ahli waris (minimal 1 data), dibuat by default terisi namanya "Ahli Waris", terutama untuk upload masal"""
    uipRegNRAhliWaris.First()
    if uipRegNRAhliWaris.Eof:
      app.ShowMessage('Ahli Waris masih kosong, proses tidak dapat dilanjutkan...')
      return False
    
    return True
    
  def btnOKClick(self, sender):
    form = sender.OwnerForm
    app = form.ClientApplication
    uipRegisterNasabahRekening = form.GetUIPartByName('uipRegisterNasabahRekening')
    uipRegNRAhliWaris = form.GetUIPartByName('uipRegNRAhliWaris')
    
    isValid = self.validatePesertaTerdaftar()
    if not isValid:
      sender.ExitAction = 1
      return
    
    isValid = self.validateForm()
    if not isValid:
      return
      
    if uipRegisterNasabahRekening.mode not in ['view','auth']:
      form.CommitBuffer()
      form.PostResult()
    elif uipRegisterNasabahRekening.mode == 'auth':
      #mode auth, go otorisasi
      app.ExecuteScript('transaction/authorize_regnsbrek',app.CreateValues(['id',\
        uipRegisterNasabahRekening.registernr_id]))
    #else: mode view, do nothing

    sender.ExitAction = 1
  
  def btnCancelClick(self, sender):
    form = sender.OwnerForm
    app = form.ClientApplication
    uipRegisterNasabahRekening = form.GetUIPartByName('uipRegisterNasabahRekening')
  
    if uipRegisterNasabahRekening.mode == 'auth':
      dlg = app.ConfirmDialog('Anda yakin membatalkan %s peserta %s %s?' \
        % (sender.OwnerForm.Caption,uipRegisterNasabahRekening.no_peserta,\
        uipRegisterNasabahRekening.nama_lengkap))
      if dlg:
        # batalkan register peserta baru
        app.ExecuteScript('transaction/delete_regnsbrek',app.CreateValues(['id',\
          uipRegisterNasabahRekening.registernr_id]))
        sender.ExitAction = 3
    else:
      sender.ExitAction = 2

  def cbKombinasiPaketOnClick(self, sender):
    # procedure(sender: TrtfCheckBox)
    if self.gReady != 0:
      form = self.FormObject
      app = form.ClientApplication
      uipPaket = form.GetUIPartByName("uipPaket")
      uipTmpPaket = form.GetUIPartByName("uipTmpPaket")
      
      uipPaket.ClearData()
      if sender.Checked:
        uipTmpPaket.First()
        while not uipTmpPaket.Eof:
          uipPaket.Append()
          uipPaket.SetFieldValue("LPaketInvestasi.kode_paket_investasi", uipTmpPaket.kode_pi)
          uipPaket.SetFieldValue("LPaketInvestasi.nama_paket_investasi", uipTmpPaket.nama_pi)
          uipPaket.SetFieldValue("proporsi", 0.0)
          uipTmpPaket.Next()

  def btnClearPaketOnClick(self, sender):
    # procedure(sender: TrtfButton)
    form = self.FormObject
    app = form.ClientApplication
      
    uipRegisterNasabahRekening = form.GetUIPartByName("uipRegisterNasabahRekening")
    uipPaket = form.GetUIPartByName("uipPaket")
    
    uipPaket.ClearData()
    uipRegisterNasabahRekening.cbKombinasiPaket = 0
    
  def LPaketInvestasi_kode_paket_investasiOnAfterLookup(self, sender, linkui):
    # procedure(sender: TrtfGridColumn; linkui: TrtfLinkUIElmtSetting)
    if self.gReady != 0:
      form = self.FormObject
      app = form.ClientApplication
      
      self.uipPaket.SetFieldValue("proporsi", 100.0)

  def validatePesertaTerdaftar(self):
      form = self.FormObject
      app = form.ClientApplication
      uipRegisterNasabahRekening = form.GetUIPartByName('uipRegisterNasabahRekening')
      
      """cek peserta"""
      ph = app.CreateValues(
        ['ibu_kandung', uipRegisterNasabahRekening.ibu_kandung],
        ['nama_lengkap', uipRegisterNasabahRekening.nama_lengkap],
        ['tanggal_lahir', uipRegisterNasabahRekening.tanggal_lahir]
      )
      resp = form.CallServerMethod('cekPeserta', ph)
      status = resp.FirstRecord
      if not status.success:
        app.ShowMessage(status.message)
        return True
      else:
        if status.registernr_id > 0\
          and status.registernr_id == uipRegisterNasabahRekening.registernr_id:
          return True
          
        if status.is_otor:
          dlg = app.ConfirmDialog("""
            Calon peserta telah terdaftar di Kepesertaan DPLK.
            Nomor Peserta: '%s', dengan status 'Sudah Otorisasi' \n
            Apakah Anda ingin membuka rekening baru atas nama peserta ini ?
            """ % status.no_peserta)
        else:
          #dlg = app.ConfirmDialog("""
          #  Calon peserta telah terdaftar di Kepesertaan DPLK.
          #  Nomor Peserta: '%s', dengan status 'Belum Otorisasi' \n
          #  Apakah Anda ingin membuka data registrasi DPLK atas nama peserta ini ?
          #  """ % status.no_peserta)
          #app.ShowMessage('Nomor ID registrasi: ' + str(status.registernr_id))
          dlg = False
          app.ShowMessage("""
            Calon peserta telah terdaftar di Kepesertaan DPLK.
            Nomor Peserta: '%s', dengan status 'Belum Otorisasi'\n
            Daftar peserta tersebut dapat diakses melalui menu:
            Nasabah -> Daftar Register Peserta Baru
          """ % status.no_peserta)
        
        if dlg:
          if status.is_otor:
            formID = 'fRegistrasi_New'
            mode = 'new_pesertaexisting'
            ph = app.CreateValues(['mode', 'exist_nasabah'], ['no_peserta', status.no_peserta])
          else:
            formID = 'fRegistrasi'
            mode = 'edit'
            pobjconst = "PObj:REGISTERNASABAHREKENING#REGISTERNR_ID=%s" % str(status.registernr_id)
            ph = app.CreateValues(['key', pobjconst])
          
          frm = app.CreateForm('transaction/'+formID, formID, 0, ph, None)
          frm.Show(app.CreateValues(['mode',mode]))  
        
        return False
      
  def btnCekPesertaTerdaftarOnClick(self, sender):
    # procedure(sender: TrtfButton)
    if self.gReady != 0:
      form = self.FormObject
      app = form.ClientApplication
      uipRegisterNasabahRekening = form.GetUIPartByName('uipRegisterNasabahRekening')
      
      """cek data ibu kandung, nama lengkap, dan tanggal lahir"""
      if uipRegisterNasabahRekening.ibu_kandung in ["", None]\
        or uipRegisterNasabahRekening.nama_lengkap in ["", None]\
        or uipRegisterNasabahRekening.tanggal_lahir in [[], None]:
        app.ShowMessage("""Untuk melanjutkan proses, data berikut harus tersedia:\n
        - Nama Ibu Kandung
        - Nama Lengkap Peserta
        - Tanggal Lahir Peserta""")
        return False
        
      isValid = self.validatePesertaTerdaftar()
      if not isValid:
        sender.ExitAction = 1
        return

  def uipRekSumberBeforePost(self, uip):
    # procedure(uip: TrtfPClassUI)
    if self.gReady != 0:
      form = self.FormObject
      app = form.ClientApplication
      
      norek_sumber = uip.norek_sumber
      #if norek_sumber[:4] == ???
      uip.SetFieldValue("LBranchLocation.branch_code",\
        self.uipRegisterNasabahRekening.GetFieldValue("LBranchLocation.branch_code"))
      uip.SetFieldValue("LBranchLocation.BranchName",\
        self.uipRegisterNasabahRekening.GetFieldValue("LBranchLocation.BranchName"))
