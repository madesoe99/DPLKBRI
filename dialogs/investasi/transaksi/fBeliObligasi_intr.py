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
  form.Caption = 'Lihat Register Beli Obligasi'
  SetSelectorReadOnly(form)

def SetControlsForAuth(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnClose').Cancel = 1
  form.Caption = 'Otorisasi Register Beli Obligasi'
  SetSelectorReadOnly(form)

def SetControlsForViewDoc(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Tutup'
  form.GetControlByName('pButton.btnOK').Cancel = 1
  form.GetControlByName('pButton.btnCancel').Visible = 0
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  SetSelectorReadOnly(form)

def UnhideControls(form):
  form.GetControlByName('pRegister.tgl_otorisasi').Visible = 1
  form.GetControlByName('pRegister.user_id_auth').Visible = 1
  form.GetControlByName('pRegister.terminal_id_auth').Visible = 1

def SetSelectorReadOnly(form):
  form.GetControlByName('pSelector.LObligasi').Enabled = 0
  #form.GetPanelByName('pSelector').SetAllControlsReadOnly()

def FormShow(form, parameter):
  # set caption
  #form.Caption = parameter.FirstRecord.caption

  uipBeliObligasi = form.GetUIPartByName('uipBeliObligasi')

  uipBeliObligasi.Edit()
  uipBeliObligasi.mode = parameter.FirstRecord.mode

  if (uipBeliObligasi.mode == 'new'):
    if uipBeliObligasi.GetFieldValue('LObligasi.id_investasi'):
      SetSelectorReadOnly(form)

  if uipBeliObligasi.mode == 'viewdoc':
    form.Caption = 'Lihat Transaksi Beli Obligasi'
    SetControlsForViewDoc(form)
    UnhideControls(form)
  else:
    if uipBeliObligasi.mode == 'view':
      SetControlsForView(form)
    elif uipBeliObligasi.mode == 'auth':
      SetControlsForAuth(form)
    elif uipBeliObligasi.mode == 'edit':
      SetSelectorReadOnly(form)
      form.Caption = 'Koreksi Register Beli Obligasi'

def LObligasiAfterLookup(sender, linkui):
  form = sender.OwnerForm

  uipBeliObligasi = form.GetUIPartByName('uipBeliObligasi')
  uipBeliObligasi.Edit()
  uipBeliObligasi.SetFieldValue('LPihakKetiga.kode_pihak_ketiga',  uipBeliObligasi.GetFieldValue('LObligasi.kode_pihak_ketiga'))
  uipBeliObligasi.SetFieldValue('LPihakKetiga.nama_pihak_ketiga', uipBeliObligasi.GetFieldValue('LObligasi.LPihakKetiga.nama_pihak_ketiga'))
  uipBeliObligasi.SetFieldValue('LPaketInvestasi.kode_paket_investasi', uipBeliObligasi.GetFieldValue('LObligasi.kode_paket_investasi'))
  uipBeliObligasi.SetFieldValue('LPaketInvestasi.nama_paket_investasi', uipBeliObligasi.GetFieldValue('LObligasi.LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi'))

  uipObligasi = form.GetUIPartByName('uipObligasi')
  uipObligasi.Edit()
  uipObligasi.akum_nominal = uipBeliObligasi.GetFieldValue('LObligasi.akum_nominal')
  uipObligasi.akum_piutangLR = uipBeliObligasi.GetFieldValue('LObligasi.akum_piutangLR')
  uipObligasi.akum_LR = uipBeliObligasi.GetFieldValue('LObligasi.akum_LR')
  uipObligasi.harga_beli = uipBeliObligasi.GetFieldValue('LObligasi.harga_beli')
  uipObligasi.harga_pari = uipBeliObligasi.GetFieldValue('LObligasi.harga_pari')
  uipObligasi.jenis_obligasi = uipBeliObligasi.GetFieldValue('LObligasi.jenis_obligasi')
  uipObligasi.tgl_jatuh_tempo = uipBeliObligasi.GetFieldValue('LObligasi.tgl_jatuh_tempo')

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipBeliObligasi = form.GetUIPartByName('uipBeliObligasi')

  if uipBeliObligasi.mode == 'viewdoc':
    sender.ExitAction = 2
  else:
    if uipBeliObligasi.mode not in ['view','auth']:
      form.CommitBuffer()

      if uipBeliObligasi.mode == 'new':
        uipBeliObligasi.Edit()
        uipBeliObligasi.__SYSFLAG = 'N'

      form.PostResult()

      sender.ExitAction = 1
    elif uipBeliObligasi.mode == 'auth':
      dlg = app.ConfirmDialog('Anda yakin menyetujui Beli Obligasi ini?')
      if dlg:
        # otorisasi
        app.ExecuteScript('investasi/transaksi/transpiutanginv_auth',\
          app.CreateValues(['id',uipBeliObligasi.id_transaksiinvestasi])\
        )
        sender.ExitAction = 1

def btnCancelClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipBeliObligasi = form.GetUIPartByName('uipBeliObligasi')

  if uipBeliObligasi.mode == 'auth':
    dlg = app.ConfirmDialog('Anda yakin membatalkan Beli Obligasi ini?')
    if dlg:
      app.ExecuteScript('investasi/transaksi/transpiutanginv_del',\
        app.CreateValues(['id',uipBeliObligasi.id_transaksiinvestasi])\
      )
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2

