def newClick(sender, context):
    app = context.OwnerForm.ClientApplication
    formid = 'kakas/' + sender.StringTag
    param  = app.CreateValues(['Mode', 'NEW'])
    form   = app.CreateForm(formid, formid, 0, param, ['NEW'])
    form.Show()

def viewClick(sender, context):
    ownerForm = context.OwnerForm
    app = ownerForm.ClientApplication

    packageDef = ownerForm.GetUIPartByName('PackageDefList')
    sourceType = packageDef.SourceType
    if sourceType == 'MSEXCEL':
        formid = 'kakas/fMSExcelPackage'
    elif sourceType == 'FIXEDLENGTH':
        formid = 'kakas/fFixedLengthPackage'
    elif sourceType == 'SEPARATOR':
        formid = 'kakas/fSeparatorPackage'

    param  = app.CreateValues(['Mode', 'VIEW'], ['Name', packageDef.GetFieldValue('Name')])
    form   = app.CreateForm(formid, formid, 0, param, ['VIEW'])
    form.Show()

def editClick(sender, context):
    ownerForm = context.OwnerForm
    app = ownerForm.ClientApplication

    packageDef = ownerForm.GetUIPartByName('PackageDefList')
    sourceType = packageDef.SourceType
    if sourceType == 'MSEXCEL':
        formid = 'kakas/fMSExcelPackage'
    elif sourceType == 'FIXEDLENGTH':
        formid = 'kakas/fFixedLengthPackage'
    elif sourceType == 'SEPARATOR':
        formid = 'kakas/fSeparatorPackage'

    param  = app.CreateValues(['Mode', 'EDIT'], ['Name', packageDef.GetFieldValue('Name')])
    form   = app.CreateForm(formid, formid, 0, param, ['EDIT', packageDef])
    form.Show()

def deleteClick(sender, context):
    ownerForm = context.OwnerForm
    app = ownerForm.ClientApplication

    packageDef = ownerForm.GetUIPartByName('PackageDefList')
    param  = app.CreateValues(['Name', packageDef.GetFieldValue('Name')])
    if app.ConfirmDialog('Anda yakin menghapus Paket Impor ini?'):
        ph = app.ExecuteScript('kakas/DeleteImportPackage', param)
        rec = ph.FirstRecord
        if rec.IsErr:
            app.ShowMessage(rec.ErrMessage)
        else:
            app.ShowMessage('Paket Impor berhasil dihapus.')
            packageDef.Delete()


    return 1

