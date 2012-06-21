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
  form.Caption = 'Lihat Register Bagi Hasil Saham'
  SetSelectorReadOnly(form)

def SetControlsForAuth(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnClose').Cancel = 1
  form.Caption = 'Otorisasi Register Bagi Hasil Saham'
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
  form.Caption = parameter.FirstRecord.caption

  uipBagiHasilSaham = form.GetUIPartByName('uipBagiHasilSaham')

  uipBagiHasilSaham.Edit()
  uipBagiHasilSaham.mode = parameter.FirstRecord.mode

  if uipBagiHasilSaham.mode == 'new':
    if uipBagiHasilSaham.GetFieldValue('LSaham.id_investasi'):
      SetSelectorReadOnly(form)

  if uipBagiHasilSaham.mode == 'viewdoc':
    form.Caption = 'Lihat Transaksi Bagi Hasil Saham'
    SetControlsForViewDoc(form)
    UnhideControls(form)
  else:
    if uipBagiHasilSaham.mode == 'view':
      SetControlsForView(form)
    elif uipBagiHasilSaham.mode == 'auth':
      SetControlsForAuth(form)
    elif uipBagiHasilSaham.mode == 'edit':
      SetSelectorReadOnly(form)
      form.Caption = 'Koreksi Register Bagi Hasil Saham'

def LSahamAfterLookup(sender, linkui):
  form = sender.OwnerForm

  uipBagiHasilSaham = form.GetUIPartByName('uipBagiHasilSaham')
  uipBagiHasilSaham.Edit()
  
  uipBagiHasilSaham.SetFieldValue('LPihakKetiga.kode_pihak_ketiga',  uipBagiHasilSaham.GetFieldValue('LSaham.kode_pihak_ketiga'))
  uipBagiHasilSaham.SetFieldValue('LPihakKetiga.nama_pihak_ketiga', uipBagiHasilSaham.GetFieldValue('LSaham.LPihakKetiga.nama_pihak_ketiga'))
  uipBagiHasilSaham.SetFieldValue('LPaketInvestasi.kode_paket_investasi', uipBagiHasilSaham.GetFieldValue('LSaham.kode_paket_investasi'))
  uipBagiHasilSaham.SetFieldValue('LPaketInvestasi.nama_paket_investasi', uipBagiHasilSaham.GetFieldValue('LSaham.LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi'))
  uipBagiHasilSaham.SetFieldValue('LJenisInvestasi.kode_jns_investasi', uipBagiHasilSaham.GetFieldValue('LSaham.kode_jns_investasi'))
  uipBagiHasilSaham.SetFieldValue('LJenisInvestasi.nama_jns_investasi', uipBagiHasilSaham.GetFieldValue('LSaham.LRincianPaketInvestasi.LJenisInvestasi.nama_jns_investasi'))

  uipSaham = form.GetUIPartByName('uipSaham')
  uipSaham.Edit()
  uipSaham.akum_nominal = uipBagiHasilSaham.GetFieldValue('LSaham.akum_nominal')
  uipSaham.akum_piutangLR = uipBagiHasilSaham.GetFieldValue('LSaham.akum_piutangLR')
  uipSaham.akum_LR = uipBagiHasilSaham.GetFieldValue('LSaham.akum_LR')
  uipSaham.NAB_awal = uipBagiHasilSaham.GetFieldValue('LSaham.NAB_awal')
  uipSaham.NAB = uipBagiHasilSaham.GetFieldValue('LSaham.NAB')
  uipSaham.nominal_jual = uipBagiHasilSaham.GetFieldValue('LSaham.nominal_jual')
  uipSaham.unit_penyertaan = uipBagiHasilSaham.GetFieldValue('LSaham.unit_penyertaan')

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipBagiHasilSaham = form.GetUIPartByName('uipBagiHasilSaham')

  if uipBagiHasilSaham.mode == 'viewdoc':
    sender.ExitAction = 2
  else:
    if uipBagiHasilSaham.mode not in ['view','auth']:
      form.CommitBuffer()

      if uipBagiHasilSaham.mode == 'new':
        uipBagiHasilSaham.Edit()
        uipBagiHasilSaham.__SYSFLAG = 'N'

      form.PostResult()

      sender.ExitAction = 1
    elif uipBagiHasilSaham.mode == 'auth':
      dlg = app.ConfirmDialog('Anda yakin menyetujui Bagi Hasil Saham ini?')
      if dlg:
        # otorisasi
        app.ExecuteScript('investasi/transaksi/bagihasilSaham_auth',\
          app.CreateValues(['id',uipBagiHasilSaham.id_transaksiinvestasi])\
        )
        sender.ExitAction = 1

def btnCancelClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipBagiHasilSaham = form.GetUIPartByName('uipBagiHasilSaham')

  if uipBagiHasilSaham.mode == 'auth':
    dlg = app.ConfirmDialog('Anda yakin membatalkan Bagi Hasil Saham ini?')
    if dlg:
      # hapus/tolak
      #app.ExecuteScript('investasi/transaksi/alokinvtambahan_del',\
      app.ExecuteScript('investasi/transaksi/translrinvestasi_del',\
        app.CreateValues(['id',uipBagiHasilSaham.id_transaksiinvestasi])\
      )
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2

