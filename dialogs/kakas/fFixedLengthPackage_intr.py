class frmImportPackage:

    def __init__(self, formObj, parentForm, mode, packageDefList=None):
        self.Mode = mode
        self.SourceFieldNames = []
        self.PackageDefList = packageDefList

    def SetSourceFieldNames(self):
        fieldDefs = self.SourceFieldDefs
        fieldDefs.First()
        
        while not fieldDefs.Eof:
            self.SourceFieldNames.append(fieldDefs.GetFieldValue('Name'))
            fieldDefs.Next()
            
        fieldDefs.First()

    def Show(self):
        formCaption = self.FormObject.Caption

        if self.Mode == 'VIEW':
            self.packageDefPanel.SetAllControlsReadOnly()
            self.sourceDefPanel.SetAllControlsReadOnly()
            self.sourceFieldDefsGrid.SetAllControlsReadOnly()
            self.transformationDefPanel.SetAllControlsReadOnly()
            self.transItemDefsGrid.SetAllControlsReadOnly()

            self.actionPanel_bOK.Enabled = 0
            self.actionPanel_bOK.Default = 0
            self.actionPanel_bCancel.Caption = '&Tutup'
            self.actionPanel_bCancel.Default = 1

            self.FormObject.Caption = 'View ' + formCaption
        elif self.Mode == 'EDIT':
            self.packageDefPanel_Name.Enabled = 0
            self.FormObject.Caption = 'Edit ' + formCaption
            self.PackageDef.Edit()
            self.PackageDef.Mode = self.Mode
            self.SetSourceFieldNames()
        elif self.Mode == 'NEW':
            self.SourceDef.Type = 'FIXEDLENGTH'
            self.FormObject.Caption = 'New ' + formCaption
            self.PackageDef.Mode = self.Mode

        self.FormContainer.Show()

    def fieldDefAfterPost(self, sender):
        fieldName = sender.GetFieldValue('Name')
        if not fieldName in self.SourceFieldNames:
            self.SourceFieldNames += [fieldName]

    def fieldDefBeforeDelete(self, sender):
        self.FieldNameToDelete = sender.GetFieldValue('Name')

    def fieldDefAfterDelete(self, sender):
        fieldName = self.FieldNameToDelete
        if fieldName in self.SourceFieldNames:
            self.SourceFieldNames.remove(fieldName)

    def itemDefBeforePost(self, sender):
        if not sender.SourceFieldName in self.SourceFieldNames:
            raise Exception, 'Field %s tidak ditemukan pada sources!' % (sender.SourceFieldName)

    def bOKClick(self, sender):
        app = self.FormObject.ClientApplication
        if app.ConfirmDialog('Anda yakin menyimpan perubahan?'):
            self.FormObject.CommitBuffer()
            self.FormObject.PostResult()
            if (self.Mode == 'EDIT') and (self.PackageDefList != None):
                self.PackageDefList.Edit()
                self.PackageDefList.Description = self.PackageDef.Description
                self.PackageDefList.TargetClassName = self.TransformationDef.TargetClassName
                self.PackageDefList.Post()
            sender.ExitAction = 1

