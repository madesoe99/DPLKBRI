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
  form.Caption = 'Lihat Register Investasi Manual'
  SetSelectorReadOnly(form)

def SetControlsForAuth(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnPrint').Visible = 1
  form.GetControlByName('pButton.btnClose').Cancel = 1
  form.Caption = 'Otorisasi Register Investasi Manual'
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
  form.GetControlByName('pSelector.LInvestasi').Enabled = 0
  #form.GetPanelByName('pSelector').SetAllControlsReadOnly()

def FormShow(form, parameter):
  # set caption
  form.Caption = parameter.FirstRecord.caption

  uipTransPiutangInvestasi = form.GetUIPartByName('uipTransPiutangInvestasi')

  uipTransPiutangInvestasi.Edit()
  uipTransPiutangInvestasi.mode = parameter.FirstRecord.mode

  if (uipTransPiutangInvestasi.mode == 'new') \
    and uipTransPiutangInvestasi.GetFieldValue('LInvestasi.id_investasi'):
    SetSelectorReadOnly(form)

  if uipTransPiutangInvestasi.mode == 'viewdoc':
    form.Caption = 'Lihat Transaksi Investasi Manual'
    SetControlsForViewDoc(form)
    UnhideControls(form)
  else:
    if uipTransPiutangInvestasi.mode == 'view':
      SetControlsForView(form)
    elif uipTransPiutangInvestasi.mode == 'auth':
      SetControlsForAuth(form)
    elif uipTransPiutangInvestasi.mode == 'edit':
      SetSelectorReadOnly(form)
      form.Caption = 'Koreksi Register Investasi Manual'

def LInvestasiAfterLookup(sender, linkui):
  form = sender.OwnerForm

  uipTransPiutangInvestasi = form.GetUIPartByName('uipTransPiutangInvestasi')
  uipTransPiutangInvestasi.Edit()

  uipTransPiutangInvestasi.SetFieldValue('LPihakKetiga.kode_pihak_ketiga',  uipTransPiutangInvestasi.GetFieldValue('LInvestasi.kode_pihak_ketiga'))
  uipTransPiutangInvestasi.SetFieldValue('LPihakKetiga.nama_pihak_ketiga', uipTransPiutangInvestasi.GetFieldValue('LInvestasi.LPihakKetiga.nama_pihak_ketiga'))
#  uipTransPiutangInvestasi.SetFieldValue('LPaketInvestasi.kode_paket_investasi', uipTransPiutangInvestasi.GetFieldValue('LInvestasi.kode_paket_investasi'))
#  uipTransPiutangInvestasi.SetFieldValue('LPaketInvestasi.nama_paket_investasi', uipTransPiutangInvestasi.GetFieldValue('LInvestasi.LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi'))

  uipInvestasi = form.GetUIPartByName('uipInvestasi')
  uipInvestasi.Edit()
  uipInvestasi.akum_nominal = uipTransPiutangInvestasi.GetFieldValue('LInvestasi.akum_nominal')
  uipInvestasi.akum_piutangLR = uipTransPiutangInvestasi.GetFieldValue('LInvestasi.akum_piutangLR')
  uipInvestasi.akum_LR = uipTransPiutangInvestasi.GetFieldValue('LInvestasi.akum_LR')

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipTransPiutangInvestasi = form.GetUIPartByName('uipTransPiutangInvestasi')
  uipInvestasi = form.GetUIPartByName('uipInvestasi')

  if uipTransPiutangInvestasi.mode == 'viewdoc':
    sender.ExitAction = 2
  else:
    if uipTransPiutangInvestasi.mode not in ['view','auth']:
      form.CommitBuffer()

      if uipTransPiutangInvestasi.mode == 'new':
        uipTransPiutangInvestasi.Edit()
        uipTransPiutangInvestasi.__SYSFLAG = 'N'

      form.PostResult()
      sender.ExitAction = 2
      dlg = app.ConfirmDialog('Cetak advis transaksi?')
      if dlg: CetakAdvis(app, uipTransPiutangInvestasi, uipInvestasi)

    elif uipTransPiutangInvestasi.mode == 'auth':
      dlg = app.ConfirmDialog('Anda yakin menyetujui Investasi secara Manual ini?')
      if dlg:
        # otorisasi
        app.ExecuteScript('investasi/transaksi/maninvestasi_auth',\
          app.CreateValues(['id',uipTransPiutangInvestasi.id_transaksiinvestasi])\
        )
        sender.ExitAction = 1

def btnCancelClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipTransPiutangInvestasi = form.GetUIPartByName('uipTransPiutangInvestasi')

  if uipTransPiutangInvestasi.mode == 'auth':
    dlg = app.ConfirmDialog('Anda yakin membatalkan Investasi secara Manual ini?')
    if dlg:
      # hapus/tolak
      #app.ExecuteScript('investasi/transaksi/maninvestasi_del',\
      app.ExecuteScript('investasi/transaksi/transpiutanginv_del',\
        app.CreateValues(['id',uipTransPiutangInvestasi.id_transaksiinvestasi])\
      )
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2

def btnPrintClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipTransPiutangInvestasi = form.GetUIPartByName('uipTransPiutangInvestasi')
  uipInvestasi = form.GetUIPartByName('uipInvestasi')
  form.CommitBuffer()
  CetakAdvis(app, uipTransPiutangInvestasi, uipInvestasi)

def CetakAdvis(app, uipTransPiutangInvestasi, uipInvestasi):
  lHeader = ['No. Bilyet', 'Rekening Deposito', 'Pihak Ketiga','Tgl Transaksi', 'Debet', 'Kredit', \
             'Keterangan', 'Nominal Akhir', 'Akum. Bunga', 'Piutang Bunga']
  sHeader = '|'.join(lHeader)
  tgl = uipTransPiutangInvestasi.tgl_transaksi
  sTgl = '%s-%s-%s' % (tgl[2],tgl[1],tgl[0])
  lData = [str(uipTransPiutangInvestasi.GetFieldValue('LInvestasi.no_bilyet')),\
           str(uipTransPiutangInvestasi.rekening_deposito),\
           '%s - %s'% (uipTransPiutangInvestasi.GetFieldValue('LPihakKetiga.kode_pihak_ketiga'),\
           uipTransPiutangInvestasi.GetFieldValue('LPihakKetiga.nama_pihak_ketiga')),\
           str(sTgl),\
           app.ModLibUtils.FormatFloat(',0.00',uipTransPiutangInvestasi.mutasi_debet or 0.0),\
           app.ModLibUtils.FormatFloat(',0.00',uipTransPiutangInvestasi.mutasi_kredit or 0.0),\
           str(uipTransPiutangInvestasi.keterangan),\
           app.ModLibUtils.FormatFloat(',0.00',uipInvestasi.akum_nominal or 0.0),\
           app.ModLibUtils.FormatFloat(',0.00',uipInvestasi.akum_LR or 0.0),\
           app.ModLibUtils.FormatFloat(',0.00',uipInvestasi.akum_piutangLR or 0.0)]
  sData = '|'.join(lData)
  ph = app.CreateValues(['nama_advis','Koreksi Investasi Deposito'],['sHeader',sHeader],['sData',sData],['inputer',uipTransPiutangInvestasi.user_id])
  phret = app.ExecuteScript('investasi/report/AdvisTransaksiInvestasi', ph)
  rec = phret.FirstRecord
  app.DownloadItem(rec.filename,'v')
