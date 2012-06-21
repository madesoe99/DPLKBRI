def SetControlsForView(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetPanelByName('gDetails').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnOK').Enabled = 0
  form.GetControlByName('pButton.btnOK').Default = 0
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Enabled = 0
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnClose').Caption = '&Tutup'
  form.GetControlByName('pButton.btnClose').Default = 1
  form.Caption = 'Lihat Detil Hasil ' + form.Caption

def SetControlsForAuth(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetPanelByName('gDetails').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.Caption = 'Otorisasi Hasil ' + form.Caption

def FormShow(form, parameter):
  app = form.ClientApplication
  uipRegisterCIF = form.GetUIPartByName('uipRegisterCIF')

  uipRegisterCIF.Edit()
  uipRegisterCIF.mode = parameter.FirstRecord.mode

  if uipRegisterCIF.mode == 'view':
    SetControlsForView(form)
  elif uipRegisterCIF.mode == 'auth':
    SetControlsForAuth(form)
  else:
    #mode new or edit
    uipRegisterCIF.user_id = app.UserID

    dh = app.ExecuteScript('getsessioninfo',app.CreateValues(['id',1]))
    uipRegisterCIF.terminal_id = dh.FirstRecord.sessioninfo

    if uipRegisterCIF.mode == 'new':
      uipMaster = form.GetUIPartByName('uipMaster')

      uipRegisterCIF.SetFieldValue('LNasabahDPLK.no_peserta',uipMaster.no_peserta)
      uipRegisterCIF.SetFieldValue('LNasabahDPLK.nama_lengkap',uipMaster.nama_lengkap)

      uipAhliWaris = form.GetUIPartByName('uipAhliWaris')
      uipRegisterAhliWarisDetail = form.GetUIPartByName('uipRegisterAhliWarisDetail')
      uipAhliWaris.First()
      while not uipAhliWaris.Eof:
        uipRegisterAhliWarisDetail.Append()
        
        uipAhliWaris.CopyAttributes(uipRegisterAhliWarisDetail,\
          'nomor_urut_prioritas;nama_lengkap;tanggal_lahir;jenis_kelamin;'\
          'status_ahli_waris;hubungan_keluarga;keterangan'\
        )

        uipAhliWaris.Next()
    else:
      #mode edit
      form.GetControlByName('pData.no_referensi').ReadOnly = 1
      form.GetControlByName('pData.no_referensi').Color = -2147483624

def RAWBeforePost(uipRegisterAhliWarisDetail):
  app = uipRegisterAhliWarisDetail.OwnerForm.ClientApplication
  
  if uipRegisterAhliWarisDetail.tanggal_lahir != None and \
    uipRegisterAhliWarisDetail.tanggal_lahir[:3] > \
    app.ModDateTime.DecodeDate(app.ModDateTime.Now())[:3]:
    raise 'Pesan Kesalahan','Tanggal lahir ahli waris tidak boleh melebihi tanggal hari ini!'

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterCIF = form.GetUIPartByName('uipRegisterCIF')

  if uipRegisterCIF.mode not in ['view','auth']:
    #mode new or edit

    #checking nomor referensi
    if uipRegisterCIF.no_referensi in ['',None]:
      form.ShowMessage('Nomor Referensi masih kosong. Mohon untuk diisi.')
      return

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
    dlg = app.ConfirmDialog('Anda yakin membatalkan hasil koreksi ahli waris peserta %s %s?'\
      % (uipRegisterCIF.GetFieldValue('LNasabahDPLK.no_peserta'),\
      uipRegisterCIF.GetFieldValue('LNasabahDPLK.nama_lengkap')))
    if dlg:
      # batalkan hasil koreksi ahli waris
      app.ExecuteScript('transaction/registercif_del',app.CreateValues(['id',\
        uipRegisterCIF.registercif_id]))
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2

