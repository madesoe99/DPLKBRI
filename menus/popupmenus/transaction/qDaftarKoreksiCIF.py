def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def GetFormIDByCIFCode(kode_jenis_registercif):
  if kode_jenis_registercif == 'A':
    return 'fRegisterUbahAlamat'
  elif kode_jenis_registercif == 'D':
    return 'fRegisterAutodebet'
  elif kode_jenis_registercif == 'I':
    return 'fRegisterIuran'
  elif kode_jenis_registercif == 'K':
    return 'fRegisterStatusKerja'
  elif kode_jenis_registercif == 'N':
    return 'fRegisterAnuitas'
  elif kode_jenis_registercif == 'P':
    return 'fRegisterPindahPaketInvestasi'
  elif kode_jenis_registercif == 'U':
    return 'fRegisterWasiatUmmat'
  elif kode_jenis_registercif == 'W':
    return 'fRegisterAhliWaris'
  else:
    raise 'GetFormIDByCIFCode Error','Kode jenis Register CIF tidak dikenali.'

def mnuNewClick(sender, context):
  app = context.OwnerForm.ClientApplication
  formid = sender.StringTag

  aform = app.GetForm('transaction/'+formid,formid,0)
  SetToCenterForm(context.OwnerForm, aform.FormObject)
  aform.Show(app.CreateValues(['mode','new']))

def displayWithData(sender, context):
  app = context.OwnerForm.ClientApplication
  key = context.KeyObjConst
  kode_jenis_registercif = context.GetFieldValue('kode_jenis_registercif')
  mode = sender.StringTag
  formid = GetFormIDByCIFCode(kode_jenis_registercif)

  aform = app.GetFormWithData('transaction/'+formid,formid,0,key,'uipRegisterCIF')
  SetToCenterForm(context.OwnerForm, aform.FormObject)
  aform.Show(app.CreateValues(['mode',mode]))

def mnuDeleteClick(sender, context):
  app = context.OwnerForm.ClientApplication
  try:
    dlg = app.ConfirmDialog('Are you sure you want to delete this row?')
    if dlg:
      key = context.KeyObjConst

      app.DeletePObj(key)
      app.ShowMessage('Data was succesfully deleted')
      context.DeleteRow()
  finally:
    app = None

  return 1

