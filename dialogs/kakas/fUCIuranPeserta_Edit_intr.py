class fUCIuranPeserta_Edit:
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
    
    """Nominal iuran"""
    if uipDetail.iuran_pst == None:
      uipDetail.iuran_pst = 0.0
    
    if uipDetail.iuran_pk == None:
      uipDetail.iuran_pk = 0.0

    if (uipDetail.iuran_pst + uipDetail.iuran_pk) <= 0.0:
      app.ShowMessage('Nominal iuran <= 0.0')
      return False
    
    """Nomor Rekening"""
    if uipDetail.GetFieldValue('LRekInvDPLK.no_rekening') in ["", None]:
      app.ShowMessage('Nomor rekening masih kosong')
      return False
    
    """Nomor Peserta"""
    if uipDetail.GetFieldValue('LRekInvDPLK.no_peserta') in ["", None]:
      app.ShowMessage('Nomor peserta masih kosong')
      return False

    """Nama Lengkap"""
    if uipDetail.GetFieldValue('LRekInvDPLK.LNasabahDPLK.nama_lengkap') in ["", None]:
      app.ShowMessage('Nama lengkap masih kosong')
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