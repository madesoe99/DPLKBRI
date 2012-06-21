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
  form.Caption = 'Lihat Register Rollover Investasi'
  SetSelectorReadOnly(form)

def SetControlsForAuth(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnClose').Cancel = 1
  form.Caption = 'Otorisasi Register Rollover Investasi'
  SetSelectorReadOnly(form)

def SetControlsForViewDoc(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Tutup'
  form.GetControlByName('pButton.btnOK').Cancel = 1
  form.GetControlByName('pButton.btnCancel').Visible = 0
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  SetSelectorReadOnly(form)

def UnhideControls(form):
  form.GetControlByName('pData.mutasi_debet').Visible = 1
  form.GetControlByName('pRegister.tgl_otorisasi').Visible = 1
  form.GetControlByName('pRegister.user_id_auth').Visible = 1
  form.GetControlByName('pRegister.terminal_id_auth').Visible = 1

def SetSelectorReadOnly(form):
  form.GetControlByName('pSelector.LDeposito').Enabled = 0
  #form.GetPanelByName('pSelector').SetAllControlsReadOnly()

def FormShow(form, parameter):
  # set caption
  form.Caption = parameter.FirstRecord.caption

  uipRolloverDeposito = form.GetUIPartByName('uipRolloverDeposito')

  uipRolloverDeposito.Edit()
  uipRolloverDeposito.mode = parameter.FirstRecord.mode

  if uipRolloverDeposito.kapitalisir_rollover == 'T':
    form.GetControlByName('pData.no_rekening').Visible = 0

  if uipRolloverDeposito.mode == 'new':
    form.GetControlByName('pPrint.btnPrint').Visible = 0
    if uipRolloverDeposito.kapitalisir_rollover == 'T':
      uipRolloverDeposito.lakukan_kapitalisir = 'T'
    else:
      uipRolloverDeposito.lakukan_kapitalisir = 'F'

  #if uipRolloverDeposito.kapitalisir_rollover == 'T':
  #  form.GetControlByName('pData.lakukan_kapitalisir').Visible = 0

  if (uipRolloverDeposito.mode == 'new') \
    and uipRolloverDeposito.GetFieldValue('LDeposito.id_investasi'):
    SetSelectorReadOnly(form)

  if uipRolloverDeposito.mode == 'viewdoc':
    form.Caption = 'Lihat Transaksi Rollover Investasi'
    SetControlsForViewDoc(form)
    UnhideControls(form)
  else:
    if uipRolloverDeposito.mode == 'view':
      SetControlsForView(form)
    elif uipRolloverDeposito.mode == 'auth':
      SetControlsForAuth(form)
    elif uipRolloverDeposito.mode == 'edit':
      SetSelectorReadOnly(form)
      form.Caption = 'Koreksi Register Rollover Investasi'
    #elif uipRolloverDeposito.mode == 'new':
    #  form.

def LDepositoAfterLookup(sender, linkui):
  form = sender.OwnerForm

  uipRolloverDeposito = form.GetUIPartByName('uipRolloverDeposito')
  uipRolloverDeposito.Edit()

  uipRolloverDeposito.SetFieldValue('LPihakKetiga.kode_pihak_ketiga',  uipRolloverDeposito.GetFieldValue('LDeposito.kode_pihak_ketiga'))
  uipRolloverDeposito.SetFieldValue('LPihakKetiga.nama_pihak_ketiga', uipRolloverDeposito.GetFieldValue('LDeposito.LPihakKetiga.nama_pihak_ketiga'))
  uipRolloverDeposito.SetFieldValue('LPaketInvestasi.kode_paket_investasi', uipRolloverDeposito.GetFieldValue('LDeposito.kode_paket_investasi'))
  uipRolloverDeposito.SetFieldValue('LPaketInvestasi.nama_paket_investasi', uipRolloverDeposito.GetFieldValue('LDeposito.LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi'))

  uipRolloverDeposito.rollover_counter = uipRolloverDeposito.GetFieldValue('LDeposito.rollover_counter')
  uipRolloverDeposito.treatmentPokok = uipRolloverDeposito.GetFieldValue('LDeposito.treatmentPokok')
  uipRolloverDeposito.kapitalisir_rollover = uipRolloverDeposito.GetFieldValue('LDeposito.kapitalisir_rollover')

  if uipRolloverDeposito.mode == 'new':
    if uipRolloverDeposito.kapitalisir_rollover == 'T':
      uipRolloverDeposito.lakukan_kapitalisir = 'T'
    else:
      uipRolloverDeposito.lakukan_kapitalisir = 'F'

  #if uipRolloverDeposito.kapitalisir_rollover == 'T':
  #  form.GetControlByName('pData.lakukan_kapitalisir').Visible = 0
  #else:
  #  form.GetControlByName('pData.lakukan_kapitalisir').Visible = 1

  uipDeposito = form.GetUIPartByName('uipDeposito')
  uipDeposito.Edit()
  uipDeposito.akum_nominal = uipRolloverDeposito.GetFieldValue('LDeposito.akum_nominal')
  uipDeposito.akum_piutangLR = uipRolloverDeposito.GetFieldValue('LDeposito.akum_piutangLR')
  uipDeposito.akum_LR = uipRolloverDeposito.GetFieldValue('LDeposito.akum_LR')

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRolloverDeposito = form.GetUIPartByName('uipRolloverDeposito')

  if uipRolloverDeposito.mode == 'viewdoc':
    sender.ExitAction = 2
  else:
    if uipRolloverDeposito.mode not in ['view','auth']:
      form.CommitBuffer()

      if uipRolloverDeposito.mode == 'new':
##        if app.ConfirmDialog('Cetak slip rollover?'):
##          res = app.ExecuteScript('investasi/report/rollover_inst',
##            app.CreateValues(
##              ['no_bilyet', uipRolloverDeposito.GetFieldValue('LDeposito.no_bilyet')]
##              , ['no_batch', uipRolloverDeposito.GetFieldValue('LTransactionBatch.no_batch')]
##              , ['kode_pihak_ketiga', uipRolloverDeposito.GetFieldValue('LPihakKetiga.kode_pihak_ketiga')]
##              , ['nama_pihak_ketiga', uipRolloverDeposito.GetFieldValue('LPihakKetiga.nama_pihak_ketiga')]
##              , ['kode_paket_investasi', uipRolloverDeposito.GetFieldValue('LPaketInvestasi.kode_paket_investasi')]
##              , ['tgl_transaksi', uipRolloverDeposito.tgl_transaksi]
##              , ['nominal', uipRolloverDeposito.mutasi_kredit]
##              , ['user_id', uipRolloverDeposito.user_id]
##            )
##          )
##
##          app.DownloadItem(res.FirstRecord.filename,'v')
##          sender.ExitAction = 1

        uipRolloverDeposito.Edit()
        uipRolloverDeposito.__SYSFLAG = 'N'

      form.PostResult()

      sender.ExitAction = 1
    elif uipRolloverDeposito.mode == 'auth':
      dlg = app.ConfirmDialog('Anda yakin menyetujui Rollover Investasi ini?')
      if dlg:
        # otorisasi
        app.ExecuteScript('investasi/transaksi/rolloverinv_auth',
          app.CreateValues(
            ['id', uipRolloverDeposito.id_transaksiinvestasi]
            , ['isKapitalisir', uipRolloverDeposito.lakukan_kapitalisir == 'T']
          )
        )
        sender.ExitAction = 1

def btnCancelClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRolloverDeposito = form.GetUIPartByName('uipRolloverDeposito')

  if uipRolloverDeposito.mode == 'auth':
    dlg = app.ConfirmDialog('Anda yakin membatalkan Rollover Investasi ini?')
    if dlg:
      # hapus/tolak
      #app.ExecuteScript('investasi/transaksi/rolloverinv_del',\
      app.ExecuteScript('investasi/transaksi/transpiutanginv_del',\
        app.CreateValues(['id',uipRolloverDeposito.id_transaksiinvestasi])\
      )
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2

def btnPrintClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRolloverDeposito = form.GetUIPartByName('uipRolloverDeposito')

  form.CommitBuffer()

  res = app.ExecuteScript('investasi/report/rollover',
    app.CreateValues(['id',uipRolloverDeposito.id_transaksiinvestasi])
  )

  app.DownloadItem(res.FirstRecord.filename,'v')
  sender.ExitAction = 1

