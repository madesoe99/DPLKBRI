def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def ShowRegisterObligasi(sender, context):
  app = context.OwnerForm.ClientApplication

  formID = 'fRegisterObligasi'
  form = app.GetFormWithData('investasi/transaksi/'+ formID, formID, 0, 'new', 'new')
  form.Show(
    app.CreateValues(
      ['mode', sender.StringTag]
      , ['inv', 'B']
      , ['caption', sender.Caption.replace('...','')]
    )
  )

def displayWithData(sender, context):
  app = context.OwnerForm.ClientApplication
  mode = sender.StringTag

  if mode == 'new':
    key = mode
    uipart = mode
    formid = 'fRegisterObligasi'
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

def mnuTransInvClick(sender, context):
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

def mnuTransOblClick(sender, context):
  app = context.OwnerForm.ClientApplication

  key = context.KeyObjConst
  uipart = 'uipObligasi'
  formid = sender.StringTag

  y,m,d = context.GetFieldValue('Obligasi.tgl_buka')[:3]
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

def mnuShowForm(sender, context) :
  app = context.OwnerForm.ClientApplication

  key = context.KeyObjConst
  uipart = 'uipObligasi'
  formid = sender.StringTag

  aform = app.GetFormWithData('investasi/transaksi/'+formid,formid,0,key,uipart)
  SetToCenterForm(context.OwnerForm, aform.FormObject)
  ea = aform.Show(
    app.CreateValues(
      ['mode',sender.Name]
      , ['caption', sender.Caption.replace('...','')]
    )
  )
