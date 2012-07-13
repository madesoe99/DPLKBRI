class fUCRegisterPeserta_Edit:
  def __init__(self, formObj, parentForm):
    pass
  #--

  def Show(self, mode):
    form = self.FormObject
    
    if mode == 'view':
      self.pInput.SetAllControlsReadOnly(1)
      self.pButton.GetControlByName('btnSave').Enabled = 0
    elif mode == 'edit' and self.uipDetail.is_auth == 'T':
      form.ShowMessage('''
      Data ini sudah diotorisasi...
      Koreksi selanjutnya dapat dilakukan melalui menu: Nasabah > Daftar Peserta''')
      form.Close(1)
      return
    
    self.FormContainer.Show()

  def validatePesertaTerdaftar(self):
    form = self.FormObject
    app = form.ClientApplication
    uipRegisterNasabahRekening = form.GetUIPartByName('uipDetail')
    uipRegisterNasabahRekening.Edit()
    
    """cek peserta"""
    ph = app.CreateValues(
      ['ibu_kandung', uipRegisterNasabahRekening.ibu_kandung],
      ['nama_lengkap', uipRegisterNasabahRekening.nama_lengkap],
      ['tanggal_lahir', uipRegisterNasabahRekening.tanggal_lahir]
    )
    resp = form.CallServerMethod('cekPeserta', ph)
    status = resp.FirstRecord
    if not status.success:
      #app.ShowMessage(status.message)
      return True
    else:
      if status.is_otor:
        uipRegisterNasabahRekening.no_rekening = ''
        uipRegisterNasabahRekening.is_valid = 'F'
        uipRegisterNasabahRekening.keterangan = 'Terdaftar #%s, Otor: T' % (status.no_peserta)
        uipRegisterNasabahRekening.no_peserta = status.no_peserta
        app.ShowMessage("""
          Calon peserta telah terdaftar di Kepesertaan DPLK.
          Nomor Peserta: '%s', dengan status 'Sudah Otorisasi'
          """ % status.no_peserta)
        '''
        dlg = app.ConfirmDialog("""
          Calon peserta telah terdaftar di Kepesertaan DPLK.
          Nomor Peserta: '%s', dengan status 'Sudah Otorisasi' \n
          Apakah Anda ingin membuka rekening baru atas nama peserta ini ?
          """ % status.no_peserta)
        '''
      else:
        uipRegisterNasabahRekening.no_rekening = ''
        uipRegisterNasabahRekening.is_valid = 'F'
        uipRegisterNasabahRekening.keterangan = 'Terdaftar #%s, Otor: F' % (status.no_peserta)
        uipRegisterNasabahRekening.no_peserta = status.no_peserta
        app.ShowMessage("""
          Calon peserta telah terdaftar di Kepesertaan DPLK.
          Nomor Peserta: '%s', dengan status 'Belum Otorisasi'
          """ % status.no_peserta)
        '''
        dlg = app.ConfirmDialog("""
          Calon peserta telah terdaftar di Kepesertaan DPLK.
          Nomor Peserta: '%s', dengan status 'Belum Otorisasi' \n
          Apakah Anda ingin membuka data registrasi DPLK atas nama peserta ini ?
          """ % status.no_peserta)
        '''
        #app.ShowMessage('Nomor ID registrasi: ' + str(status.registernr_id))
      
      return False
      
  def validateForm(self):
    form = self.FormObject
    app = form.ClientApplication
    uipRegisterNasabahRekening = form.GetUIPartByName('uipDetail')
    
    """nama ibu kandung"""
    if uipRegisterNasabahRekening.ibu_kandung in ["", None]:
      app.ShowMessage('Ibu Kandung masih kosong')
      return False
    
    """nama lengkap peserta"""
    if uipRegisterNasabahRekening.nama_lengkap in ["", None]:
      app.ShowMessage('Nama Lengkap masih kosong')
      return False
    
    """tempat lahir"""
    if uipRegisterNasabahRekening.tempat_lahir in ["", None]:
      app.ShowMessage('Tempat Lahir masih kosong')
      return False
    
    """tanggal lahir"""
    if uipRegisterNasabahRekening.tanggal_lahir in [[], None]:
      app.ShowMessage('Tanggal Lahir masih kosong, proses tidak dapat dilanjutkan...')
      return False

    """jenis kelamin"""
    if uipRegisterNasabahRekening.jenis_kelamin in ["", None]:
      app.ShowMessage('Jenis Kelamin masih kosong')
      return False
    
    """nomor referensi"""
    if uipRegisterNasabahRekening.no_referensi in ["", None]:
      app.ShowMessage('Nomor Referensi masih kosong')
      return False
    
    """alamat: jalan, rt/rw, kota, provinsi, kode pos, telp rumah (+kode area), handphone"""
    if uipRegisterNasabahRekening.alamat_jalan in ["", None]\
      or uipRegisterNasabahRekening.alamat_rtrw in ["", None]\
      or uipRegisterNasabahRekening.GetFieldValue('LATKota.kode_kota') in ["", None]\
      or uipRegisterNasabahRekening.GetFieldValue('LATPropinsi.kode_propinsi') in ["", None]:
      app.ShowMessage("""Alamat Tempat Tinggal yang harus diisi:\n
        - Jalan
        - RT / RW
        - Kota
        - Propinsi""")
      return False

    """cek tanggal: tanggal lahir, tanggal pensiun (usia pensiun terkait tanggal lahir)"""
    floatTglNow = app.ModDateTime.Now()
    y,m,d = uipRegisterNasabahRekening.tanggal_lahir[:3]
    
    """cek usia peserta"""
    usiaPeserta = (floatTglNow - app.ModDateTime.EncodeDate(y,m,d))/365
    if usiaPeserta < 18:
      form.ShowMessage('Usia peserta belum 18 Tahun!')
      return False

    if uipRegisterNasabahRekening.tanggal_lahir[:3] > \
      app.ModDateTime.DecodeDate(floatTglNow)[:3]:
      form.ShowMessage('Tanggal lahir peserta tidak boleh melebihi tanggal hari ini!')
      return False
    
    return True
    
  def btnSaveOnClick(self, sender):
    # procedure(sender: TrtfButton)
    form = sender.OwnerForm
    app = form.ClientApplication
    uipRegisterNasabahRekening = form.GetUIPartByName('uipDetail')
    
    isValid = self.validatePesertaTerdaftar()
    if not isValid:
      sender.ExitAction = 1
      return
    
    isValid = self.validateForm()
    if not isValid:
      return
    
    uipRegisterNasabahRekening.Edit()
    uipRegisterNasabahRekening.is_valid = 'T'
    uipRegisterNasabahRekening.keterangan = None
          
    form.CommitBuffer()
    form.PostResult()
  
    sender.ExitAction = 1