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
  SetSelectorReadOnly(form)

def SetControlsForAuth(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnPrint').Visible = 1
  form.GetControlByName('pButton.btnClose').Cancel = 1
  form.Caption = 'Otorisasi Register Piutang LR Investasi Manual'
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

  uipTransPiutangLRInvestasi = form.GetUIPartByName('uipTransPiutangLRInvestasi')

  uipTransPiutangLRInvestasi.Edit()
  uipTransPiutangLRInvestasi.mode = parameter.FirstRecord.mode

  if (uipTransPiutangLRInvestasi.mode == 'new') \
    and uipTransPiutangLRInvestasi.GetFieldValue('LInvestasi.id_investasi'):
    SetSelectorReadOnly(form)

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
      SetSelectorReadOnly(form)
      form.Caption = 'Koreksi Register Piutang LR Investasi Manual'

def LInvestasiAfterLookup(sender, linkui):
  form = sender.OwnerForm

  uipTransPiutangLRInvestasi = form.GetUIPartByName('uipTransPiutangLRInvestasi')
  uipTransPiutangLRInvestasi.Edit()

  uipTransPiutangLRInvestasi.SetFieldValue('LPihakKetiga.kode_pihak_ketiga',  uipTransPiutangLRInvestasi.GetFieldValue('LInvestasi.kode_pihak_ketiga'))
  uipTransPiutangLRInvestasi.SetFieldValue('LPihakKetiga.nama_pihak_ketiga', uipTransPiutangLRInvestasi.GetFieldValue('LInvestasi.LPihakKetiga.nama_pihak_ketiga'))
#  uipTransPiutangLRInvestasi.SetFieldValue('LPaketInvestasi.kode_paket_investasi', uipTransPiutangLRInvestasi.GetFieldValue('LInvestasi.kode_paket_investasi'))
#  uipTransPiutangLRInvestasi.SetFieldValue('LPaketInvestasi.nama_paket_investasi', uipTransPiutangLRInvestasi.GetFieldValue('LInvestasi.LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi'))

  uipInvestasi = form.GetUIPartByName('uipInvestasi')
  uipInvestasi.Edit()
  uipInvestasi.akum_nominal = uipTransPiutangLRInvestasi.GetFieldValue('LInvestasi.akum_nominal')
  uipInvestasi.akum_piutangLR = uipTransPiutangLRInvestasi.GetFieldValue('LInvestasi.akum_piutangLR')
  uipInvestasi.akum_LR = uipTransPiutangLRInvestasi.GetFieldValue('LInvestasi.akum_LR')

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipTransPiutangLRInvestasi = form.GetUIPartByName('uipTransPiutangLRInvestasi')
  uipInvestasi = form.GetUIPartByName('uipInvestasi')

  if uipTransPiutangLRInvestasi.mode == 'viewdoc':
    sender.ExitAction = 2
  else:
    if uipTransPiutangLRInvestasi.mode not in ['view','auth']:
      form.CommitBuffer()

      if uipTransPiutangLRInvestasi.mode == 'new':
        uipTransPiutangLRInvestasi.Edit()
        uipTransPiutangLRInvestasi.__SYSFLAG = 'N'

      form.PostResult()

      sender.ExitAction = 2      
      dlg = app.ConfirmDialog('Cetak advis transaksi?')
      if dlg: CetakAdvis(app, uipTransPiutangLRInvestasi, uipInvestasi)

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

def btnPrintClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipTransPiutangLRInvestasi = form.GetUIPartByName('uipTransPiutangLRInvestasi')
  uipInvestasi = form.GetUIPartByName('uipInvestasi')
  form.CommitBuffer()
  CetakAdvis(app, uipTransPiutangLRInvestasi, uipInvestasi)

def CetakAdvis(app, uipTransPiutangLRInvestasi, uipInvestasi):
  lHeader = ['No. Bilyet', 'Rekening Deposito', 'Pihak Ketiga','Tgl Transaksi', 'Debet', 'Kredit', \
             'Keterangan', 'Nominal Akhir', 'Akum. Bunga', 'Piutang Bunga']
  sHeader = '|'.join(lHeader)
  tgl = uipTransPiutangLRInvestasi.tgl_transaksi
  sTgl = '%s-%s-%s' % (tgl[2],tgl[1],tgl[0])
  lData = [str(uipTransPiutangLRInvestasi.GetFieldValue('LInvestasi.no_bilyet')),\
           str(uipTransPiutangLRInvestasi.rekening_deposito),\
           '%s - %s'% (uipTransPiutangLRInvestasi.GetFieldValue('LPihakKetiga.kode_pihak_ketiga'),\
           uipTransPiutangLRInvestasi.GetFieldValue('LPihakKetiga.nama_pihak_ketiga')),\
           str(sTgl),\
           app.ModLibUtils.FormatFloat(',0.00',uipTransPiutangLRInvestasi.mutasi_debet or 0.0),\
           app.ModLibUtils.FormatFloat(',0.00',uipTransPiutangLRInvestasi.mutasi_kredit or 0.0),\
           str(uipTransPiutangLRInvestasi.keterangan),\
           app.ModLibUtils.FormatFloat(',0.00',uipInvestasi.akum_nominal or 0.0),\
           app.ModLibUtils.FormatFloat(',0.00',uipInvestasi.akum_LR or 0.0),\
           app.ModLibUtils.FormatFloat(',0.00',uipInvestasi.akum_piutangLR or 0.0)]
  sData = '|'.join(lData)
  ph = app.CreateValues(['nama_advis','Koreksi Piutang Hasil Investasi Deposito'],['sHeader',sHeader],['sData',sData],['inputer',uipTransPiutangLRInvestasi.user_id])
  phret = app.ExecuteScript('investasi/report/AdvisTransaksiInvestasi', ph)
  rec = phret.FirstRecord
  app.DownloadItem(rec.filename,'v')
