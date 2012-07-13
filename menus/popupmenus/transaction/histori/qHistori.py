def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def GetFormInfoByCIFCode(kode_jenis_registercif):
  if kode_jenis_registercif == 'A':
    return ['fHistoriUbahAlamat','uipHistoriUbahAlamat']
  elif kode_jenis_registercif == 'D':
    return ['fHistoriAutodebet','uipHistoriAutodebet']
  elif kode_jenis_registercif == 'I':
    return ['fHistoriIuran','uipHistoriIuran']
  elif kode_jenis_registercif == 'K':
    return ['fHistoriStatusKerja','uipHistoriStatusKerja']
  elif kode_jenis_registercif == 'N':
    return ['fHistoriAnuitas','uipHistoriAnuitas']
  elif kode_jenis_registercif == 'P':
    return ['fHistoriPindahPaketInvestasi','uipHistoriPindahPaketInvestasi']
  elif kode_jenis_registercif == 'U':
    return ['fHistoriWasiatUmmat','uipHistoriWasiatUmmat']
  elif kode_jenis_registercif == 'W':
    return ['fHistoriAhliWaris','uipHistoriAhliWaris']
  elif kode_jenis_registercif == 'Z':
    return ['fEditNasabahRekening','uipEditNasabahRekening']
  else:
    raise Exception, 'GetFormInfoByCIFCode Error' + 'Kode jenis Register CIF tidak dikenali.'

def displayWithData(sender, context):
  form = context.OwnerForm
  app = form.ClientApplication
  uipNoData = form.GetUIPartByName('uipNoData')

  keyobjconst = context.KeyObjConst
  formid, uipart = GetFormInfoByCIFCode(uipNoData.kode_jenis_registercif)[:2]

  aform = app.GetFormWithData('transaction/histori/'+formid,formid,0,keyobjconst,uipart)
  SetToCenterForm(context.OwnerForm, aform.FormObject)
  aform.Show()

