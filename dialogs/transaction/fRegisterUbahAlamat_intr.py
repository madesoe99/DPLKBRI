def SetControlsForView(form):
  form.GetPanelByName('pData').SetAllControlsReadOnly()
  form.GetPanelByName('pAlamat').SetAllControlsReadOnly()
  form.GetPanelByName('pAlamatSurat').SetAllControlsReadOnly()
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
  form.GetPanelByName('pAlamat').SetAllControlsReadOnly()
  form.GetPanelByName('pAlamatSurat').SetAllControlsReadOnly()
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
        'alamat_jalan;alamat_jalan2;alamat_rtrw;alamat_kelurahan;'\
        'alamat_kecamatan;alamat_kota;alamat_propinsi;'\
        'alamat_kode_pos;alamat_telepon;alamat_telepon2;'\
        'alamat_surat_jalan;alamat_surat_jalan2;alamat_surat_rtrw;alamat_surat_kelurahan;'\
        'alamat_surat_kecamatan;alamat_surat_kota;alamat_surat_propinsi;'\
        'alamat_surat_kode_pos;alamat_surat_telepon;alamat_surat_telepon2'\
      )
      
      uipRegisterCIF.SetFieldValue('LATPropinsi.kode_propinsi',uipMaster.GetFieldValue('LATPropinsi.kode_propinsi'))
      uipRegisterCIF.SetFieldValue('LATPropinsi.nama_propinsi',uipMaster.GetFieldValue('LATPropinsi.nama_propinsi'))
      uipRegisterCIF.SetFieldValue('LATKota.kode_kota',uipMaster.GetFieldValue('LATKota.kode_kota'))
      uipRegisterCIF.SetFieldValue('LATKota.nama_kota',uipMaster.GetFieldValue('LATKota.nama_kota'))
      uipRegisterCIF.SetFieldValue('LATKecamatan.kode_kecamatan',uipMaster.GetFieldValue('LATKecamatan.kode_kecamatan'))
      uipRegisterCIF.SetFieldValue('LATKecamatan.nama_kecamatan',uipMaster.GetFieldValue('LATKecamatan.nama_kecamatan'))
      
      uipRegisterCIF.SetFieldValue('LASPropinsi.kode_propinsi',uipMaster.GetFieldValue('LASPropinsi.kode_propinsi'))
      uipRegisterCIF.SetFieldValue('LASPropinsi.nama_propinsi',uipMaster.GetFieldValue('LASPropinsi.nama_propinsi'))
      uipRegisterCIF.SetFieldValue('LASKota.kode_kota',uipMaster.GetFieldValue('LASKota.kode_kota'))
      uipRegisterCIF.SetFieldValue('LASKota.nama_kota',uipMaster.GetFieldValue('LASKota.nama_kota'))
      uipRegisterCIF.SetFieldValue('LASKecamatan.kode_kecamatan',uipMaster.GetFieldValue('LASKecamatan.kode_kecamatan'))
      uipRegisterCIF.SetFieldValue('LASKecamatan.nama_kecamatan',uipMaster.GetFieldValue('LASKecamatan.nama_kecamatan'))

    else:
      #mode Edit
      form.GetControlByName('pData.no_referensi').ReadOnly = 1
      form.GetControlByName('pData.no_referensi').Color = -2147483624
      
def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterCIF = form.GetUIPartByName('uipRegisterCIF')

  if uipRegisterCIF.mode not in ['view','auth']:
    #mode New or Edit

    """alamat: jalan, rt/rw, kota, provinsi, kode pos, telp rumah (+kode area), handphone"""
    if uipRegisterCIF.alamat_jalan in ["", None]\
      or uipRegisterCIF.alamat_rtrw in ["", None]\
      or uipRegisterCIF.GetFieldValue('LATKota.kode_kota') in ["", None]\
      or uipRegisterCIF.GetFieldValue('LATPropinsi.kode_propinsi') in ["", None]\
      or uipRegisterCIF.alamat_kode_pos in ["", None]\
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
      or uipRegisterCIF.GetFieldValue('LASKota.kode_kota') in ["", None]\
      or uipRegisterCIF.GetFieldValue('LASPropinsi.kode_propinsi') in ["", None]\
      or uipRegisterCIF.alamat_surat_kode_pos in ["", None]\
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
    if uipRegisterCIF.no_referensi in ['',None]:
      form.ShowMessage('Nomor Referensi masih kosong! Mohon untuk diisi.')
      return
      
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
    dlg = app.ConfirmDialog('Anda yakin membatalkan Perubahan Alamat Peserta %s %s?' \
      % (uipRegisterCIF.GetFieldValue('LNasabahDPLK.no_peserta'),\
      uipRegisterCIF.GetFieldValue('LNasabahDPLK.nama_lengkap')))
    if dlg:
      # batalkan perubahan alamat nasabah
      app.ExecuteScript('transaction/registercif_del',app.CreateValues(['id',\
        uipRegisterCIF.registercif_id]))
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2
