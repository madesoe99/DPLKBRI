def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def ShowRegisterDeposito(sender, context):
  app = context.OwnerForm.ClientApplication

  formID = 'fRegisterDeposito'
  form = app.GetFormWithData('investasi/transaksi/'+ formID, formID, 0, 'new', 'new')
  form.Show(
    app.CreateValues(
      ['mode', sender.StringTag]
      , ['inv', 'A']
      , ['caption', sender.Caption.replace('...','')]
    )
  )

def displayWithData(sender, context):
  app = context.OwnerForm.ClientApplication
  mode = sender.StringTag

  if mode == 'new':
    key = mode
    uipart = mode
    formid = 'fRegisterDeposito'
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

def mnuTransDepositoClick(sender, context):
  app = context.OwnerForm.ClientApplication

  key = context.KeyObjConst
  uipart = 'uipDeposito'
  formid = sender.StringTag
  y,m,d = context.GetFieldValue('Deposito.tgl_buka')[:3]
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

def mnuRolloverClick(sender, context):
  app = context.OwnerForm.ClientApplication

  key = context.KeyObjConst
  uipart = 'uipDeposito'
  formid = sender.StringTag

  aform = app.GetFormWithData('investasi/transaksi/'+formid,formid,0,key,uipart)
  SetToCenterForm(context.OwnerForm, aform.FormObject)
  ea = aform.Show(
    app.CreateValues(
      ['mode','new']
      , ['caption', sender.Caption.replace('...','')]
    )
  )

def mnuKoreksiAROClick(sender, context):
  app = context.OwnerForm.ClientApplication

  key = context.KeyObjConst
  uipart = 'uipDeposito'
  formid = sender.StringTag

  aform = app.GetFormWithData('investasi/transaksi/'+formid,formid,0,key,uipart)
  SetToCenterForm(context.OwnerForm, aform.FormObject)
  aform.Show(
    app.CreateValues(
      ['mode',sender.Name]
      , ['caption', sender.Caption.replace('...','')]
    )
    )
    
def BatalkanDeposito (sender, context) :
  app = context.OwnerForm.ClientApplication
  key = context.KeyObjConst
  uipart = 'uipDeposito'
  if app.ConfirmDialog('Apakah Deposito ini akan dibatalkan?') :
    app.ExecuteScript('investasi/Transaksi/S_BatalkanDeposito',app.CreateValues(['key',key]))
