dictJenisSukuk = {'K':'Korporat','P':'Pemda','N':'Negara',None:'','R':''}

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
  form.Caption = 'Lihat Register Pendapatan Obligasi'
  SetSelectorReadOnly(form)

def SetControlsForAuth(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnPrint').Visible = 1
  form.GetControlByName('pButton.btnClose').Cancel = 1
  form.Caption = 'Otorisasi Register Pendapatan Obligasi'
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
  form.Caption = parameter.FirstRecord.caption

  uipPendapatanObligasi = form.GetUIPartByName('uipPendapatanObligasi')

  uipPendapatanObligasi.Edit()
  uipPendapatanObligasi.mode = parameter.FirstRecord.mode

  if (uipPendapatanObligasi.mode == 'new') \
    and uipPendapatanObligasi.GetFieldValue('LObligasi.id_investasi'):
    SetSelectorReadOnly(form)

    uipObligasi = form.GetUIPartByName('uipObligasi')
    # set nilai no_rekening sebagai default pencairan
    uipPendapatanObligasi.no_rekening = uipObligasi.no_rekening
  uipPendapatanObligasi.SetFieldValue('LMasterGiro.no_giro',uipPendapatanObligasi.no_rekening)
  if uipPendapatanObligasi.mode == 'viewdoc':
    form.Caption = 'Lihat Transaksi Pendapatan Obligasi'
    SetControlsForViewDoc(form)
    UnhideControls(form)
  else:
    if uipPendapatanObligasi.mode == 'view':
      SetControlsForView(form)
    elif uipPendapatanObligasi.mode == 'auth':
      SetControlsForAuth(form)
    elif uipPendapatanObligasi.mode == 'edit':
      SetSelectorReadOnly(form)
      form.Caption = 'Koreksi Register Pendapatan Investasi FIX'

def OnAfterLookup_Rek(sender, linkui) :
  form = sender.OwnerForm
  app = form.ClientApplication
  uip = form.GetUIPartByName('uipPendapatanObligasi')
  uip.no_rekening = uip.GetFieldValue('LMasterGiro.no_giro')

def LObligasiAfterLookup(sender, linkui):
  form = sender.OwnerForm

  uipPendapatanObligasi = form.GetUIPartByName('uipPendapatanObligasi')
  uipPendapatanObligasi.Edit()

  uipPendapatanObligasi.SetFieldValue('LPihakKetiga.kode_pihak_ketiga',  uipPendapatanObligasi.GetFieldValue('LObligasi.kode_pihak_ketiga'))
  uipPendapatanObligasi.SetFieldValue('LPihakKetiga.nama_pihak_ketiga', uipPendapatanObligasi.GetFieldValue('LObligasi.LPihakKetiga.nama_pihak_ketiga'))
  uipPendapatanObligasi.SetFieldValue('LPaketInvestasi.kode_paket_investasi', uipPendapatanObligasi.GetFieldValue('LObligasi.kode_paket_investasi'))
  uipPendapatanObligasi.SetFieldValue('LPaketInvestasi.nama_paket_investasi', uipPendapatanObligasi.GetFieldValue('LObligasi.LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi'))

  uipObligasi = form.GetUIPartByName('uipObligasi')
  uipObligasi.Edit()
  uipObligasi.akum_nominal = uipPendapatanObligasi.GetFieldValue('LObligasi.akum_nominal')
  uipObligasi.jenis_obligasi = uipPendapatanObligasi.GetFieldValue('LObligasi.jenis_obligasi')
  uipObligasi.tgl_jatuh_tempo = uipPendapatanObligasi.GetFieldValue('LObligasi.tgl_jatuh_tempo')
  uipObligasi.no_rekening = uipPendapatanObligasi.GetFieldValue('LObligasi.no_rekening')
  uipPendapatanObligasi.no_rekening = uipPendapatanObligasi.GetFieldValue('LObligasi.no_rekening')

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipPendapatanObligasi = form.GetUIPartByName('uipPendapatanObligasi')
  uipObligasi = form.GetUIPartByName('uipObligasi')

  if uipPendapatanObligasi.mode == 'viewdoc':
    sender.ExitAction = 2
  else:
    if uipPendapatanObligasi.mode not in ['view','auth']:

      form.CommitBuffer()
      if uipPendapatanObligasi.mode == 'new':
        uipPendapatanObligasi.Edit()
        uipPendapatanObligasi.__SYSFLAG = 'N'
      form.PostResult()
      sender.ExitAction = 2

      dlg = app.ConfirmDialog('Cetak advis transaksi?')
      if dlg: CetakAdvis(app, uipPendapatanObligasi, uipObligasi)
      
    elif uipPendapatanObligasi.mode == 'auth':
      dlg = app.ConfirmDialog('Anda yakin menyetujui Pendapatan Obligasi ini?')
      if dlg:
        # otorisasi
        app.ExecuteScript('investasi/transaksi/pendapatanobligasi_auth',\
          app.CreateValues(['id',uipPendapatanObligasi.id_transaksiinvestasi])\
        )
        sender.ExitAction = 1

def btnCancelClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipPendapatanObligasi = form.GetUIPartByName('uipPendapatanObligasi')

  if uipPendapatanObligasi.mode == 'auth':
    dlg = app.ConfirmDialog('Anda yakin membatalkan Pendapatan Obligasi ini?')
    if dlg:
      # hapus/tolak
      app.ExecuteScript('investasi/transaksi/translrinvestasi_del',\
        app.CreateValues(['id',uipPendapatanObligasi.id_transaksiinvestasi])\
      )
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2

def btnPrintClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipPendapatanObligasi = form.GetUIPartByName('uipPendapatanObligasi')
  uipObligasi = form.GetUIPartByName('uipObligasi')
  form.CommitBuffer()
  CetakAdvis(app, uipPendapatanObligasi, uipObligasi)

def CetakAdvis(app, uipPendapatanObligasi, uipObligasi):
  lHeader = ['Nama Investasi', 'Pihak Ketiga', 'Paket Investasi', \
             'Tgl Transaksi', 'Pendapatan', 'No. Rekening', 'Nominal', \
             'Tgl Jatuh Tempo']
  sHeader = '|'.join(lHeader)
  tgl = uipPendapatanObligasi.tgl_transaksi
  sTgl = '%s-%s-%s' % (tgl[2],tgl[1],tgl[0])
  tglJT = uipObligasi.tgl_jatuh_tempo
  sTglJT = '%s-%s-%s' % (tglJT[2],tglJT[1],tglJT[0])
  lData = [str(uipPendapatanObligasi.GetFieldValue('LObligasi.nama_obligasi')),\
           '%s - %s'% (uipPendapatanObligasi.GetFieldValue('LPihakKetiga.kode_pihak_ketiga'),\
           uipPendapatanObligasi.GetFieldValue('LPihakKetiga.nama_pihak_ketiga')),\
           str(uipPendapatanObligasi.GetFieldValue('LPaketInvestasi.kode_paket_investasi')),\
           str(sTgl),\
           app.ModLibUtils.FormatFloat(',0.00',uipPendapatanObligasi.nominal or 0.0),\
           str(uipPendapatanObligasi.no_rekening),\
           app.ModLibUtils.FormatFloat(',0.00',uipObligasi.akum_nominal or 0.0),\
           str(sTglJT)]
  sData = '|'.join(lData)
  ph = app.CreateValues(['nama_advis','Pembayaran Kupon'],['sHeader',sHeader],['sData',sData],['inputer',uipPendapatanObligasi.user_id])
  phret = app.ExecuteScript('investasi/report/AdvisTransaksiInvestasi', ph)
  rec = phret.FirstRecord
  app.DownloadItem(rec.filename,'v')
