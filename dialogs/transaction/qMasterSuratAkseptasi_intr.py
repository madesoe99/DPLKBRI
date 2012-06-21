#import rpdb2

bInitial = 1

def ApplyParameter(form):
  qRekeningWasiatUmmat = form.GetPanelByName('qRekeningWasiatUmmat')
  qRekeningWasiatUmmat.DisplayData()

def RefreshQuery(form):
  qRekeningWasiatUmmat = form.GetPanelByName('qRekeningWasiatUmmat')
  qRekeningWasiatUmmat.Refresh()

def SetQueryParameter(form, paramname, paramvalue):
  qRekeningWasiatUmmat = form.GetPanelByName('qRekeningWasiatUmmat')
  qRekeningWasiatUmmat.SetParameter(paramname, paramvalue)

def FormShow(form, parameter):
  global bInitial
  
  #rpdb2.start_embedded_debugger("000")
  uipNoData = form.GetUIPartByName('uipNoData')
  if uipNoData.NoLimitLocation == 'F':
    # branch dibatasi
    form.GetControlByName('pFilter.LBranchLocation').Enabled = 0
    form.GetControlByName('pFilter.cbDisplayAllCabang').Enabled = 0
    SetQueryParameter(form, 'display_all_cabang', 0)
  else:
    form.GetControlByName('pFilter.cbDisplayAllCabang').Checked = 1
    SetQueryParameter(form, 'display_all_cabang', 1)

  SetQueryParameter(form, 'kode_cab_daftar', uipNoData.GetFieldValue('LBranchLocation.branch_code'))
  ApplyParameter(form)
  bInitial = 0
  
def BranchLocationAfterLookup(sender, linkui):
  form = sender.OwnerForm
  uipNoData = form.GetUIPartByName('uipNoData')
  SetQueryParameter(form, 'kode_cab_daftar', uipNoData.GetFieldValue('LBranchLocation.branch_code'))
  RefreshQuery(form)

def cbDisplayAllCabangClick(sender):
  if bInitial == 0:
    form = sender.OwnerForm
    if sender.Checked:
      pVal = 1
    else:
      pVal = 0
    SetQueryParameter(form, 'display_all_cabang', pVal)
    RefreshQuery(form)

  
