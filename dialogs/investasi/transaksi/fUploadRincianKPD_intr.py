class fUploadRincianKPD:

  def __init__(self, formObj, parentForm):
    self.form = formObj
    self.id_investasi = None
    self.app = formObj.ClientApplication

  def Show(self, parameter):
    self.id_investasi = parameter.FirstRecord.id_investasi
    self.FormContainer.Show()
    
  def onBrowseClick(self, sender):
    filename = self.FormObject.OpenFileDialog('Source filename', \
        'MS Excel (*.xls)|*.xls')
    if filename:
      self.uipTransaction.Edit()
      self.uipTransaction.filename = filename

  def onProsesClick(self, sender):
    ph = self.app.CreateValues(['filename', self.uipTransaction.filename],['id_investasi', self.id_investasi])

    sourceFileName = self.uipTransaction.filename
    sw = ph.Packet.AddStreamWrapper()
    sw.LoadFromFile(sourceFileName)
    sw.Name = "fileupload"
    sw.FileName = sourceFileName
    sw.MIMEType = self.app.GetMIMETypeFromExtension(sourceFileName)

    rph = self.FormObject.CallServerMethod('ProsesUpload', ph)

    if rph.FirstRecord.Is_Err:
      raise 'PERINGATAN', rph.FirstRecord.Err_Msg
    else:
      self.app.ShowMessage('Upload rincian KPD berhasil')
