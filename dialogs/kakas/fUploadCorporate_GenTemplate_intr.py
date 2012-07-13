class fUploadCorporate_GenTemplate:
  def __init__(self, formObj, parentForm):
    pass
  #--

  def Show(self):
    form = self.FormObject
    app = form.ClientApplication
    
    uipNoData = self.uipNoData
    uipNoData.Edit()
    uipNoData.upload_type = 'I'
    
    self.FormContainer.Show()
    
  def btnGenerateOnClick(self, sender):
    # procedure(sender: TrtfButton)
    form = self.FormObject
    app = form.ClientApplication
    form.CommitBuffer()
    
    uipNoData = self.uipNoData
    if uipNoData.GetFieldValue('LNasabahDPLKCorporate.kode_nasabah_corporate') in ['', 0, None]:
      app.ShowMessage("Nasabah Korporat belum dipilih...")
      return
      
    ph = app.CreateValues(\
      ['upload_type', uipNoData.upload_type],\
      ['kode_nasabah_corporate', uipNoData.GetFieldValue('LNasabahDPLKCorporate.kode_nasabah_corporate')],\
      ['nama_perusahaan', uipNoData.GetFieldValue('LNasabahDPLKCorporate.nama_perusahaan')])
    resp = form.CallServerMethod('GenerateFile',ph)
    status = resp.FirstRecord
    if status.Is_Err:
      app.ShowMessage(status.Err_Message)
      return
      
    app.ShowMessage('File template berhasil digenerate...')
    if resp.Packet.StreamWrapperCount > 0:
      sw = resp.Packet.GetStreamWrapper(0)
      _tmpFile = app.GetTemporaryFileName("xls") + ".xls"
      sw.SaveToFile(_tmpFile)
      app.ShellExecuteFile(_tmpFile)
    else:
      app.ShowMessage('File tidak dapat ditemukan...!')
      return
      
    return
    