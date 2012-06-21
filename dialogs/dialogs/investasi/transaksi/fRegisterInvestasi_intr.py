def SetControlsForView(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
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
  form.Caption = 'Lihat Register Investasi'

def SetControlsForAuth(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnClose').Cancel = 1
  form.Caption = 'Otorisasi Register Investasi'

def FormShow(form, parameter):
  uipRegisterInvestasi = form.GetUIPartByName('uipRegisterInvestasi')
  
  uipRegisterInvestasi.Edit()
  uipRegisterInvestasi.mode = parameter.FirstRecord.mode

  if uipRegisterInvestasi.mode == 'view':
    SetControlsForView(form)
  elif uipRegisterInvestasi.mode == 'auth':
    SetControlsForAuth(form)
  elif uipRegisterInvestasi.mode == 'edit':
    form.Caption = 'Koreksi Register Investasi'

def LPaketInvestasiAfterLookup(sender, linkui):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterInvestasi = form.GetUIPartByName('uipRegisterInvestasi')

  kode_paket_investasi = uipRegisterInvestasi.GetFieldValue('LPaketInvestasi.kode_paket_investasi')
  dh = app.ExecuteScript('investasi/transaksi/rincianpaketinv',\
    app.CreateValues(['kode_paket_investasi',kode_paket_investasi])\
  )

  kode_jns_investasi = dh.FirstRecord.kode_jns_investasi
  if kode_jns_investasi <> '':
    uipRegisterInvestasi.SetFieldValue('LRincianPaketInvestasi.kode_paket_investasi',kode_paket_investasi)
    uipRegisterInvestasi.SetFieldValue('LRincianPaketInvestasi.kode_jns_investasi',kode_jns_investasi)
    uipRegisterInvestasi.SetFieldValue('LRincianPaketInvestasi.LJenisInvestasi.nama_jns_investasi',dh.FirstRecord.nama_jns_investasi)

  uipRegisterInvestasi.Edit()

def LRincianPaketInvestasiBeforeLookup(sender, linkui):
  openlookup = 1
  uipRegisterInvestasi = sender.OwnerForm.GetUIPartByName('uipRegisterInvestasi')
  if uipRegisterInvestasi.GetFieldValue('LPaketInvestasi.kode_paket_investasi') \
    in [None,'']:
    sender.OwnerForm.ShowMessage('Pilih dahulu Paket Investasi!')
    openlookup = 0
  
  return openlookup

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterInvestasi = form.GetUIPartByName('uipRegisterInvestasi')
  
  if uipRegisterInvestasi.mode not in ['view','auth']:
    form.CommitBuffer()

    if uipRegisterInvestasi.mode == 'new':
      uipRegisterInvestasi.Edit()
      uipRegisterInvestasi.__SYSFLAG = 'N'

    form.PostResult()

    sender.ExitAction = 1
  elif uipRegisterInvestasi.mode == 'auth':
    dlg = app.ConfirmDialog('Anda yakin mengotorisasi investasi baru ini?')
    if dlg:
      # otorisasi
      app.ExecuteScript('investasi/transaksi/registerinvestasi_auth',\
        app.CreateValues(['id',uipRegisterInvestasi.id_registerinvestasi])\
      )
      sender.ExitAction = 1

def btnCancelClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterInvestasi = form.GetUIPartByName('uipRegisterInvestasi')

  if uipRegisterInvestasi.mode == 'auth':
    dlg = app.ConfirmDialog('Anda yakin membatalkan register investasi baru ini?')
    if dlg:
      # hapus/tolak
      app.ExecuteScript('investasi/transaksi/registerinvestasi_del',\
        app.CreateValues(['id',uipRegisterInvestasi.id_registerinvestasi])\
      )
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2


