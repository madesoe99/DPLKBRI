#global variable
gReady = 0

def SetControlsEnability(panel, value, color):
  for i in range(panel.ControlCount):
    #panel.GetControl(i).Color = color
    panel.GetControl(i).Enabled = value

def ResetAlamatKantorValue(uipart):
  uipart.nama_perusahaan = None
  uipart.alamat_kantor_jalan = None
  uipart.alamat_kantor_kode_pos = None
  uipart.alamat_kantor_kelurahan = None
  uipart.alamat_kantor_kecamatan = None
  uipart.alamat_kantor_kota = None
  uipart.alamat_kantor_propinsi = None
  uipart.alamat_kantor_telepon = None
  uipart.alamat_kantor_telepon2 = None

def SetControlsForView(form):
  form.GetPanelByName('pNasabah').SetAllControlsReadOnly()
  form.GetPanelByName('pAlamat').SetAllControlsReadOnly()
  form.GetPanelByName('pAlamatKantor').SetAllControlsReadOnly()
  form.GetPanelByName('pAlamatSurat').SetAllControlsReadOnly()
  form.GetPanelByName('pRekening').SetAllControlsReadOnly()
  form.GetPanelByName('pRekening2').SetAllControlsReadOnly()
  form.GetPanelByName('pPekerjaan').SetAllControlsReadOnly()
  form.GetPanelByName('pRegister').SetAllControlsReadOnly()
  form.GetPanelByName('gAhliWaris').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnOK').Enabled = 0
  form.GetControlByName('pButton.btnOK').Default = 0
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Enabled = 0
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  form.GetControlByName('pButton.btnClose').Caption = '&Tutup'
  form.GetControlByName('pButton.btnClose').Default = 1
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnClose').Cancel = 1
  form.Caption = 'Lihat Detil Hasil ' + form.Caption

def SetControlsForAuth(form):
  form.GetPanelByName('pNasabah').SetAllControlsReadOnly()
  form.GetPanelByName('pAlamat').SetAllControlsReadOnly()
  form.GetPanelByName('pAlamatKantor').SetAllControlsReadOnly()
  form.GetPanelByName('pAlamatSurat').SetAllControlsReadOnly()
  form.GetPanelByName('pRekening').SetAllControlsReadOnly()
  form.GetPanelByName('pRekening2').SetAllControlsReadOnly()
  form.GetPanelByName('pPekerjaan').SetAllControlsReadOnly()
  form.GetPanelByName('pRegister').SetAllControlsReadOnly()
  form.GetPanelByName('gAhliWaris').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnClose').Cancel = 1
  form.Caption = 'Otorisasi Hasil ' + form.Caption

def FormShow(form, parameter):
  app = form.ClientApplication
  uipRegisterNasabahRekening = form.GetUIPartByName('uipRegisterNasabahRekening')
  uipRegisterNasabahRekening.Edit()
  uipRegisterNasabahRekening.mode = parameter.FirstRecord.mode
  
  if uipRegisterNasabahRekening.mode == 'view':
    SetControlsForView(form)
  elif uipRegisterNasabahRekening.mode == 'auth':  
    SetControlsForAuth(form)
  else:
    #mode edit
    form.Caption = 'Koreksi ' + form.Caption
    uipRegisterNasabahRekening.tanggal_register = app.ModDateTime.Now()
    uipRegisterNasabahRekening.user_id = app.UserID

    if uipRegisterNasabahRekening.auto_debet == 'T':
      form.GetControlByName('pRekening2.no_rek_autodebet').Enabled = 1
      form.GetControlByName('pRekening2.nama_rek_autodebet').Enabled = 1
      form.GetControlByName('pRekening2.tanggal_autodebet').Enabled = 1
    else:
      form.GetControlByName('pRekening2.no_rek_autodebet').Enabled = 0
      form.GetControlByName('pRekening2.nama_rek_autodebet').Enabled = 0
      form.GetControlByName('pRekening2.tanggal_autodebet').Enabled = 0

    if uipRegisterNasabahRekening.nolimitlocation == 'F':
      form.GetControlByName('pNasabah.LBranchLocation').Enabled = 0

    if uipRegisterNasabahRekening.GetFieldValue('LNasabahDPLKCorporate.kode_nasabah_corporate') \
      not in [None,'']:
      #termasuk anggota peserta korporat
      uipRegisterNasabahRekening.nasabah_korporat = 1
      SetControlsEnability(form.GetPanelByName('pAlamatKantor'), 0, -2147483624)
    else:
      #tidak termasuk peserta korporat
      uipRegisterNasabahRekening.nasabah_korporat = 0
      SetControlsEnability(form.GetPanelByName('pAlamatKantor'), -1, 0)
      form.GetControlByName('pNasabah.LNasabahDPLKCorporate').Enabled = \
      form.GetControlByName('pRekening2.iuran_pk').Enabled = 0

  global gReady
  gReady = 1

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
    form.GetControlByName('pRekening2.TipeRekening').Enabled = \
    form.GetControlByName('pRekening2.bCekRekening').Enabled = 1
    form.GetControlByName('pButton.btnOK').Enabled = \
    form.GetControlByName('pButton.btnOK').Default = 0
  else:
    no_rek_autodebet.Enabled = \
    tanggal_autodebet.Enabled = \
    form.GetControlByName('pRekening2.TipeRekening').Enabled = \
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

def btnCancelClick(sender):
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

