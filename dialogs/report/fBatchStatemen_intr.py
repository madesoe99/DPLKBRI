isShowed = 0

def MyZFill(strinput, maxlen):
  while len(strinput) < maxlen:
    strinput = '0' + strinput
  return strinput

def GetYear(app, valDateTime):
  return app.ModDateTime.DecodeDate(valDateTime)[0]

def GetBeginningOfYear(app, year):
  return app.ModDateTime.EncodeDate(year, 1, 1)

def GetEndOfYear(app, year):
  return app.ModDateTime.EncodeDate(year, 12, 31)

def FormShow(form, parameter):
  global isShowed

  app = form.ClientApplication
  now = app.ModDateTime.Now()
  year = GetYear(app, now)

  uipNoData = form.GetUIPartByName('uipNoData')
  uipNoData.Edit()
  uipNoData.tanggal_awal = GetBeginningOfYear(app, year)
  uipNoData.tanggal_akhir = GetEndOfYear(app, year)

  uipNoData.jumlah_baris = 100
  uipNoData.margin_atas = 5
  uipNoData.margin_bawah = 5

  y, m, d, h, n, s, z = app.ModDateTime.DecodeDate(now)[:3] + app.ModDateTime.DecodeTime(now)[:4]
  strDate = '%s%s%s' % (MyZFill(str(d), 2), MyZFill(str(m), 2), str(y))
  strTime = '%s.%s.%s.%s' % (MyZFill(str(h), 2), MyZFill(str(n), 2), MyZFill(str(s), 2), MyZFill(str(z), 3))
  uipNoData.nama_file = 'bs_%s_%s.txt' % (strDate, strTime)

  uipNoData.urutan_1 = 'N'
  uipNoData.urutan_2 = 'N'
  uipNoData.urutan_3 = 'N'

  isShowed = 1

  uipNoData.batasi_cabang = 0
  uipNoData.batasi_kelompok = 0
  uipNoData.batasi_perusahaan = 0

  form.GetControlByName('pFilter.LBranchLocation').Enabled = 0
  form.GetControlByName('pFilter.LKelompok').Enabled = 0
  form.GetControlByName('pFilter.LNasabahDPLKCorporate').Enabled = 0

def batasi_cabangClick(sender):
  global isShowed

  form = sender.OwnerForm

  if isShowed:
    if sender.Checked:
      form.GetControlByName('pFilter.LBranchLocation').Enabled = 1
    else:
      form.GetControlByName('pFilter.LBranchLocation').Enabled = 0

def batasi_kelompokClick(sender):
  global isShowed

  form = sender.OwnerForm

  if isShowed:
    if sender.Checked:
      form.GetControlByName('pFilter.LKelompok').Enabled = 1
    else:
      form.GetControlByName('pFilter.LKelompok').Enabled = 0

def batasi_perusahaanClick(sender):
  global isShowed

  form = sender.OwnerForm

  if isShowed:
    if sender.Checked:
      form.GetControlByName('pFilter.LNasabahDPLKCorporate').Enabled = 1
    else:
      form.GetControlByName('pFilter.LNasabahDPLKCorporate').Enabled = 0

def btnOKClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipNoData = form.GetUIPartByName('uipNoData')

  if form.GetControlByName('pFilter.batasi_cabang').Checked:
    kode_cab_daftar = uipNoData.GetFieldValue('LBranchLocation.branch_code')
  else:
    kode_cab_daftar = ''

  if form.GetControlByName('pFilter.batasi_kelompok').Checked:
    kode_kelompok = uipNoData.GetFieldValue('LKelompok.kode_kelompok')
  else:
    kode_kelompok = ''

  if form.GetControlByName('pFilter.batasi_perusahaan').Checked:
    kode_nasabah_corporate = uipNoData.GetFieldValue('LNasabahDPLKCorporate.kode_nasabah_corporate')
  else:
    kode_nasabah_corporate = ''

  strOrdering = ''
  if uipNoData.urutan_1 <> 'N':
    strComma = ''
    if strOrdering <> '':
      strComma = ', '
    strOrdering += strComma + uipNoData.urutan_1

  if uipNoData.urutan_2 <> 'N':
    strComma = ''
    if strOrdering <> '':
      strComma = ', '
    strOrdering += strComma + uipNoData.urutan_2

  if uipNoData.urutan_3 <> 'N':
    strComma = ''
    if strOrdering <> '':
      strComma = ', '
    strOrdering += strComma + uipNoData.urutan_3

  task_id = app.ExecuteScriptTrackable('report/batch_statemen',\
  #res = app.ExecuteScript('report/batch_statemen',\
    app.CreateValues(\
      ['fromdate',uipNoData.tanggal_awal]\
      ,['todate',uipNoData.tanggal_akhir]\
      ,['line',uipNoData.jumlah_baris]\
      ,['top',uipNoData.margin_atas]\
      ,['bottom',uipNoData.margin_bawah]\
      ,['filename',uipNoData.nama_file]\
      ,['kode_cab_daftar',kode_cab_daftar]\
      ,['kode_kelompok',kode_kelompok]\
      ,['kode_nasabah_corporate',kode_nasabah_corporate]\
      ,['str_ordering',strOrdering]\
    )\
  )
  app.ShowTaskProgress(task_id)

  sender.ExitAction = 1

