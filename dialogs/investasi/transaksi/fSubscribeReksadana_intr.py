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
  form.Caption = 'Lihat Register Subscribe Investasi EQ'
  SetSelectorReadOnly(form)

def SetControlsForAuth(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnClose').Cancel = 1
  form.GetControlByName('pButton.btnPrint').Visible = 1
  form.Caption = 'Otorisasi Register Subscribe Investasi EQ'
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
  form.GetControlByName('pSelector.LReksadana').Enabled = 0
  #form.GetPanelByName('pSelector').SetAllControlsReadOnly()

def FormShow(form, parameter):
  # set caption
  #form.Caption = parameter.FirstRecord.caption

  uipSubscribeReksadana = form.GetUIPartByName('uipSubscribeReksadana')

  uipSubscribeReksadana.Edit()
  uipSubscribeReksadana.mode = parameter.FirstRecord.mode

  if (uipSubscribeReksadana.mode == 'new'):
    if uipSubscribeReksadana.GetFieldValue('LReksadana.id_investasi'):
      SetSelectorReadOnly(form)

  if uipSubscribeReksadana.mode == 'viewdoc':
    form.Caption = 'Lihat Transaksi Subscribe Investasi EQ'
    SetControlsForViewDoc(form)
    UnhideControls(form)
  else:
    if uipSubscribeReksadana.mode == 'view':
      SetControlsForView(form)
    elif uipSubscribeReksadana.mode == 'auth':
      SetControlsForAuth(form)
    elif uipSubscribeReksadana.mode == 'edit':
      SetSelectorReadOnly(form)
      form.Caption = 'Koreksi Register Subscribe Investasi EQ'

def LReksadanaAfterLookup(sender, linkui):
  form = sender.OwnerForm

  uipSubscribeReksadana = form.GetUIPartByName('uipSubscribeReksadana')
  uipSubscribeReksadana.Edit()
  uipSubscribeReksadana.SetFieldValue('LPihakKetiga.kode_pihak_ketiga',  uipSubscribeReksadana.GetFieldValue('LReksadana.kode_pihak_ketiga'))
  uipSubscribeReksadana.SetFieldValue('LPihakKetiga.nama_pihak_ketiga', uipSubscribeReksadana.GetFieldValue('LReksadana.LPihakKetiga.nama_pihak_ketiga'))
  uipSubscribeReksadana.SetFieldValue('LPaketInvestasi.kode_paket_investasi', uipSubscribeReksadana.GetFieldValue('LReksadana.kode_paket_investasi'))
  uipSubscribeReksadana.SetFieldValue('LPaketInvestasi.nama_paket_investasi', uipSubscribeReksadana.GetFieldValue('LReksadana.LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi'))

  uipReksadana = form.GetUIPartByName('uipReksadana')
  uipReksadana.Edit()
  uipReksadana.akum_nominal = uipSubscribeReksadana.GetFieldValue('LReksadana.akum_nominal')
  uipReksadana.unit_penyertaan = uipSubscribeReksadana.GetFieldValue('LReksadana.unit_penyertaan')
  uipReksadana.NAB = uipSubscribeReksadana.GetFieldValue('LReksadana.NAB')
  #uipReksadana.akum_piutangLR = uipSubscribeReksadana.GetFieldValue('LReksadana.akum_piutangLR')
  #uipReksadana.akum_LR = uipSubscribeReksadana.GetFieldValue('LReksadana.akum_LR')
  #uipReksadana.min_inv_tambahan = uipSubscribeReksadana.GetFieldValue('LReksadana.min_inv_tambahan')

def nilai_subscribeExit(sender):
  form = sender.OwnerForm

  uipReksadana = form.GetUIPartByName('uipReksadana')
  uipSubscribeReksadana = form.GetUIPartByName('uipSubscribeReksadana')
  uipSubscribeReksadana.Edit()
  uipSubscribeReksadana.nilai_subscribe = (uipSubscribeReksadana.nilai_subscribe or 0.0)
  if uipReksadana.NAB == 0.0 :
    raise 'PERINGATAN','Update NAB terlebih dahulu'
  uipSubscribeReksadana.unit_penyertaan = uipSubscribeReksadana.nilai_subscribe / uipReksadana.NAB

def uipSubscribeReksadanaBeforePost(uipSubscribeReksadana):
  form = uipSubscribeReksadana.OwnerForm

  uipReksadana = form.GetUIPartByName('uipReksadana')
  uipSubscribeReksadana.Edit()
  if uipSubscribeReksadana.unit_penyertaan:
    uipSubscribeReksadana.nilai_subscribe = uipSubscribeReksadana.unit_penyertaan * uipReksadana.NAB
  else:
    uipSubscribeReksadana.nilai_subscribe = 0.0

def checkNilaiSubscribe(form, app):
  uipReksadana = form.GetUIPartByName('uipReksadana')
  uipSubscribeReksadana = form.GetUIPartByName('uipSubscribeReksadana')

  if uipSubscribeReksadana.nilai_subscribe < uipReksadana.min_inv_tambahan:
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
  uipSubscribeReksadana = form.GetUIPartByName('uipSubscribeReksadana')
  uipReksadana = form.GetUIPartByName('uipReksadana')

  if uipSubscribeReksadana.mode == 'viewdoc':
    sender.ExitAction = 2
  else:
    if uipSubscribeReksadana.mode not in ['view','auth']:
      form.CommitBuffer()
      
      #if not checkNilaiSubscribe(form, app):
      #  return

      if uipSubscribeReksadana.mode == 'new':
        uipSubscribeReksadana.Edit()
        uipSubscribeReksadana.__SYSFLAG = 'N'

      form.PostResult()

      sender.ExitAction = 2
      dlg = app.ConfirmDialog('Cetak advis transaksi?')
      if dlg: CetakAdvis(app, uipSubscribeReksadana, uipReksadana)

    elif uipSubscribeReksadana.mode == 'auth':
      dlg = app.ConfirmDialog('Anda yakin menyetujui Subscribe Investasi EQ ini?')
      if dlg:
        # otorisasi
        app.ExecuteScript('investasi/transaksi/subscribereksadana_auth',\
          app.CreateValues(['id',uipSubscribeReksadana.id_transaksiinvestasi])\
        )
        sender.ExitAction = 1

def btnCancelClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipSubscribeReksadana = form.GetUIPartByName('uipSubscribeReksadana')

  if uipSubscribeReksadana.mode == 'auth':
    dlg = app.ConfirmDialog('Anda yakin membatalkan Subscribe Investasi EQ ini?')
    if dlg:
      app.ExecuteScript('investasi/transaksi/transpiutanginv_del',\
        app.CreateValues(['id',uipSubscribeReksadana.id_transaksiinvestasi])\
      )
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2
    
def btnPrintClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipSubscribeReksadana = form.GetUIPartByName('uipSubscribeReksadana')
  uipReksadana = form.GetUIPartByName('uipReksadana')

  form.CommitBuffer()

  CetakAdvis(app, uipSubscribeReksadana, uipReksadana)

def CetakAdvis(app, uipSubscribeReksadana, uipReksadana):
  lHeader = ['Nama Investasi', 'Pihak Ketiga', 'Paket Investasi', \
             'Tgl Transaksi', 'Nilai Subscribe', 'Nominal Investasi']
  sHeader = '|'.join(lHeader)
  tgl = uipSubscribeReksadana.tgl_transaksi
  sTgl = '%s-%s-%s' % (tgl[2],tgl[1],tgl[0])
  lData = [str(uipSubscribeReksadana.GetFieldValue('LReksadana.nama_reksadana')),\
           '%s - %s'% (uipSubscribeReksadana.GetFieldValue('LPihakKetiga.kode_pihak_ketiga'),\
           uipSubscribeReksadana.GetFieldValue('LPihakKetiga.nama_pihak_ketiga')),\
           str(uipSubscribeReksadana.GetFieldValue('LPaketInvestasi.kode_paket_investasi')),\
           str(sTgl),\
           app.ModLibUtils.FormatFloat(',0.00',uipSubscribeReksadana.nilai_subscribe or 0.0),\
           app.ModLibUtils.FormatFloat(',0.00',uipReksadana.akum_nominal or 0.0)]
  sData = '|'.join(lData)
  ph = app.CreateValues(['nama_advis','Subscribe Investasi EQ Tambahan'],['sHeader',sHeader],['sData',sData],['inputer',uipSubscribeReksadana.user_id])
  phret = app.ExecuteScript('investasi/report/AdvisTransaksiInvestasi', ph)
  rec = phret.FirstRecord
  app.DownloadItem(rec.filename,'v')
