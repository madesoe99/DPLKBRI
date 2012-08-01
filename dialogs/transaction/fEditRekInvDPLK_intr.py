def SetControlsForView(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetPanelByName('pDataBaru').SetAllControlsReadOnly()
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
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetPanelByName('pDataBaru').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnClose').Cancel = 1
  form.Caption = 'Otorisasi Hasil ' + form.Caption

def FormShow(form, parameter):
  app = form.ClientApplication
  uipRegisterCIF = form.GetUIPartByName('uipRegisterCIF')
  uipMaster = form.GetUIPartByName('uipMaster')

  uipRegisterCIF.Edit()
  uipRegisterCIF.mode = parameter.FirstRecord.mode

  if uipRegisterCIF.mode == 'view':
    SetControlsForView(form)
  elif uipRegisterCIF.mode == 'auth':
    SetControlsForAuth(form)
  else:
    #mode New or Edit
    uipRegisterCIF.user_id = app.UserID

    dh = app.ExecuteScript('getsessioninfo',app.CreateValues(['id',1]))
    uipRegisterCIF.terminal_id = dh.FirstRecord.sessioninfo

    if uipRegisterCIF.mode == 'new':
      uipRegisterCIF.SetFieldValue('LNasabahDPLK.no_peserta',uipMaster.no_peserta)
      uipRegisterCIF.SetFieldValue('LNasabahDPLK.nama_lengkap',uipMaster.GetFieldValue('LNasabahDPLK.nama_lengkap'))
      uipRegisterCIF.SetFieldValue('LRekeningDPLK.no_rekening',uipMaster.no_rekening)
      #uipRegisterCIF.SetFieldValue('LRekeningDPLK.keterangan',uipMaster.keterangan)
      uipRegisterCIF.SetFieldValue("LSumberDana.sumber_dana", uipMaster.GetFieldValue("LSumberDana.sumber_dana"))
      uipRegisterCIF.SetFieldValue("LSumberDana.keterangan", uipMaster.GetFieldValue("LSumberDana.keterangan"))
      uipRegisterCIF.SetFieldValue("usia_pensiun", uipMaster.GetFieldValue("usia_pensiun"))
      uipRegisterCIF.SetFieldValue("tgl_pensiun", uipMaster.GetFieldValue("tgl_pensiun"))
      uipRegisterCIF.SetFieldValue("tgl_pensiun_dipercepat", uipMaster.GetFieldValue("tgl_pensiun_dipercepat"))
      uipRegisterCIF.SetFieldValue("LTujuanBukaRekening.tujuan_buka_rekening", uipMaster.GetFieldValue("LTujuanBukaRekening.tujuan_buka_rekening"))
      uipRegisterCIF.SetFieldValue("LTujuanBukaRekening.keterangan", uipMaster.GetFieldValue("LTujuanBukaRekening.keterangan"))
      uipRegisterCIF.SetFieldValue("tujuan_pembukaan_rekening", uipMaster.GetFieldValue("tujuan_pembukaan_rekening"))
      uipRegisterCIF.SetFieldValue("kirim_statemen", uipMaster.GetFieldValue("kirim_statemen"))
      uipRegisterCIF.SetFieldValue("confidential_code", uipMaster.GetFieldValue("confidential_code"))
      
      uipRegisterCIF.SetFieldValue("ISPESERTAPENGALIHAN", uipMaster.GetFieldValue("ISPESERTAPENGALIHAN"))
      uipRegisterCIF.SetFieldValue("LLDPLain.kode_dp", uipMaster.GetFieldValue("LLDPLain.kode_dp"))
      uipRegisterCIF.SetFieldValue("LLDPLain.nama_dp", uipMaster.GetFieldValue("LLDPLain.nama_dp"))
      uipRegisterCIF.SetFieldValue("LKelompok.kode_kelompok", uipMaster.GetFieldValue("LKelompok.kode_kelompok"))
      uipRegisterCIF.SetFieldValue("LKelompok.nama_kelompok", uipMaster.GetFieldValue("LKelompok.nama_kelompok"))
      
    else:
      #mode edit
      form.GetControlByName('pData.no_referensi').ReadOnly = 1
      form.GetControlByName('pData.no_referensi').Color = -2147483624

def validateForm(form):
  app = form.ClientApplication
  uipRegisterCIF = form.GetUIPartByName('uipRegisterCIF')
  uipMaster = form.GetUIPartByName('uipMaster')
  uipNasabahDPLK = form.GetUIPartByName('uipNasabahDPLK')
  
  """sumber dana"""
  #if uipRegisterCIF.GetFieldValue("no_referensi") in ['', 0, None]:
  #  app.ShowMessage('Nomor Referensi masih kosong')
  #  return False
          
  """tanggal lahir"""
  if uipNasabahDPLK.tanggal_lahir in [[], None]:
    app.ShowMessage('Tanggal Lahir masih kosong, proses tidak dapat dilanjutkan...')
    return False
  
  """sumber dana"""
  if uipRegisterCIF.GetFieldValue("LSumberDana.sumber_dana") in ['', 0, None]:
    app.ShowMessage('Sumber Dana masih kosong')
    return False
          
  """usia pensiun"""
  if uipRegisterCIF.usia_pensiun in ['', 0, None]:
    app.ShowMessage('Usia Pensiun masih kosong, proses tidak dapat dilanjutkan...')
    return False
          
  """cek kiriman statemen"""
  if uipRegisterCIF.kirim_statemen == 'K' and uipMaster.LNasabahDPLKCorporate.IsNull:
    #bukan nasabah korporat tapi statemen minta dikirim ke alamat kantor
    form.ShowMessage('Peserta mendaftar tidak sebagai anggota peserta korporat manapun. '\
      'Untuk itu, Statemen tidak bisa dikirim ke alamat Kantor (Korporat)!')
    return False
  
  if uipRegisterCIF.kirim_statemen == 'R' and uipNasabahDPLK.alamat_surat_jalan == None:
    #kirim statemen ke rumah, tetapi alamat surat masih kosong
    form.ShowMessage('Alamat Surat masih kosong. '\
      'Untuk itu, Statemen tidak bisa dikirim ke alamat Rumah (Alamat Surat)!')
    return False
    
  """cek tanggal: tanggal lahir, tanggal pensiun (usia pensiun terkait tanggal lahir)"""
  floatTglNow = app.ModDateTime.Now()
  y,m,d = uipNasabahDPLK.tanggal_lahir[:3]
  floatTglPensiun = app.ModDateTime.EncodeDate(y + uipRegisterCIF.usia_pensiun, m, d)
  
  """cek usia peserta"""
  usiaPeserta = (floatTglNow - app.ModDateTime.EncodeDate(y,m,d))/365
  if usiaPeserta < 18:
    form.ShowMessage('Usia peserta belum 18 Tahun!')
    return False

  if uipNasabahDPLK.tanggal_lahir[:3] > \
    app.ModDateTime.DecodeDate(floatTglNow)[:3]:
    form.ShowMessage('Tanggal lahir peserta tidak boleh melebihi tanggal hari ini!')
    return False
  
  if app.ModDateTime.DecodeDate(floatTglPensiun)[:3] < \
    app.ModDateTime.DecodeDate(floatTglNow)[:3]:
    form.ShowMessage('Tanggal saat peserta akan pensiun telah terlewati. '\
      'Usia pensiun yang diinputkan tidak valid!')
    return False
  
  return True
    
def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterCIF = form.GetUIPartByName('uipRegisterCIF')

  isValid = validateForm(form)
  if not isValid:
    return
      
  if uipRegisterCIF.mode not in ['view','auth']:
    #mode New or Edit
    form.CommitBuffer()
    form.PostResult()
  elif uipRegisterCIF.mode == 'auth':
    #mode auth, go otorisasi
    app.ExecuteScript('transaction/registercif_auth',app.CreateValues(['id',\
      uipRegisterCIF.registercif_id]))
  #else: mode view, do nothing

  sender.ExitAction = 1

def btnCancelClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterCIF = form.GetUIPartByName('uipRegisterCIF')

  if uipRegisterCIF.mode == 'auth':
    dlg = app.ConfirmDialog('Anda yakin membatalkan %s peserta %s %s?'\
      % (sender.OwnerForm.Caption, uipRegisterCIF.GetFieldValue('LNasabahDPLK.no_peserta'),\
      uipRegisterCIF.GetFieldValue('LNasabahDPLK.nama_lengkap')))
    if dlg:
      # batalkan hasil koreksi iuran peserta / pemberi kerja
      app.ExecuteScript('transaction/registercif_del',app.CreateValues(['id',\
        uipRegisterCIF.registercif_id]))
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2

def UsiaPensiunExit(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterCIF = form.GetUIPartByName('uipRegisterCIF')
  uipMaster = form.GetUIPartByName('uipMaster')
  uipNasabahDPLK = form.GetUIPartByName('uipNasabahDPLK')

  """usia pensiun"""
  if uipRegisterCIF.usia_pensiun in ['', 0, None]:
    app.ShowMessage('Usia Pensiun masih kosong, proses tidak dapat dilanjutkan...')
    return False
          
  """cek tanggal lahir"""
  if uipNasabahDPLK.tanggal_lahir in [None,[]]:
    app.ShowMessage('Tanggal Lahir masih kosong, tidak bisa menentukan tanggal pensiun dan tanggal pensiun dipercepat.')
    uipRegisterCIF.tgl_pensiun = uipRegisterCIF.tgl_pensiun_dipercepat = None
    return

  y, m, d = uipNasabahDPLK.tanggal_lahir[:3]
  y += uipRegisterCIF.usia_pensiun
  if (m == 2) and (d == 29) and (not app.ModDateTime.IsLeapYear(y)):
    # tanggal 29 februari, tetapi tahun yang akan datang bukan tahun kabisat
    # dibulatkan menjadi tanggal 28 februari
    d = 28

  uipRegisterCIF.tgl_pensiun = app.ModDateTime.EncodeDate(y,m,d)
  uipRegisterCIF.tgl_pensiun_dipercepat = app.ModDateTime.EncodeDate(y-10,m,d)

