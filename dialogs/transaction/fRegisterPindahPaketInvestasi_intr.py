def SetControlsForView(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
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
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.Caption = 'Otorisasi ' + form.Caption

def FormShow(form, parameter):
  app = form.ClientApplication
  uipRegisterCIF = form.GetUIPartByName('uipRegisterCIF')
  uipRegisterCIF.cbKombinasiPaket = 0

  uipMaster = form.GetUIPartByName('uipMaster')

  uipRegisterCIF.Edit()
  uipRegisterCIF.mode = parameter.FirstRecord.mode

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
      uipRegisterCIF.SetFieldValue('LNasabahDPLK.nama_lengkap',\
        uipMaster.GetFieldValue('LNasabahDPLK.nama_lengkap'))
      uipRegisterCIF.SetFieldValue('LRekeningDPLK.no_rekening',uipMaster.no_rekening)
      uipRegisterCIF.SetFieldValue('LRekeningDPLK.keterangan',uipMaster.keterangan)
      '''uipRegisterCIF.SetFieldValue('LPaketInvestasi.kode_paket_investasi',\
        uipMaster.GetFieldValue('LPaketInvestasi.kode_paket_investasi'))
      uipRegisterCIF.SetFieldValue('LPaketInvestasi.nama_paket_investasi',\
        uipMaster.GetFieldValue('LPaketInvestasi.nama_paket_investasi'))

      uipRegisterCIF.SetFieldValue('LNasabahDPLK.LRekeningDPLK.LPaketInvestasi.kode_paket_investasi',\
        uipMaster.GetFieldValue('LPaketInvestasi.kode_paket_investasi'))
      uipRegisterCIF.SetFieldValue('LNasabahDPLK.LRekeningDPLK.LPaketInvestasi.nama_paket_investasi',\
        uipMaster.GetFieldValue('LPaketInvestasi.nama_paket_investasi'))'''
    else:
      form.GetControlByName('pData.no_referensi').ReadOnly = 1
      form.GetControlByName('pData.no_referensi').Color = -2147483624

  '''kode_paket_investasi = \
    uipRegisterCIF.GetFieldValue('LNasabahDPLK.LRekeningDPLK.LPaketInvestasi.kode_paket_investasi')
  nama_paket_investasi = \
    uipRegisterCIF.GetFieldValue('LNasabahDPLK.LRekeningDPLK.LPaketInvestasi.nama_paket_investasi')

  uipRegisterCIF.SetFieldValue('LPaketInvestasi_lama.kode_paket_investasi',\
    kode_paket_investasi)
  uipRegisterCIF.SetFieldValue('LPaketInvestasi_lama.nama_paket_investasi',\
    nama_paket_investasi)'''

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterCIF = form.GetUIPartByName('uipRegisterCIF')
  uipRekDPLK_New = form.GetUIPartByName('uipRekDPLK_New')

  if uipRegisterCIF.mode not in ['view','auth']:
    #mode New or edit

    #checking nomor referensi
    if uipRegisterCIF.no_referensi in ['',None]:
      form.ShowMessage('Nomor Referensi masih kosong. Mohon untuk diisi.')
      return

    remProp = 100
    uipRekDPLK_New.First()
    while not uipRekDPLK_New.Eof:
      remProp = remProp - uipRekDPLK_New.pct_alokasi
      uipRekDPLK_New.Next()    
    if remProp != 0:
      form.ShowMessage('Proporsi pembagian paket investasi belum tepat mencapai 100%')
      return
      
    '''kode_paket_investasi = \
      uipRegisterCIF.GetFieldValue('LPaketInvestasi.kode_paket_investasi')
    kode_paket_investasi_lama = \
      uipRegisterCIF.GetFieldValue('LPaketInvestasi_lama.kode_paket_investasi')

    #checking paket investasi lama dengan paket baru yang dipilih
    if kode_paket_investasi == kode_paket_investasi_lama:
      form.ShowMessage('Paket Investasi Baru masih sama dengan Paket Investasi Lama!'\
        '\nMohon pilih Paket Investasi Baru yang berbeda.')
      return'''

    form.CommitBuffer()
    
    ph = form.GetDataPacket()
    returns = form.CallServerMethod('saveRegisterPPI', ph)
    retval = returns.FirstRecord
    form.ShowMessage(retval.msgreturn)
    if not retval.success:
      return
    
    #form.PostResult()
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
    dlg = app.ConfirmDialog('Anda yakin membatalkan Pemindahan Paket Investasi peserta %s %s?' \
      % (uipRegisterCIF.GetFieldValue('LNasabahDPLK.no_peserta'),\
      uipRegisterCIF.GetFieldValue('LNasabahDPLK.nama_lengkap')))
    if dlg:
      # batalkan pindah paket investasi
      app.ExecuteScript('transaction/registercif_del',app.CreateValues(['id',\
        uipRegisterCIF.registercif_id]))
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2
    
def cbKombinasiPaketOnClick(sender):
  # procedure(sender: TrtfCheckBox)
  form = sender.OwnerForm
  app = form.ClientApplication
  uipPaket = form.GetUIPartByName("uipRekDPLK_New")
  uipTmpPaket = form.GetUIPartByName("uipTmpPaket")
  
  uipPaket.ClearData()
  if sender.Checked:
    uipTmpPaket.First()
    while not uipTmpPaket.Eof:
      uipPaket.Append()
      uipPaket.SetFieldValue("LPaketInvestasi.kode_paket_investasi", uipTmpPaket.kode_pi)
      uipPaket.SetFieldValue("LPaketInvestasi.nama_paket_investasi", uipTmpPaket.nama_pi)
      uipPaket.SetFieldValue("pct_alokasi", 0.0)
      uipTmpPaket.Next()

def btnClearPaketOnClick(sender):
  # procedure(sender: TrtfButton)
  form = sender.OwnerForm
  app = form.ClientApplication
    
  uipRegisterCIF = form.GetUIPartByName("uipRegisterCIF")
  uipPaket = form.GetUIPartByName("uipRekDPLK_New")
  
  uipPaket.ClearData()
  uipRegisterCIF.cbKombinasiPaket = 0
  
def LPaketInvestasi_kode_paket_investasiOnAfterLookup(sender, linkui):
  # procedure(sender: TrtfGridColumn; linkui: TrtfLinkUIElmtSetting)
  form = sender.OwnerForm
  app = form.ClientApplication
  uipPaket = form.GetUIPartByName("uipRekDPLK_New")
  
  uipPaket.SetFieldValue("pct_alokasi", 100.0)
