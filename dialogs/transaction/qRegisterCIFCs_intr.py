def SetQueryParameter(form, paramname, paramvalue, flagAdmin):
  qRegisterCIF = form.GetPanelByName('qRegisterCIF')
  qRegisterCIF.SetParameter(paramname, paramvalue)
  qRegisterCIF.SetParameter('isAdmin', flagAdmin)
  qRegisterCIF.DisplayData()
  """
  select from RegisterCIF
  [
    (1 = :isAdmin or LUserApp.branch_code = :branch_code)
    AND (kode_jenis_registercif <> 'U' and kode_jenis_registercif <> 'N')
    AND (kode_jenis_registercif <> 'D' and kode_jenis_registercif <> 'P')
  ]
  """

def ResetQueryParameter(form, paramname, paramvalue, flagAdmin):
  qRegisterCIF = form.GetPanelByName('qRegisterCIF')
  qRegisterCIF.SetParameter(paramname, paramvalue)
  qRegisterCIF.SetParameter('isAdmin', flagAdmin)
  qRegisterCIF.Refresh()

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

