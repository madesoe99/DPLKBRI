gReady = 0

def FormShow(form, parameter):
  app = form.ClientApplication

  uipRegisterNasabahRekening = form.GetUIPartByName('uipRegisterNasabahRekening')
  uipRegisterNasabahRekening.Edit()
  uipRegisterNasabahRekening.mode = parameter.FirstRecord.mode
  
  uipRegisterNasabahRekening.nasabah_korporat = 0
  form.GetControlByName('pNasabah.LNasabahDPLKCorporate').Enabled = 0
  form.GetControlByName('pRekening2.iuran_pk').Enabled = 0

  if uipRegisterNasabahRekening.nolimitlocation == 'F':
    form.GetControlByName('pNasabah.LBranchLocation').Enabled = 0

  uipRegisterNasabahRekening.isSamaAlamat = 0
  uipRegisterNasabahRekening.isPesertaPengalihan = 'F'

  global gReady
  gReady = 1

def SetControlsEnability(panel, value, color):
  for i in range(panel.ControlCount):
    #panel.GetControl(i).Color = color
    panel.GetControl(i).Enabled = value

def ResetAlamatKantorValue(uipart):
  uipart.alamat_kantor_jalan = \
  uipart.alamat_kantor_kode_pos = \
  uipart.alamat_kantor_kelurahan = \
  uipart.alamat_kantor_kecamatan = \
  uipart.alamat_kantor_kota = \
  uipart.alamat_kantor_propinsi = \
  uipart.alamat_kantor_telepon = \
  uipart.alamat_kantor_telepon2 = None

def ResetAlamatSuratValue(uipart):
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

def nasabah_korporatClick(sender):
  global gReady

  if gReady != 0:
    form = sender.OwnerForm

    uipRegisterNasabahRekening = form.GetUIPartByName('uipRegisterNasabahRekening')
    uipRegisterNasabahRekening.Edit()

    if sender.Checked:
      form.GetControlByName('pNasabah.LNasabahDPLKCorporate').Enabled = 1
      form.GetControlByName('pPekerjaan.LKepemilikan').Enabled = \
      form.GetControlByName('pPekerjaan.LJenisUsaha').Enabled = \
      form.GetControlByName('pPekerjaan.nama_perusahaan').Enabled = 0

      SetControlsEnability(form.GetPanelByName('pAlamatKantor'), 0, -2147483624)
      ResetAlamatKantorValue(uipRegisterNasabahRekening)
      
      #enable juga iuran pk
      form.GetControlByName('pRekening2.iuran_pk').Enabled = 1
      
    else:
      form.GetControlByName('pNasabah.LNasabahDPLKCorporate').Enabled = 0

      form.GetControlByName('pPekerjaan.LKepemilikan').Enabled = 1
      uipRegisterNasabahRekening.SetFieldValue('LKepemilikan.kode_pemilikan',None)
      uipRegisterNasabahRekening.SetFieldValue('LKepemilikan.keterangan',None)

      form.GetControlByName('pPekerjaan.LJenisUsaha').Enabled = 1
      uipRegisterNasabahRekening.SetFieldValue('LJenisUsaha.kode_jenis_usaha',None)
      uipRegisterNasabahRekening.SetFieldValue('LJenisUsaha.nama_jenis_usaha',None)

      form.GetControlByName('pPekerjaan.nama_perusahaan').Enabled = 1
      uipRegisterNasabahRekening.SetFieldValue('nama_perusahaan',None)

      uipRegisterNasabahRekening.SetFieldValue('LNasabahDPLKCorporate.kode_nasabah_corporate',None)
      uipRegisterNasabahRekening.SetFieldValue('LNasabahDPLKCorporate.nama_perusahaan',None)
      SetControlsEnability(form.GetPanelByName('pAlamatKantor'), -1, 0)

      #disable juga iuran pk
      form.GetControlByName('pRekening2.iuran_pk').Enabled = 0

def LNasabahDPLKCorporateAfterLookup(sender, linkui):
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

def DaerahAsalAfterLookup(sender, linkui):
  form = sender.OwnerForm
  uipRegisterNasabahRekening = form.GetUIPartByName('uipRegisterNasabahRekening')
  uipRegisterNasabahRekening.Edit()
  
  uipRegisterNasabahRekening.alamat_propinsi = \
    uipRegisterNasabahRekening.GetFieldValue('LDaerahAsal.nama_propinsi')

def auto_debetClick(sender):
  form = sender.OwnerForm
  pRekening2 = form.GetPanelByName('pRekening2')
  uipRegisterNasabahRekening = form.GetUIPartByName('uipRegisterNasabahRekening')
  no_rek_autodebet = pRekening2.GetControlByName('no_rek_autodebet')
  nama_rek_autodebet = pRekening2.GetControlByName('nama_rek_autodebet')
  tanggal_autodebet = pRekening2.GetControlByName('tanggal_autodebet')

  if sender.Checked:
    no_rek_autodebet.Enabled = \
    tanggal_autodebet.Enabled = \
    form.GetControlByName('pRekening2.bCekRekening').Enabled = 1
    form.GetControlByName('pButton.btnOK').Enabled = \
    form.GetControlByName('pButton.btnOK').Default = 0
  else:
    no_rek_autodebet.Enabled = \
    tanggal_autodebet.Enabled = \
    form.GetControlByName('pRekening2.bCekRekening').Enabled = 0
    form.GetControlByName('pButton.btnOK').Enabled = \
    form.GetControlByName('pButton.btnOK').Default = 1
    uipRegisterNasabahRekening.no_rek_autodebet = \
    uipRegisterNasabahRekening.nama_rek_autodebet = \
    uipRegisterNasabahRekening.tanggal_autodebet = \
    uipRegisterNasabahRekening.IDNumber = \
    uipRegisterNasabahRekening.BranchCode = \
    uipRegisterNasabahRekening.CurrencyCode = \
    uipRegisterNasabahRekening.TipeRekening = None
    
def isSamaAlamatClick(sender):
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
    form.GetControlByName('pAlamatSurat.alamat_surat_jalan').Enabled = \
    form.GetControlByName('pAlamatSurat.alamat_surat_jalan2').Enabled = \
    form.GetControlByName('pAlamatSurat.alamat_surat_rtrw').Enabled = \
    form.GetControlByName('pAlamatSurat.alamat_surat_kelurahan').Enabled = \
    form.GetControlByName('pAlamatSurat.alamat_surat_kecamatan').Enabled = \
    form.GetControlByName('pAlamatSurat.alamat_surat_kota').Enabled = \
    form.GetControlByName('pAlamatSurat.alamat_surat_propinsi').Enabled = \
    form.GetControlByName('pAlamatSurat.alamat_surat_kode_pos').Enabled = \
    form.GetControlByName('pAlamatSurat.alamat_surat_telepon').Enabled = \
    form.GetControlByName('pAlamatSurat.alamat_surat_telepon2').Enabled = 0

  else:
    #reset isi Alamat Surat
    ResetAlamatSuratValue(uipRNR)
    
    #enabled field Alamat Surat
    form.GetControlByName('pAlamatSurat.alamat_surat_jalan').Enabled = \
    form.GetControlByName('pAlamatSurat.alamat_surat_jalan2').Enabled = \
    form.GetControlByName('pAlamatSurat.alamat_surat_rtrw').Enabled = \
    form.GetControlByName('pAlamatSurat.alamat_surat_kelurahan').Enabled = \
    form.GetControlByName('pAlamatSurat.alamat_surat_kecamatan').Enabled = \
    form.GetControlByName('pAlamatSurat.alamat_surat_kota').Enabled = \
    form.GetControlByName('pAlamatSurat.alamat_surat_propinsi').Enabled = \
    form.GetControlByName('pAlamatSurat.alamat_surat_kode_pos').Enabled = \
    form.GetControlByName('pAlamatSurat.alamat_surat_telepon').Enabled = \
    form.GetControlByName('pAlamatSurat.alamat_surat_telepon2').Enabled = 1

def RAWBeforePost(uipRegNRAhliWaris):
  app = uipRegNRAhliWaris.OwnerForm.ClientApplication

  if uipRegNRAhliWaris.tanggal_lahir != None and \
    uipRegNRAhliWaris.tanggal_lahir[:3] > \
    app.ModDateTime.DecodeDate(app.ModDateTime.Now())[:3]:
    raise Exception, 'Pesan Kesalahan' + 'Tanggal lahir ahli waris tidak boleh melebihi tanggal hari ini!'

def UsiaPensiunExit(sender):
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
  
def bCekRekeningClick(sender):
  app = sender.OwnerForm.ClientApplication
  uipT = sender.OwnerForm.GetUIPartByName('uipRegisterNasabahRekening')

  #cek field nomor rekening autodebet
  if uipT.no_rek_autodebet in [None,'']:
    #belum ada nomor rekening
    app.ShowMessage('Nomor Rekening Autodebet masih kosong, mohon diisi dahulu.')
  else:
    #nomor rekening sudah ada
    res = app.ExecuteScript('transaksi/CekRekeningCoreBanking',\
      app.CreateValues(['noRekening',uipT.no_rek_autodebet]))

    uipT.Edit()
    uipT.nama_rek_autodebet = res.FirstRecord.namaPemilikRekening
    if uipT.nama_rek_autodebet != 'Rekening tidak terdefinisi':
      #tampilkan informasi lain rekening
      uipT.TipeRekening = res.FirstRecord.accountType
      uipT.IDNumber = res.FirstRecord.idNumber
      uipT.BranchCode = res.FirstRecord.branchCode
      uipT.CurrencyCode = res.FirstRecord.currencyCode
      sender.OwnerForm.GetControlByName('pButton.btnOK').Enabled = \
      sender.OwnerForm.GetControlByName('pButton.btnOK').Default = 1
    else:
      uipT.TipeRekening = uipT.IDNumber = uipT.BranchCode = uipT.CurrencyCode = None

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterNasabahRekening = form.GetUIPartByName('uipRegisterNasabahRekening')

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

  #SEMUA CHECKING BERIKUT DILAKUKAN DI SERVER (APPLY ROW)
  #checking nomor referensi
  #checking usia pensiun
  #checking nasabah korporat
  #checking autodebet

  uipRegisterNasabahRekening.Edit()
  uipRegisterNasabahRekening.__SYSFLAG = 'N'

  form.CommitBuffer()
  form.PostResult()

  sender.ExitAction = 1

def btnCancelClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterNasabahRekening = form.GetUIPartByName('uipRegisterNasabahRekening')

  sender.ExitAction = 2

