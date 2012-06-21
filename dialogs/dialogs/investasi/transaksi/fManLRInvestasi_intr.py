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
  form.Caption = 'Lihat Register LR Investasi Manual'

def SetControlsForAuth(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnClose').Cancel = 1
  form.Caption = 'Otorisasi Register LR Investasi Manual'

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
  uipTransLRInvestasi = form.GetUIPartByName('uipTransLRInvestasi')

  uipTransLRInvestasi.Edit()
  uipTransLRInvestasi.mode = parameter.FirstRecord.mode

  if uipTransLRInvestasi.mode == 'viewdoc':
    form.Caption = 'Lihat Transaksi LR Investasi Manual'
    SetControlsForViewDoc(form)
    UnhideControls(form)
  else:
    if uipTransLRInvestasi.mode == 'view':
      SetControlsForView(form)
    elif uipTransLRInvestasi.mode == 'auth':
      SetControlsForAuth(form)
    elif uipTransLRInvestasi.mode == 'edit':
      form.Caption = 'Koreksi Register LR Investasi Manual'

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipTransLRInvestasi = form.GetUIPartByName('uipTransLRInvestasi')

  if uipTransLRInvestasi.mode == 'viewdoc':
    sender.ExitAction = 2
  else:
    if uipTransLRInvestasi.mode not in ['view','auth']:
      form.CommitBuffer()

      if uipTransLRInvestasi.mode == 'new':
        uipTransLRInvestasi.Edit()
        uipTransLRInvestasi.__SYSFLAG = 'N'

      form.PostResult()

      sender.ExitAction = 1
    elif uipTransLRInvestasi.mode == 'auth':
      dlg = app.ConfirmDialog('Anda yakin menyetujui LR Investasi secara Manual ini?')
      if dlg:
        # otorisasi
        app.ExecuteScript('investasi/transaksi/manlrinvestasi_auth',\
          app.CreateValues(['id',uipTransLRInvestasi.id_transaksiinvestasi])\
        )
        sender.ExitAction = 1

def btnCancelClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipTransLRInvestasi = form.GetUIPartByName('uipTransLRInvestasi')

  if uipTransLRInvestasi.mode == 'auth':
    dlg = app.ConfirmDialog('Anda yakin membatalkan LR Investasi secara Manual ini?')
    if dlg:
      # hapus/tolak
      #app.ExecuteScript('investasi/transaksi/manlrinvestasi_del',\
      app.ExecuteScript('investasi/transaksi/translrinvestasi_del',\
        app.CreateValues(['id',uipTransLRInvestasi.id_transaksiinvestasi])\
      )
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2

