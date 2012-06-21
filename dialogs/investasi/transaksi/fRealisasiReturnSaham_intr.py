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
  form.Caption = 'Lihat Register Realisasi Return Saham'
  SetSelectorReadOnly(form)

def SetControlsForAuth(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnClose').Cancel = 1
  form.Caption = 'Otorisasi Register Realisasi Return Saham'
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

def InitValues(uipRealisasiReturnSaham, uipSaham):
  uipRealisasiReturnSaham.Edit()
  uipRealisasiReturnSaham.nominal_investasi = uipSaham.akum_nominal
  uipRealisasiReturnSaham.NAB = uipSaham.NAB
  NABUdpate(uipRealisasiReturnSaham, uipSaham)
  uipRealisasiReturnSaham.unit_penyertaan = uipSaham.unit_penyertaan

def FormShow(form, parameter):
  # set caption
  form.Caption = parameter.FirstRecord.caption

  uipRealisasiReturnSaham = form.GetUIPartByName('uipRealisasiReturnSaham')

  uipRealisasiReturnSaham.Edit()
  uipRealisasiReturnSaham.mode = parameter.FirstRecord.mode

  if uipRealisasiReturnSaham.mode == 'new':
    InitValues(uipRealisasiReturnSaham, form.GetUIPartByName('uipSaham'))
    if uipRealisasiReturnSaham.GetFieldValue('LSaham.id_investasi'):
      SetSelectorReadOnly(form)

  if uipRealisasiReturnSaham.mode == 'viewdoc':
    form.Caption = 'Lihat Transaksi Realisasi Return Saham'
    SetControlsForViewDoc(form)
    UnhideControls(form)
  else:
    if uipRealisasiReturnSaham.mode == 'view':
      SetControlsForView(form)
    elif uipRealisasiReturnSaham.mode == 'auth':
      SetControlsForAuth(form)
    elif uipRealisasiReturnSaham.mode == 'edit':
      SetSelectorReadOnly(form)
      form.Caption = 'Koreksi Register Realisasi Return Saham'

def LSahamAfterLookup(sender, linkui):
  form = sender.OwnerForm

  uipRealisasiReturnSaham = form.GetUIPartByName('uipRealisasiReturnSaham')
  uipRealisasiReturnSaham.Edit()
  
  uipRealisasiReturnSaham.SetFieldValue('LPihakKetiga.kode_pihak_ketiga',  uipRealisasiReturnSaham.GetFieldValue('LSaham.kode_pihak_ketiga'))
  uipRealisasiReturnSaham.SetFieldValue('LPihakKetiga.nama_pihak_ketiga', uipRealisasiReturnSaham.GetFieldValue('LSaham.LPihakKetiga.nama_pihak_ketiga'))
  uipRealisasiReturnSaham.SetFieldValue('LPaketInvestasi.kode_paket_investasi', uipRealisasiReturnSaham.GetFieldValue('LSaham.kode_paket_investasi'))
  uipRealisasiReturnSaham.SetFieldValue('LPaketInvestasi.nama_paket_investasi', uipRealisasiReturnSaham.GetFieldValue('LSaham.LRincianPaketInvestasi.LPaketInvestasi.nama_paket_investasi'))
  uipRealisasiReturnSaham.SetFieldValue('LJenisInvestasi.kode_jns_investasi', uipRealisasiReturnSaham.GetFieldValue('LSaham.kode_jns_investasi'))
  uipRealisasiReturnSaham.SetFieldValue('LJenisInvestasi.nama_jns_investasi', uipRealisasiReturnSaham.GetFieldValue('LSaham.LRincianPaketInvestasi.LJenisInvestasi.nama_jns_investasi'))

  uipSaham = form.GetUIPartByName('uipSaham')
  uipSaham.Edit()
  uipSaham.akum_nominal = uipRealisasiReturnSaham.GetFieldValue('LSaham.akum_nominal')
  uipSaham.NAB_awal = uipRealisasiReturnSaham.GetFieldValue('LSaham.NAB_awal')
  uipSaham.NAB = uipRealisasiReturnSaham.GetFieldValue('LSaham.NAB')
  uipSaham.unit_penyertaan = uipRealisasiReturnSaham.GetFieldValue('LSaham.unit_penyertaan')
  #uipSaham.akum_piutangLR = uipRealisasiReturnSaham.GetFieldValue('LSaham.akum_piutangLR')
  #uipSaham.akum_LR = uipRealisasiReturnSaham.GetFieldValue('LSaham.akum_LR')
  #uipSaham.NAB_awal = uipRealisasiReturnSaham.GetFieldValue('LSaham.NAB_awal')
  #uipSaham.nominal_jual = uipRealisasiReturnSaham.GetFieldValue('LSaham.nominal_jual')

def NABUdpate(uipRealisasiReturnSaham, uipSaham):
  uipRealisasiReturnSaham.Edit()
  if uipRealisasiReturnSaham.NAB:
    uipRealisasiReturnSaham.unit_penyertaan = uipRealisasiReturnSaham.nominal_investasi / uipRealisasiReturnSaham.NAB
    uipRealisasiReturnSaham.profit = uipRealisasiReturnSaham.NAB * uipSaham.unit_penyertaan - uipRealisasiReturnSaham.nominal_investasi

def NABExit(sender):
  form = sender.OwnerForm
  uipRealisasiReturnSaham = form.GetUIPartByName('uipRealisasiReturnSaham')
  uipSaham = form.GetUIPartByName('uipSaham')
  NABUdpate(uipRealisasiReturnSaham, uipSaham)

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRealisasiReturnSaham = form.GetUIPartByName('uipRealisasiReturnSaham')

  if uipRealisasiReturnSaham.mode == 'viewdoc':
    sender.ExitAction = 2
  else:
    if uipRealisasiReturnSaham.mode not in ['view','auth']:
      form.CommitBuffer()
      
      if uipRealisasiReturnSaham.mode == 'new':
        uipRealisasiReturnSaham.Edit()
        uipRealisasiReturnSaham.__SYSFLAG = 'N'

      form.PostResult()

      sender.ExitAction = 1
    elif uipRealisasiReturnSaham.mode == 'auth':
      dlg = app.ConfirmDialog('Anda yakin menyetujui Realisasi Return Saham ini?')
      if dlg:
        # otorisasi
        app.ExecuteScript('investasi/transaksi/realisasireturnsaham_auth',\
          app.CreateValues(['id',uipRealisasiReturnSaham.id_transaksiinvestasi])\
        )
        sender.ExitAction = 1

def btnCancelClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRealisasiReturnSaham = form.GetUIPartByName('uipRealisasiReturnSaham')

  if uipRealisasiReturnSaham.mode == 'auth':
    dlg = app.ConfirmDialog('Anda yakin membatalkan Realisasi Return Saham ini?')
    if dlg:
      # hapus/tolak
      app.ExecuteScript('investasi/transaksi/translrinvestasi_del',\
        app.CreateValues(['id',uipRealisasiReturnSaham.id_transaksiinvestasi])\
      )
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2

