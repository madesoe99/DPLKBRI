#import rpdb2

bInitial = 1

def ApplyParameter(form):
  qRekeningKecelakaanDiri = form.GetPanelByName('qRekeningKecelakaanDiri')
  qRekeningKecelakaanDiri.DisplayData()

def RefreshQuery(form):
  qRekeningKecelakaanDiri = form.GetPanelByName('qRekeningKecelakaanDiri')
  qRekeningKecelakaanDiri.Refresh()

def SetQueryParameter(form, paramname, paramvalue):
  qRekeningKecelakaanDiri = form.GetPanelByName('qRekeningKecelakaanDiri')
  qRekeningKecelakaanDiri.SetParameter(paramname, paramvalue)

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


def bPetunjukClick(sender):
  app = sender.OwnerForm.ClientApplication
  app.ShowMessage('KETERANGAN : \n'\
  '\nTunggakan Bulan --> Jumlah bulan yang preminya belum dibayarkan oleh peserta '\
  '\n                                   tidak termasuk bulan berjalan \n'\
  '\nJumlah Premi       --> Nominal premi yang belum dibayarkan oleh peserta '\
  '\n                                   tidak termasuk bulan berjalan ')

