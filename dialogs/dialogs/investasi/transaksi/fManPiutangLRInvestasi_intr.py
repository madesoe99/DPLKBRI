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
  form.Caption = 'Lihat Register Piutang LR Investasi Manual'

def SetControlsForAuth(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnClose').Cancel = 1
  form.Caption = 'Otorisasi Register Piutang LR Investasi Manual'

def SetControlsForViewDoc(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Tutup'
  form.GetControlByName('pButton.btnOK').Cancel = 1
  form.GetControlByName('pButton.btnCancel').Visible = 0
  form.GetControlByName('pButton.btnCancel').Cancel = 0

def UnhideControls(form):
  form.GetControlByName('pRegister.tgl_otorisasi').Visible = 1
  form.GetControlByName('pRegister.user_id_auth').Visible = 1
  form.GetControlByName('pRegister.terminal_id_auth').Visible = 1

def FormShow(form, parameter):
  uipTransPiutangLRInvestasi = form.GetUIPartByName('uipTransPiutangLRInvestasi')

  uipTransPiutangLRInvestasi.Edit()
  uipTransPiutangLRInvestasi.mode = parameter.FirstRecord.mode

  if uipTransPiutangLRInvestasi.mode == 'viewdoc':
    form.Caption = 'Lihat Transaksi Piutang LR Investasi Manual'
    SetControlsForViewDoc(form)
    UnhideControls(form)
  else:
    if uipTransPiutangLRInvestasi.mode == 'view':
      SetControlsForView(form)
    elif uipTransPiutangLRInvestasi.mode == 'auth':
      SetControlsForAuth(form)
    elif uipTransPiutangLRInvestasi.mode == 'edit':
      form.Caption = 'Koreksi Register Piutang LR Investasi Manual'

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipTransPiutangLRInvestasi = form.GetUIPartByName('uipTransPiutangLRInvestasi')

  if uipTransPiutangLRInvestasi.mode == 'viewdoc':
    sender.ExitAction = 2
  else:
    if uipTransPiutangLRInvestasi.mode not in ['view','auth']:
      form.CommitBuffer()

      if uipTransPiutangLRInvestasi.mode == 'new':
        uipTransPiutangLRInvestasi.Edit()
        uipTransPiutangLRInvestasi.__SYSFLAG = 'N'

      form.PostResult()

      sender.ExitAction = 1
    elif uipTransPiutangLRInvestasi.mode == 'auth':
      dlg = app.ConfirmDialog('Anda yakin menyetujui Piutang LR Investasi secara Manual ini?')
      if dlg:
        # otorisasi
        app.ExecuteScript('investasi/transaksi/manpiutanglr_auth',\
          app.CreateValues(['id',uipTransPiutangLRInvestasi.id_transaksiinvestasi])\
        )
        sender.ExitAction = 1

def btnCancelClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipTransPiutangLRInvestasi = form.GetUIPartByName('uipTransPiutangLRInvestasi')

  if uipTransPiutangLRInvestasi.mode == 'auth':
    dlg = app.ConfirmDialog('Anda yakin membatalkan Piutang LR Investasi secara Manual ini?')
    if dlg:
      # hapus/tolak
      #app.ExecuteScript('investasi/transaksi/manpiutanglr_del',\
      app.ExecuteScript('investasi/transaksi/transpiutanglrinv_del',\
        app.CreateValues(['id',uipTransPiutangLRInvestasi.id_transaksiinvestasi])\
      )
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2

