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
  SetSelectorReadOnly(form)

def SetControlsForAuth(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnClose').Cancel = 1
  form.Caption = 'Otorisasi Register LR Investasi Manual'
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

  uipTransLRInvestasi = form.GetUIPartByName('uipTransLRInvestasi')

  uipTransLRInvestasi.Edit()
  uipTransLRInvestasi.mode = parameter.FirstRecord.mode

  if (uipTransLRInvestasi.mode == 'new') \
    and uipTransLRInvestasi.GetFieldValue('LInvestasi.id_investasi'):
    SetSelectorReadOnly(form)

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
      SetSelectorReadOnly(form)
      form.Caption = 'Koreksi Register LR Investasi Manual'

def LInvestasiAfterLookup(sender, linkui):
  form = sender.OwnerForm

  uipTransLRInvestasi = form.GetUIPartByName('uipTransLRInvestasi')
  uipTransLRInvestasi.Edit()

  uipTransLRInvestasi.SetFieldValue('LPihakKetiga.kode_pihak_ketiga',  uipTransLRInvestasi.GetFieldValue('LInvestasi.kode_pihak_ketiga'))
  uipTransLRInvestasi.SetFieldValue('LPihakKetiga.nama_pihak_ketiga', uipTransLRInvestasi.GetFieldValue('LInvestasi.LPihakKetiga.nama_pihak_ketiga'))
  uipTransLRInvestasi.SetFieldValue('LPaketInvestasi.kode_paket_investasi', uipTransLRInvestasi.GetFieldValue('LInvestasi.kode_paket_investasi'))
  uipTransLRInvestasi.SetFieldValue('LPaketInvestasi.nama_paket_investasi', uipTransLRInvestasi.GetFieldValue('LInvestasi.LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi'))

  uipInvestasi = form.GetUIPartByName('uipInvestasi')
  uipInvestasi.Edit()
  uipInvestasi.akum_nominal = uipTransLRInvestasi.GetFieldValue('LInvestasi.akum_nominal')
  uipInvestasi.akum_piutangLR = uipTransLRInvestasi.GetFieldValue('LInvestasi.akum_piutangLR')
  uipInvestasi.akum_LR = uipTransLRInvestasi.GetFieldValue('LInvestasi.akum_LR')

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
      sender.ExitAction = 2

      dlg = app.ConfirmDialog('Cetak advis transaksi?')
      if dlg: CetakAdvis(app, uipTransLRInvestasi)

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


def CetakAdvis(app, uipTransLRInvestasi):
  lHeader = ['ID Sukuk', 'No. Batch', 'Pihak Ketiga', 'Paket Investasi', \
             'Tgl Transaksi', 'Mutasi Debet', 'Mutasi Kredit', 'Keterangan']
  sHeader = '|'.join(lHeader)
  tgl = uipTransLRInvestasi.tgl_transaksi
  sTgl = '%s-%s-%s' % (tgl[2],tgl[1],tgl[0])
  lData = [str(uipTransLRInvestasi.GetFieldValue('LInvestasi.id_investasi')),\
           str(uipTransLRInvestasi.GetFieldValue('LTransactionBatch.no_batch')),\
           '%s - %s'% (uipTransLRInvestasi.GetFieldValue('LPihakKetiga.kode_pihak_ketiga'),\
           uipTransLRInvestasi.GetFieldValue('LPihakKetiga.nama_pihak_ketiga')),\
           str(uipTransLRInvestasi.GetFieldValue('LPaketInvestasi.kode_paket_investasi')),\
           str(sTgl),\
           app.ModLibUtils.FormatFloat(',0.00',uipTransLRInvestasi.mutasi_debet or 0.0),\
           app.ModLibUtils.FormatFloat(',0.00',uipTransLRInvestasi.mutasi_kredit or 0.0),\
           str(uipTransLRInvestasi.keterangan)]
  sData = '|'.join(lData)
  ph = app.CreateValues(['nama_advis','Koreksi Hasil Investasi Sukuk'],['sHeader',sHeader],['sData',sData],['inputer',uipTransLRInvestasi.user_id])
  phret = app.ExecuteScript('investasi/report/AdvisTransaksiInvestasi', ph)
  rec = phret.FirstRecord
  app.DownloadItem(rec.filename,'v')
