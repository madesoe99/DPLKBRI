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

def DisplayMasterInvestasiQuery(sender, app):
  DisplayQuery(sender, app, 'investasi/master')
  
def DisplayTransaksiInvestasiQuery(sender, app):
  DisplayQuery(sender, app, 'investasi/transaksi')

def DisplayForm(sender, app, folder):
  formID = sender.StringTag
  form = app.GetForm(folder+'/'+formID, formID, 0)
  
  ph = app.CreateValues(['mode',sender.Name])
  form.Show(ph)

def DisplayFormTransaksi(sender, app):
  DisplayForm(sender, app, 'investasi/transaksi')

def DisplayFormWithData(sender, app, folder, key, uipart):
  formID = sender.StringTag
  form = app.GetFormWithData(folder+'/'+formID, formID, 0, key, uipart)
  form.Show(app.CreateValues(['mode','new']))

def DisplayWithDataTransX(sender, app):
  DisplayFormWithData(sender, app, 'investasi/transaksi', 'new', 'new')

def DisplayQueryWDataTransX(sender, app):
  DisplayQueryWithData(sender, app, 'investasi/transaksi', 'x', 'x')

def mnuRegistrasiInvestasiClick(sender, app):
  formID = sender.StringTag
  form = app.GetFormWithData('investasi/transaksi/'+ formID, formID, 0, 'new', 'new')
  form.Show(
    app.CreateValues(
      ['mode','new']
      , ['caption',sender.Caption.replace('...','')]
    )
  )

def mnuTransDepositoClick(sender, app):
  formID = sender.StringTag
  form = app.GetFormWithData('investasi/transaksi/'+ formID, formID, 0, 'new', 'new')
  form.Show(
    app.CreateValues(
      ['mode','new']
      , ['inv','A']
      , ['caption',sender.Caption.replace('...','')]
    )
  )

def mnuTransObligasiClick(sender, app):
  formID = sender.StringTag
  form = app.GetFormWithData('investasi/transaksi/'+ formID, formID, 0, 'new', 'new')
  form.Show(
    app.CreateValues(
      ['mode','new']
      , ['inv','B']
      , ['caption',sender.Caption.replace('...','')]
    )
  )

def mnuTransReksadanaClick(sender, app):
  formID = sender.StringTag
  form = app.GetFormWithData('investasi/transaksi/'+ formID, formID, 0, 'new', 'new')
  form.Show(
    app.CreateValues(
      ['mode','new']
      , ['inv','C']
      , ['caption',sender.Caption.replace('...','')]
    )
  )

def mnuPODClick(sender, app):
  formID = sender.StringTag
  form = app.GetForm('investasi/transaksi/'+ formID, formID, 0)
  form.Show()

def mnuReportClick(sender, app):
  DisplayForm(sender, app, 'investasi/report')

def mnuViewClick(sender, app):
  formid = sender.StringTag

  oRForm = app.CreateForm(
    formid
    , formid
    , 0
    , app.CreateValues(['kode_jns_investasi', sender.Name])
    , None
  )
  aform = oRForm.FormContainer
  ea = aform.Show()

def mnuReportPiutangClick(sender, context):
  form_id = sender.StringTag
  form = context.FindForm(form_id)
  if form == None:
    form   = context.CreateForm('investasi/report/' + form_id, form_id, 2, None, None)

  ph = context.CreateValues(['mode',sender.Name])
  form.Show(ph)
