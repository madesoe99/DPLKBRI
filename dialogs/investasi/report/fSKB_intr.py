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

dictPeriode={
  '1':'Maret sampai dengan bulan Agustus',
  '2':'September sampai dengan bulan Februari'
}

dictLampiran={
  0:'Lampiran1',
  1:'LampiranIVA',
  2:'LampiranVA',
  3:'LampiranVB'
}

mode = ''; nama_file = ''; as_filename = ''; wb = None

def FormShow(form, parameter):
  global mode
  app = form.ClientApplication
  mode = parameter.FirstRecord.mode

def is_all_lampiran_onchange(sender):
  form = sender.OwnerForm
  if sender.Checked:
    form.GetControlByName('pInfo.Lampiran').Visible = 0
    form.GetControlByName('pInfo.Periode').Visible = 1
    form.GetControlByName('pInfo.Semester').Visible = 1
  else:
    form.GetControlByName('pInfo.Lampiran').Visible = 1
    form.GetControlByName('pInfo.Periode').Visible = 1
    form.GetControlByName('pInfo.Semester').Visible = 0

def lampiran_onchange(sender):
  form = sender.OwnerForm
  if sender.ItemIndex <> 0:
    form.GetControlByName('pInfo.Periode').Visible = 0
    form.GetControlByName('pInfo.Semester').Visible = 1
  else:
    form.GetControlByName('pInfo.Periode').Visible = 1
    form.GetControlByName('pInfo.Semester').Visible = 0

def is_all_pihak_ketiga_onchange(sender):
  form = sender.OwnerForm
  if sender.Checked:
    form.GetControlByName('pInfo.pihak_ketiga').Visible = 0
  else:
    form.GetControlByName('pInfo.pihak_ketiga').Visible = 1


def btnOKClick(sender):
  global mode
  form = sender.OwnerForm
  app = form.ClientApplication
  uipNoData = form.GetUIPartByName('uipNoData')
  form.ShowMessage(uipNoData.Lampiran)
  lampiran = dictLampiran[form.GetControlByName('pInfo.Lampiran').ItemIndex]

  form.CommitBuffer()
  res = None
  if lampiran <> 'Lampiran1':
    nama_script = 'reportinv.cetak_skb'

    res = app.ExecuteScript('investasi/report/' + nama_script
    , app.CreateValues(['lampiran', uipNoData.Lampiran],
                       ['semester', uipNoData.Semester],
                       ['tahun', uipNoData.Tahun],
                       ['kode_pihak_ketiga', uipNoData.GetFieldValue('pihak_ketiga.kode_pihak_ketiga')])
    )
  

  PrepareReportSKB(sender, lampiran)
  CreateReportSKB(sender, lampiran, res)
  #CreateReportSKB(sender)

def PrepareReportSKB(sender, lampiran):
  global wb, as_filename
  form = sender.OwnerForm
  uip = form.GetUIPartByName('uipNoData')
  nama_file = 'SKB_%s' % lampiran

  xl_filename = 'C:/__accountingDPLK/template/%s.xls' % nama_file
  as_filename = 'C:/__accountingDPLK/%s-%s.xls' % (nama_file, uip.GetFieldValue('pihak_ketiga.nama_pihak_ketiga'))

  wb = pyFlexcel.Open(xl_filename)

#def CreateReportSKB(sender):
def CreateReportSKB(sender, lampiran, res):
  global wb, as_filename
  form = sender.OwnerForm
  app = form.ClientApplication
#   if lampiran <> 'Lampiran1':
#     rec = res.FirstRecord
#     if rec.Is_Err:
#       raise rec.Err_Message

  IsiHeaderExcel(form, wb, res)
  

    
  #IsiExcel(app, wb, uip)
  SaveFileAs(as_filename, wb)
  
  app.ShowMessage('Laporan %s telah tergenerate di %s' % (nama_file, as_filename))
  
def SaveFileAs(filename, workbook):
    workbook.SaveAs(filename)

def IsiHeaderExcel(form, workbook, res):
    lamp = form.GetControlByName('pInfo.Lampiran').ItemIndex
#     if lamp <> 0:
#       rec = res.FirstRecord
#       ds  = res.Packet.danapaket

    app = form.ClientApplication
    uip = form.GetUIPartByName('uipNoData')
    ketpihakketiga = uip.GetFieldValue('pihak_ketiga.nama_pihak_ketiga')
    alamat = uip.GetFieldValue('pihak_ketiga.alamat_pihak_ketiga')
    NPWP = uip.GetFieldValue('pihak_ketiga.NPWP')
    semester = uip.Semester
    ketperiode = 'untuk Periode bulan %s tahun %s' % (dictPeriode[uip.Periode], uip.Tahun)
    
    y,m,d = app.ModLibUtils.DecodeDate(app.ModLibUtils.Now())
    strtgl_now = '%s %s %s' % (d, dictMonth[m], y)
    
    if lamp == 0: # lampiran 1
      workbook.SetCellValue(29,2, ketpihakketiga)
      workbook.SetCellValue(29,5, ketperiode)
      workbook.SetCellValue(34,8, strtgl_now)
      
    elif lamp == 1: # lampiran IVA
      workbook.SetCellValue(12,4, ketpihakketiga)
      workbook.SetCellValue(13,4, NPWP)
      workbook.SetCellValue(14,4, alamat)
      workbook.SetCellValue(15,4, semester)
      rec = res.FirstRecord
      b = 0
      if rec.Is_Err:
         raise rec.Err_Message

      ds  = res.Packet.lampiranA
      IsiDanaPaket(ds, workbook, 'Sheet1',b)
      workbook.SetCellValue(57,6, strtgl_now)
      
    elif lamp == 2: # lampiran VA
      workbook.SetCellValue(18,4, semester)
      rec = res.FirstRecord
      b = 3
      if rec.Is_Err:
         raise rec.Err_Message

      ds  = res.Packet.lampiranA
      IsiDanaPaket(ds, workbook, 'Sheet1', b)
      workbook.SetCellValue(68,6, strtgl_now)
      workbook.SetCellValue(69,5, ketpihakketiga)
      
    elif lamp == 3: # lampiran VB
      workbook.SetCellValue(18,4, semester)

      rec = res.FirstRecord
      b = 3
      if rec.Is_Err:
         raise rec.Err_Message

      ds  = res.Packet.lampiranB
      IsiDanaPaketOnCall(ds, workbook, 'Sheet1', b)

      workbook.SetCellValue(49,5, strtgl_now)
      workbook.SetCellValue(50,4, ketpihakketiga)
    

def IsiDanaPaket(ds, workbook, worksheetname, b):

    n = ds.RecordCount; i = 0 ; a = 1
    workbook.SetCellValue(i+19+b,1, n)
    workbook.ActivateWorksheet(worksheetname)
    while i < n:
      rec = ds.GetRecord(i)
      workbook.SetCellValue(i+19+b,1, a )
      workbook.SetCellValue(i+19+b,2, rec.nomor_rekening+' / '+rec.nomor_bilyet)
      workbook.SetCellValue(i+19+b,3, rec.tgl_penempatan)
      workbook.SetCellValue(i+19+b,4, rec.tgl_pencairan)
      workbook.SetCellValue(i+19+b,5, rec.nominal_investasi)
      workbook.SetCellValue(i+19+b,6, rec.nominal_baghas)

      i += 1
      a += 1
      

def IsiDanaPaketOnCall(ds, workbook, worksheetname, b):

    n = ds.RecordCount; i = 0 ; a = 1
    workbook.SetCellValue(i+19+b,1, n)
    workbook.ActivateWorksheet(worksheetname)
    while i < n:
      rec = ds.GetRecord(i)
      workbook.SetCellValue(i+19+b,1, a )
      workbook.SetCellValue(i+19+b,2, rec.nomor_rekening)
      workbook.SetCellValue(i+19+b,3, rec.tgl_penempatan)
      workbook.SetCellValue(i+19+b,4, rec.tgl_pencairan)
      workbook.SetCellValue(i+19+b,5, rec.nominal_investasi)
      workbook.SetCellValue(i+19+b,6, rec.nominal_baghas)

      i += 1
      a += 1
      
    #i += 10
    #workbook.SetCellValue(i+19+b,5, 'Bank Rakyat Indonesia KPO Arthaloka' )
