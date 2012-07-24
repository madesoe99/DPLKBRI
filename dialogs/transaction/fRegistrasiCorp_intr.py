def SetControlsForView(form):
  form.GetPanelByName('pDataLeft').SetAllControlsReadOnly()
  form.GetPanelByName('pDataRight').SetAllControlsReadOnly()
  form.GetPanelByName('pKorporatHolding').SetAllControlsReadOnly()
  form.GetPanelByName('pPerjanjian').SetAllControlsReadOnly()
  form.GetPanelByName('pRefr').SetAllControlsReadOnly()
  form.GetPanelByName('pRegister').SetAllControlsReadOnly()
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
  form.GetPanelByName('pKorporatHolding').SetAllControlsReadOnly()
  form.GetPanelByName('pPerjanjian').SetAllControlsReadOnly()
  form.GetPanelByName('pRefr').SetAllControlsReadOnly()
  form.GetPanelByName('pRegister').SetAllControlsReadOnly()
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
  elif uipRegEditNasabahDPLKCorporate.mode == 'editdoc':
    uipNasabahDPLKCorporate = form.GetUIPartByName('uipNasabahDPLKCorporate')
    
    dataCopy = ';'.join([
      'LNasabahDPLKHolding.kode_nasabah_corporate;LNasabahDPLKHolding.nama_perusahaan;kode_holding;',
      'kode_nasabah_corporate;nama_perusahaan;ljenisusaha.nama_jenis_usaha;NPWP;',
      'ljenisusaha.kode_jenis_usaha;ljenisusaha.risk_flag;',
      'lkepemilikan.kode_pemilikan;lkepemilikan.keterangan;tgl_bergabung;',
      'tgl_bayar_iuran;biaya_daftar_anggota;',
      'lnegara.kode_negara;lnegara.nama_negara;lnegara.risk_flag;',
      'alamat_kantor_jalan;alamat_kantor_kelurahan;alamat_kantor_kecamatan;',
      'alamat_kantor_kota;alamat_kantor_propinsi;alamat_kantor_kode_pos;',
      'alamat_kantor_telepon;alamat_kantor_telepon2;alamat_kantor_fax;',
      'no_perjanjian;keterangan1;keterangan2;keterangan3;keterangan4;',
      'REFR_ACCNO;REFR_NAMA;REFR_UKER;',
      'LAKPropinsi.kode_propinsi;LAKPropinsi.nama_propinsi;',
      'LAKKota.kode_kota;LAKKota.nama_kota;',
      'LAKKecamatan.kode_kecamatan;LAKKecamatan.nama_kecamatan'
    ])
    uipNasabahDPLKCorporate.CopyAttributes(uipRegEditNasabahDPLKCorporate,dataCopy)
    form.GetControlByName('pDataLeft.kode_nasabah_corporate').ReadOnly = 1
    form.GetControlByName('pDataLeft.kode_nasabah_corporate').Color = -2147483624
    form.Caption = 'Koreksi Data Peserta Perusahaan'
  elif uipRegEditNasabahDPLKCorporate.mode == 'edit':
    form.Caption = 'Koreksi ' + form.Caption
    if uipRegEditNasabahDPLKCorporate.operation_code == 'E':
      form.GetControlByName('pDataLeft.kode_nasabah_corporate').ReadOnly = 1
      form.GetControlByName('pDataLeft.kode_nasabah_corporate').Color = -2147483624

def btnOKClick(sender):  
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegEditNasabahDPLKCorporate = form.GetUIPartByName('uipRegEditNasabahDPLKCorporate')
  uipP = form.GetUIPartByName('uipParameter')

  if uipRegEditNasabahDPLKCorporate.mode not in ['view','auth']:
    #mode new, edit, editdoc
    form.CommitBuffer()
    
    if uipRegEditNasabahDPLKCorporate.no_referensi in ['',None]:
      form.ShowMessage('Nomor Referensi masih kosong. Mohon untuk diisi.')
      return
  
    if uipRegEditNasabahDPLKCorporate.kode_nasabah_corporate in ['',None]:
      form.ShowMessage('Kode Peserta Korporat masih kosong. Mohon untuk diisi.')
      return
  
    if uipRegEditNasabahDPLKCorporate.nama_perusahaan in ['',None]:
      form.ShowMessage('Nama Korporat masih kosong. Mohon untuk diisi.')
      return
  
    if uipRegEditNasabahDPLKCorporate.GetFieldValue("LJenisUsaha.kode_jenis_usaha") in ['',None]:
      form.ShowMessage('Jenis Usaha masih kosong. Mohon untuk diisi.')
      return
  
    if uipRegEditNasabahDPLKCorporate.GetFieldValue("LKepemilikan.kode_pemilikan") in ['',None]:
      form.ShowMessage('Kepemilikan masih kosong. Mohon untuk diisi.')
      return

    #checking tgl bayar iuran
    if uipRegEditNasabahDPLKCorporate.tgl_bayar_iuran in ['',None]:
      form.ShowMessage('Tanggal Bayar Iuran masih kosong. Mohon untuk diisi.')
      return

    #checking biaya daftar anggota
    if uipRegEditNasabahDPLKCorporate.biaya_daftar_anggota in ['',None] or \
      uipRegEditNasabahDPLKCorporate.biaya_daftar_anggota < 0.0:
      form.ShowMessage('Biaya Daftar Anggota tidak boleh kosong atau 0.')
      return

    if uipRegEditNasabahDPLKCorporate.GetFieldValue("LNegara.kode_negara") in ['',None]:
      form.ShowMessage('Negara masih kosong. Mohon untuk diisi.')
      return
    
    if uipRegEditNasabahDPLKCorporate.mode <> 'edit':
      uipRegEditNasabahDPLKCorporate.Edit()
      uipRegEditNasabahDPLKCorporate.SetFieldValue('__SYSFLAG', 'N')

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
