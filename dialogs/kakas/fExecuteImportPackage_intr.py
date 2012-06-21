class frmExecutePackage:

    def __init__(self, formObj, parentForm):
        pass

    def Show(self):
        self.PackageDefList.First()
        self.FormContainer.Show()

    def bSelectFileClick(self, sender):
        filename = self.FormObject.OpenFileDialog('Source filename', \
            'Text, MS Excel (*.txt, *.xls)|*.xls;*.txt')
        self.pInput_sourceFilename.Text = filename

    def packageClick(self, sender):
        packageName = self.PackageDefList.GetFieldValue('Name')
        self.pInput_selectedPackagename.Text = packageName

    def btnOKClick(self, sender):
        app = self.FormObject.ClientApplication

        sourceFilename = self.pInput_sourceFilename.Text
        packageName = self.pInput_selectedPackagename.Text
        if sourceFilename.strip() == '':
            app.ShowMessage('Mohon pilih file source untuk diimpor!')
            return

        if app.ConfirmDialog('Anda yakin memulai impor %s untuk file %s?' % (
            packageName, sourceFilename)):

            # replaced by new upload API through datapacket
            #app.UploadItem('SaveUploadedData', [sourceFilename])

            param = app.CreateValues(['packageName', packageName],
                ['sourceFilename', sourceFilename],
                ['execFile','kakas/ExecuteImportPackage'])

            sw = param.packet.AddStreamWrapper()
            sw.LoadFromFile(sourceFilename)
            sw.Name = "upload"
            sw.FileName = sourceFilename
            sw.MIMEType = app.GetMIMETypeFromExtension(sourceFilename)

            #pid = app.ExecuteScriptTrackable('kakas/ExecuteImportPackage', param)
            app.ExecuteScript('longscripts/ExecuteLongScript', param)

            #pcConsole.ConsoleFilterName = 'ExecutePackage_' + str(pid)

            sender.Enabled = sender.Default = 0
            btnCancel = self.pButton_btnCancel
            btnCancel.Caption = '&Tutup'
            btnCancel.Default = 1

