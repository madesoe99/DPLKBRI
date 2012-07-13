class fCorporateParams:
  def __init__(self, formObj, parentForm):
    self.gReady = 0
    if parentForm != None:
      self.parentForm = parentForm
    else:
      self.parentForm = None
  #--

  def Show(self):
    self.FormShow()
    self.FormContainer.Show()

  def FormShow(self):
    form = self.FormObject
    app = form.ClientApplication
    self.gReady = 1

  def LMasterParameter_Key_ParameterOnAfterLookup(self, sender, linkui):
    # procedure(sender: TrtfGridColumn; linkui: TrtfLinkUIElmtSetting)
    if self.gReady != 0:
      form = sender.OwnerForm
      uipCP = form.GetUIPartByName('uipCorpParams')

      uipCP.SetFieldValue("NUMERIC_VALUE", uipCP.GetFieldValue("LMasterParameter.NUMERIC_VALUE"))
      uipCP.SetFieldValue("VARCHAR_VALUE", uipCP.GetFieldValue("LMasterParameter.VARCHAR_VALUE"))
      uipCP.SetFieldValue("DESCRIPTION", uipCP.GetFieldValue("LMasterParameter.DESCRIPTION"))

  def btnSubmitOnClick(self, sender):
    # procedure(sender: TrtfButton)
    form = sender.OwnerForm
    app = form.ClientApplication
  
    form.CommitBuffer()
    form.PostResult()

    sender.ExitAction = 1
    
    