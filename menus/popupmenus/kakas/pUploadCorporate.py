def GetFSpecificString(context):
  app = context.OwnerForm.ClientApplication
  
  fSpecific = None
  upload_type = context.GetFieldValue('UploadCorporate.upload_type')
  if upload_type == "P":
    fSpecific = 'fUCRegisterPeserta,UploadCorporate'
  elif upload_type == "I":
    fSpecific = 'fUCIuranPeserta,UploadCorporate'
  elif upload_type == "W":
    fSpecific = 'fUCAhliWaris,UploadCorporate'
  elif upload_type == "K":
    fSpecific = 'fFinColKendaraan,UploadCorporate'
  elif upload_type == "A":
    fSpecific = 'fFinColIntDeposito,UploadCorporate'
  elif upload_type == "R":
    fSpecific = 'fUCBiayaDaftar,UploadCorporate'
  else:
    raise Exception, '\n\nPERHATIAN!\nJenis upload tidak terdaftar...'
    
  return fSpecific

def ShowForm(sender, context):
  app = context.OwnerForm.ClientApplication
  formid = sender.StringTag

  """  
  fSpecific = GetFSpecificString(context)
  if fSpecific != None:      
    ph = app.CreateValues(['key', ''])
    form = app.CreateForm('kakas/'+formid, formid, 0, ph, None)
    form.Show(app.CreateValues(['fMode','new'],['fType','kakas/'+fSpecific]))
  """

  ph = app.CreateValues(['key', ''])
  form = app.CreateForm('kakas/'+formid, formid, 0, ph, None)
  form.Show()

def ShowFormData(sender, context):
  app = context.OwnerForm.ClientApplication
  formid = sender.StringTag
  key = context.KeyObjConst
  
  fMode = 'view'
  if sender.Name == 'mnuAuth':
    if context.GetFieldValue('UploadCorporate.is_auth') == 'T':
      app.ShowMessage('Paket import ini sudah diotorisasi...')
      return
    fMode = 'auth'
  
  fSpecific = GetFSpecificString(context)
  if fSpecific != None:      
    ph = app.CreateValues(['key', key])
    form = app.CreateForm('kakas/'+formid, formid, 0, ph, None)
    form.Show(app.CreateValues(['fMode',fMode],['fType','kakas/'+fSpecific]))

def ShowFormDataEdit(sender, context):
  app = context.OwnerForm.ClientApplication
  formid = sender.StringTag
  key = context.KeyObjConst
  
  fSpecific = GetFSpecificString(context)
  if fSpecific != None:      
    ph = app.CreateValues(['key', key])
    form = app.CreateForm('kakas/'+formid, formid, 0, ph, None)
    form.Show(app.CreateValues(['fMode','edit'],['fType','kakas/'+fSpecific]))