class fRegistrationPayment:
  def __init__(self, formObj, parentForm):
    #self.formObj, self.app = formObj, formObj.ClientApplication
    self.fReady = 0
    self.isOnClick = 0
    if parentForm != None:
      self.parentForm = parentForm
    else:
      self.parentForm = None
  #--

  def Show(self):
    app = self.FormObject.ClientApplication
    
    self.FormShow(self.FormObject)
    self.FormContainer.Show()

  def FormShow(self, form):
    uipIuranPendaftaran = form.GetUIPartByName('uipIuranPendaftaran')
    form.GetPanelByName('pIuranPeserta').GetControlByName('cbLangsungIuran').Checked = 0
    
    self.fReady = 1
  
  def btnOKClick(self, sender):
    form = sender.OwnerForm
    form.CommitBuffer()
    
    app = form.ClientApplication
    uipIuranPendaftaran = form.GetUIPartByName('uipIuranPendaftaran')
    uipIuranPeserta = form.GetUIPartByName('uipIuranPeserta')
  
    cbLangsungIuran = form.GetPanelByName('pIuranPeserta').GetControlByName('cbLangsungIuran')
    if not cbLangsungIuran.Checked or uipIuranPeserta.GetFieldValue('cbLangsungIuran') in [None]:
      dlg = app.ConfirmDialog(\
        'Peserta seharusnya membayar iuran pertama ketika membayar pendaftaran.\n'\
        'Anda yakin untuk melanjutkan?')
      if not dlg:
        return

    if cbLangsungIuran.Checked and uipIuranPeserta.GetFieldValue('mutasi_iuran_pst') in [None, 0, '']:
      dlg = app.ConfirmDialog(\
        'Iuran Pertama Peserta bernilai 0 (nol)\n'\
        'Anda yakin untuk melanjutkan?')
      if not dlg:
        return
  
    try:
      uipIuranPendaftaran.Edit()
      uipIuranPendaftaran.SetFieldValue('__SYSFLAG', 'N')
      
      if cbLangsungIuran.Checked:
        uipIuranPeserta.Edit()
        uipIuranPeserta.SetFieldValue('__SYSFLAG', 'N')
      
      ph = form.GetDataPacket()
      ret = form.CalServerMethod("saveBiayaDaftar", ph)
      form.ShowMessage('3')
      
      if not ret.FirstRecord.success:
        form.ShowMessage(ret.FirstRecord.message)
        return
      
        #form.CommitBuffer()
        #form.PostResult()
        
        '''
        form.ShowMessage('Pendaftaran berhasil. Siapkan printer untuk mencetak Slip Transaksi.')
        uipP = form.GetUIPartByName('uipParameterBatch')
        if uipP.FileSlipPendaftaran not in [None,'']:
          downloadRes = form.CallServerMethod("downloadFile", \
            app.CreateValues(["fileName", uipP.FileSlipPendaftaran]))
          libDLClass = form.ClientApplication.GetClientClass("libDownload", "libDownload")
          libDL = libDLClass()
          libDL.printStream(form.ClientApplication, downloadRes.Packet.GetStreamWrapper(0))
    
        if uipP.FileSlipIuran not in [None,'']:
          downloadRes = form.CallServerMethod("downloadFile", \
            app.CreateValues(["fileName", uipP.FileSlipIuran]))
          libDLClass = form.ClientApplication.GetClientClass("libDownload", "libDownload")
          libDL = libDLClass()
          libDL.printStream(form.ClientApplication, downloadRes.Packet.GetStreamWrapper(0))
        '''
        
        sender.ExitAction = 1
    except:
      raise Exception, '\n\nData pembayaran gagal disimpan'
