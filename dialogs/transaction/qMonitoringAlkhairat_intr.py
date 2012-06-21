#import rpdb2

bInitial = 1

def ApplyParameter(form):
  qMonitoringAlkhairat = form.GetPanelByName('qMonitoringAlkhairat')
  qMonitoringAlkhairat.DisplayData()

def RefreshQuery(form):
  qMonitoringAlkhairat = form.GetPanelByName('qMonitoringAlkhairat')
  qMonitoringAlkhairat.Refresh()

def SetQueryParameter(form, paramname, paramvalue):
  qMonitoringAlkhairat = form.GetPanelByName('qMonitoringAlkhairat')
  qMonitoringAlkhairat.SetParameter(paramname, paramvalue)

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
  app.ShowMessage('KETERANGAN : \n '\
  '\nTgl Registrasi       --> Tgl pada saat proses perhitungan Premi '\
  '\nTgl Input              --> Proses perhitungan yang dilakukan oleh pihak DPLK '\
  '\nTgl Kirim               --> Proses Pengiriman Data Peserta Alkhairat ke Pihak Asuransi '\
  '\nTingkat Investasi --> Berdasarkan paket yang dipilih peserta pada saat bergabung dengan DPLK'\
  '\nSaldo Awal           --> Akumulasi Dana Peserta yang ada di DPLK ' \
  '\nRate Premi           --> Rate yang digunakan pada saat proses perhitungan Alkhairat')


