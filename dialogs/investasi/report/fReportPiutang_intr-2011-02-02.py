import pyFlexcel

dictMonth={
  1:'Januari',
  2:'Februari',
  3:'Maret',
  4:'April',
  5:'Mei',
  6:'Juni',
  7:'Juli',
  8:'Agustus',
  9:'September',
  10:'Oktober',
  11:'November',
  12:'Desember'
}

mode = ''; nama_file = ''; as_filename = ''; wb = None

def FormShow(form, parameter):
  global mode
  app = form.ClientApplication
  mode = parameter.FirstRecord.mode
  #app.ShowMessage(mode)
  
  nowDT = app.ModDateTime.Now()
  y, m, d = app.ModDateTime.DecodeDate(nowDT)

  uipNoData = form.GetUIPartByName('uipNoData')
  uipNoData.Edit()
  uipNoData.monthBaghas = m
  uipNoData.yearBaghas = y
  if m == 1:
    uipNoData.monthPiutang = 12
    uipNoData.yearPiutang = y-1
  else:
    uipNoData.monthPiutang = m-1
    uipNoData.yearPiutang = y


def MonthBaghasChange(sender):
  form = sender.OwnerForm
  AdjustDatePiutang(form)

def YearBaghasChange(sender):
  form = sender.OwnerForm
  AdjustDatePiutang(form)

def AdjustDatePiutang(form):
  app = form.ClientApplication
  uipNoData = form.GetUIPartByName('uipNoData')
  uipNoData.Edit()
  m = uipNoData.monthBaghas
  y = uipNoData.yearBaghas
  
  if m == 1:
    uipNoData.monthPiutang = 12
    uipNoData.yearPiutang = y-1
  else:
    uipNoData.monthPiutang = m-1
    uipNoData.yearPiutang = y
    
def checkInterval(form):
  MIN_SMALLDATETIME = [1900, 1]
  MAX_SMALLDATETIME = [2079, 6]

  uipNoData = form.GetUIPartByName('uipNoData')

  dateBaghasTup = [uipNoData.yearBaghas, uipNoData.monthBaghas]
  datePiutangTup = [uipNoData.yearPiutang, uipNoData.monthPiutang]

  if dateBaghasTup < datePiutangTup:
    form.ShowMessage('Bulan dan tahun piutang tidak boleh lebih dari bulan dan tahun baghas.')
    return 0

  if (dateBaghasTup < MIN_SMALLDATETIME) or (datePiutangTup < MIN_SMALLDATETIME):
    form.ShowMessage('Bulan dan tahun tidak boleh kurang dari Januari 1900.')
    return 0

  if (dateBaghasTup >= MAX_SMALLDATETIME) or (datePiutangTup >= MAX_SMALLDATETIME):
    form.ShowMessage('Bulan dan tahun tidak boleh lebih dari Mei 2079.')
    return 0

  
  return 1

def btnOKClick(sender):
  global mode
  form = sender.OwnerForm
  app = form.ClientApplication
  uipNoData = form.GetUIPartByName('uipNoData')

  AdjustDatePiutang(form)
  
  form.CommitBuffer()

  if not checkInterval(form):
    return
    
  if mode == 'Depo': nama_script = 'piutang_baghas_depo'
  elif mode == 'Sukuk': nama_script = 'piutang_yield_sukuk'
  else: 
    nama_script = 'reportinv.get_distribusi_hi'
    PrepareReportDistribusiHI(sender, uipNoData)
  
  res = app.ExecuteScript('investasi/report/' + nama_script
    , app.CreateValues(
      ['monthBaghas', uipNoData.monthBaghas]
      , ['yearBaghas', uipNoData.yearBaghas]
      , ['monthPiutang', uipNoData.monthPiutang]
      , ['yearPiutang', uipNoData.yearPiutang]
      )
  )
  if mode in ('Depo','Sukuk'):
    CreateReportPiutang(sender, res)
  else:
    CreateReportDistribusiHI(sender, res)

def CreateReportPiutang(sender, res):
  form = sender.OwnerForm
  app = form.ClientApplication
  Exef = '.htm'
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

def PrepareReportDistribusiHI(sender, uip):
  global wb, as_filename
  nama_file = 'Distribusi Hasil Investasi'
  m = uip.monthBaghas
  y = uip.yearBaghas
  
  strtgl_baghas = '%s %s' % (dictMonth[m], y)
  xl_filename = 'C:/__accountingDPLK/template/%s.xls' % nama_file
  as_filename = 'C:/__accountingDPLK/%s-%s.xls' % (nama_file, strtgl_baghas)

  wb = pyFlexcel.Open(xl_filename)

  
def CreateReportDistribusiHI(sender, res):
  global wb, as_filename
  form = sender.OwnerForm
  app = form.ClientApplication
  
  rec = res.FirstRecord
  if rec.Is_Err:
    raise rec.Err_Message
    
  IsiExcel(app, wb, res)
  SaveFileAs(as_filename, wb)
  
  app.ShowMessage('Laporan %s telah tergenerate di %s' % (nama_file, as_filename))
  
def SaveFileAs(filename, workbook):
    workbook.SaveAs(filename)

def IsiExcel(app, workbook, res):
    rec = res.FirstRecord
    ds = res.Packet.danapaket        
    IsiDanaPaket(ds, workbook, 'Sheet1')
    workbook.SetCellValue(3,2, rec.tgl_investasi)
    workbook.SetCellValue(3,3, rec.tgl_investasi)
    workbook.SetCellValue(3,5, rec.tgl_investasi)
    workbook.SetCellValue(3,7, rec.tgl_baghas)
    workbook.SetCellValue(3,9, rec.tgl_baghas)
    workbook.SetCellValue(5,3, rec.inv_sukuk)
    workbook.SetCellValue(6,3, rec.inv_reksadana)
    workbook.SetCellValue(4,5, rec.inv_deposito)
    workbook.SetCellValue(4,7, rec.hi_deposito)
    workbook.SetCellValue(5,11, rec.hi_sukuk)
    workbook.SetCellValue(6,11, rec.hi_reksadana)
    y,m,d = app.ModLibUtils.DecodeDate(app.ModLibUtils.Now())
    strtgl_now = '%s %s %s' % (d, dictMonth[m], y)
    workbook.SetCellValue(9,10, strtgl_now)
    
def IsiDanaPaket(ds, workbook, worksheetname):
    n = ds.RecordCount; i = 0
    workbook.ActivateWorksheet(worksheetname)
    while i < n:
      rec = ds.GetRecord(i)
      workbook.SetCellValue(i+4,1, rec.paket)
      workbook.SetCellValue(i+4,2, rec.nominal)
      i += 1
