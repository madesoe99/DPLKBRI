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
  form.Caption = 'Lihat Register Bagi Hasil Deposito'
  SetSelectorReadOnly(form)

def SetControlsForAuth(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnClose').Cancel = 1
  form.GetControlByName('pButton.btnPrint').Visible = 1
  form.Caption = 'Otorisasi Register Bagi Hasil Deposito'
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
  form.GetControlByName('pSelector.LDeposito').Enabled = 0
  #form.GetPanelByName('pSelector').SetAllControlsReadOnly()

def FormShow(form, parameter):
  # set caption
  form.Caption = parameter.FirstRecord.caption

  uipBagiHasilDeposito = form.GetUIPartByName('uipBagiHasilDeposito')

  uipBagiHasilDeposito.Edit()
  uipBagiHasilDeposito.mode = parameter.FirstRecord.mode

  if (uipBagiHasilDeposito.mode == 'new'):
    form.GetControlByName('pPrint.btnPrint').Visible = 0
    if uipBagiHasilDeposito.GetFieldValue('LDeposito.id_investasi'):
      SetSelectorReadOnly(form)

  if uipBagiHasilDeposito.mode == 'viewdoc':
    form.Caption = 'Lihat Transaksi Bagi Hasil Deposito'
    SetControlsForViewDoc(form)
    UnhideControls(form)
  else:
    if uipBagiHasilDeposito.mode == 'view':
      SetControlsForView(form)
    elif uipBagiHasilDeposito.mode == 'auth':
      SetControlsForAuth(form)
    elif uipBagiHasilDeposito.mode == 'edit':
      SetSelectorReadOnly(form)
      form.Caption = 'Koreksi Register Bagi Hasil Deposito'

def LDepositoAfterLookup(sender, linkui):
  form = sender.OwnerForm

  uipBagiHasilDeposito = form.GetUIPartByName('uipBagiHasilDeposito')
  uipBagiHasilDeposito.Edit()
  uipBagiHasilDeposito.SetFieldValue('LPihakKetiga.kode_pihak_ketiga',  uipBagiHasilDeposito.GetFieldValue('LDeposito.kode_pihak_ketiga'))
  uipBagiHasilDeposito.SetFieldValue('LPihakKetiga.nama_pihak_ketiga', uipBagiHasilDeposito.GetFieldValue('LDeposito.LPihakKetiga.nama_pihak_ketiga'))
  #uipBagiHasilDeposito.SetFieldValue('LPaketInvestasi.kode_paket_investasi', uipBagiHasilDeposito.GetFieldValue('LDeposito.kode_paket_investasi'))
  #uipBagiHasilDeposito.SetFieldValue('LPaketInvestasi.nama_paket_investasi', uipBagiHasilDeposito.GetFieldValue('LDeposito.LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi'))
  #uipBagiHasilDeposito.SetFieldValue('LJenisInvestasi.kode_jns_investasi', uipBagiHasilDeposito.GetFieldValue('LDeposito.kode_jns_investasi'))
  #uipBagiHasilDeposito.SetFieldValue('LJenisInvestasi.nama_jns_investasi', uipBagiHasilDeposito.GetFieldValue('LDeposito.LRincianPaketInvestasi.LJenisInvestasi.nama_jns_investasi'))

  uipDeposito = form.GetUIPartByName('uipDeposito')
  uipDeposito.Edit()
  uipDeposito.akum_nominal = uipBagiHasilDeposito.GetFieldValue('LDeposito.akum_nominal')
  uipDeposito.akum_piutangLR = uipBagiHasilDeposito.GetFieldValue('LDeposito.akum_piutangLR')
  uipDeposito.akum_LR = uipBagiHasilDeposito.GetFieldValue('LDeposito.akum_LR')

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipBagiHasilDeposito = form.GetUIPartByName('uipBagiHasilDeposito')
  uipDeposito = form.GetUIPartByName('uipDeposito')

  if uipBagiHasilDeposito.mode == 'viewdoc':
    sender.ExitAction = 2
  else:
    if uipBagiHasilDeposito.mode not in ['view','auth']:
      form.CommitBuffer()

      if uipBagiHasilDeposito.mode == 'new':
##        if app.ConfirmDialog('Cetak slip bagi hasil?'):
##          res = app.ExecuteScript('investasi/report/bagihasil_inst',
##            app.CreateValues(
##              ['no_bilyet', uipBagiHasilDeposito.GetFieldValue('LDeposito.no_bilyet')]
##              , ['no_batch', uipBagiHasilDeposito.GetFieldValue('LTransactionBatch.no_batch')]
##              , ['kode_pihak_ketiga', uipBagiHasilDeposito.GetFieldValue('LPihakKetiga.kode_pihak_ketiga')]
##              , ['nama_pihak_ketiga', uipBagiHasilDeposito.GetFieldValue('LPihakKetiga.nama_pihak_ketiga')]
##              , ['tgl_transaksi', uipBagiHasilDeposito.tgl_transaksi]
##              , ['nominal', uipBagiHasilDeposito.mutasi_kredit]
##              , ['user_id', uipBagiHasilDeposito.user_id]
##            )
##          )
##
##          app.DownloadItem(res.FirstRecord.filename,'v')
##          sender.ExitAction = 1

        uipBagiHasilDeposito.Edit()
        uipBagiHasilDeposito.__SYSFLAG = 'N'

      form.PostResult()
      sender.ExitAction = 2

      dlg = app.ConfirmDialog('Cetak advis transaksi?')
      if dlg: CetakAdvis(app, uipBagiHasilDeposito, uipDeposito)
    
    elif uipBagiHasilDeposito.mode == 'auth':
      dlg = app.ConfirmDialog('Anda yakin menyetujui Bagi Hasil Deposito ini?')
      if dlg:
        # otorisasi
        app.ExecuteScript('investasi/transaksi/bagihasildeposito_auth',
          app.CreateValues(['id',uipBagiHasilDeposito.id_transaksiinvestasi])
        )
        sender.ExitAction = 1

def btnCancelClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipBagiHasilDeposito = form.GetUIPartByName('uipBagiHasilDeposito')

  if uipBagiHasilDeposito.mode == 'auth':
    dlg = app.ConfirmDialog('Anda yakin membatalkan Bagi Hasil Deposito ini?')
    if dlg:
      # hapus/tolak
      app.ExecuteScript('investasi/transaksi/translrinvestasi_del',
        app.CreateValues(['id',uipBagiHasilDeposito.id_transaksiinvestasi])
      )
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2

def btnPrintClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipBagiHasilDeposito = form.GetUIPartByName('uipBagiHasilDeposito')
  uipDeposito = form.GetUIPartByName('uipDeposito')

  form.CommitBuffer()
  CetakAdvis(app, uipBagiHasilDeposito, uipDeposito)

  '''res = app.ExecuteScript('investasi/report/bagihasil',
    app.CreateValues(['id',uipBagiHasilDeposito.id_transaksiinvestasi])
  )

  app.DownloadItem(res.FirstRecord.filename,'v')
  sender.ExitAction = 1'''


def CetakAdvis(app, uipBagiHasilDeposito, uipDeposito):
  lHeader = ['No. Bilyet', 'Rekening Deposito', 'Nominal', 'Pihak Ketiga','Tgl Transaksi', \
             'Bagi Hasil', 'Akum. Bagi Hasil','Piutang Bagi Hasil', ]
  sHeader = '|'.join(lHeader)
  tgl = uipBagiHasilDeposito.tgl_transaksi
  sTgl = '%s-%s-%s' % (tgl[2],tgl[1],tgl[0])
  lData = [str(uipBagiHasilDeposito.GetFieldValue('LDeposito.no_bilyet')),\
           str(uipBagiHasilDeposito.GetFieldValue('LDeposito.rekening_deposito')),\
           app.ModLibUtils.FormatFloat(',0.00',uipBagiHasilDeposito.nominal_pembukaan or 0.0),\
           '%s - %s'% (uipBagiHasilDeposito.GetFieldValue('LPihakKetiga.kode_pihak_ketiga'),\
           uipBagiHasilDeposito.GetFieldValue('LPihakKetiga.nama_pihak_ketiga')),\
           str(sTgl),\
           app.ModLibUtils.FormatFloat(',0.00',uipBagiHasilDeposito.mutasi_kredit or 0.0),\
           app.ModLibUtils.FormatFloat(',0.00',uipDeposito.akum_LR or 0.0),\
           app.ModLibUtils.FormatFloat(',0.00',uipDeposito.akum_piutangLR or 0.0)]
  sData = '|'.join(lData)
  ph = app.CreateValues(['nama_advis','Bagi Hasil Deposito'],['sHeader',sHeader],['sData',sData],['inputer',uipBagiHasilDeposito.user_id])
  phret = app.ExecuteScript('investasi/report/AdvisTransaksiInvestasi', ph)
  rec = phret.FirstRecord
  app.DownloadItem(rec.filename,'v')
