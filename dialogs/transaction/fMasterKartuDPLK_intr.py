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
    elif self.mode == 'new':
      self.uipMasterKartuDPLK.Edit()
      self.uipMasterKartuDPLK.no_seri_kartu = '%s-xxxxxx-xxxxxxx' % self.uipMasterKartuDPLK.tmp_year
    
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
        
    #if self.mode == 'new':
    #  uipMasterKartuDPLK.Edit()
    #  uipMasterKartuDPLK.no_seri_kartu = None
          
    uipMasterKartuDPLK.Edit()
    uipMasterKartuDPLK.SetFieldValue('__SYSFLAG', 'N')
    
    #try:
    form.CommitBuffer()
    form.PostResult()  
    #except:
    #  raise Exception, 'gagal'
  
    sender.ExitAction = 1

  def LNasabahDPLKOnAfterLookup(self, sender, linkui):
    # procedure(sender: TrtfDBLookupEdit; linkui: TrtfLinkUIElmtSetting)
    form = self.FormObject
    app = form.ClientApplication
    uipMasterKartuDPLK = form.GetUIPartByName('uipMasterKartuDPLK')
    uipMasterKartuDPLK.no_seri_kartu = self.setNomorKartu()

  def setNomorKartu(self):
    form = self.FormObject
    app = form.ClientApplication
    uipMasterKartuDPLK = form.GetUIPartByName('uipMasterKartuDPLK')

    no_peserta = uipMasterKartuDPLK.GetFieldValue('LNasabahDPLK.no_peserta') or '000000'
    no_peserta = int(no_peserta)
    if no_peserta <= 999999:
      no_peserta = '%06d' % no_peserta
    
    no_rekening = uipMasterKartuDPLK.GetFieldValue('LRekeningDPLK.no_rekening') or '0000000'
    no_rekening = int(no_rekening)
    if no_rekening <= 9999999:
      no_rekening = '%07d' % no_rekening

    year, noPst, noRek = str(uipMasterKartuDPLK.no_seri_kartu).split('-')
    noPst = str(no_peserta)
    noRek = str(no_rekening)
    
    no_seri_kartu = "%s-%s-%s" % (year, noPst, noRek)
    return no_seri_kartu
    