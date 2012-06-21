def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def SetControlsForView(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetPanelByName('pDataTransaksi').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnOK').Enabled = 0
  form.GetControlByName('pButton.btnOK').Default = 0
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Enabled = 0
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnClose').Caption = '&Tutup'
  form.GetControlByName('pButton.btnClose').Default = 1
  form.Caption = 'Lihat Detil ' + form.Caption

def SetControlsForAuth(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetPanelByName('pDataTransaksi').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.Caption = 'Otorisasi ' + form.Caption

def FormShow(form, parameter):
  app = form.ClientApplication
  uipRegisterCIF = form.GetUIPartByName('uipRegisterCIF')
  uipMaster = form.GetUIPartByName('uipMaster')

  uipRegisterCIF.Edit()
  uipRegisterCIF.mode = parameter.FirstRecord.mode

  if uipRegisterCIF.mode in ['view','auth']:
    if uipRegisterCIF.jenis_transaksi == 'O':
      form.GetControlByName('pDataTransaksi.alasan_berhenti').Visible = 1
      form.Caption = 'Penutupan Asuransi'

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
      uipRegisterCIF.SetFieldValue('LNasabahDPLK.nama_lengkap',uipMaster.GetFieldValue('LNasabahDPLK.nama_lengkap'))

      if uipMaster.status_asuransi == 'T':
        # sudah Asuransi, transaksi berhenti Asuransi
        form.GetControlByName('pDataTransaksi.alasan_berhenti').Visible = 1
        form.Caption = 'Penutupan Asuransi'
        uipRegisterCIF.jenis_transaksi = 'O'
      else:
        uipRegisterCIF.jenis_transaksi = 'R'
    else:
      #mode edit
      form.GetControlByName('pDataTransaksi.no_referensi').ReadOnly = 1
      form.GetControlByName('pDataTransaksi.no_referensi').Color = -2147483624

      if uipRegisterCIF.jenis_transaksi == 'O':
        form.GetControlByName('pDataTransaksi.alasan_berhenti').Visible = 1
        form.Caption = 'Penutupan Asuransi'

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

    form.CommitBuffer()
    form.PostResult()
    sender.ExitAction = 1
  elif uipRegisterCIF.mode == 'auth':
    #mode auth, go otorisasi
    keyobjconst = 'PObj:RegisterWasiatUmmat#REGISTERCIF_ID=%d' \
      % (uipRegisterCIF.registercif_id)

    aform = app.GetFormWithData('transaction/fRegisterWasiatUmmat_preauth',\
      'fRegisterWasiatUmmat_preauth',0,keyobjconst,'uipRegisterWasiatUmmat')
    #SetToCenterForm(form, aform.FormObject)
    if aform.Show() == 1:
      # eaQuitOK
      sender.ExitAction = 1
  #else: mode view, do nothing

def btnCancelClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterCIF = form.GetUIPartByName('uipRegisterCIF')

  if uipRegisterCIF.mode == 'auth':
    dlg = app.ConfirmDialog('Anda yakin membatalkan %s peserta %s %s?' \
      % (sender.OwnerForm.Caption, uipRegisterCIF.GetFieldValue('LNasabahDPLK.no_peserta'),\
      uipRegisterCIF.GetFieldValue('LNasabahDPLK.nama_lengkap')))
    if dlg:
      # batalkan pendaftaran / penyudahan Asuransi
      app.ExecuteScript('transaction/registercif_del',app.CreateValues(['id',\
        uipRegisterCIF.registercif_id]))
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2

