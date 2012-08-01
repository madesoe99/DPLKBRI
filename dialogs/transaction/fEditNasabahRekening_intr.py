gReady=0

def SetControlsForView(form):
  form.GetPanelByName('pDataLeft').SetAllControlsReadOnly()
  form.GetPanelByName('pDataRight').SetAllControlsReadOnly()
  form.GetPanelByName('pDataIndukRegister').SetAllControlsReadOnly()
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
  form.GetPanelByName('pDataLeft').SetAllControlsReadOnly()
  form.GetPanelByName('pDataRight').SetAllControlsReadOnly()
  form.GetPanelByName('pDataIndukRegister').SetAllControlsReadOnly()
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
    uipRegisterCIF.SetFieldValue('LNasabahDPLK.ibu_kandung',uipMaster.ibu_kandung)

    uipMaster.CopyAttributes(uipRegisterCIF,\
      'nama_lengkap;tempat_lahir;tanggal_lahir;jenis_kelamin;'\
      'golongan_darah;agama;pendidikan_terakhir;status_perkawinan;'\
      'ldaerahasal.kode_propinsi;ldaerahasal.nama_propinsi;'\
      'kewarganegaraan;jenis_kartu_identitas;no_identitas_diri;tgl_exp_identitas;'\
      'lkelompok.kode_kelompok;lkelompok.nama_kelompok;'\
      'alamat_email;NPWP;nama_perusahaan;LKepemilikan.kode_pemilikan;LKepemilikan.keterangan'\
    )

  elif uipRegisterCIF.mode == 'edit':
    form.GetControlByName('pDataIndukRegister.no_referensi').ReadOnly = 1
    form.GetControlByName('pDataIndukRegister.no_referensi').Color = -2147483624
  elif uipRegisterCIF.mode == 'view':
    SetControlsForView(form)
  elif uipRegisterCIF.mode == 'auth':
    SetControlsForAuth(form)
    
  global gReady
  gReady=1

def validateForm(form):
  app = form.ClientApplication
  uipRegisterCIF = form.GetUIPartByName('uipRegisterCIF')
  
  """nama lengkap peserta"""
  if uipRegisterCIF.nama_lengkap in ["", None]:
    app.ShowMessage('Nama Lengkap masih kosong')
    return False
  
  """tempat lahir"""
  if uipRegisterCIF.tempat_lahir in ["", None]:
    app.ShowMessage('Tempat Lahir masih kosong')
    return False
  
  """tanggal lahir"""
  if uipRegisterCIF.tanggal_lahir in [[], None]:
    app.ShowMessage('Tanggal Lahir masih kosong, proses tidak dapat dilanjutkan...')
    return False
  
  """jenis kelamin"""
  if uipRegisterCIF.jenis_kelamin in ["", None]:
    app.ShowMessage('Jenis Kelamin masih kosong')
    return False
  
  """cek usia peserta"""
  floatTglNow = app.ModDateTime.Now()
  y,m,d = uipRegisterCIF.tanggal_lahir[:3]
  usiaPeserta = (floatTglNow - app.ModDateTime.EncodeDate(y,m,d))/365
  if usiaPeserta < 18:
    app.ShowMessage('Usia peserta belum 18 Tahun!')
    return False

  if uipRegisterCIF.tanggal_lahir[:3] > \
    app.ModDateTime.DecodeDate(floatTglNow)[:3]:
    app.ShowMessage('Tanggal lahir peserta tidak boleh melebihi tanggal hari ini!')
    return False
  
  """nomor referensi"""
  #if uipRegisterCIF.no_referensi in ["", None]:
  #  app.ShowMessage('Nomor Referensi masih kosong')
  #  return False

  return True

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipRegisterCIF = form.GetUIPartByName('uipRegisterCIF')

  isValid = validatePesertaTerdaftar(form,'save')
  if not isValid:
    sender.ExitAction = 1
    return

  isValid = validateForm(form)
  if not isValid:
    return
    
  if uipRegisterCIF.mode not in ['view','auth']:
    #mode New or Edit
    if uipRegisterCIF.mode in ['editdoc','new']:
      uipRegisterCIF.Edit()
      # set sysflag supaya mode pemrosesannya adalah membuat regeditnasabahrekening baru
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

def validatePesertaTerdaftar(form, mode='validate'):
    app = form.ClientApplication
    uipRegisterCIF = form.GetUIPartByName('uipRegisterCIF')
    uipMaster = form.GetUIPartByName('uipMaster')
    
    """cek peserta"""
    ph = app.CreateValues(
      ['ibu_kandung', uipRegisterCIF.GetFieldValue('LNasabahDPLK.ibu_kandung')],
      ['nama_lengkap', uipRegisterCIF.nama_lengkap],
      ['tanggal_lahir', uipRegisterCIF.tanggal_lahir]
    )
    
    resp = form.CallServerMethod('cekPeserta', ph)
    status = resp.FirstRecord
    if not status.success:
      if mode == 'validate':
        app.ShowMessage(status.message)
      return True
    else:
      if uipRegisterCIF.GetFieldValue('LNasabahDPLK.no_peserta') == status.no_peserta:
        if mode == 'validate':
          app.ShowMessage('Data valid...')
        
        return True
        
      if status.is_otor:
        #dlg = app.ConfirmDialog("""
        #  Calon peserta telah terdaftar di Kepesertaan DPLK.
        #  CIF Peserta: '%s', dengan status 'Sudah Approve' \n
        #  Apakah Anda ingin membuka Account DPLK baru atas nama peserta ini ?
        #  """ % status.no_peserta)
        dlg = False
        app.ShowMessage("""
          Calon peserta telah terdaftar di Kepesertaan DPLK.
          CIF Peserta: '%s', dengan status 'Sudah Approve'\n
          Daftar peserta tersebut dapat diakses melalui menu:
          Nasabah -> Daftar Peserta
        """ % status.no_peserta)
      else:
        #dlg = app.ConfirmDialog("""
        #  Calon peserta telah terdaftar di Kepesertaan DPLK.
        #  CIF Peserta: '%s', dengan status 'Belum Approve' \n
        #  Apakah Anda ingin membuka data registrasi DPLK atas nama peserta ini ?
        #  """ % status.no_peserta)
        #app.ShowMessage('Nomor ID registrasi: ' + str(status.registernr_id))
        dlg = False
        app.ShowMessage("""
          Calon peserta telah terdaftar di Kepesertaan DPLK.
          CIF Peserta: '%s', dengan status 'Belum Approve'\n
          Daftar peserta tersebut dapat diakses melalui menu:
          Nasabah -> Daftar Register Peserta Baru
        """ % status.no_peserta)
      
      if dlg:
        if status.is_otor:
          formID = 'fRegistrasi_New'
          mode = 'new_pesertaexisting'
          ph = app.CreateValues(['mode', 'exist_nasabah'], ['no_peserta', status.no_peserta])
        else:
          formID = 'fRegistrasi'
          mode = 'edit'
          pobjconst = "PObj:REGISTERNASABAHREKENING#REGISTERNR_ID=%s" % str(status.registernr_id)
          ph = app.CreateValues(['key', pobjconst])
        
        frm = app.CreateForm('transaction/'+formID, formID, 0, ph, None)
        frm.Show(app.CreateValues(['mode',mode]))  
      
      return False
    
def btnCekPesertaTerdaftarOnClick(sender):
  global gReady
  if gReady == 1:
    form = sender.Ownerform
    app = form.ClientApplication
    uipRegisterCIF = form.GetUIPartByName('uipRegisterCIF')
    uipMaster = form.GetUIPartByName('uipMaster')
    
    """cek data ibu kandung, nama lengkap, dan tanggal lahir"""
    if uipRegisterCIF.GetFieldValue('LNasabahDPLK.ibu_kandung') in ["", None]\
      or uipRegisterCIF.nama_lengkap in ["", None]\
      or uipRegisterCIF.tanggal_lahir in [[], None]:
      app.ShowMessage("""Untuk melanjutkan proses, data berikut harus tersedia:\n
      - Nama Ibu Kandung
      - Nama Lengkap Peserta
      - Tanggal Lahir Peserta""")
      return False
      
    isValid = validatePesertaTerdaftar(form)
    if not isValid:
      sender.ExitAction = 1
      return
        