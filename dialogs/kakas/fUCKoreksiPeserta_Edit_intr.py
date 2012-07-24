class fUCKoreksiPeserta_Edit:
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

  def validateForm(self):
    form = self.FormObject
    app = form.ClientApplication
    uipDetail = form.GetUIPartByName('uipDetail')
    
    """nomor referensi"""
    if uipDetail.no_referensi in ["", None]:
      app.ShowMessage('Nomor Referensi masih kosong')
      return False
    
    """alamat: jalan, rt/rw, kota, provinsi, kode pos, telp rumah (+kode area), handphone"""
    if uipDetail.alamat_jalan in ["", None]\
      or uipDetail.alamat_rtrw in ["", None]\
      or uipDetail.GetFieldValue('LATKota.kode_kota') in ["", None]\
      or uipDetail.GetFieldValue('LATPropinsi.kode_propinsi') in ["", None]\
      or uipDetail.alamat_kode_pos in ["", None]\
      or uipDetail.alamat_telepon in ["", None]\
      or uipDetail.alamat_telepon2 in ["", None]:
      app.ShowMessage("""Alamat Tempat Tinggal yang harus diisi:\n
        - Jalan
        - RT / RW
        - Kota
        - Propinsi
        - Kode Pos
        - Telp. Rumah
        - Handphone""")
      return False
    
    return True
    
  def btnSaveOnClick(self, sender):
    # procedure(sender: TrtfButton)
    form = sender.OwnerForm
    app = form.ClientApplication
    uipDetail = form.GetUIPartByName('uipDetail')
    
    isValid = self.validateForm()
    if not isValid:
      return
    
    uipDetail.Edit()
    uipDetail.is_valid = 'T'
    uipDetail.keterangan = None
          
    form.CommitBuffer()
    form.PostResult()
  
    sender.ExitAction = 1