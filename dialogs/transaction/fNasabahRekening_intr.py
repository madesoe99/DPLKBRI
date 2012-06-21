class fNasabahRekening:
  def __init__(self, formObj, parentForm):
    if parentForm != None:
      self.parentForm = parentForm
    else:
      self.parentForm = None

  def Show(self, mode):
    form = self.FormObject
    app = form.ClientApplication
    
    uipNasabahDPLK = form.GetUIPartByName('uipNasabahDPLK')
    uipNasabahDPLK.Edit()
    
    if uipNasabahDPLK.GetFieldValue('LNasabahDPLKCorporate.kode_nasabah_corporate') \
      not in [None,'']:
      #termasuk anggota peserta korporat
      uipNasabahDPLK.nasabah_korporat = 1
    else:
      #tidak termasuk peserta korporat
      uipNasabahDPLK.nasabah_korporat = 0

    self.bindRekInvDPLK()
    self.bindRekeningDPLK()
    self.FormContainer.Show()
    
  def bindRekInvDPLK(self):
    form = self.FormObject
    uipNasabahDPLK = form.GetUIPartByName('uipNasabahDPLK')
    
    qRekInvDPLK = form.GetPanelByName('qRekInvDPLK')
    qRekInvDPLK.SetParameter('no_peserta', uipNasabahDPLK.no_peserta)
    qRekInvDPLK.DisplayData()

  def bindRekeningDPLK(self):
    form = self.FormObject
    uipNasabahDPLK = form.GetUIPartByName('uipNasabahDPLK')
    
    formObj = self.FormObject; app = formObj.ClientApplication
    ph = formObj.CallServerMethod("searchRekeningDPLK", \
      app.CreateValues(['no_peserta', uipNasabahDPLK.no_peserta]))
    
    # process return
    dsStatus = ph.packet.status
    rec = dsStatus.GetRecord(0)
    if rec.error_status:
      # show error message
      formObj.ShowMessage(rec.error_message)
    else:
      self.qRekeningDPLK.SetDirectResponse(ph.Packet)
    
  
  
  