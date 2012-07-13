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
  
  def SetControlsForView(self, form):
    form.GetPanelByName('pNasabah').SetAllControlsReadOnly()
    form.GetPanelByName('pNasabahRight').SetAllControlsReadOnly()
    form.GetPanelByName('pAlamat').SetAllControlsReadOnly()
    #form.GetPanelByName('pAlamatKantor').SetAllControlsReadOnly()
    form.GetPanelByName('pAlamatSurat').SetAllControlsReadOnly()
    form.GetPanelByName('pRekening').SetAllControlsReadOnly()
    form.GetPanelByName('pRekening2').SetAllControlsReadOnly()
    form.GetPanelByName('pPekerjaan').SetAllControlsReadOnly()
    form.GetPanelByName('pRegister').SetAllControlsReadOnly()
    form.GetPanelByName('gAhliWaris').SetAllControlsReadOnly()
    form.GetPanelByName('gPaket').SetAllControlsReadOnly()
    
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
    form.GetPanelByName('pRegister').SetAllControlsReadOnly()
    form.GetPanelByName('gAhliWaris').SetAllControlsReadOnly()
    form.GetPanelByName('gPaket').SetAllControlsReadOnly()
    
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
    formMode = parameter.FirstRecord.mode
    #if formMode == "new_pesertaexisting":
    if uipRegisterNasabahRekening.no_peserta_existing not in [0, '', None]:
      #formMode = "new"
      self.pNasabah.SetAllControlsReadOnly(1)
      self.pNasabahRight.SetAllControlsReadOnly(1)
      self.pAlamat.SetAllControlsReadOnly(1)
      self.pAlamatSurat.SetAllControlsReadOnly(1)
      self.pPekerjaan.SetAllControlsReadOnly(1)
      #self.pRegister.SetAllControlsReadOnly(1)
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
        pPekerjaan.GetControlByName('LNasabahDPLKCorporate').Enabled = 0
        pRekening2.GetControlByName('iuran_pk').Enabled = 0
    
    self.LJenisPekerjaan_OnAfterLookup(pPekerjaan.GetControlByName('LJenisPekerjaan'), self.uipRegisterNasabahRekening)
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
        
        #disable field Alamat Surat
        '''form.GetControlByName('pAlamatSurat.alamat_surat_jalan').Enabled = \
        form.GetControlByName('pAlamatSurat.alamat_surat_jalan2').Enabled = \
        form.GetControlByName('pAlamatSurat.alamat_surat_rtrw').Enabled = \
        form.GetControlByName('pAlamatSurat.alamat_surat_kelurahan').Enabled = \
        form.GetControlByName('pAlamatSurat.alamat_surat_kecamatan').Enabled = \
        form.GetControlByName('pAlamatSurat.alamat_surat_kota').Enabled = \
        form.GetControlByName('pAlamatSurat.alamat_surat_propinsi').Enabled = \
        form.GetControlByName('pAlamatSurat.alamat_surat_kode_pos').Enabled = \
        form.GetControlByName('pAlamatSurat.alamat_surat_telepon').Enabled = \
        form.GetControlByName('pAlamatSurat.alamat_surat_telepon2').Enabled = 0'''
    
      else:
        #reset isi Alamat Surat
        self.ResetAlamatSuratValue(uipRNR)
        
        #enabled field Alamat Surat
        '''form.GetControlByName('pAlamatSurat.alamat_surat_jalan').Enabled = \
        form.GetControlByName('pAlamatSurat.alamat_surat_jalan2').Enabled = \
        form.GetControlByName('pAlamatSurat.alamat_surat_rtrw').Enabled = \
        form.GetControlByName('pAlamatSurat.alamat_surat_kelurahan').Enabled = \
        form.GetControlByName('pAlamatSurat.alamat_surat_kecamatan').Enabled = \
        form.GetControlByName('pAlamatSurat.alamat_surat_kota').Enabled = \
        form.GetControlByName('pAlamatSurat.alamat_surat_propinsi').Enabled = \
        form.GetControlByName('pAlamatSurat.alamat_surat_kode_pos').Enabled = \
        form.GetControlByName('pAlamatSurat.alamat_surat_telepon').Enabled = \
        form.GetControlByName('pAlamatSurat.alamat_surat_telepon2').Enabled = 1'''
  
  
  def LJenisPekerjaan_OnAfterLookup(self, sender, linkui):
    form = sender.OwnerForm
    pPekerjaan = form.GetPanelByName('pPekerjaan')
    uipPekerjaan = form.GetUIPartByName('uipRegisterNasabahRekening')
    uipPekerjaan.Edit()
  
    #if sender.Checked:
      #Jika pekerjaan Pelajar/Mahasiswa dan Ibu Rumah Tangga
    kode_jenis_pekerjaan = uipPekerjaan.GetFieldValue("LJenisPekerjaan.kode_jenis_pekerjaan")
    if kode_jenis_pekerjaan in ['05','08'] :
      pPekerjaan.GetControlByName('LJenisPekerjaanOrtu').ControlCaption = 'Jenis Pekerjaan Orang Tua'
      pPekerjaan.GetControlByName('penghasilan_orang_tua').ControlCaption = 'Penghasilan Orang Tua'
  
      pPekerjaan.GetControlByName('datasuami').Visible = \
      pPekerjaan.GetControlByName('nama_orang_tua').Visible = \
      pPekerjaan.GetControlByName('LJenisPekerjaanOrtu').visible = \
      pPekerjaan.GetControlByName('nama_perusahaan_ortu').Visible = \
      pPekerjaan.GetControlByName('penghasilan_orang_tua').Visible = 1
      #uipPekerjaan.SetFieldValue('nama_orang_tua',nama_orang_tua)
    else:
      pPekerjaan.GetControlByName('LJenisPekerjaanOrtu').ControlCaption = ''
      pPekerjaan.GetControlByName('penghasilan_orang_tua').ControlCaption = ''
      
      pPekerjaan.GetControlByName('datasuami').Visible = \
      pPekerjaan.GetControlByName('nama_orang_tua').Visible = \
      pPekerjaan.GetControlByName('LJenisPekerjaanOrtu').visible = \
      pPekerjaan.GetControlByName('nama_perusahaan_ortu').Visible = \
      pPekerjaan.GetControlByName('penghasilan_orang_tua').Visible = 0
  
      #nama_orang_tua = 'Ade Herman'
      #uipPekerjaan.SetFieldValue('nama_orang_tua',nama_orang_tua)
  
  
  ### -----End By Ade herman -------2010-12-31----#
  
  
  
  def nasabah_korporatClick(self, sender):
    if self.gReady != 0:
      form = sender.OwnerForm
      pNasabah = form.GetPanelByName('pNasabah')
      pPekerjaan = form.GetPanelByName('pPekerjaan')
      pRekening2 = form.GetPanelByName('pRekening2')
      
      uipRegisterNasabahRekening = form.GetUIPartByName('uipRegisterNasabahRekening')
      uipRegisterNasabahRekening.Edit()
      if sender.Checked:
        pPekerjaan.GetControlByName('LNasabahDPLKCorporate').Enabled = 1
        pPekerjaan.GetControlByName('LKepemilikan').Enabled = \
        pPekerjaan.GetControlByName('LJenisUsaha').Enabled = \
        pPekerjaan.GetControlByName('nama_perusahaan').Enabled = 0
  
        #SetControlsEnability(form.GetPanelByName('pAlamatKantor'), 0, -2147483624)
        self.ResetAlamatKantorValue(uipRegisterNasabahRekening)
        
        #enable juga iuran pk
        pRekening2.GetControlByName('iuran_pk').Enabled = 1
      else:
        pPekerjaan.GetControlByName('LNasabahDPLKCorporate').Enabled = 0
  
        pPekerjaan.GetControlByName('LKepemilikan').Enabled = 1
        uipRegisterNasabahRekening.SetFieldValue('LKepemilikan.kode_pemilikan',None)
        uipRegisterNasabahRekening.SetFieldValue('LKepemilikan.keterangan',None)
  
        pPekerjaan.GetControlByName('LJenisUsaha').Enabled = 1
        uipRegisterNasabahRekening.SetFieldValue('LJenisUsaha.kode_jenis_usaha',None)
        uipRegisterNasabahRekening.SetFieldValue('LJenisUsaha.nama_jenis_usaha',None)
        
        pPekerjaan.GetControlByName('nama_perusahaan').Enabled = 1
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
  
    uipRegisterNasabahRekening.alamat_propinsi = \
      uipRegisterNasabahRekening.GetFieldValue('LDaerahAsal.nama_propinsi')
  
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
  
  def btnOKClick(self, sender):
    form = sender.OwnerForm
    app = form.ClientApplication
    uipRegisterNasabahRekening = form.GetUIPartByName('uipRegisterNasabahRekening')
  
    if uipRegisterNasabahRekening.mode not in ['view','auth']:
      #checking besar iuran peserta dan iuran pemberi kerja
      uipP = form.GetUIPartByName('uipParameter')
      if uipP.IS_ONLY_MIN_JML_IURAN_PST:
        #cek minimal iuran masing-masing
        if uipRegisterNasabahRekening.iuran_pst < uipP.MIN_JML_IURAN_PST:
          form.ShowMessage('Iuran Peserta tidak boleh kurang dari Minimum Iuran '\
            'Peserta Default, yaitu Rp %.2f' % (uipP.MIN_JML_IURAN_PST))
          return
        elif uipRegisterNasabahRekening.iuran_pk < uipP.MIN_JML_IURAN_PK:
          form.ShowMessage('Iuran Pemberi Kerja tidak boleh kurang dari Minimum Iuran '\
            'Pemberi Kerja Default, yaitu Rp %.2f' % (uipP.MIN_JML_IURAN_PST))
          return
      else:
        #cek minimal iuran akumulasi
        if (uipRegisterNasabahRekening.iuran_pst+uipRegisterNasabahRekening.iuran_pk) < \
          uipP.MIN_JML_IURAN_PST:
          form.ShowMessage('Gabungan Iuran Peserta dan Iuran Pemberi Kerja tidak boleh '\
            'kurang dari Minimum Iuran Default,\nyaitu Rp %.2f' % (uipP.MIN_JML_IURAN_PST))
          return
  
      remProp = 100
      self.uipPaket.First()
      while not self.uipPaket.Eof:
        remProp = remProp - self.uipPaket.proporsi
        self.uipPaket.Next()
      
      if remProp != 0:
        form.ShowMessage('Proporsi pembagian paket investasi belum tepat mencapai 100%')
        return
      
      #cek tanggal: tanggal lahir, tanggal pensiun (usia pensiun terkait tanggal lahir)
      y,m,d = uipRegisterNasabahRekening.tanggal_lahir[:3]
      floatTglPensiun = \
        app.ModDateTime.EncodeDate(y+uipRegisterNasabahRekening.usia_pensiun,m,d)
      floatTglNow = app.ModDateTime.Now()
  
      if uipRegisterNasabahRekening.tanggal_lahir[:3] > \
        app.ModDateTime.DecodeDate(floatTglNow)[:3]:
        form.ShowMessage('Tanggal lahir peserta tidak boleh melebihi tanggal hari ini!')
        return
      elif app.ModDateTime.DecodeDate(floatTglPensiun)[:3] < \
        app.ModDateTime.DecodeDate(floatTglNow)[:3]:
        form.ShowMessage('Tanggal saat peserta akan pensiun telah terlewati. '\
          'Usia pensiun yang diinputkan tidak valid!')
        return
      elif (floatTglPensiun - floatTglNow) < uipP.MIN_SELISIH_TGL_DAFTAR_PENSIUN:
        form.ShowMessage('Selisih hari antara tanggal saat peserta akan pensiun dan '\
          'tanggal hari ini minimal %d hari. \nMohon perbesar usia pensiun yang diinputkan.' \
          % (int(uipP.MIN_SELISIH_TGL_DAFTAR_PENSIUN)))
        return
        
      #cek kiriman statemen
      if uipRegisterNasabahRekening.kirim_statemen == 'K' and \
        not uipRegisterNasabahRekening.nasabah_korporat:
        #bukan nasabah korporat tapi statemen minta dikirim ke alamat kantor
        form.ShowMessage('Peserta mendaftar tidak sebagai anggota peserta korporat manapun. '\
          'Untuk itu, Statemen tidak bisa dikirim ke alamat Kantor (Korporat)!')
        return
      elif uipRegisterNasabahRekening.kirim_statemen == 'R' and \
        uipRegisterNasabahRekening.alamat_surat_jalan == None:
        #kirim statemen ke rumah, tetapi alamat surat masih kosong
        form.ShowMessage('Alamat Surat masih kosong. '\
          'Untuk itu, Statemen tidak bisa dikirim ke alamat Rumah (Alamat Surat)!')
        return
  
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

