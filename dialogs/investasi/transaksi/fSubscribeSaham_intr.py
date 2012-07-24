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
  form.Caption = 'Lihat Register Subscribe Saham'
  SetSelectorReadOnly(form)

def SetControlsForAuth(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnClose').Cancel = 1
  form.GetControlByName('pButton.btnPrint').Visible = 1
  form.Caption = 'Otorisasi Register Subscribe Saham'
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
  form.GetControlByName('pSelector.LSaham').Enabled = 0
  #form.GetPanelByName('pSelector').SetAllControlsReadOnly()

def FormShow(form, parameter):
  # set caption
  #form.Caption = parameter.FirstRecord.caption

  uipSubscribeSaham = form.GetUIPartByName('uipSubscribeSaham')

  uipSubscribeSaham.Edit()
  uipSubscribeSaham.mode = parameter.FirstRecord.mode

  if (uipSubscribeSaham.mode == 'new'):
    if uipSubscribeSaham.GetFieldValue('LSaham.id_investasi'):
      SetSelectorReadOnly(form)

  if uipSubscribeSaham.mode == 'viewdoc':
    form.Caption = 'Lihat Transaksi Subscribe Saham'
    SetControlsForViewDoc(form)
    UnhideControls(form)
  else:
    if uipSubscribeSaham.mode == 'view':
      SetControlsForView(form)
    elif uipSubscribeSaham.mode == 'auth':
      SetControlsForAuth(form)
    elif uipSubscribeSaham.mode == 'edit':
      SetSelectorReadOnly(form)
      form.Caption = 'Koreksi Register Subscribe Saham'

def LSahamAfterLookup(sender, linkui):
  form = sender.OwnerForm

  uipSubscribeSaham = form.GetUIPartByName('uipSubscribeSaham')
  uipSubscribeSaham.Edit()
  uipSubscribeSaham.SetFieldValue('LPihakKetiga.kode_pihak_ketiga',  uipSubscribeSaham.GetFieldValue('LSaham.kode_pihak_ketiga'))
  uipSubscribeSaham.SetFieldValue('LPihakKetiga.nama_pihak_ketiga', uipSubscribeSaham.GetFieldValue('LSaham.LPihakKetiga.nama_pihak_ketiga'))
  uipSubscribeSaham.SetFieldValue('LPaketInvestasi.kode_paket_investasi', uipSubscribeSaham.GetFieldValue('LSaham.kode_paket_investasi'))
  uipSubscribeSaham.SetFieldValue('LPaketInvestasi.nama_paket_investasi', uipSubscribeSaham.GetFieldValue('LSaham.LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi'))

  uipSaham = form.GetUIPartByName('uipSaham')
  uipSaham.Edit()
  uipSaham.akum_nominal = uipSubscribeSaham.GetFieldValue('LSaham.akum_nominal')
  uipSaham.unit_penyertaan = uipSubscribeSaham.GetFieldValue('LSaham.unit_penyertaan')
  uipSaham.NAB = uipSubscribeSaham.GetFieldValue('LSaham.NAB')
  #uipSaham.akum_piutangLR = uipSubscribeSaham.GetFieldValue('LSaham.akum_piutangLR')
  #uipSaham.akum_LR = uipSubscribeSaham.GetFieldValue('LSaham.akum_LR')
  #uipSaham.min_inv_tambahan = uipSubscribeSaham.GetFieldValue('LSaham.min_inv_tambahan')

def nilai_subscribeExit(sender):
  form = sender.OwnerForm

  uipSaham = form.GetUIPartByName('uipSaham')
  uipSubscribeSaham = form.GetUIPartByName('uipSubscribeSaham')
  uipSubscribeSaham.Edit()
  uipSubscribeSaham.nilai_subscribe = (uipSubscribeSaham.nilai_subscribe or 0.0)
  if uipSaham.NAB == 0.0 :
    raise Exception, 'PERINGATAN' + 'Update NAB terlebih dahulu'
  uipSubscribeSaham.unit_penyertaan = uipSubscribeSaham.nilai_subscribe / uipSaham.NAB

def uipSubscribeSahamBeforePost(uipSubscribeSaham):
  form = uipSubscribeSaham.OwnerForm

  uipSaham = form.GetUIPartByName('uipSaham')
  uipSubscribeSaham.Edit()
  if uipSubscribeSaham.unit_penyertaan:
    uipSubscribeSaham.nilai_subscribe = uipSubscribeSaham.unit_penyertaan * uipSaham.NAB
  else:
    uipSubscribeSaham.nilai_subscribe = 0.0

def checkNilaiSubscribe(form, app):
  uipSaham = form.GetUIPartByName('uipSaham')
  uipSubscribeSaham = form.GetUIPartByName('uipSubscribeSaham')

  if uipSubscribeSaham.nilai_subscribe < uipSaham.min_inv_tambahan:
    if not app.ConfirmDialog('PERHATIAN:'\
      '\nNilai subscribe kurang dari minimum investasi tambahan.'
      '\nLanjutkan?.'
    ):
      form.GetControlByName('pData.unit_penyertaan').SetFocus()
      return 0

  return 1

#def nilai_subscribeChange(sender):
#  form = sender.OwnerForm
#  app = form.ClientApplication
#  #checkNilaiSubscribe(form, app)

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipSubscribeSaham = form.GetUIPartByName('uipSubscribeSaham')
  uipSaham = form.GetUIPartByName('uipSaham')

  if uipSubscribeSaham.mode == 'viewdoc':
    sender.ExitAction = 2
  else:
    if uipSubscribeSaham.mode not in ['view','auth']:
      form.CommitBuffer()
      
      #if not checkNilaiSubscribe(form, app):
      #  return

      if uipSubscribeSaham.mode == 'new':
        uipSubscribeSaham.Edit()
        uipSubscribeSaham.__SYSFLAG = 'N'

      form.PostResult()

      sender.ExitAction = 2
#       dlg = app.ConfirmDialog('Cetak advis transaksi?')
#       if dlg: CetakAdvis(app, uipSubscribeSaham, uipSaham)

    elif uipSubscribeSaham.mode == 'auth':
      dlg = app.ConfirmDialog('Anda yakin menyetujui Subscribe Saham ini?')
      if dlg:
        # otorisasi
        app.ExecuteScript('investasi/transaksi/subscribeSaham_auth',\
          app.CreateValues(['id',uipSubscribeSaham.id_transaksiinvestasi])\
        )
        sender.ExitAction = 1

def btnCancelClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipSubscribeSaham = form.GetUIPartByName('uipSubscribeSaham')

  if uipSubscribeSaham.mode == 'auth':
    dlg = app.ConfirmDialog('Anda yakin membatalkan Subscribe Saham ini?')
    if dlg:
      app.ExecuteScript('investasi/transaksi/transpiutanginv_del',\
        app.CreateValues(['id',uipSubscribeSaham.id_transaksiinvestasi])\
      )
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2
    
def btnPrintClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipSubscribeSaham = form.GetUIPartByName('uipSubscribeSaham')
  uipSaham = form.GetUIPartByName('uipSaham')

  form.CommitBuffer()

  CetakAdvis(app, uipSubscribeSaham, uipSaham)

def CetakAdvis(app, uipSubscribeSaham, uipSaham):
  lHeader = ['Nama Saham', 'Pihak Ketiga', 'Paket Investasi', \
             'Tgl Transaksi', 'Nilai Subscribe', 'Nominal Investasi']
  sHeader = '|'.join(lHeader)
  tgl = uipSubscribeSaham.tgl_transaksi
  sTgl = '%s-%s-%s' % (tgl[2],tgl[1],tgl[0])
  lData = [str(uipSubscribeSaham.GetFieldValue('LSaham.nama_Saham')),\
           '%s - %s'% (uipSubscribeSaham.GetFieldValue('LPihakKetiga.kode_pihak_ketiga'),\
           uipSubscribeSaham.GetFieldValue('LPihakKetiga.nama_pihak_ketiga')),\
           str(uipSubscribeSaham.GetFieldValue('LPaketInvestasi.kode_paket_investasi')),\
           str(sTgl),\
           app.ModLibUtils.FormatFloat(',0.00',uipSubscribeSaham.nilai_subscribe or 0.0),\
           app.ModLibUtils.FormatFloat(',0.00',uipSaham.akum_nominal or 0.0)]
  sData = '|'.join(lData)
  ph = app.CreateValues(['nama_advis','Subscribe Saham Tambahan'],['sHeader',sHeader],['sData',sData],['inputer',uipSubscribeSaham.user_id])
  phret = app.ExecuteScript('investasi/report/AdvisTransaksiInvestasi', ph)
  rec = phret.FirstRecord
  app.DownloadItem(rec.filename,'v')
