def SetControlsForView(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetPanelByName('pDataBaru').SetAllControlsReadOnly()
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
  form.Caption = 'Lihat Detil Hasil ' + form.Caption

def SetControlsForAuth(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetPanelByName('pDataBaru').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnClose').Cancel = 1
  form.Caption = 'Otorisasi Hasil ' + form.Caption

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
    #mode New or Edit
    uipRegisterCIF.user_id = app.UserID

    dh = app.ExecuteScript('getsessioninfo',app.CreateValues(['id',1]))
    uipRegisterCIF.terminal_id = dh.FirstRecord.sessioninfo

    if uipRegisterCIF.mode == 'new':
      uipRegisterCIF.SetFieldValue('LNasabahDPLK.no_peserta',uipMaster.no_peserta)
      uipRegisterCIF.SetFieldValue('LNasabahDPLK.nama_lengkap',\
        uipMaster.GetFieldValue('LNasabahDPLK.nama_lengkap'))
      uipRegisterCIF.SetFieldValue('LRekeningDPLK.no_rekening',uipMaster.no_rekening)
      uipRegisterCIF.SetFieldValue('LRekeningDPLK.keterangan',uipMaster.keterangan)
      uipRegisterCIF.iuran_pst = uipMaster.iuran_pst
      uipRegisterCIF.iuran_pk = uipMaster.iuran_pk
      uipRegisterCIF.sistem_pembayaran_iuran = uipMaster.sistem_pembayaran_iuran
      uipRegisterCIF.tgl_penarikan_iuran = uipMaster.tgl_penarikan_iuran
      uipRegisterCIF.REKSUMBER_NO = uipMaster.REKSUMBER_NO
      uipRegisterCIF.REKSUMBER_NAMA = uipMaster.REKSUMBER_NAMA

      '''uipRegisterCIF.SetFieldValue('LNasabahDPLK.LRekeningDPLK.iuran_pst',\
        uipMaster.iuran_pst)
      uipRegisterCIF.SetFieldValue('LNasabahDPLK.LRekeningDPLK.iuran_pk',\
        uipMaster.iuran_pk)'''
    else:
      #mode edit
      form.GetControlByName('pData.no_referensi').ReadOnly = 1
      form.GetControlByName('pData.no_referensi').Color = -2147483624

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterCIF = form.GetUIPartByName('uipRegisterCIF')
  uipP = form.GetUIPartByName('uipParameter')

  if uipRegisterCIF.mode not in ['view','auth']:
    #mode New or Edit

    #checking nomor referensi
    if uipRegisterCIF.no_referensi in ['',None]:
      form.ShowMessage('Nomor Referensi masih kosong. Mohon untuk diisi.')
      return
    
    if uipRegisterCIF.sistem_pembayaran_iuran == "R":
      """iuran peserta"""
      if uipRegisterCIF.iuran_pst in ['', 0, None]:
        app.ShowMessage('Iuran Rutin Peserta masih kosong')
        return
              
      """tgl penarikan iuran rutin"""
      if uipRegisterCIF.tgl_penarikan_iuran in ['', 0, None]:
        app.ShowMessage('Tanggal Penarikan Iuran Rutin masih kosong')
        return
              
      """nomor akun rekening sumber"""
      if uipRegisterCIF.REKSUMBER_NO in ['', 0, None]:
        app.ShowMessage('No. Akun Rekening Sumber masih kosong')
        return
              
      """nama pemilik rekening sumber"""
      if uipRegisterCIF.REKSUMBER_NAMA in ['', 0, None]:
        app.ShowMessage('Nama Pemilik Rekening Sumber masih kosong')
        return
              
      """checking besar iuran peserta dan iuran pemberi kerja"""
      if uipP.IS_ONLY_MIN_JML_IURAN_PST:
        #cek minimal iuran masing-masing
        if uipRegisterCIF.iuran_pst < uipP.MIN_JML_IURAN_PST:
          form.ShowMessage('Iuran Peserta tidak boleh kurang dari Minimum Iuran '\
            'Peserta Default, yaitu Rp %.2f' % (uipP.MIN_JML_IURAN_PST))
          return
        elif uipRegisterCIF.iuran_pk < uipP.MIN_JML_IURAN_PK:
          form.ShowMessage('Iuran Pemberi Kerja tidak boleh kurang dari Minimum Iuran '\
            'Pemberi Kerja Default, yaitu Rp %.2f' % (uipP.MIN_JML_IURAN_PST))
          return
      else:
        #cek minimal iuran akumulasi
        if (uipRegisterCIF.iuran_pst+uipRegisterCIF.iuran_pk) < uipP.MIN_JML_IURAN_PST:
          form.ShowMessage('Gabungan Iuran Peserta dan Iuran Pemberi Kerja tidak boleh '\
            'kurang dari Minimum Iuran Default,\nyaitu Rp %.2f' % (uipP.MIN_JML_IURAN_PST))
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
    dlg = app.ConfirmDialog('Anda yakin membatalkan %s peserta %s %s?'\
      % (sender.OwnerForm.Caption, uipRegisterCIF.GetFieldValue('LNasabahDPLK.no_peserta'),\
      uipRegisterCIF.GetFieldValue('LNasabahDPLK.nama_lengkap')))
    if dlg:
      # batalkan hasil koreksi iuran peserta / pemberi kerja
      app.ExecuteScript('transaction/registercif_del',app.CreateValues(['id',\
        uipRegisterCIF.registercif_id]))
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2

