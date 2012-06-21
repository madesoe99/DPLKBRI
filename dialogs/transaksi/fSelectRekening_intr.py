class fSelectRekening:
  def __init__(self, formObj, parentForm, nextForm, addCaption):
    # nextForm akan dipanggil setelah rekening dipilih
    self.NextForm = nextForm
    self.OriginalCaption = 'Pilih Rekening Atau Nama Peserta'
    formObj.Caption = self.OriginalCaption + ' Untuk ' + addCaption
  #--
    
  def ChangeNextForm(self, nextForm, changeCaption):
    # ubah nextForm
    self.NextForm = nextForm
    self.FormObject.Caption = self.OriginalCaption + ' Untuk ' + changeCaption
  #--
  
  def bCariRekeningPeserta(self, button):
    formObj = self.FormObject; app = formObj.ClientApplication
      
    if self.pSearch_eNomorRekening.Text != "" or self.pSearch_eNamaPeserta.Text != "":
      nomorRekening = self.pSearch_eNomorRekening.Text or "None"
      namaPeserta = self.pSearch_eNamaPeserta.Text or "None"
      ph = formObj.CallServerMethod("searchRekening", \
        app.CreateValues(['nomorRekening', nomorRekening], \
        ['namaPeserta', namaPeserta]))
      
      # process return
      dsStatus = ph.packet.status
      rec = dsStatus.GetRecord(0)
      if rec.error_status:
        # show error message
        formObj.ShowMessage(rec.error_message)
      else:
        self.qNomorRekening.SetDirectResponse(ph.Packet)
        if rec.has_more_data:
          formObj.ShowMessage("Diketahui ada data lebih. Silahkan isi pencarian Nomor Rekening atau Nama Peserta lebih spesifik!")
          return
    else:
      formObj.ShowMessage("Silahkan isi Nomor Rekening atau Nama Peserta!")
      return
  #--
  
  def bPilihClick(self, button):
    app = self.FormObject.ClientApplication
    group_id, form_id = self.NextForm.split('/')
    form = app.FindForm(form_id)
    if form == None:
      nomorRekening = self.qNomorRekening.GetFieldValue('no_rekening')
      nomorPeserta = self.qNomorRekening.GetFieldValue('no_peserta') 
      ph = app.CreateValues(["no_rekening", nomorRekening], ["no_peserta", nomorPeserta])
      f = app.CreateForm(group_id+'/'+form_id, form_id, 0, ph, None)
      form = f.FormContainer
    form.Show()    
  #--
  
  def Form_OnClose(self, formObj):
    # procedure(formobj: TrtfForm)
    app = formObj.ClientApplication
    userApp = app.UserAppObject
    userApp.unregisterForm('fSelectRekening')
  #--  