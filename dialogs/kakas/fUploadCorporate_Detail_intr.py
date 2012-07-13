class fUploadCorporate_Detail:
  def __init__(self, formObj, parentForm):
    self.fMode = None
  #--
  
  def Show(self, fSpecific):
    self.fMode = fSpecific.FirstRecord.fMode
    fType = fSpecific.FirstRecord.fType
    
    spec = fType.split(',')
    self.uipUploadCorporate.Edit()
    self.uipUploadCorporate.SetFieldValue('classtypename', spec[1])
    
    self.OpenFrameForm(spec[0])
    self.FormContainer.Show()
  #--
  
  def OpenFrameForm(self, fSpec):
    form = self.FormObject;
    app = form.ClientApplication;
    uipUploadCorporate = form.GetUIPartByName('uipUploadCorporate')
    
    ph = app.CreateValues(
      ['trx_session_id', str(uipUploadCorporate.trx_session_id)]
    )
    
    formSpecific = self.frameSpecific.Activate(fSpec,ph,None)
    
    if self.fMode == 'new':
      form.Caption = 'Input Data Baru ' + form.Caption
    elif self.fMode == 'edit':
      form.Caption = 'Koreksi Data ' + form.Caption
    elif self.fMode == 'auth':
      form.Caption = 'Otorisasi Data ' + form.Caption
      
      self.pGeneral.SetAllControlsReadOnly(1)
      #formSpecific.qDetails.ContextMenuName = ''
      formSpecific.qDetails.SetParameter('trx_session_id', uipUploadCorporate.trx_session_id)
      formSpecific.qDetails.DisplayData()
      
      self.pButton.GetControlByName('btnAuth').Enabled = 1
      self.pButton.GetControlByName('bSave').Enabled = 0 
    elif self.fMode == 'view':
      form.Caption = 'Lihat Detil Data ' + form.Caption
      
      self.pGeneral.SetAllControlsReadOnly(1)
      #formSpecific.qDetails.ContextMenuName = 'popupmenus/kakas/pUploadCorporate_Detail'
      formSpecific.qDetails.SetParameter('trx_session_id', uipUploadCorporate.trx_session_id)
      formSpecific.qDetails.DisplayData()
      
      self.pButton.GetControlByName('btnAuth').Enabled = 0
      self.pButton.GetControlByName('bSave').Enabled = 0 
  #--

  def bSaveOnClick(self, sender):
    # procedure(sender: TrtfButton)
    form = self.FormObject
    app = form.ClientApplication
    
    # ambil dari frame
    formSpecific = self.frameSpecific.ContainedFormObject
    #uipColSpecific = formSpecific.uipColSpecific
    formSpecific.CommitBuffer()
    phFS = formSpecific.GetDataPacket()
            
    form.CommitBuffer()
    ph = form.GetDataPacket()
    
    ph.Packet.AcquireAnotherPacket(phFS.Packet)
    resp = form.CallServerMethod('saveData', ph)    
    status = resp.FirstRecord
    
    if status.success:
      app.ShowMessage(status.message)
      sender.ExitAction = 1
    else:
      app.ShowMessage(status.message)
  #--

  def btnAuthOnClick(self, sender):
    # procedure(sender: TrtfButton)
    form = sender.OwnerForm
    app = form.ClientApplication
    
    if self.uipUploadCorporate.upload_type in ['P','W']:
      ph = app.CreateValues(['id', self.uipUploadCorporate.trx_session_id])
      app.ExecuteScript('transaction/authorize_regnsbrek_masal', ph)
    elif self.uipUploadCorporate.upload_type == 'I':
      ph = app.CreateValues(['id', self.uipUploadCorporate.trx_session_id])
      resp = form.CallServerMethod('createTrxIuran', ph)
      status = resp.FirstRecord
      
      if status.success:
        app.ShowMessage(status.message)
      else:
        app.ShowMessage(status.message)
        return
    elif self.uipUploadCorporate.upload_type == 'R':
      ph = app.CreateValues(['id', self.uipUploadCorporate.trx_session_id])
      resp = form.CallServerMethod('createTrxBiayaDaftar', ph)
      status = resp.FirstRecord
      
      if status.success:
        app.ShowMessage(status.message)
      else:
        app.ShowMessage(status.message)
        return
    else:
      app.ShowMessage('Jenis Upload tidak terdaftar...')
      
    sender.ExitAction = 1
    