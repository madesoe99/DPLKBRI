class fUCAhliWaris_Edit:
  def __init__(self, formObj, parentForm):
    pass
  #--

  def Show(self, mode):
    form = self.FormObject
    
    if mode == 'view':
      self.pInput.SetAllControlsReadOnly(1)
      self.pButton.GetControlByName('btnSave').Enabled = 0
    elif mode == 'edit' and self.uipDetail.is_auth == 'T':
      form.ShowMessage('Data ini sudah diotorisasi...')
      form.Close(1)
      return
    
    self.FormContainer.Show()

  def validateForm(self):
    form = self.FormObject
    app = form.ClientApplication
    uipDetail = form.GetUIPartByName('uipDetail')
    
    """Nomor Peserta"""
    if uipDetail.GetFieldValue('LNasabahDPLK.no_peserta') in ["", None]:
        app.ShowMessage('Nomor peserta masih kosong')
        return False

    """Nama Lengkap"""
    if uipDetail.GetFieldValue('LNasabahDPLK.nama_lengkap') in ["", None]:
      app.ShowMessage('Nama lengkap masih kosong')
      return False
    
    if uipDetail.nama_ahli_waris in ['', None]:
      app.ShowMessage('Nama Ahli Waris masih kosong')
      return False
    
    if uipDetail.hubungan_keluarga in ['', None]:
      app.ShowMessage('Hubungan Keluarga masih kosong')
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