class fHistoriNasabahRekening:
  def __init__(self, formObj, parentForm):
    if parentForm != None:
      self.parentForm = parentForm
    else:
      self.parentForm = None

  def Show(self):
    app = self.FormObject.ClientApplication
    no_peserta = self.uipNasabahDPLK.no_peserta
    
    self.SetQueryParameter('qAhliWaris','no_peserta',no_peserta)
    self.DisplayQueryData('qAhliWaris')

    self.SetQueryParameter('qUbahAlamat','no_peserta',no_peserta)
    self.DisplayQueryData('qUbahAlamat')

    self.SetQueryParameter('qUbahStatusKerja','no_peserta',no_peserta)
    self.DisplayQueryData('qUbahStatusKerja')

    self.SetQueryParameter('qPindahPaketInvestasi','no_peserta',no_peserta)
    self.DisplayQueryData('qPindahPaketInvestasi')

    self.SetQueryParameter('qIuran','no_peserta',no_peserta)
    self.DisplayQueryData('qIuran')
    
    self.SetQueryParameter('qAsuransi','no_peserta',no_peserta)
    self.DisplayQueryData('qAsuransi')
    
    self.FormContainer.Show()
    
  def SetQueryParameter(self, qryName, paramname, paramvalue):
    form = self.FormObject
    
    qryName = form.GetPanelByName(qryName)
    qryName.SetParameter(paramname, paramvalue)
  
  def DisplayQueryData(self, qryName):
    form = self.FormObject

    qryName = form.GetPanelByName(qryName)
    qryName.DisplayData()
    