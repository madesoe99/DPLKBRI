def SetControlsForView(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetPanelByName('pStatusKerja').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnOK').Enabled = 0
  form.GetControlByName('pButton.btnOK').Default = 0
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Enabled = 0
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnClose').Caption = '&Tutup'
  form.GetControlByName('pButton.btnClose').Default = 1
  form.Caption = 'Lihat Detil Status ' + form.Caption

def SetControlsForAuth(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetPanelByName('pStatusKerja').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.Caption = 'Otorisasi Status ' + form.Caption

def FormShow(form, parameter):
  app = form.ClientApplication
  uipRegisterCIF = form.GetUIPartByName('uipRegisterCIF')
  uipMaster = form.GetUIPartByName('uipMaster')

  uipRegisterCIF.Edit()
  uipRegisterCIF.mode = parameter.FirstRecord.mode

  if uipRegisterCIF.mode in ['view','auth']:
    if uipRegisterCIF.jenis_transaksi == 'O':
      form.GetPanelByName('pStatusKerja').GetControlByName('LNasabahDPLKCorporate').Enabled = 0
      form.Caption = 'PHK dari Perusahaan'

    if uipRegisterCIF.mode == 'view':
      SetControlsForView(form)
    else:
      #mode auth
      SetControlsForAuth(form)
  else:
    #mode New or Edit
    uipRegisterCIF.user_id = app.UserID

    dh = app.ExecuteScript('getsessioninfo',app.CreateValues(['id',1]))
    uipRegisterCIF.terminal_id = dh.FirstRecord.sessioninfo

    if uipRegisterCIF.mode == 'new':
      uipRegisterCIF.SetFieldValue('LNasabahDPLK.no_peserta',uipMaster.no_peserta)
      uipRegisterCIF.SetFieldValue('LNasabahDPLK.nama_lengkap',uipMaster.nama_lengkap)

      if uipMaster.GetFieldValue('LNasabahDPLKCorporate.kode_nasabah_corporate') <> None:
        # sudah menjadi peserta perusahaan, transaksi PHK
        form.GetPanelByName('pStatusKerja').GetControlByName('LNasabahDPLKCorporate').Enabled = 0
        form.Caption = 'PHK dari Perusahaan'
        uipRegisterCIF.jenis_transaksi = 'O'
      else:
        uipRegisterCIF.jenis_transaksi = 'R'
    else:
      #mode Edit
      form.GetPanelByName('pData').GetControlByName('no_referensi').ReadOnly = 1
      form.GetPanelByName('pData').GetControlByName('no_referensi').Color = -2147483624

      if uipRegisterCIF.jenis_transaksi == 'O':
        form.GetPanelByName('pStatusKerja').GetControlByName('LNasabahDPLKCorporate').Enabled = 0
        form.Caption = 'PHK dari Perusahaan'

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterCIF = form.GetUIPartByName('uipRegisterCIF')

  if uipRegisterCIF.mode not in ['view','auth']:
    #mode New or Edit
    
    #checking nomor referensi
    if uipRegisterCIF.no_referensi in ['',None]:
      form.ShowMessage('Nomor Referensi masih kosong. Mohon untuk diisi.')
      return
      
    #checking perusahaan
    if uipRegisterCIF.jenis_transaksi == 'R' and \
      uipRegisterCIF.GetFieldValue('LNasabahDPLKCorporate.kode_nasabah_corporate') in ['',None]:
      #status peserta belum ter-PHK
      form.ShowMessage('Kolom Perusahaan masih kosong. Mohon untuk diisi.')
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
    dlg = app.ConfirmDialog('Anda yakin membatalkan %s peserta %s %s?' \
      % (sender.OwnerForm.Caption, uipRegisterCIF.GetFieldValue('LNasabahDPLK.no_peserta'),\
      uipRegisterCIF.GetFieldValue('LNasabahDPLK.nama_lengkap')))
    if dlg:
      # batalkan PHK dari / Pendaftaran ke Perusahaan
      app.ExecuteScript('transaction/registercif_del',app.CreateValues(['id',\
        uipRegisterCIF.registercif_id]))
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2

