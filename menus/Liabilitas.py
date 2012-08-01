def DisplayQuery(sender, app, folder):
  #display MDI window
  #assuming stringTag property contains form ID / name

  formID = sender.StringTag
  form = app.FindForm(formID)
  if form == None:
    form = app.GetForm(folder+'/'+formID, formID, 2)
  form.Show()

def DisplayQueryWithData(sender, app, folder, key, uipart):
  #display MDI window
  #assuming stringTag property contains form ID / name

  formID = sender.StringTag
  form = app.FindForm(formID)
  if form == None:
    form = app.GetFormWithData(folder+'/'+formID, formID, 2, key, uipart)
  form.Show()

def DisplayForm(sender, app, folder):
  formID = sender.StringTag
  form = app.GetForm(folder+'/'+formID, formID, 0)
  form.Show(app.CreateValues(['mode','new']))

def DisplayFormInputBukuDPLK(sender, app):
  folder = 'transaction'
  formID = sender.StringTag
  form = app.CreateForm('transaction/'+formID, formID, 0, None, None)
  
  mode = 'new'
  if sender.Name == 'GantiBukuBaru':
    mode = 'ganti'
  
  form.Show(app.CreateValues(['mode',mode]))

def DisplayFormWithData(sender, app, folder, key, uipart):
  formID = sender.StringTag
  form = app.GetFormWithData(folder+'/'+formID, formID, 0, key, uipart)
  form.Show(app.CreateValues(['mode','new']))

def DisplayMasterQuery(sender, app):
  DisplayQuery(sender, app, 'master')

def DisplayListQuery(sender, app):
  DisplayQuery(sender, app, 'list')

def DisplayTransactionQuery(sender, app):
  DisplayQuery(sender, app, 'transaction')

def DisplayTransactionForm(sender, app):
  DisplayForm(sender, app, 'transaction')

def DisplayWithDataTransX(sender, app):
  formID = sender.StringTag
  form = app.CreateForm('transaction/'+formID, formID, 0, None, None)
  form.Show(app.CreateValues(['mode','new']))
  
def DisplayQueryWDataTransX(sender, app):
  DisplayQueryWithData(sender, app, 'transaction', 'x', 'x')

def DisplayHistoriQuery(sender, app):
  formID = 'qHistori'
  form = app.FindForm(formID)

  if form == None:
    form = app.GetForm('transaction/histori/'+formID, formID, 2)
  else:
    oform = form.FormObject
    uipNoData = oform.GetUIPartByName('uipNoData')
    if uipNoData.kode_jenis_registercif <> sender.StringTag:
      form = app.GetForm('transaction/histori/'+formID, formID, 2)

  form.Show(app.CreateValues(['kode_jenis_registercif',sender.StringTag]))

def DisplayReportForm(sender, app):
  DisplayForm(sender, app, 'report')
  
def DisplayReportForm2(sender, app):
  formID = sender.StringTag
  form = app.CreateForm('report/'+formID, formID, 0, None, None)
  form.FormContainer.Show()

def mnuKontrolJmlPstBlnClick(sender, app):
  formID = 'fKontrolJmlPeserta'
  form = app.GetForm('report/'+formID, formID, 0)
  form.Show()
  #form.Show(app.CreateValues(['jenis',sender.StringTag]))

def mnuRekapTransClick(sender, app):
  formID = 'fRekapTransaksi'
  form = app.GetForm('report/'+formID, formID, 0)
  form.Show(app.CreateValues(['jenis',sender.StringTag]))

def mnuMasaPensiunClick(sender, app):
  formID = 'fMasaPensiun'
  form = app.GetForm('report/'+formID, formID, 0)
  form.Show(app.CreateValues(['isDipercepat',sender.StringTag]))

def mnuLaporanTransaksiClick(sender, app):
  formID = 'fDaftarTransaksi'
  form = app.GetForm('report/'+formID, formID, 0)
  form.Show(app.CreateValues(['jenis',sender.StringTag]))

def mnuLaporanClick(sender, app):
  formID = sender.StringTag
  form = app.GetForm('report/'+formID, formID, 0)
  form.Show()

def mnuPembayaranPremiClick(sender, app):
  formID = 'fLapPembayaranPremi'
  form = app.GetForm('report/'+formID, formID, 0)
  form.Show()

def DisplayDocumentQuery(sender, app):
  #display MDI window
  #assuming stringTag property contains form ID / name

  formID = sender.StringTag
  form = app.FindForm(formID)
  if form == None:
    form = app.GetForm(formID, formID, 2)
  form.Show()
  
#event click umum---------------------------------------------------------------

#aturan NumberTag (terutama untuk memanggil form InputSingle)
# 10 Pengalihan ke DPLK Lain
# 11 Pengalihan dari DPLK lain
# 12 Pengalihan dari DPPK lain
# 13 Pengalihan dari DPK lain
# 20 View detil Batch Transaksi
# 30 Daftar Transaksi DPLK (sudah terotorisasi)
# 31 Daftar Transaksi DPLK belum terotorisasi
# 40 Daftar Iuran Pendaftaran (sudah terotorisasi)
# 41 Daftar Iuran Pendaftaran belum terotorisasi
# 50 Daftar Transaksi Premi (sudah terotorisasi)
# 51 Daftar Transaksi Premi belum terotorisasi
# 60 Penarikan Dana Normal 30%
# 61 Penarikan Dana PHK
# 70 Pembayaran Iuran Peserta
# 80 Pengambilan Manfaat Pensiun

# 100 Input Transaksi DPLK Manual
# 110 Input Iuran Pendaftaran Manual
# 120 Input Titipan Premi
# 121 Input Transaksi Premi Manual

# 130 Input Biaya Administrasi Transaksi (Tahunan)
# 131 Input Biaya Pengelolaan Dana (Tahunan)

def mnuShowModal(sender, context):
  form_id = sender.Name
  group_id = sender.StringTag
  form = context.GetForm(group_id+'/'+form_id, form_id, 0)

  form.Show(context.CreateValues(['code',sender.NumberTag]))

def mnuShowModal2(sender, context):
  form_id = sender.Name
  group_id = sender.StringTag
  form = context.CreateForm(group_id+'/'+form_id, form_id, 0, None, None)
  form.FormContainer.Show()

def mnuShowModalWithData(sender, context):
  form_id = sender.Name
  group_id = sender.StringTag
  form = context.GetFormWithData(group_id+'/'+form_id, form_id, 0, 'x', 'x')

  form.Show(context.CreateValues(['code',sender.NumberTag]))

def mnuShow(sender, context):
  form_id = sender.Name
  group_id = sender.StringTag
  form = context.FindForm(form_id)
  if form == None:
    form = context.GetForm(group_id+'/'+form_id, form_id, 2)

  form.Show(context.CreateValues(['code',sender.NumberTag]))

def mnuShowWithData(sender, context):
  form_id = sender.Name
  group_id = sender.StringTag
  form = context.FindForm(form_id)
  if form == None:
    form = context.GetFormWithData(group_id+'/'+form_id, form_id, 2, 'x', 'x')

  form.Show(context.CreateValues(['code',sender.NumberTag]))

def mnuSelectRekening(menu, app):
  appObject = app.UserAppObject
  group_id, form_id = menu.Name.split('/')
  next_form = menu.StringTag
  f = appObject.checkLoadedForm(form_id)
  if f == None:
    f = app.CreateForm(group_id+'/'+form_id, form_id, 2, None, [next_form, menu.Caption.replace('&','')])
    form = f.FormContainer
    appObject.registerForm(form_id, f)
  else:
    f.ChangeNextForm(next_form, menu.Caption)
  f.FormContainer.Show()

def mnuSelectTransaksi(menu, app):
  group_id, form_id = menu.Name.split('/')
  form = app.FindForm(form_id)
  if form == None:
    f = app.CreateForm(group_id+'/'+form_id, form_id, 2, None, None)
    form = f.FormContainer
  form.Show()

#event click menu transaksi-----------------------------------------------------
def mnuTutupBatchClick(sender, context):
  try:
    if context.ConfirmDialog('Anda yakin akan menutup semua Batch Transaksi '\
      'yang masih berstatus terbuka?'):
      #status semua Batch yang 'open' jadikan 'closed'
      context.ExecuteScript('transaksi/CloseAllOpenBatch', \
        context.CreateValues(['idbatch', '']))
      context.ShowMessage('Semua Batch Transaksi yang berstatus Buka sudah ditutup.')
  finally:
    context = None
    
def UnconvertedBatchClick(sender, context):
  form_id = sender.Name
  group_id = sender.StringTag
  oform = context.CreateForm(group_id+'/'+form_id,form_id,0,\
    context.CreateValues(['journal_no',''],['numbertag',0]),None)
  oform.FormShow()
  
def ClassFormClick(sender, context):
  form_id = sender.Name
  group_id = sender.StringTag
  oform = context.CreateForm(group_id+'/'+form_id,form_id,0,None,None)
  oform.FormShow()

def CreateCoreBankingBatchClick(sender, context):
  if context.ConfirmDialog('Anda yakin membuat Batch Core Banking untuk hari ini?'):
    #execute script untuk create core banking batch
    res = context.ExecuteScript('transaksi/NewCoreBankingBatch',None)
    if res.FirstRecord.status == 1:
      context.ShowMessage('Batch Core Banking berhasil dibuat.')
    elif res.FirstRecord.status == 0:
      context.ShowMessage('Batch Core Banking GAGAL dibuat.')
    elif res.FirstRecord.status == -999:
      context.ShowMessage('Batch Core Banking sudah ada.')
      
def mnuCollectivityClick(sender, context):
  theD = context.ModDateTime.Now()
  y,m,d = context.ModDateTime.DecodeDate(theD)[:3]
  if context.ConfirmDialog('Anda yakin melakukan pengecekan Kolektibilitas '\
    'peserta Wasiat Ummat untuk bulan %d-%d?' % (m,y)):
    dtTglChecking = context.ModDateTime.EncodeDate(y,m,d)
    #execute script untuk cek kolektibilitas peserta wasiat ummat
    #pid = context.ExecuteScriptTrackable('transaksi/L_CekCollectivityWasiatUmmat',\
    context.ExecuteScript('longscripts/ExecuteLongScript',
      context.CreateValues(['tglChecking',dtTglChecking],['execFile','transaksi/L_CekCollectivityWasiatUmmat']))

def executePackageClick(sender, context):
  formid = 'kakas/fExecuteImportPackage'
  form   = context.CreateForm(formid, formid, 0, None, None)
  form.Show()

#event for testing only---------------------------------------------------------
def PickBatchClick(sender, context):
  oform = context.CreateForm('transaksi/fDaftarPickBatch','fDaftarPickBatch',0,None,None)
  oform.FormContainer.Show()

def SimpleShowForm(menuitem, app):
  formname = menuitem.StringTag
  form = app.FindForm(formname)
  if form == None:
    form = app.CreateForm(formname, formname, menuitem.NumberTag, None, None)
  
  form.FormContainer.Show()

def showForm(menuitem, app):
  formname = menuitem.StringTag
  
  form = app.FindForm(formname)
  if form == None:
    form = app.CreateForm(formname, formname, menuitem.NumberTag, None, None)
  
  form.Show()

def showForm2(menuitem, app):
  jenis = menuitem.Name
  formname = menuitem.StringTag
  form = app.FindForm(formname)
  if form == None:
    form = app.CreateForm(formname, formname, menuitem.NumberTag, None, None)
  
  form.Show(jenis)
