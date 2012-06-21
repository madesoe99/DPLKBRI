class fUpload:

    filename = ''
    
    def __init__(self, formObj, parentForm):
        pass

    def FormShow(self):
        self.FormContainer.Show()

    def btUploadClick(self, sender):
      global filename

      app = self.FormObject.ClientApplication

      if app.ConfirmDialog('Anda yakin mengupload file iuran : %s?' % filename):
        sender.Enabled = 0
        param = app.CreateValues(['filename', filename])
        
        self.UploadFile(app, param, filename)
        
        rph = app.ExecuteScript('S_UploadMassal', param)
        if rph.FirstRecord.succeed:
          app.ShowMessage('Upload data iuran berhasil')

    def UploadFile(self, app, param, filename):
        sw = param.packet.AddStreamWrapper()
        sw.LoadFromFile(filename)
        sw.Name = "upload"+filename
        sw.FileName = filename
        sw.MIMEType = app.GetMIMETypeFromExtension(filename)

    def btBrowseClick(self, sender):
      global filename
      
      filename = self.FormObject.OpenFileDialog('Source filename', \
            'Delimited text (*.txt)|*.txt')
      self.pnInput_eFilename.Text = filename


