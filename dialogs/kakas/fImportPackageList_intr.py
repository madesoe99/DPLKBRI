def FormShow(form, parameter):
    form.GetUIPartByName('PackageDefList').First()

def refreshClick(sender):
    form = sender.OwnerForm
    form.SetData('PackageDefList', 'x:')
    form.GetUIPartByName('PackageDefList').First()

