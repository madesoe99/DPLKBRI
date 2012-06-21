def selectClick(sender, context):
    form = context.OwnerForm
    packageName = form.GetUIPartByName('PackageDefList').GetFieldValue('Name')
    form.GetControlByName('pInput.selectedPackagename').Text = packageName

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

