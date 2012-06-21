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
  form.GetControlByName('pButton.btnClose').Cancel = 1
  form.Caption = 'Lihat Register Tutup Investasi'
  SetSelectorReadOnly(form)

def SetControlsForAuth(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnClose').Cancel = 1
  form.Caption = 'Otorisasi Register Tutup Investasi'
  SetSelectorReadOnly(form)

def SetControlsForViewDoc(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Tutup'
  form.GetControlByName('pButton.btnOK').Cancel = 1
  form.GetControlByName('pButton.btnCancel').Visible = 0
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  SetSelectorReadOnly(form)

def UnhideControls(form):
  form.GetControlByName('pData.mutasi_kredit').Visible = 1
  form.GetControlByName('pRegister.tgl_otorisasi').Visible = 1
  form.GetControlByName('pRegister.user_id_auth').Visible = 1
  form.GetControlByName('pRegister.terminal_id_auth').Visible = 1

def SetSelectorReadOnly(form):
  form.GetControlByName('pSelector.LInvestasi').Enabled = 0
  #form.GetPanelByName('pSelector').SetAllControlsReadOnly()

def SetInvCateg(form, kode_jns_investasi):
  uipTransPiutangInvestasi = form.GetUIPartByName('uipTransPiutangInvestasi')

  uipTransPiutangInvestasi.Edit()
  uipTransPiutangInvestasi.kode_jns_investasi = kode_jns_investasi

def FormShow(form, parameter):
  # set caption
  form.Caption = parameter.FirstRecord.caption

  uipTransPiutangInvestasi = form.GetUIPartByName('uipTransPiutangInvestasi')

  uipTransPiutangInvestasi.Edit()
  uipTransPiutangInvestasi.mode = parameter.FirstRecord.mode

  if (uipTransPiutangInvestasi.mode == 'new'):
    if uipTransPiutangInvestasi.GetFieldValue('LInvestasi.id_investasi'):
      SetSelectorReadOnly(form)
    else:
      SetInvCateg(form, parameter.FirstRecord.inv)

  if uipTransPiutangInvestasi.mode == 'viewdoc':
    #form.Caption = 'Lihat Transaksi Tutup Investasi'
    SetControlsForViewDoc(form)
    UnhideControls(form)
  else:
    if uipTransPiutangInvestasi.mode == 'view':
      SetControlsForView(form)
    elif uipTransPiutangInvestasi.mode == 'auth':
      SetControlsForAuth(form)
    elif uipTransPiutangInvestasi.mode == 'edit':
      SetSelectorReadOnly(form)
      form.Caption = 'Koreksi Register Tutup Investasi'

def LInvestasiAfterLookup(sender, linkui):
  form = sender.OwnerForm

  uipTransPiutangInvestasi = form.GetUIPartByName('uipTransPiutangInvestasi')
  uipTransPiutangInvestasi.Edit()
  uipTransPiutangInvestasi.SetFieldValue('LPihakKetiga.kode_pihak_ketiga',  uipTransPiutangInvestasi.GetFieldValue('LInvestasi.kode_pihak_ketiga'))
  uipTransPiutangInvestasi.SetFieldValue('LPihakKetiga.nama_pihak_ketiga', uipTransPiutangInvestasi.GetFieldValue('LInvestasi.LPihakKetiga.nama_pihak_ketiga'))
  uipTransPiutangInvestasi.SetFieldValue('LPaketInvestasi.kode_paket_investasi', uipTransPiutangInvestasi.GetFieldValue('LInvestasi.kode_paket_investasi'))
  uipTransPiutangInvestasi.SetFieldValue('LPaketInvestasi.nama_paket_investasi', uipTransPiutangInvestasi.GetFieldValue('LInvestasi.LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi'))
  uipTransPiutangInvestasi.SetFieldValue('LJenisInvestasi.kode_jns_investasi', uipTransPiutangInvestasi.GetFieldValue('LInvestasi.kode_jns_investasi'))
  uipTransPiutangInvestasi.SetFieldValue('LJenisInvestasi.nama_jns_investasi', uipTransPiutangInvestasi.GetFieldValue('LInvestasi.LRincianPaketInvestasi.LJenisInvestasi.nama_jns_investasi'))

  uipInvestasi = form.GetUIPartByName('uipInvestasi')
  uipInvestasi.Edit()
  uipInvestasi.akum_nominal = uipTransPiutangInvestasi.GetFieldValue('LInvestasi.akum_nominal')
  uipInvestasi.akum_piutangLR = uipTransPiutangInvestasi.GetFieldValue('LInvestasi.akum_piutangLR')
  uipInvestasi.akum_LR = uipTransPiutangInvestasi.GetFieldValue('LInvestasi.akum_LR')

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipTransPiutangInvestasi = form.GetUIPartByName('uipTransPiutangInvestasi')

  if uipTransPiutangInvestasi.mode == 'viewdoc':
    sender.ExitAction = 2
  else:
    if uipTransPiutangInvestasi.mode not in ['view','auth']:
      form.CommitBuffer()

      if uipTransPiutangInvestasi.mode == 'new':
        uipTransPiutangInvestasi.Edit()
        uipTransPiutangInvestasi.__SYSFLAG = 'N'

      form.PostResult()

      sender.ExitAction = 1
    elif uipTransPiutangInvestasi.mode == 'auth':
      dlg = app.ConfirmDialog('Anda yakin menyetujui Penutupan Investasi ini?')
      if dlg:
        # otorisasi
        app.ExecuteScript('investasi/transaksi/tutupinv_auth',\
          app.CreateValues(['id',uipTransPiutangInvestasi.id_transaksiinvestasi])\
        )
        sender.ExitAction = 1

def btnCancelClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipTransPiutangInvestasi = form.GetUIPartByName('uipTransPiutangInvestasi')

  if uipTransPiutangInvestasi.mode == 'auth':
    dlg = app.ConfirmDialog('Anda yakin membatalkan Penutupan Investasi ini?')
    if dlg:
      # hapus/tolak
      #app.ExecuteScript('investasi/transaksi/tutupinv_del',\
      app.ExecuteScript('investasi/transaksi/transpiutanginv_del',\
        app.CreateValues(['id',uipTransPiutangInvestasi.id_transaksiinvestasi])\
      )
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2

