global fready
fready = False

def SetControlsForView(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetPanelByName('pPaketInvestasi').SetAllControlsReadOnly()
  
  #form.gPaketBaru.ReadOnly = 1
  form.GetPanelByName('gPaketBaru').SetAllControlsReadOnly()
  form.GetPanelByName('gPaketBaru').SuppressHelpLine = 1
  
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnOK').Enabled = 0
  form.GetControlByName('pButton.btnOK').Default = 0
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Enabled = 0
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnClose').Caption = '&Tutup'
  form.GetControlByName('pButton.btnClose').Default = 1
  form.Caption = 'Lihat Detil ' + form.Caption

def SetControlsForAuth(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetPanelByName('pPaketInvestasi').SetAllControlsReadOnly()
  
  #form.gPaketBaru.ReadOnly = 1
  form.GetPanelByName('gPaketBaru').SetAllControlsReadOnly()
  form.GetPanelByName('gPaketBaru').SuppressHelpLine = 1
  
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.Caption = 'Otorisasi ' + form.Caption

def FormShow(form, parameter):
  app = form.ClientApplication
  uipRegisterCIF = form.GetUIPartByName('uipRegisterCIF')
  uipMaster = form.GetUIPartByName('uipMaster')

  uipRegisterCIF.Edit()
  uipRegisterCIF.mode = parameter.FirstRecord.mode
  uipRegisterCIF.cbKombinasiPaket = 0
  
  if uipRegisterCIF.mode == 'view':
    SetControlsForView(form)
  elif uipRegisterCIF.mode == 'auth':
    SetControlsForAuth(form)
  else:
    #mode New atau Edit
    uipRegisterCIF.user_id = app.UserID

    dh = app.ExecuteScript('getsessioninfo',app.CreateValues(['id',1]))
    uipRegisterCIF.terminal_id = dh.FirstRecord.sessioninfo

    if uipRegisterCIF.mode == 'new':
      uipRegisterCIF.SetFieldValue('LNasabahDPLK.no_peserta',uipMaster.no_peserta)
      uipRegisterCIF.SetFieldValue('LNasabahDPLK.nama_lengkap',uipMaster.GetFieldValue('LNasabahDPLK.nama_lengkap'))
      uipRegisterCIF.SetFieldValue('LRekeningDPLK.no_rekening',uipMaster.no_rekening)
      
      uipRekDPLK = form.GetUIPartByName('uipRekDPLK')
      uipRegDetail = form.GetUIPartByName('uipRegDetail')
      uipRekDPLK.First()
      while not uipRekDPLK.Eof:
        uipRegDetail.Append()        
        uipRekDPLK.CopyAttributes(uipRegDetail,\
          'LPaketInvestasi.kode_paket_investasi;LPaketInvestasi.nama_paket_investasi'\
        )
        uipRegDetail.SetFieldValue('proporsi', uipRekDPLK.GetFieldValue('pct_alokasi'))

        uipRekDPLK.Next()
    else:
      form.GetControlByName('pData.no_referensi').ReadOnly = 1
      form.GetControlByName('pData.no_referensi').Color = -2147483624
  
  global fready
  fready = True

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterCIF = form.GetUIPartByName('uipRegisterCIF')

  if uipRegisterCIF.mode not in ['view','auth']:
    #mode New or edit

    """checking nomor referensi"""
    #if uipRegisterCIF.no_referensi in ['',None]:
    #  form.ShowMessage('Nomor Referensi masih kosong. Mohon untuk diisi.')
    #  return

    """cek proporsi paket"""
    uipPaket = form.GetUIPartByName("uipRegDetail")
    remProp = 100
    uipPaket.First()
    while not uipPaket.Eof:
      remProp = remProp - uipPaket.proporsi
      uipPaket.Next()
    
    if remProp != 0:
      form.ShowMessage('Proporsi pembagian paket investasi belum tepat mencapai 100%')
      return False
      
    form.CommitBuffer()
    form.PostResult()
  elif uipRegisterCIF.mode == 'auth':
    #mode auth, go otorisasi
    app.ExecuteScript('transaction/registercif_auth',app.CreateValues(['id',\
      uipRegisterCIF.registercif_id]))
  #else: mode view, do nothing

  sender.ExitAction = 1

def btnCancelClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterCIF = form.GetUIPartByName('uipRegisterCIF')

  if uipRegisterCIF.mode == 'auth':
    dlg = app.ConfirmDialog('Anda yakin membatalkan Pemindahan Paket Investasi peserta %s?' \
      % (uipRegisterCIF.GetFieldValue('LNasabahDPLK.no_peserta')))
    if dlg:
      # batalkan pindah paket investasi
      app.ExecuteScript('transaction/registercif_del',app.CreateValues(['id',\
        uipRegisterCIF.registercif_id]))
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2


def cbKombinasiPaketOnClick(sender):
  # procedure(sender: TrtfCheckBox)
  global fready
  if fready:
    form = sender.Ownerform
    app = form.ClientApplication
    uipPaket = form.GetUIPartByName("uipRegDetail")
    uipTmpPaket = form.GetUIPartByName("uipTmpPaket")
    
    uipPaket.ClearData()
    if sender.Checked:
      uipTmpPaket.First()
      while not uipTmpPaket.Eof:
        uipPaket.Append()
        uipPaket.SetFieldValue("LPaketInvestasi.kode_paket_investasi", uipTmpPaket.kode_pi)
        uipPaket.SetFieldValue("LPaketInvestasi.nama_paket_investasi", uipTmpPaket.nama_pi)
        uipPaket.SetFieldValue("proporsi", 0.0)
        uipTmpPaket.Next()

def btnClearPaketOnClick(sender):
  # procedure(sender: TrtfButton)
  form = sender.OwnerForm
  app = form.ClientApplication
    
  uipRegisterCIF = form.GetUIPartByName("uipRegisterCIF")
  uipPaket = form.GetUIPartByName("uipRegDetail")
  
  uipPaket.ClearData()
  uipRegisterCIF.cbKombinasiPaket = 0
  
def LPaketInvestasi_kode_paket_investasiOnAfterLookup(sender, linkui):
  # procedure(sender: TrtfGridColumn; linkui: TrtfLinkUIElmtSetting)
  global fready
  if fready:
    form = sender.OwnerForm
    app = form.ClientApplication
    uipPaket = form.GetUIPartByName("uipRegDetail")
    
    uipPaket.SetFieldValue("proporsi", 100.0)
  
