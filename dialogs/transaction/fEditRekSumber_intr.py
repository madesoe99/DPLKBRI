global fready
fready = False

def SetControlsForView(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  #form.gRekBaru.ReadOnly = 1
  form.GetPanelByName('gRekBaru').SetAllControlsReadOnly()
  form.GetPanelByName('gRekBaru').SuppressHelpLine = 1
  
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
  #form.gRekBaru.ReadOnly = 1
  form.GetPanelByName('gRekBaru').SetAllControlsReadOnly()
  form.GetPanelByName('gRekBaru').SuppressHelpLine = 1
  
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
      
      uipRekSumberLama = form.GetUIPartByName('uipRekSumberLama')
      uipRekSumberBaru = form.GetUIPartByName('uipRekSumberBaru')
      uipRekSumberLama.First()
      while not uipRekSumberLama.Eof:
        uipRekSumberBaru.Append()        
        uipRekSumberLama.CopyAttributes(uipRekSumberBaru,\
          'LBranchLocation.branch_code;LBranchLocation.branchname;norek_sumber'\
        )
        uipRekSumberLama.Next()
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
    if uipRegisterCIF.no_referensi in ['',None]:
      form.ShowMessage('Nomor Referensi masih kosong. Mohon untuk diisi.')
      return

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
    dlg = app.ConfirmDialog('Anda yakin membatalkan Penggantian Rekening Tabungan Sumber dari peserta %s?' \
      % (uipRegisterCIF.GetFieldValue('LNasabahDPLK.no_peserta')))
    if dlg:
      # batalkan penggantian rekening tabungan sumber
      app.ExecuteScript('transaction/registercif_del',app.CreateValues(['id',\
        uipRegisterCIF.registercif_id]))
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2

def uipRekSumberBaruBeforePost(uip):
  # procedure(uip: TrtfPClassUI)
  if fready:
    form = uip.OwnerForm
    app = form.ClientApplication
    uipMaster = form.GetUIPartByName('uipMaster')
    
    norek_sumber = uip.norek_sumber
    #if norek_sumber[:4] == ???
    uip.SetFieldValue("LBranchLocation.branch_code",\
      uipMaster.GetFieldValue("LBranchLocation.branch_code"))
    uip.SetFieldValue("LBranchLocation.BranchName",\
      uipMaster.GetFieldValue("LBranchLocation.BranchName"))