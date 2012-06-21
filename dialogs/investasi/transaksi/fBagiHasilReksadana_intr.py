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
  form.Caption = 'Lihat Register Bagi Hasil Reksadana'
  SetSelectorReadOnly(form)

def SetControlsForAuth(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnClose').Cancel = 1
  form.Caption = 'Otorisasi Register Bagi Hasil Reksadana'
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
  form.Caption = parameter.FirstRecord.caption

  uipBagiHasilReksadana = form.GetUIPartByName('uipBagiHasilReksadana')

  uipBagiHasilReksadana.Edit()
  uipBagiHasilReksadana.mode = parameter.FirstRecord.mode

  if uipBagiHasilReksadana.mode == 'new':
    if uipBagiHasilReksadana.GetFieldValue('LReksadana.id_investasi'):
      SetSelectorReadOnly(form)

  if uipBagiHasilReksadana.mode == 'viewdoc':
    form.Caption = 'Lihat Transaksi Bagi Hasil Reksadana'
    SetControlsForViewDoc(form)
    UnhideControls(form)
  else:
    if uipBagiHasilReksadana.mode == 'view':
      SetControlsForView(form)
    elif uipBagiHasilReksadana.mode == 'auth':
      SetControlsForAuth(form)
    elif uipBagiHasilReksadana.mode == 'edit':
      SetSelectorReadOnly(form)
      form.Caption = 'Koreksi Register Bagi Hasil Reksadana'

def LReksadanaAfterLookup(sender, linkui):
  form = sender.OwnerForm

  uipBagiHasilReksadana = form.GetUIPartByName('uipBagiHasilReksadana')
  uipBagiHasilReksadana.Edit()
  
  uipBagiHasilReksadana.SetFieldValue('LPihakKetiga.kode_pihak_ketiga',  uipBagiHasilReksadana.GetFieldValue('LReksadana.kode_pihak_ketiga'))
  uipBagiHasilReksadana.SetFieldValue('LPihakKetiga.nama_pihak_ketiga', uipBagiHasilReksadana.GetFieldValue('LReksadana.LPihakKetiga.nama_pihak_ketiga'))
  uipBagiHasilReksadana.SetFieldValue('LPaketInvestasi.kode_paket_investasi', uipBagiHasilReksadana.GetFieldValue('LReksadana.kode_paket_investasi'))
  uipBagiHasilReksadana.SetFieldValue('LPaketInvestasi.nama_paket_investasi', uipBagiHasilReksadana.GetFieldValue('LReksadana.LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi'))
  uipBagiHasilReksadana.SetFieldValue('LJenisInvestasi.kode_jns_investasi', uipBagiHasilReksadana.GetFieldValue('LReksadana.kode_jns_investasi'))
  uipBagiHasilReksadana.SetFieldValue('LJenisInvestasi.nama_jns_investasi', uipBagiHasilReksadana.GetFieldValue('LReksadana.LRincianPaketInvestasi.LJenisInvestasi.nama_jns_investasi'))

  uipReksadana = form.GetUIPartByName('uipReksadana')
  uipReksadana.Edit()
  uipReksadana.akum_nominal = uipBagiHasilReksadana.GetFieldValue('LReksadana.akum_nominal')
  uipReksadana.akum_piutangLR = uipBagiHasilReksadana.GetFieldValue('LReksadana.akum_piutangLR')
  uipReksadana.akum_LR = uipBagiHasilReksadana.GetFieldValue('LReksadana.akum_LR')
  uipReksadana.NAB_awal = uipBagiHasilReksadana.GetFieldValue('LReksadana.NAB_awal')
  uipReksadana.NAB = uipBagiHasilReksadana.GetFieldValue('LReksadana.NAB')
  uipReksadana.nominal_jual = uipBagiHasilReksadana.GetFieldValue('LReksadana.nominal_jual')
  uipReksadana.unit_penyertaan = uipBagiHasilReksadana.GetFieldValue('LReksadana.unit_penyertaan')

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipBagiHasilReksadana = form.GetUIPartByName('uipBagiHasilReksadana')

  if uipBagiHasilReksadana.mode == 'viewdoc':
    sender.ExitAction = 2
  else:
    if uipBagiHasilReksadana.mode not in ['view','auth']:
      form.CommitBuffer()

      if uipBagiHasilReksadana.mode == 'new':
        uipBagiHasilReksadana.Edit()
        uipBagiHasilReksadana.__SYSFLAG = 'N'

      form.PostResult()

      sender.ExitAction = 1
    elif uipBagiHasilReksadana.mode == 'auth':
      dlg = app.ConfirmDialog('Anda yakin menyetujui Bagi Hasil Reksadana ini?')
      if dlg:
        # otorisasi
        app.ExecuteScript('investasi/transaksi/bagihasilreksadana_auth',\
          app.CreateValues(['id',uipBagiHasilReksadana.id_transaksiinvestasi])\
        )
        sender.ExitAction = 1

def btnCancelClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipBagiHasilReksadana = form.GetUIPartByName('uipBagiHasilReksadana')

  if uipBagiHasilReksadana.mode == 'auth':
    dlg = app.ConfirmDialog('Anda yakin membatalkan Bagi Hasil Reksadana ini?')
    if dlg:
      # hapus/tolak
      #app.ExecuteScript('investasi/transaksi/alokinvtambahan_del',\
      app.ExecuteScript('investasi/transaksi/translrinvestasi_del',\
        app.CreateValues(['id',uipBagiHasilReksadana.id_transaksiinvestasi])\
      )
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2

