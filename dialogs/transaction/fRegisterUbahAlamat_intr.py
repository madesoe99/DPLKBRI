gReady=0

def SetControlsForView(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetPanelByName('pAlamatTinggal').SetAllControlsReadOnly()
  form.GetPanelByName('pAlamatSurat').SetAllControlsReadOnly()
  form.GetPanelByName('pAlamatKantor').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnOK').Enabled = 0
  form.GetControlByName('pButton.btnOK').Default = 0
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Enabled = 0
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  form.GetControlByName('pButton.btnClose').Caption = '&Tutup'
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnClose').Default = 1
  form.GetControlByName('pButton.btnClose').Cancel = 1
  form.Caption = 'Lihat Detil ' + form.Caption

def SetControlsForAuth(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetPanelByName('pAlamatTinggal').SetAllControlsReadOnly()
  form.GetPanelByName('pAlamatSurat').SetAllControlsReadOnly()
  form.GetPanelByName('pAlamatKantor').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnClose').Cancel = 1
  form.Caption = 'Otorisasi ' + form.Caption

def FormShow(form, parameter):
  app = form.ClientApplication
  uipRegisterCIF = form.GetUIPartByName('uipRegisterCIF')
  uipMaster = form.GetUIPartByName('uipMaster')

  uipRegisterCIF.Edit()
  uipRegisterCIF.mode = parameter.FirstRecord.mode
  uipRegisterCIF.isSamaAlamat = 0

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
      uipRegisterCIF.SetFieldValue('LNasabahDPLK.nama_lengkap',uipMaster.nama_lengkap)
      
      uipMaster.CopyAttributes(uipRegisterCIF,\
        'alamat_jalan;alamat_jalan2;alamat_rtrw;alamat_rw;alamat_kelurahan;'\
        'alamat_kecamatan;alamat_kota;alamat_propinsi;'\
        'alamat_kode_pos;alamat_telepon;alamat_telepon2;'\
        'alamat_kantor_jalan;alamat_kantor_jalan2;alamat_kantor_kelurahan;'\
        'alamat_kantor_kecamatan;alamat_kantor_kota;alamat_kantor_propinsi;'\
        'alamat_kantor_kode_pos;alamat_kantor_telepon;alamat_kantor_telepon2;'\
        'alamat_surat_jalan;alamat_surat_jalan2;alamat_surat_rtrw;alamat_surat_rw;alamat_surat_kelurahan;'\
        'alamat_surat_kecamatan;alamat_surat_kota;alamat_surat_propinsi;'\
        'alamat_surat_kode_pos;alamat_surat_telepon;alamat_surat_telepon2'\
      )
      
      uipRegisterCIF.SetFieldValue('LATKodePos.id_kodepos',uipMaster.GetFieldValue('LATKodePos.id_kodepos'))
      uipRegisterCIF.SetFieldValue('LATKodePos.kode_pos',uipMaster.GetFieldValue('LATKodePos.kode_pos'))
      uipRegisterCIF.SetFieldValue('LATPropinsi.kode_propinsi',uipMaster.GetFieldValue('LATPropinsi.kode_propinsi'))
      uipRegisterCIF.SetFieldValue('LATPropinsi.nama_propinsi',uipMaster.GetFieldValue('LATPropinsi.nama_propinsi'))
      uipRegisterCIF.SetFieldValue('LATKota.kode_kota',uipMaster.GetFieldValue('LATKota.kode_kota'))
      uipRegisterCIF.SetFieldValue('LATKota.nama_kota',uipMaster.GetFieldValue('LATKota.nama_kota'))
      uipRegisterCIF.SetFieldValue('LATKecamatan.kode_kecamatan',uipMaster.GetFieldValue('LATKecamatan.kode_kecamatan'))
      uipRegisterCIF.SetFieldValue('LATKecamatan.nama_kecamatan',uipMaster.GetFieldValue('LATKecamatan.nama_kecamatan'))
      
      uipRegisterCIF.SetFieldValue('LASKodePos.id_kodepos',uipMaster.GetFieldValue('LASKodePos.id_kodepos'))
      uipRegisterCIF.SetFieldValue('LASKodePos.kode_pos',uipMaster.GetFieldValue('LASKodePos.kode_pos'))
      uipRegisterCIF.SetFieldValue('LASPropinsi.kode_propinsi',uipMaster.GetFieldValue('LASPropinsi.kode_propinsi'))
      uipRegisterCIF.SetFieldValue('LASPropinsi.nama_propinsi',uipMaster.GetFieldValue('LASPropinsi.nama_propinsi'))
      uipRegisterCIF.SetFieldValue('LASKota.kode_kota',uipMaster.GetFieldValue('LASKota.kode_kota'))
      uipRegisterCIF.SetFieldValue('LASKota.nama_kota',uipMaster.GetFieldValue('LASKota.nama_kota'))
      uipRegisterCIF.SetFieldValue('LASKecamatan.kode_kecamatan',uipMaster.GetFieldValue('LASKecamatan.kode_kecamatan'))
      uipRegisterCIF.SetFieldValue('LASKecamatan.nama_kecamatan',uipMaster.GetFieldValue('LASKecamatan.nama_kecamatan'))

      uipRegisterCIF.SetFieldValue('LAKKodePos.id_kodepos',uipMaster.GetFieldValue('LAKKodePos.id_kodepos'))
      uipRegisterCIF.SetFieldValue('LAKKodePos.kode_pos',uipMaster.GetFieldValue('LAKKodePos.kode_pos'))
      uipRegisterCIF.SetFieldValue('LAKPropinsi.kode_propinsi',uipMaster.GetFieldValue('LAKPropinsi.kode_propinsi'))
      uipRegisterCIF.SetFieldValue('LAKPropinsi.nama_propinsi',uipMaster.GetFieldValue('LAKPropinsi.nama_propinsi'))
      uipRegisterCIF.SetFieldValue('LAKKota.kode_kota',uipMaster.GetFieldValue('LAKKota.kode_kota'))
      uipRegisterCIF.SetFieldValue('LAKKota.nama_kota',uipMaster.GetFieldValue('LAKKota.nama_kota'))
      uipRegisterCIF.SetFieldValue('LAKKecamatan.kode_kecamatan',uipMaster.GetFieldValue('LAKKecamatan.kode_kecamatan'))
      uipRegisterCIF.SetFieldValue('LAKKecamatan.nama_kecamatan',uipMaster.GetFieldValue('LAKKecamatan.nama_kecamatan'))

    else:
      #mode Edit
      form.GetControlByName('pData.no_referensi').ReadOnly = 1
      form.GetControlByName('pData.no_referensi').Color = -2147483624
  
  global gReady 
  gReady=1
    
def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterCIF = form.GetUIPartByName('uipRegisterCIF')

  if uipRegisterCIF.mode not in ['view','auth']:
    #mode New or Edit

    """alamat: jalan, rt/rw, kota, provinsi, kode pos, telp rumah (+kode area), handphone"""
    if uipRegisterCIF.alamat_jalan in ["", None]\
      or uipRegisterCIF.alamat_rtrw in ["", None]\
      or uipRegisterCIF.alamat_rw in ["", None]\
      or uipRegisterCIF.GetFieldValue('LATKota.kode_kota') in ["", None]\
      or uipRegisterCIF.GetFieldValue('LATPropinsi.kode_propinsi') in ["", None]\
      or uipRegisterCIF.GetFieldValue('LATKodePos.id_kodepos') in ["", None]\
      or uipRegisterCIF.alamat_telepon in ["", None]\
      or uipRegisterCIF.alamat_telepon2 in ["", None]:
      form.ShowMessage("""Alamat Tempat Tinggal yang harus diisi:\n
        - Jalan
        - RT / RW
        - Kota
        - Propinsi
        - Kode Pos
        - Telp. Rumah
        - Handphone""")
      return False

    if uipRegisterCIF.alamat_surat_jalan in ["", None]\
      or uipRegisterCIF.alamat_surat_rtrw in ["", None]\
      or uipRegisterCIF.alamat_surat_rw in ["", None]\
      or uipRegisterCIF.GetFieldValue('LASKota.kode_kota') in ["", None]\
      or uipRegisterCIF.GetFieldValue('LASPropinsi.kode_propinsi') in ["", None]\
      or uipRegisterCIF.GetFieldValue('LASKodePos.id_kodepos') in ["", None]\
      or uipRegisterCIF.alamat_surat_telepon in ["", None]\
      or uipRegisterCIF.alamat_surat_telepon2 in ["", None]:
      form.ShowMessage("""Alamat Surat yang harus diisi:\n
        - Jalan
        - RT / RW
        - Kota
        - Propinsi
        - Kode Pos
        - Telp. Rumah
        - Handphone""")
      return False
      
    """nomor referensi"""
    #if uipRegisterCIF.no_referensi in ['',None]:
    #  form.ShowMessage('Nomor Referensi masih kosong! Mohon untuk diisi.')
    #  return
      
    # kenapa?
    if uipRegisterCIF.mode == 'new':
      uipRegisterCIF.Edit()
      uipRegisterCIF.__SYSFLAG = 'N'

    form.CommitBuffer()
    form.PostResult()
  elif uipRegisterCIF.mode == 'auth':
    #mode auth, go otorisasi
    app.ExecuteScript('transaction/registercif_auth',\
      app.CreateValues(['id',uipRegisterCIF.registercif_id]))
  #else: mode view, do nothing

  sender.ExitAction = 1

def btnCancelClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterCIF = form.GetUIPartByName('uipRegisterCIF')

  if uipRegisterCIF.mode == 'auth':
    dlg = app.ConfirmDialog('Anda yakin membatalkan Perubahan Alamat Peserta %s a/n. %s?' \
      % (uipRegisterCIF.GetFieldValue('LNasabahDPLK.no_peserta'),\
      uipRegisterCIF.GetFieldValue('LNasabahDPLK.nama_lengkap')))
    if dlg:
      # batalkan perubahan alamat nasabah
      app.ExecuteScript('transaction/registercif_del',app.CreateValues(['id',\
        uipRegisterCIF.registercif_id]))
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2

def ResetAlamatSuratValue(uipart):
  uipart.alamat_surat_jalan = \
  uipart.alamat_surat_jalan2 = \
  uipart.alamat_surat_rtrw = \
  uipart.alamat_surat_rw = \
  uipart.alamat_surat_kelurahan = \
  uipart.alamat_surat_kecamatan = \
  uipart.alamat_surat_kota = \
  uipart.alamat_surat_propinsi = \
  uipart.alamat_surat_telepon = \
  uipart.alamat_surat_telepon2 = None

  uipart.SetFieldValue('LASKodePos.id_kodepos', None)
  uipart.SetFieldValue('LASKodePos.kode_pos', None)
  uipart.SetFieldValue('LASPropinsi.kode_propinsi', None)
  uipart.SetFieldValue('LASPropinsi.nama_propinsi', None)
  uipart.SetFieldValue('LASKota.kode_kota', None)
  uipart.SetFieldValue('LASKota.nama_kota', None)
  uipart.SetFieldValue('LASKecamatan.kode_kecamatan', None)
  uipart.SetFieldValue('LASKecamatan.nama_kecamatan', None)
  
def isSamaAlamatClick(sender):
  global gReady
  form = sender.OwnerForm
  
  if gReady == 1:
    pAlamatSurat = form.GetPanelByName('pAlamatSurat')
    uipRNR = form.GetUIPartByName('uipRegisterCIF')
    uipRNR.Edit()
  
    if sender.Checked:
      #copy isi Alamat ke Alamat Surat
      uipRNR.alamat_surat_jalan = uipRNR.alamat_jalan
      uipRNR.alamat_surat_jalan2 = uipRNR.alamat_jalan2
      uipRNR.alamat_surat_rtrw = uipRNR.alamat_rtrw
      uipRNR.alamat_surat_rw = uipRNR.alamat_rw
      uipRNR.alamat_surat_kelurahan = uipRNR.alamat_kelurahan
      uipRNR.alamat_surat_kecamatan = uipRNR.alamat_kecamatan
      uipRNR.alamat_surat_kota = uipRNR.alamat_kota
      uipRNR.alamat_surat_propinsi = uipRNR.alamat_propinsi
      uipRNR.alamat_surat_telepon = uipRNR.alamat_telepon
      uipRNR.alamat_surat_telepon2 = uipRNR.alamat_telepon2

      uipRNR.SetFieldValue('LASKodePos.id_kodepos', uipRNR.GetFieldValue('LATKodePos.id_kodepos'))
      uipRNR.SetFieldValue('LASKodePos.kode_pos', uipRNR.GetFieldValue('LATKodePos.kode_pos'))
      uipRNR.SetFieldValue('LASPropinsi.kode_propinsi', uipRNR.GetFieldValue('LATPropinsi.kode_propinsi'))
      uipRNR.SetFieldValue('LASPropinsi.nama_propinsi', uipRNR.GetFieldValue('LATPropinsi.nama_propinsi'))
      uipRNR.SetFieldValue('LASKota.kode_kota', uipRNR.GetFieldValue('LATKota.kode_kota'))
      uipRNR.SetFieldValue('LASKota.nama_kota', uipRNR.GetFieldValue('LATKota.nama_kota'))
      uipRNR.SetFieldValue('LASKecamatan.kode_kecamatan', uipRNR.GetFieldValue('LATKecamatan.kode_kecamatan'))
      uipRNR.SetFieldValue('LASKecamatan.nama_kecamatan', uipRNR.GetFieldValue('LATKecamatan.nama_kecamatan'))
  
    else:
      #reset isi Alamat Surat
      ResetAlamatSuratValue(uipRNR)

def LATKodePosOnAfterLookup(sender, linkui):
  # procedure(sender: TrtfDBLookupEdit; linkui: TrtfLinkUIElmtSetting)
  form = sender.OwnerForm
  pAlamat = form.GetPanelByName('pAlamatTinggal')
  
  uipReg = form.GetUIPartByName('uipRegisterCIF')
  uipReg.Edit()
  
  uipReg.SetFieldValue('LATPropinsi.kode_propinsi', uipReg.GetFieldValue('LATKodePos.kode_propinsi'))
  uipReg.SetFieldValue('LATPropinsi.nama_propinsi', uipReg.GetFieldValue('LATKodePos.LPropinsi.nama_propinsi'))
  pAlamat.GetControlByName('LATPropinsi').Enabled = 0
  
  uipReg.SetFieldValue('LATKota.kode_kota', uipReg.GetFieldValue('LATKodePos.kode_kota'))
  uipReg.SetFieldValue('LATKota.nama_kota', uipReg.GetFieldValue('LATKodePos.LKota.nama_kota'))
  pAlamat.GetControlByName('LATKota').Enabled = 0
  
  uipReg.SetFieldValue('LATKecamatan.kode_kecamatan', uipReg.GetFieldValue('LATKodePos.kode_kecamatan'))
  uipReg.SetFieldValue('LATKecamatan.nama_kecamatan', uipReg.GetFieldValue('LATKodePos.LKecamatan.nama_kecamatan'))
  pAlamat.GetControlByName('LATKecamatan').Enabled = 0
  
  uipReg.SetFieldValue('alamat_kelurahan', uipReg.GetFieldValue('LATKodePos.nama_kelurahan'))
  if not uipReg.GetFieldValue('LATKodePos.nama_kelurahan') in ['', None]:
    pAlamat.GetControlByName('alamat_kelurahan').Enabled = 0

def LASKodePosOnAfterLookup(sender, linkui):
  # procedure(sender: TrtfDBLookupEdit; linkui: TrtfLinkUIElmtSetting)
  form = sender.OwnerForm
  pAlamatSurat = form.GetPanelByName('pAlamatSurat')
  
  uipReg = form.GetUIPartByName('uipRegisterCIF')
  uipReg.Edit()
  
  uipReg.SetFieldValue('LASPropinsi.kode_propinsi', uipReg.GetFieldValue('LASKodePos.kode_propinsi'))
  uipReg.SetFieldValue('LASPropinsi.nama_propinsi', uipReg.GetFieldValue('LASKodePos.LPropinsi.nama_propinsi'))
  pAlamatSurat.GetControlByName('LASPropinsi').Enabled = 0
  
  uipReg.SetFieldValue('LASKota.kode_kota', uipReg.GetFieldValue('LASKodePos.kode_kota'))
  uipReg.SetFieldValue('LASKota.nama_kota', uipReg.GetFieldValue('LASKodePos.LKota.nama_kota'))
  pAlamatSurat.GetControlByName('LASKota').Enabled = 0
  
  uipReg.SetFieldValue('LASKecamatan.kode_kecamatan', uipReg.GetFieldValue('LASKodePos.kode_kecamatan'))
  uipReg.SetFieldValue('LASKecamatan.nama_kecamatan', uipReg.GetFieldValue('LASKodePos.LKecamatan.nama_kecamatan'))
  pAlamatSurat.GetControlByName('LASKecamatan').Enabled = 0
  
  uipReg.SetFieldValue('alamat_surat_kelurahan', uipReg.GetFieldValue('LASKodePos.nama_kelurahan'))
  if not uipReg.GetFieldValue('LASKodePos.nama_kelurahan') in ['', None]:
    pAlamatSurat.GetControlByName('alamat_surat_kelurahan').Enabled = 0
  
def LAKKodePosOnAfterLookup(sender, linkui):
  # procedure(sender: TrtfDBLookupEdit; linkui: TrtfLinkUIElmtSetting)
  form = sender.OwnerForm
  pKantor = form.GetPanelByName('pAlamatKantor')
  
  uipReg = form.GetUIPartByName('uipRegisterCIF')
  uipReg.Edit()
  
  uipReg.SetFieldValue('LAKPropinsi.kode_propinsi', uipReg.GetFieldValue('LAKKodePos.kode_propinsi'))
  uipReg.SetFieldValue('LAKPropinsi.nama_propinsi', uipReg.GetFieldValue('LAKKodePos.LPropinsi.nama_propinsi'))
  pKantor.GetControlByName('LAKPropinsi').Enabled = 0
  
  uipReg.SetFieldValue('LAKKota.kode_kota', uipReg.GetFieldValue('LAKKodePos.kode_kota'))
  uipReg.SetFieldValue('LAKKota.nama_kota', uipReg.GetFieldValue('LAKKodePos.LKota.nama_kota'))
  pKantor.GetControlByName('LAKKota').Enabled = 0
  
  uipReg.SetFieldValue('LAKKecamatan.kode_kecamatan', uipReg.GetFieldValue('LAKKodePos.kode_kecamatan'))
  uipReg.SetFieldValue('LAKKecamatan.nama_kecamatan', uipReg.GetFieldValue('LAKKodePos.LKecamatan.nama_kecamatan'))
  pKantor.GetControlByName('LAKKecamatan').Enabled = 0
  
  uipReg.SetFieldValue('alamat_kantor_kelurahan', uipReg.GetFieldValue('LAKKodePos.nama_kelurahan'))
  if not uipReg.GetFieldValue('LAKKodePos.nama_kelurahan') in ['', None]:
    pKantor.GetControlByName('alamat_kantor_kelurahan').Enabled = 0
  
