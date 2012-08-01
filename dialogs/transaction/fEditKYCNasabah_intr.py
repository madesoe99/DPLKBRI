def SetControlsForView(form):
  form.GetPanelByName('pDataAbove').SetAllControlsReadOnly()
  form.GetPanelByName('pDataLeft').SetAllControlsReadOnly()
  form.GetPanelByName('pDataRight').SetAllControlsReadOnly()
  form.GetPanelByName('pKelengkapan').SetAllControlsReadOnly()
  
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
  form.Caption = 'Lihat Detil ' + form.Caption

def SetControlsForAuth(form):
  form.GetPanelByName('pDataAbove').SetAllControlsReadOnly()
  form.GetPanelByName('pDataLeft').SetAllControlsReadOnly()
  form.GetPanelByName('pDataRight').SetAllControlsReadOnly()
  form.GetPanelByName('pKelengkapan').SetAllControlsReadOnly()
  
  form.GetControlByName('pButton.btnOK').Caption = '&Setujui'
  form.GetControlByName('pButton.btnCancel').Caption = '&Tolak'
  form.GetControlByName('pButton.btnCancel').Cancel = 0
  form.GetControlByName('pButton.btnClose').Visible = 1
  form.GetControlByName('pButton.btnClose').Cancel = 1
  form.Caption = 'Otorisasi ' + form.Caption

def FormShow(form, parameter):
  uipMaster = form.GetUIPartByName('uipMaster')
  uipRegisterCIF = form.GetUIPartByName('uipRegisterCIF')

  uipRegisterCIF.Edit()
  uipRegisterCIF.mode = parameter.FirstRecord.mode

  if uipRegisterCIF.mode in ['editdoc','new']:
    #mode New
    uipRegisterCIF.SetFieldValue('LNasabahDPLK.no_peserta',uipMaster.no_peserta)
    uipRegisterCIF.SetFieldValue('LNasabahDPLK.nama_lengkap',uipMaster.nama_lengkap)
    #if uipMaster.kode_nasabah_corporate <> None:
    #  uipRegisterCIF.SetFieldValue('LNasabahDPLK.kode_nasabah_corporate',\
    #  uipMaster.kode_nasabah_corporate)

    uipMaster.CopyAttributes(uipRegisterCIF,
      'LJenisUsaha.kode_jenis_usaha;LJenisUsaha.nama_jenis_usaha;LJenisUsaha.risk_flag;'\
      'ibu_kandung;penghasilan_tetap;penghasilan_tambahan;'\
      'status_risk_request;risk_flag_request;status_pep;keterangan_pep;'\
      'beneficial_owner;limit_credit;limit_debit;limit_frek_credit;'\
      'limit_frek_debit;LNegara.kode_negara;LNegara.nama_negara;LNegara.risk_flag;'\
      'LJenisPekerjaan.kode_jenis_pekerjaan;LJenisPekerjaan.nama_jenis_pekerjaan;LJenisPekerjaan.risk_flag;'\
      'LJenisPekerjaanDetail.jpd_id;LJenisPekerjaanDetail.kode_jenis_jabatan;LJenisPekerjaanDetail.LJenisJabatan.nama_jenis_jabatan;LJenisPekerjaanDetail.risk_flag;'\
      'LJenisUsahaOrtu.kode_jenis_usaha;LJenisUsahaOrtu.nama_jenis_usaha;LJenisUsahaOrtu.risk_flag;'\
      'LJenisPekerjaanOrtu.kode_jenis_pekerjaan;LJenisPekerjaanOrtu.nama_jenis_pekerjaan;LJenisPekerjaanOrtu.risk_flag;'\
      'LJenisPekerjaanDetailOrtu.jpd_id;LJenisPekerjaanDetailOrtu.kode_jenis_jabatan;LJenisPekerjaanDetailOrtu.LJenisJabatan.nama_jenis_jabatan;LJenisPekerjaanDetailOrtu.risk_flag;'\
      'nama_orang_tua;nama_perusahaan_ortu;penghasilan_orang_tua;hubungan_kelengkapan'\
    )
    #uipRegisterCIF.keterangan_nasabahdplk = uipMaster.keterangan
    #uipRegisterCIF.nama_lengkap = uipMaster.nama_lengkap
  elif uipRegisterCIF.mode == 'edit':
    form.GetControlByName('pDataAbove.no_referensi').ReadOnly = 1
    form.GetControlByName('pDataAbove.no_referensi').Color = -2147483624
  elif uipRegisterCIF.mode == 'view':
    SetControlsForView(form)
  elif uipRegisterCIF.mode == 'auth':
    SetControlsForAuth(form)

  #if uipRegisterCIF.GetFieldValue('LNasabahDPLK.kode_nasabah_corporate') <> None:
  #  form.GetControlByName('pDataLeft.nama_perusahaan').ReadOnly = 1
  #  form.GetControlByName('pDataLeft.nama_perusahaan').Color = -2147483624
  #  form.GetControlByName('pDataLeft.LJenisUsaha').Enabled = 0
  #  form.GetControlByName('pDataLeft.LKepemilikan').Enabled = 0

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterCIF = form.GetUIPartByName('uipRegisterCIF')

  if uipRegisterCIF.mode not in ['view','auth']:
    #mode New or Edit
    
    """cek nomor referensi"""
    #if uipRegisterCIF.no_referensi in ['',None]:
    #  form.ShowMessage('Nomor Referensi masih kosong. Mohon untuk diisi.')
    #  return

    """cek nama ibu kandung"""
    if uipRegisterCIF.ibu_kandung in ['',None]:
      form.ShowMessage('Nama Ibu Kandung masih kosong. Mohon untuk diisi.')
      return

    if uipRegisterCIF.mode in ['editdoc','new']:
      uipRegisterCIF.Edit()
      # set sysflag supaya mode pemrosesannya adalah membuat RegEditKYCNasabah baru
      uipRegisterCIF.SetFieldValue('__SYSFLAG', 'N')

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
    dlg = app.ConfirmDialog('Anda yakin membatalkan Koreksi Data Umum peserta %s %s?' \
      % (uipRegisterCIF.GetFieldValue('LNasabahDPLK.no_peserta'),\
      uipRegisterCIF.GetFieldValue('LNasabahDPLK.nama_lengkap')))
    if dlg:
      # batalkan koreksi data umum nasabah
      app.ExecuteScript('transaction/registercif_del',app.CreateValues(['id',\
        uipRegisterCIF.registercif_id]))
      sender.ExitAction = 3
  else:
    sender.ExitAction = 2

