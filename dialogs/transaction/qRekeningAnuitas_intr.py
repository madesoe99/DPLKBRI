def SetQueryParameter(form, paramname, paramvalue, flagAdmin):
  qRekeningAnuitas = form.GetPanelByName('qRekeningAnuitas')
  qRekeningAnuitas.SetParameter(paramname, paramvalue)
  qRekeningAnuitas.SetParameter('isAdmin', flagAdmin)
  qRekeningAnuitas.DisplayData()

def ResetQueryParameter(form, paramname, paramvalue, flagAdmin):
  qRekeningAnuitas = form.GetPanelByName('qRekeningAnuitas')
  qRekeningAnuitas.SetParameter(paramname, paramvalue)
  qRekeningAnuitas.SetParameter('isAdmin', flagAdmin)
  qRekeningAnuitas.Refresh()

def FormShow(form, parameter):
  uipNoData = form.GetUIPartByName('uipNoData')

  if uipNoData.NoLimitLocation == 'F':
    # branch dibatasi
    form.GetControlByName('pFilter.LBranchLocation').Enabled = 0
  else:
    #sama juga, filter tidak dipakai (bypass filter) untuk kemudahan
    form.GetControlByName('pFilter.LBranchLocation').Enabled = 0

  SetQueryParameter(form, 'branch_code', \
    uipNoData.GetFieldValue('LBranchLocation.branch_code'),\
    uipNoData.GetFieldValue('isAdmin'))

def BranchLocationAfterLookup(sender, linkui):
  form = sender.OwnerForm
  uipNoData = form.GetUIPartByName('uipNoData')
  ResetQueryParameter(form, 'branch_code', \
    uipNoData.GetFieldValue('LBranchLocation.branch_code'), \
    uipNoData.GetFieldValue('isAdmin'))

