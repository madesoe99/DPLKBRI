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
  form.Caption = 'Lihat Detil Status ' + form.Caption

def SetControlsForAuth(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetPanelByName('pDataBaru').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnClose').Cancel = 1
  form.Caption = 'Otorisasi ' + form.Caption

def FormShow(form, parameter):
  app = form.ClientApplication
  uipRegisterCIF = form.GetUIPartByName('uipRegisterCIF')
  uipMaster = form.GetUIPartByName('uipMaster')
  uipRekeningAutoDebet = form.GetUIPartByName('uipRekeningAutoDebet')

  uipRegisterCIF.Edit()
  uipRegisterCIF.mode = parameter.FirstRecord.mode

  if uipRegisterCIF.mode in ['view','auth']:
    if uipRegisterCIF.jenis_transaksi == 'O':
      form.Caption = 'Penutupan Autodebet'

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

      uipRegisterCIF.no_rekening = uipRekeningAutoDebet.no_rekening
      uipRegisterCIF.nama_rekening = uipRekeningAutoDebet.nama_rekening
      uipRegisterCIF.tanggal_autodebet = uipRekeningAutoDebet.tanggal_autodebet

      if uipMaster.status_autodebet == 'T':
        # sudah autodebet, transaksi berhenti autodebet
        form.GetPanelByName('pDataBaru').SetAllControlsReadOnly()
        form.Caption = 'Penutupan Autodebet'
        uipRegisterCIF.jenis_transaksi = 'O'
      else:
        uipRegisterCIF.jenis_transaksi = 'R'
        form.GetControlByName('pButton.btnOK').Enabled = \
        form.GetControlByName('pButton.btnOK').Default = 0
    else:
      #mode edit
      form.GetControlByName('pData.no_referensi').ReadOnly = 1
      form.GetControlByName('pData.no_referensi').Color = -2147483624

      if uipRegisterCIF.jenis_transaksi == 'O':
        form.GetPanelByName('pDataBaru').SetAllControlsReadOnly()
        form.Caption = 'Penutupan Autodebet'

def bCekRekeningClick(sender):
  app = sender.OwnerForm.ClientApplication
  uipT = sender.OwnerForm.GetUIPartByName('uipRegisterCIF')

  #cek field nomor rekening autodebet
  if uipT.no_rekening in [None,'']:
    #belum ada nomor rekening
    app.ShowMessage('Nomor Rekening Autodebet masih kosong, mohon diisi dahulu.')
  else:
    #nomor rekening sudah ada
    res = app.ExecuteScript('transaksi/CekRekeningCoreBanking',\
      app.CreateValues(['noRekening',uipT.no_rekening]))

    uipT.Edit()
    uipT.nama_rekening = res.FirstRecord.namaPemilikRekening
    if uipT.nama_rekening != 'Rekening tidak terdefinisi':
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
  uipRegisterCIF = form.GetUIPartByName('uipRegisterCIF')

  if uipRegisterCIF.mode not in ['view','auth']:
    #mode New or Edit

    #checking nomor referensi
    if uipRegisterCIF.no_referensi in ['',None]:
      form.ShowMessage('Nomor Referensi masih kosong. Mohon untuk diisi.')
      return
      
    #cek nomor rekening, nama rekening, tanggal autodebet
    if uipRegisterCIF.no_rekening in ['',None] or \
      uipRegisterCIF.nama_rekening in ['',None] or \
      uipRegisterCIF.tanggal_autodebet in ['',None]:
      form.ShowMessage('Diantara data Auto Debet masih kosong. Mohon untuk diisi dahulu.')
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
      # batalkan pendaftaran / penyudahan status autodebet
      app.ExecuteScript('transaction/registercif_del',app.CreateValues(['id',\
        uipRegisterCIF.registercif_id]))
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2

