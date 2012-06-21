def SetQueryParameter(form, paramname, paramvalue, flagAdmin):
  if paramvalue in [None]:
    paramvalue = '-'

  qRegistrasi = form.GetPanelByName('qRegistrasi')
  qRegistrasi.SetParameter(paramname, paramvalue)
  qRegistrasi.SetParameter('isAdmin', flagAdmin)
  qRegistrasi.DisplayData()

def ResetQueryParameter(form, paramname, paramvalue, flagAdmin):
  qRegistrasi = form.GetPanelByName('qRegistrasi')
  qRegistrasi.SetParameter(paramname, paramvalue)
  qRegistrasi.SetParameter('isAdmin', flagAdmin)
  qRegistrasi.Refresh()

def FormShow(form, parameter):
  uipNoData = form.GetUIPartByName('uipNoData')

  if uipNoData.NoLimitLocation == 'F':
    # branch dibatasi
    form.GetControlByName('pFilter.LBranchLocation').Enabled = 0
  else:
    #sama juga, filter tidak dipakai (bypass filter) untuk kemudahan
    form.GetControlByName('pFilter.LBranchLocation').Enabled = 0

  SetQueryParameter(\
    form, \
    'kode_cab_daftar', \
    uipNoData.GetFieldValue('LBranchLocation.branch_code'), \
    uipNoData.GetFieldValue('isAdmin'))

def BranchLocationAfterLookup(sender, linkui):
  form = sender.OwnerForm
  uipNoData = form.GetUIPartByName('uipNoData')
  ResetQueryParameter(form, 'kode_cab_daftar', \
    uipNoData.GetFieldValue('LBranchLocation.branch_code'), \
    uipNoData.GetFieldValue('isAdmin'))

