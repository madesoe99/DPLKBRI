class fMasterKartuDPLK:
  def __init__(self, formObj, parentForm):
    self.mode = None
  #--
  
  def Show(self, mode):
    form = self.FormObject
    self.mode = mode
    
    if self.mode == 'edit':
      self.pMain.GetControlByName('LNasabahDPLK').Enabled = 0
      self.pMain.GetControlByName('LRekeningDPLK').Enabled = 0
    
    self.FormContainer.Show()

  def btnSaveOnClick(self, sender):
    # procedure(sender: TrtfButton)
    form = sender.OwnerForm
    app = form.ClientApplication
    uipMasterKartuDPLK = form.GetUIPartByName('uipMasterKartuDPLK')
    
    if uipMasterKartuDPLK.GetFieldValue('LNasabahDPLK.no_peserta') == None:
      app.ShowMessage('Nasabah masih kosong...')
      return
    
    if uipMasterKartuDPLK.GetFieldValue('LRekeningDPLK.no_rekening') == None:
      app.ShowMessage('Rekening DPLK masih kosong...')
      return
    
    if self.mode == 'new':
      uipMasterKartuDPLK.Edit()
      uipMasterKartuDPLK.no_rekening = uipMasterKartuDPLK.GetFieldValue('LRekeningDPLK.no_rekening')
          
    form.CommitBuffer()
    form.PostResult()
  
    sender.ExitAction = 1