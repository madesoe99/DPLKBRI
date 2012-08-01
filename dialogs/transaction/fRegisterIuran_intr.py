gReady=0

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

  uipRegisterCIF.SetFieldValue('nasabah_korporat',0)
  if not uipMaster.GetFieldValue('LNasabahDPLKCorporate.kode_nasabah_corporate') in [0,'',None]:
    uipRegisterCIF.SetFieldValue('nasabah_korporat',1)

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
      uipRegisterCIF.SetFieldValue('LNasabahDPLK.nama_lengkap',uipMaster.GetFieldValue('LNasabahDPLK.nama_lengkap'))
      uipRegisterCIF.SetFieldValue('LRekeningDPLK.no_rekening',uipMaster.no_rekening)
      #uipRegisterCIF.SetFieldValue('LRekeningDPLK.keterangan',uipMaster.keterangan)
      
      if not uipMaster.GetFieldValue('LNasabahDPLKCorporate.kode_nasabah_corporate') in [0,'',None]:
        uipRegisterCIF.SetFieldValue('LRekeningDPLK.kode_nasabah_corporate',uipMaster.GetFieldValue('LNasabahDPLKCorporate.kode_nasabah_corporate'))
        uipRegisterCIF.SetFieldValue('LRekeningDPLK.LNasabahDPLKCorporate.nama_perusahaan',uipMaster.GetFieldValue('LNasabahDPLKCorporate.nama_perusahaan'))
      
      uipRegisterCIF.iuran_pst = uipMaster.iuran_pst
      uipRegisterCIF.iuran_pk = uipMaster.iuran_pk
      uipRegisterCIF.iuran_tmb = uipMaster.iuran_tmb
      uipRegisterCIF.sistem_pembayaran_iuran = uipMaster.sistem_pembayaran_iuran
      uipRegisterCIF.tgl_penarikan_iuran = uipMaster.tgl_penarikan_iuran
      uipRegisterCIF.REKSUMBER_NO = uipMaster.REKSUMBER_NO
      uipRegisterCIF.REKSUMBER_NAMA = uipMaster.REKSUMBER_NAMA
    else:
      #mode edit
      form.GetControlByName('pData.no_referensi').ReadOnly = 1
      form.GetControlByName('pData.no_referensi').Color = -2147483624
      
    SetInformasiIuran(form, uipRegisterCIF.sistem_pembayaran_iuran)
  
  global gReady
  gReady=1

def SetInformasiIuran(form, sistem_pembayaran_iuran):
  pRekening = form.GetPanelByName('pData')
  pRekening2 = form.GetPanelByName('pDataBaru')

  uipReg = form.GetUIPartByName('uipRegisterCIF')
  uipReg.Edit()

  nasabah_korporat = 0
  if pRekening.GetControlByName('nasabah_korporat').Checked:
    nasabah_korporat = 1    
  if nasabah_korporat == 0:
    pRekening2.GetControlByName('sistem_pembayaran_iuran').ControlCaption = 'Sistem Pembayaran Iuran Peserta'
    #pRekening2.GetControlByName('tgl_penarikan_iuran').ControlCaption = 'Tgl. Penarikan Iuran Peserta'
  else:
    pRekening2.GetControlByName('sistem_pembayaran_iuran').ControlCaption = 'Sistem Pembayaran Iuran Tambahan'
    #pRekening2.GetControlByName('tgl_penarikan_iuran').ControlCaption = 'Tgl. Penarikan Iuran Tambahan'
  
  if sistem_pembayaran_iuran == 'R':
    pRekening2.GetControlByName('tgl_penarikan_iuran').Enabled = 1
    pRekening2.GetControlByName('iuran_pk').Enabled = 0
    pRekening2.GetControlByName('REKSUMBER_NO').Enabled = 1
    pRekening2.GetControlByName('REKSUMBER_NAMA').Enabled = 1
    
    uipReg.tgl_penarikan_iuran = 1
    uipReg.iuran_pk = 0.0
    
    if nasabah_korporat == 0:
      pRekening2.GetControlByName('iuran_pst').Enabled = 1
      pRekening2.GetControlByName('iuran_tmb').Enabled = 0
      
      uipReg.iuran_tmb = 0.0
    else:
      pRekening2.GetControlByName('iuran_pst').Enabled = 0
      pRekening2.GetControlByName('iuran_tmb').Enabled = 1
      
      uipReg.iuran_pst = 0.0
  else:
    pRekening2.GetControlByName('tgl_penarikan_iuran').Enabled = 0
    pRekening2.GetControlByName('iuran_pk').Enabled = 0
    pRekening2.GetControlByName('iuran_pst').Enabled = 0
    pRekening2.GetControlByName('iuran_tmb').Enabled = 0
    pRekening2.GetControlByName('REKSUMBER_NO').Enabled = 0
    pRekening2.GetControlByName('REKSUMBER_NAMA').Enabled = 0
    
    uipReg.tgl_penarikan_iuran = None
    uipReg.iuran_pk = 0.0
    uipReg.iuran_pst = 0.0
    uipReg.iuran_tmb = 0.0
    uipReg.REKSUMBER_NO = None
    uipReg.REKSUMBER_NAMA = None
      
def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterCIF = form.GetUIPartByName('uipRegisterCIF')
  uipParam = form.GetUIPartByName('uipParameter')

  if uipRegisterCIF.mode not in ['view','auth']:
    #mode New or Edit

    #checking nomor referensi
    #if uipRegisterCIF.no_referensi in ['',None]:
    #  form.ShowMessage('Nomor Referensi masih kosong. Mohon untuk diisi.')
    #  return
    
    if uipRegisterCIF.sistem_pembayaran_iuran == "R":
      if uipRegisterCIF.nasabah_korporat:
        """iuran tambahan"""
        if uipRegisterCIF.iuran_tmb in ['', 0, None]:
          app.ShowMessage('Iuran Tambahan masih kosong')
          return False
      else:
        """iuran peserta"""
        if uipRegisterCIF.iuran_pst in ['', 0, None]:
          app.ShowMessage('Iuran Peserta masih kosong')
          return False
              
      """tgl penarikan iuran rutin"""
      if uipRegisterCIF.tgl_penarikan_iuran in ['', 0, None]:
        app.ShowMessage('Tanggal Penarikan Iuran Rutin masih kosong')
        return
              
      """nomor akun rekening sumber"""
      if uipRegisterCIF.REKSUMBER_NO in ['', 0, None]:
        app.ShowMessage('Nomor Rekening Sumber masih kosong')
        return
              
      """nama pemilik rekening sumber"""
      if uipRegisterCIF.REKSUMBER_NAMA in ['', 0, None]:
        app.ShowMessage('Nama Pemilik Rekening Sumber masih kosong')
        return
              
      """iuran pemberi kerja, iuran peserta, dan iuran tambahan"""
      if uipParam.IS_ONLY_MIN_JML_IURAN_PST:
        #cek minimal iuran masing-masing
        #if uipRegisterCIF.iuran_pk < uipParam.MIN_JML_IURAN_PK:
        #  form.ShowMessage('Iuran Pemberi Kerja tidak boleh kurang dari Minimum Iuran '\
        #    'Pemberi Kerja Default, yaitu Rp %.2f' % (uipParam.MIN_JML_IURAN_PK))
        #  return False

        if uipRegisterCIF.nasabah_korporat:
          if uipRegisterCIF.iuran_tmb < uipParam.MIN_JML_IURAN_TMB:
            form.ShowMessage('Iuran Tambahan tidak boleh kurang dari Minimum Iuran '\
              'Tambahan Default, yaitu Rp %.2f' % (uipParam.MIN_JML_IURAN_TMB))
            return False
        else:
          if uipRegisterCIF.iuran_pst < uipParam.MIN_JML_IURAN_PST:
            form.ShowMessage('Iuran Peserta tidak boleh kurang dari Minimum Iuran '\
              'Peserta Default, yaitu Rp %.2f' % (uipParam.MIN_JML_IURAN_PST))
            return False
      else:
        #cek minimal iuran akumulasi
        if (uipRegisterCIF.iuran_pk \
          + uipRegisterCIF.iuran_pst \
          + uipRegisterCIF.iuran_tmb) < uipParam.MIN_JML_IURAN_PST:
          form.ShowMessage('Gabungan Iuran Peserta, Iuran Pemberi Kerja, dan Iuran Tambahan tidak boleh '\
            'kurang dari Minimum Iuran Default,\nyaitu Rp %.2f' % (uipParam.MIN_JML_IURAN_PST))
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


def sistem_pembayaran_iuranOnChange(sender):
  # procedure(sender: TrtfDBComboBox)
  global gReady
  if gReady == 1:
    form = sender.OwnerForm
    SetInformasiIuran(form, sender.Values[sender.ItemIndex])