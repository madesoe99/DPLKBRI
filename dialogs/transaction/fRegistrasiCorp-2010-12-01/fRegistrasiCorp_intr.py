def SetControlsForView(form):
  form.GetPanelByName('pDataLeft').SetAllControlsReadOnly()
  form.GetPanelByName('pDataRight').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnOK').Enabled = 0
  form.GetControlByName('pButton.btnOK').Default = 0
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Enabled = 0
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnClose').Caption = '&Tutup'
  form.GetControlByName('pButton.btnClose').Default = 1
  form.Caption = 'Lihat Detil Hasil ' + form.Caption

def SetControlsForAuth(form):
  form.GetPanelByName('pDataLeft').SetAllControlsReadOnly()
  form.GetPanelByName('pDataRight').SetAllControlsReadOnly()
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.Caption = 'Otorisasi Hasil ' + form.Caption

def FormShow(form, parameter):
  app = form.ClientApplication
  uipRegEditNasabahDPLKCorporate = form.GetUIPartByName('uipRegEditNasabahDPLKCorporate')

  uipRegEditNasabahDPLKCorporate.Edit()
  uipRegEditNasabahDPLKCorporate.mode = parameter.FirstRecord.mode

  if uipRegEditNasabahDPLKCorporate.mode == 'view':
    SetControlsForView(form)
  elif uipRegEditNasabahDPLKCorporate.mode == 'auth':
    SetControlsForAuth(form)

  if uipRegEditNasabahDPLKCorporate.mode == 'editdoc':
    uipNasabahDPLKCorporate = form.GetUIPartByName('uipNasabahDPLKCorporate')
    uipNasabahDPLKCorporate.CopyAttributes(uipRegEditNasabahDPLKCorporate,\
      'kode_nasabah_corporate;nama_perusahaan;alamat_kantor_jalan;alamat_kantor_kode_pos;alamat_kantor_kelurahan;'\
      'alamat_kantor_kecamatan;alamat_kantor_kota;alamat_kantor_telepon;alamat_kantor_telepon2;alamat_kantor_fax;no_perjanjian;no_perjanjian;tgl_bayar_iuran;biaya_daftar_anggota;'\
      'NPWP;keterangan;ljenisusaha.kode_jenis_usaha;ljenisusaha.nama_jenis_usaha;'\
      'lkepemilikan.kode_pemilikan;lkepemilikan.keterangan;lkepemilikan.kode_pemilikan'\
    )
    form.GetControlByName('pDataLeft.kode_nasabah_corporate').ReadOnly = 1
    form.GetControlByName('pDataLeft.kode_nasabah_corporate').Color = -2147483624
    form.Caption = 'Koreksi Data Peserta Perusahaan'
  elif uipRegEditNasabahDPLKCorporate.mode == 'edit':
    form.Caption = 'Koreksi ' + form.Caption

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegEditNasabahDPLKCorporate = form.GetUIPartByName('uipRegEditNasabahDPLKCorporate')
  uipP = form.GetUIPartByName('uipParameter')

  if uipRegEditNasabahDPLKCorporate.mode not in ['view','auth']:
    #mode New or Edit
    
    #checking tgl bayar iuran
    if uipRegEditNasabahDPLKCorporate.tgl_bayar_iuran in ['',None]:
      form.ShowMessage('Tanggal Bayar Iuran masih kosong. Mohon untuk diisi.')
      return

    #checking biaya daftar anggota
    if uipRegEditNasabahDPLKCorporate.biaya_daftar_anggota in ['',None] or \
      uipRegEditNasabahDPLKCorporate.biaya_daftar_anggota < 0.0:
      form.ShowMessage('Biaya Daftar Anggota tidak boleh kosong atau 0.')
      return

    form.CommitBuffer()
    if uipRegEditNasabahDPLKCorporate.mode <> 'edit':
      uipRegEditNasabahDPLKCorporate.Edit()
      uipRegEditNasabahDPLKCorporate.__SYSFLAG = 'N'

    form.PostResult()

  elif uipRegEditNasabahDPLKCorporate.mode == 'auth':
    #mode auth, go otorisasi
    app.ExecuteScript('transaction/authorize_regcorp',app.CreateValues(['id',\
      uipRegEditNasabahDPLKCorporate.regeditndplkcorp_id]))
  #else: mode view, do nothing

  sender.ExitAction = 1

def btnCancelClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegEditNasabahDPLKCorporate = form.GetUIPartByName('uipRegEditNasabahDPLKCorporate')

  if uipRegEditNasabahDPLKCorporate.mode == 'auth':
    dlg = app.ConfirmDialog('Anda yakin membatalkan %s perusahaan %s?' \
      % (sender.OwnerForm.Caption, uipRegEditNasabahDPLKCorporate.nama_perusahaan))
    if dlg:
      # batalkan register perusahaan baru
      app.ExecuteScript('transaction/delete_regcorp',app.CreateValues(['id',\
        uipRegEditNasabahDPLKCorporate.regeditndplkcorp_id]))
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2

