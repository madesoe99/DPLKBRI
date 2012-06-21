def FormShow(form, parameter):
  app = form.ClientApplication
  
  nowDT = app.ModDateTime.Now()
  y, m, d = app.ModDateTime.DecodeDate(nowDT)

  uipNoData = form.GetUIPartByName('uipNoData')
  uipNoData.Edit()
  uipNoData.pilihinvestasi = 1
  uipNoData.monthFrom = m
  uipNoData.yearFrom = y
  uipNoData.monthUntil = m
  uipNoData.yearUntil = y

def pilihinvestasiClick(sender):
  form = sender.OwnerForm
  LJenisInvestasi = form.GetControlByName('pInfo.LJenisInvestasi')
  if sender.Checked:
    LJenisInvestasi.Enabled = 1
  else:
    uipNoData = form.GetUIPartByName('uipNoData')
    uipNoData.Edit()
    uipNoData.SetFieldValue('LJenisInvestasi.kode_jns_investasi', None)
    uipNoData.SetFieldValue('LJenisInvestasi.nama_jns_investasi', None)
    LJenisInvestasi.Enabled = 0

def checkInterval(form):
  MIN_SMALLDATETIME = [1900, 1]
  MAX_SMALLDATETIME = [2079, 6]

  uipNoData = form.GetUIPartByName('uipNoData')
  
  dateFromTup = [uipNoData.yearFrom, uipNoData.monthFrom]
  dateUntilTup = [uipNoData.yearUntil, uipNoData.monthUntil]

  if dateFromTup > dateUntilTup:
    form.ShowMessage('Bulan dan tahun akhir tidak boleh lebih dari bulan dan tahun awal.')
    return 0
    
  if (dateFromTup < MIN_SMALLDATETIME) or (dateUntilTup < MIN_SMALLDATETIME):
    form.ShowMessage('Bulan dan tahun tidak boleh kurang dari Januari 1900.')
    return 0

  if (dateFromTup >= MAX_SMALLDATETIME) or (dateUntilTup >= MAX_SMALLDATETIME):
    form.ShowMessage('Bulan dan tahun tidak boleh lebih dari Mei 2079.')
    return 0

  return 1

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipNoData = form.GetUIPartByName('uipNoData')

  form.CommitBuffer()

  if not checkInterval(form):
    return

  kode_jns_investasi = ''
  if form.GetControlByName('pInfo.pilihinvestasi').Checked:
    kode_jns_investasi = uipNoData.GetFieldValue('LJenisInvestasi.kode_jns_investasi')

  res = app.ExecuteScript('investasi/report/invakhirbulan'
    , app.CreateValues(
      ['kode_jns_investasi', kode_jns_investasi]
      , ['monthFrom', uipNoData.monthFrom]
      , ['yearFrom', uipNoData.yearFrom]
      , ['monthUntil', uipNoData.monthUntil]
      , ['yearUntil', uipNoData.yearUntil]
      )
  )

  Exef = '.htm'
  #app.DownloadItem(res.FirstRecord.filename,'v')
  streamWrapper = res.Packet.GetStreamWrapper(0)
  fileName = form.OpenFileDialog("Select file to save..",
      "Format Save Files(*%s)|*%s"%(Exef,Exef))
  if fileName != "":
     if fileName[-4:] != Exef :
        fileName = fileName + Exef
     streamWrapper.SaveToFile(fileName)
     if app.ConfirmDialog('Apakah file akan ditampilkan ?') :
        app.ShellExecuteFile(fileName)
     sender.ExitAction = 1
