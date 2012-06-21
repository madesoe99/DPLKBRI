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
  form.Caption = 'Lihat Register Realisasi Return Reksadana'
  SetSelectorReadOnly(form)

def SetControlsForAuth(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnClose').Cancel = 1
  form.Caption = 'Otorisasi Register Realisasi Return Reksadana'
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

def InitValues(uipRealisasiReturn, uipReksadana):
  uipRealisasiReturn.Edit()
  uipRealisasiReturn.nominal_investasi = uipReksadana.akum_nominal
  uipRealisasiReturn.NAB = uipReksadana.NAB
  NABUdpate(uipRealisasiReturn, uipReksadana)
  uipRealisasiReturn.unit_penyertaan = uipReksadana.unit_penyertaan

def FormShow(form, parameter):
  # set caption
  form.Caption = parameter.FirstRecord.caption

  uipRealisasiReturn = form.GetUIPartByName('uipRealisasiReturn')

  uipRealisasiReturn.Edit()
  uipRealisasiReturn.mode = parameter.FirstRecord.mode

  if uipRealisasiReturn.mode == 'new':
    InitValues(uipRealisasiReturn, form.GetUIPartByName('uipReksadana'))
    if uipRealisasiReturn.GetFieldValue('LReksadana.id_investasi'):
      SetSelectorReadOnly(form)

  if uipRealisasiReturn.mode == 'viewdoc':
    form.Caption = 'Lihat Transaksi Realisasi Return Reksadana'
    SetControlsForViewDoc(form)
    UnhideControls(form)
  else:
    if uipRealisasiReturn.mode == 'view':
      SetControlsForView(form)
    elif uipRealisasiReturn.mode == 'auth':
      SetControlsForAuth(form)
    elif uipRealisasiReturn.mode == 'edit':
      SetSelectorReadOnly(form)
      form.Caption = 'Koreksi Register Realisasi Return Reksadana'

def LReksadanaAfterLookup(sender, linkui):
  form = sender.OwnerForm

  uipRealisasiReturn = form.GetUIPartByName('uipRealisasiReturn')
  uipRealisasiReturn.Edit()
  
  uipRealisasiReturn.SetFieldValue('LPihakKetiga.kode_pihak_ketiga',  uipRealisasiReturn.GetFieldValue('LReksadana.kode_pihak_ketiga'))
  uipRealisasiReturn.SetFieldValue('LPihakKetiga.nama_pihak_ketiga', uipRealisasiReturn.GetFieldValue('LReksadana.LPihakKetiga.nama_pihak_ketiga'))
  uipRealisasiReturn.SetFieldValue('LPaketInvestasi.kode_paket_investasi', uipRealisasiReturn.GetFieldValue('LReksadana.kode_paket_investasi'))
  uipRealisasiReturn.SetFieldValue('LPaketInvestasi.nama_paket_investasi', uipRealisasiReturn.GetFieldValue('LReksadana.LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi'))
  uipRealisasiReturn.SetFieldValue('LJenisInvestasi.kode_jns_investasi', uipRealisasiReturn.GetFieldValue('LReksadana.kode_jns_investasi'))
  uipRealisasiReturn.SetFieldValue('LJenisInvestasi.nama_jns_investasi', uipRealisasiReturn.GetFieldValue('LReksadana.LRincianPaketInvestasi.LJenisInvestasi.nama_jns_investasi'))

  uipReksadana = form.GetUIPartByName('uipReksadana')
  uipReksadana.Edit()
  uipReksadana.akum_nominal = uipRealisasiReturn.GetFieldValue('LReksadana.akum_nominal')
  uipReksadana.NAB_awal = uipRealisasiReturn.GetFieldValue('LReksadana.NAB_awal')
  uipReksadana.NAB = uipRealisasiReturn.GetFieldValue('LReksadana.NAB')
  uipReksadana.unit_penyertaan = uipRealisasiReturn.GetFieldValue('LReksadana.unit_penyertaan')
  #uipReksadana.akum_piutangLR = uipRealisasiReturn.GetFieldValue('LReksadana.akum_piutangLR')
  #uipReksadana.akum_LR = uipRealisasiReturn.GetFieldValue('LReksadana.akum_LR')
  #uipReksadana.NAB_awal = uipRealisasiReturn.GetFieldValue('LReksadana.NAB_awal')
  #uipReksadana.nominal_jual = uipRealisasiReturn.GetFieldValue('LReksadana.nominal_jual')

def NABUdpate(uipRealisasiReturn, uipReksadana):
  uipRealisasiReturn.Edit()
  if uipRealisasiReturn.NAB:
    uipRealisasiReturn.unit_penyertaan = uipRealisasiReturn.nominal_investasi / uipRealisasiReturn.NAB
    uipRealisasiReturn.profit = uipRealisasiReturn.NAB * uipReksadana.unit_penyertaan - uipRealisasiReturn.nominal_investasi

def NABExit(sender):
  form = sender.OwnerForm
  uipRealisasiReturn = form.GetUIPartByName('uipRealisasiReturn')
  uipReksadana = form.GetUIPartByName('uipReksadana')
  NABUdpate(uipRealisasiReturn, uipReksadana)

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRealisasiReturn = form.GetUIPartByName('uipRealisasiReturn')

  if uipRealisasiReturn.mode == 'viewdoc':
    sender.ExitAction = 2
  else:
    if uipRealisasiReturn.mode not in ['view','auth']:
      form.CommitBuffer()
      
      if uipRealisasiReturn.mode == 'new':
        uipRealisasiReturn.Edit()
        uipRealisasiReturn.__SYSFLAG = 'N'

      form.PostResult()

      sender.ExitAction = 1
    elif uipRealisasiReturn.mode == 'auth':
      dlg = app.ConfirmDialog('Anda yakin menyetujui Realisasi Return Reksadana ini?')
      if dlg:
        # otorisasi
        app.ExecuteScript('investasi/transaksi/realisasireturn_auth',\
          app.CreateValues(['id',uipRealisasiReturn.id_transaksiinvestasi])\
        )
        sender.ExitAction = 1

def btnCancelClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRealisasiReturn = form.GetUIPartByName('uipRealisasiReturn')

  if uipRealisasiReturn.mode == 'auth':
    dlg = app.ConfirmDialog('Anda yakin membatalkan Realisasi Return Reksadana ini?')
    if dlg:
      # hapus/tolak
      app.ExecuteScript('investasi/transaksi/translrinvestasi_del',\
        app.CreateValues(['id',uipRealisasiReturn.id_transaksiinvestasi])\
      )
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2

