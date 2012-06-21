def SetControlsForView(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  #form.gPaketBaru.ReadOnly = 1
  form.GetPanelByName('gPaketBaru').SetAllControlsReadOnly()
  form.GetPanelByName('gPaketBaru').SuppressHelpLine = 1
  
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
  #form.gPaketBaru.ReadOnly = 1
  form.GetPanelByName('gPaketBaru').SetAllControlsReadOnly()
  form.GetPanelByName('gPaketBaru').SuppressHelpLine = 1
  
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
  if uipRegisterCIF.mode == 'view':
    SetControlsForView(form)
  elif uipRegisterCIF.mode == 'auth':
    SetControlsForAuth(form)
  else:
    #mode New atau Edit
    uipRegisterCIF.user_id = app.UserID

    dh = app.ExecuteScript('getsessioninfo',app.CreateValues(['id',1]))
    uipRegisterCIF.terminal_id = dh.FirstRecord.sessioninfo

    if uipRegisterCIF.mode == 'new':
      uipRegisterCIF.SetFieldValue('LNasabahDPLK.no_peserta',uipMaster.no_peserta)
    else:
      form.GetControlByName('pData.no_referensi').ReadOnly = 1
      form.GetControlByName('pData.no_referensi').Color = -2147483624

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterCIF = form.GetUIPartByName('uipRegisterCIF')

  if uipRegisterCIF.mode not in ['view','auth']:
    #mode New or edit

    #checking nomor referensi
    if uipRegisterCIF.no_referensi in ['',None]:
      form.ShowMessage('Nomor Referensi masih kosong. Mohon untuk diisi.')
      return

    #cek transaction batch
    if uipRegisterCIF.GetFieldValue('LTransactionBatch.ID_TransactionBatch') in [None,'']:
      form.ShowMessage('Batch Transaksi masih kosong. Mohon untuk diisi dahulu.')
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
    dlg = app.ConfirmDialog('Anda yakin membatalkan Pemindahan Paket Investasi peserta %s?' \
      % (uipRegisterCIF.GetFieldValue('LNasabahDPLK.no_peserta')))
    if dlg:
      # batalkan pindah paket investasi
      app.ExecuteScript('transaction/registercif_del',app.CreateValues(['id',\
        uipRegisterCIF.registercif_id]))
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2
