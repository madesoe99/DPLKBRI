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
  form.Caption = 'Lihat Register Kapitalisir Investasi'

def SetControlsForAuth(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnClose').Cancel = 1
  form.Caption = 'Otorisasi Register Kapitalisir Investasi'

def SetControlsForViewDoc(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Tutup'
  form.GetControlByName('pButton.btnOK').Cancel = 1
  form.GetControlByName('pButton.btnCancel').Visible = 0
  form.GetControlByName('pButton.btnCancel').Cancel = 0

def UnhideControls(form):
  form.GetControlByName('pData.mutasi_debet').Visible = 1
  form.GetControlByName('pRegister.tgl_otorisasi').Visible = 1
  form.GetControlByName('pRegister.user_id_auth').Visible = 1
  form.GetControlByName('pRegister.terminal_id_auth').Visible = 1

def FormShow(form, parameter):
  uipTransPiutangInvestasi = form.GetUIPartByName('uipTransPiutangInvestasi')

  uipTransPiutangInvestasi.Edit()
  uipTransPiutangInvestasi.mode = parameter.FirstRecord.mode

  if uipTransPiutangInvestasi.mode == 'viewdoc':
    form.Caption = 'Lihat Transaksi Kapitalisir Investasi'
    SetControlsForViewDoc(form)
    UnhideControls(form)
  else:
    if uipTransPiutangInvestasi.mode == 'view':
      SetControlsForView(form)
    elif uipTransPiutangInvestasi.mode == 'auth':
      SetControlsForAuth(form)
    elif uipTransPiutangInvestasi.mode == 'edit':
      form.Caption = 'Koreksi Register Kapitalisir Investasi'

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
      dlg = app.ConfirmDialog('Anda yakin menyetujui Kapitalisir Investasi ini?')
      if dlg:
        # otorisasi
        app.ExecuteScript('investasi/transaksi/rolloverinv_auth',\
          app.CreateValues(['id',uipTransPiutangInvestasi.id_transaksiinvestasi])\
        )
        sender.ExitAction = 1

def btnCancelClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipTransPiutangInvestasi = form.GetUIPartByName('uipTransPiutangInvestasi')

  if uipTransPiutangInvestasi.mode == 'auth':
    dlg = app.ConfirmDialog('Anda yakin membatalkan Kapitalisir Investasi ini?')
    if dlg:
      # hapus/tolak
      #app.ExecuteScript('investasi/transaksi/rolloverinv_del',\
      app.ExecuteScript('investasi/transaksi/transpiutanginv_del',\
        app.CreateValues(['id',uipTransPiutangInvestasi.id_transaksiinvestasi])\
      )
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2

