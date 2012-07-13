def BukaClick(sender, context):
  try:
    app = context.OwnerForm.ClientApplication
    id = context.GetFieldValue('Saham.id')
    nama = context.GetFieldValue('Saham.nama_saham')

    aform = app.GetForm('investasi/transaksi/fRegisterDepositoKPD', 'fRegisterDepositoKPD', 0)
    aform.FormObject.Caption = 'Buka Deposito KPD Untuk SAHAM %s' % nama
    aform.Show(app.CreateValues(['id',id]))
  finally:
    app = None
    aform = None
    
def DetailClick(sender, context):
  try:
    app = context.OwnerForm.ClientApplication
    id = context.GetFieldValue('Saham.id')
    nama = context.GetFieldValue('Saham.nama_saham')

    aform = app.GetForm('investasi/transaksi/qDepositoKPD', 'qDepositoKPD', 0)
    queryobj = aform.FormObject.GetPanelByName('qDepositoKPD')
    aform.FormObject.Caption = 'Detail Deposito KPD Untuk SAHAM %s' % nama
    aform.Execute()

    queryobj.SetParameter('id_investasi', id)
    queryobj.DisplayData()
    aform.Show()
  finally:
    app = None
    aform = None
    queryobj = None

def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def ShowRegisterSaham(sender, context):
  app = context.OwnerForm.ClientApplication

  formID = 'fRegisterSaham'
  form = app.GetFormWithData('investasi/transaksi/'+ formID, formID, 0, 'new', 'new')
  form.Show(
    app.CreateValues(
      ['mode', sender.StringTag]
      , ['inv', 'C']
      , ['caption', sender.Caption.replace('...','')]
    )
  )

def displayWithData(sender, context):
  app = context.OwnerForm.ClientApplication
  mode = sender.StringTag

  if mode == 'new':
    key = mode
    uipart = mode
    formid = 'fRegisterSaham'
  else:
    # mode == view
    key = context.KeyObjConst
    uipart = 'uipInvestasi'
    formid = 'fInvestasi'

  aform = app.GetFormWithData('investasi/transaksi/'+formid,formid,0,key,uipart)
  SetToCenterForm(context.OwnerForm, aform.FormObject)
  ea = aform.Show(app.CreateValues(['mode',mode]))

def mnuViewClick(sender, context):
  app = context.OwnerForm.ClientApplication

  key = context.KeyObjConst
  formid = 'fInvestasi'

  oRForm = app.CreateForm(
    'investasi/transaksi/'+formid
    , formid
    , 0
    , app.CreateValues(['key', key])
    , None
  )
  aform = oRForm.FormContainer
  SetToCenterForm(context.OwnerForm, aform.FormObject)
  ea = aform.Show()

def mnuTransManClick(sender, context):
  app = context.OwnerForm.ClientApplication

  key = context.KeyObjConst
  uipart = 'uipInvestasi'
  formid = sender.StringTag

  aform = app.GetFormWithData('investasi/transaksi/'+formid,formid,0,key,uipart)
  SetToCenterForm(context.OwnerForm, aform.FormObject)
  ea = aform.Show(
    app.CreateValues(
      ['mode','new']
      , ['caption', sender.Caption.replace('...','')]
    )
  )

def mnuTransInvClick(sender, context):
  app = context.OwnerForm.ClientApplication

  key = context.KeyObjConst
  uipart = 'uipSaham'
  formid = sender.StringTag

  y,m,d = context.GetFieldValue('Saham.tgl_buka')[:3]
  if app.ModDateTime.EncodeDate(y,m,d) > app.ModDateTime.Now() :
     raise Exception, 'PERINGATAN' + 'Tanggal transaksi tidak boleh lebih kecil dari tanggal buka'

  aform = app.GetFormWithData('investasi/transaksi/'+formid,formid,0,key,uipart)
  SetToCenterForm(context.OwnerForm, aform.FormObject)
  ea = aform.Show(
    app.CreateValues(
      ['mode','new']
      , ['caption', sender.Caption.replace('...','')]
    )
  )

def mnuKoreksiNABClick(sender, context):
  app = context.OwnerForm.ClientApplication

  key = context.KeyObjConst
  uipart = 'uipSaham'
  formid = sender.StringTag

  aform = app.GetFormWithData('investasi/transaksi/'+formid,formid,0,key,uipart)
  SetToCenterForm(context.OwnerForm, aform.FormObject)
  aform.Show(app.CreateValues(
      ['mode',sender.Name]
      , ['caption', sender.Caption.replace('...','')]
    )
    )

def mnuUploadClick(sender, context) :
    app = context.OwnerForm.ClientApplication
    formname = 'investasi/transaksi/fUploadRincianKPD'
    dlg = app.CreateForm(formname,formname,0,None,None)
    dlg.Show(app.CreateValues(['id_investasi',context.GetFieldValue('Saham.ID')]))


