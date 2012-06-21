def SetControlsForView(form):
  form.GetPanelByName('pDataLeft').SetAllControlsReadOnly()
  form.GetPanelByName('pDataRight').SetAllControlsReadOnly()
  form.GetPanelByName('pDataIndukRegister').SetAllControlsReadOnly()
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
  form.Caption = 'Lihat Detil ' + form.Caption

def SetControlsForAuth(form):
  form.GetPanelByName('pDataLeft').SetAllControlsReadOnly()
  form.GetPanelByName('pDataRight').SetAllControlsReadOnly()
  form.GetPanelByName('pDataIndukRegister').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnClose').Cancel = 1
  form.Caption = 'Otorisasi ' + form.Caption

def FormShow(form, parameter):
  uipMaster = form.GetUIPartByName('uipMaster')
  uipRegisterCIF = form.GetUIPartByName('uipRegisterCIF')

  uipRegisterCIF.Edit()
  uipRegisterCIF.mode = parameter.FirstRecord.mode

  if uipRegisterCIF.mode in ['editdoc','new']:
    #mode New
    uipRegisterCIF.SetFieldValue('LNasabahDPLK.no_peserta',uipMaster.no_peserta)
    uipRegisterCIF.SetFieldValue('LNasabahDPLK.nama_lengkap',uipMaster.nama_lengkap)

    uipMaster.CopyAttributes(uipRegisterCIF,\
      'nama_lengkap;tempat_lahir;tanggal_lahir;jenis_kelamin;'\
      'golongan_darah;agama;pendidikan_terakhir;status_perkawinan;'\
      'ldaerahasal.kode_propinsi;ldaerahasal.nama_propinsi;'\
      'kewarganegaraan;no_identitas_diri;tgl_exp_identitas;'\
      'lkelompok.kode_kelompok;lkelompok.nama_kelompok;'\
      'alamat_email;NPWP;LLDPLain.kode_dp;LLDPLain.nama_dp'\
    )

  elif uipRegisterCIF.mode == 'edit':
    form.GetControlByName('pDataIndukRegister.no_referensi').ReadOnly = 1
    form.GetControlByName('pDataIndukRegister.no_referensi').Color = -2147483624
  elif uipRegisterCIF.mode == 'view':
    SetControlsForView(form)
  elif uipRegisterCIF.mode == 'auth':
    SetControlsForAuth(form)

def validateForm(form):
  app = form.ClientApplication
  uipRegisterCIF = form.GetUIPartByName('uipRegisterCIF')
  
  """nama lengkap peserta"""
  if uipRegisterCIF.nama_lengkap in ["", None]:
    app.ShowMessage('Nama Lengkap masih kosong')
    return False
  
  """tempat lahir"""
  if uipRegisterCIF.tempat_lahir in ["", None]:
    app.ShowMessage('Tempat Lahir masih kosong')
    return False
  
  """tanggal lahir"""
  if uipRegisterCIF.tanggal_lahir in [[], None]:
    app.ShowMessage('Tanggal Lahir masih kosong, proses tidak dapat dilanjutkan...')
    return False
  
  """jenis kelamin"""
  if uipRegisterCIF.jenis_kelamin in ["", None]:
    app.ShowMessage('Jenis Kelamin masih kosong')
    return False
  
  """cek usia peserta"""
  floatTglNow = app.ModDateTime.Now()
  y,m,d = uipRegisterCIF.tanggal_lahir[:3]
  usiaPeserta = (floatTglNow - app.ModDateTime.EncodeDate(y,m,d))/365
  if usiaPeserta < 18:
    app.ShowMessage('Usia peserta belum 18 Tahun!')
    return False

  if uipRegisterCIF.tanggal_lahir[:3] > \
    app.ModDateTime.DecodeDate(floatTglNow)[:3]:
    app.ShowMessage('Tanggal lahir peserta tidak boleh melebihi tanggal hari ini!')
    return False
  
  """nomor referensi"""
  if uipRegisterCIF.no_referensi in ["", None]:
    app.ShowMessage('Nomor Referensi masih kosong')
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
    if uipRegisterCIF.mode in ['editdoc','new']:
      uipRegisterCIF.Edit()
      # set sysflag supaya mode pemrosesannya adalah membuat regeditnasabahrekening baru
      uipRegisterCIF.SetFieldValue('__SYSFLAG', 'N')

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
    dlg = app.ConfirmDialog('Anda yakin membatalkan Koreksi Data Umum peserta %s %s?' \
      % (uipRegisterCIF.GetFieldValue('LNasabahDPLK.no_peserta'),\
      uipRegisterCIF.GetFieldValue('LNasabahDPLK.nama_lengkap')))
    if dlg:
      # batalkan koreksi data umum nasabah
      app.ExecuteScript('transaction/registercif_del',app.CreateValues(['id',\
        uipRegisterCIF.registercif_id]))
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2

