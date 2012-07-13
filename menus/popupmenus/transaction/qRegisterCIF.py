def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def GetFormInfoByCIFCode(kode_jenis_registercif):
  if kode_jenis_registercif == 'A':
    return ['fRegisterUbahAlamat','RegisterUbahAlamat']
  elif kode_jenis_registercif == 'D':
    return ['fRegisterAutodebet','RegisterAutoDebet']
  elif kode_jenis_registercif == 'I':
    return ['fRegisterIuran','RegisterIuran']
  elif kode_jenis_registercif == 'K':
    return ['fRegisterStatusKerja','RegisterUbahStatusKerja']
  elif kode_jenis_registercif == 'N':
    return ['fRegisterAnuitas','RegisterAnuitas']
  elif kode_jenis_registercif == 'P':
    return ['fRegisterPindahPaketInvestasiUnitized','RegisterPindahPaketInvestasi']
  elif kode_jenis_registercif == 'U':
    return ['fRegisterWasiatUmmat','RegisterWasiatUmmat']
  elif kode_jenis_registercif == 'W':
    return ['fRegisterAhliWaris','RegisterAhliWaris']
  elif kode_jenis_registercif == 'Y':
    return ['fEditKYCNasabah','RegEditKYCNasabah']
  elif kode_jenis_registercif == 'Z':
    return ['fEditNasabahRekening','RegEditNasabahRekening']
  elif kode_jenis_registercif == 'X':
    return ['fEditRekInvDPLK','RegEditRekening']
  elif kode_jenis_registercif == 'S':
    return ['fEditRekSumber','RegEditRekSumber']
  else:
    raise Exception,'\n\nGetFormInfoByCIFCode Error\nKode jenis Register CIF tidak dikenali.'

def mnuNewClick(sender, context):
  app = context.OwnerForm.ClientApplication
  formid = sender.StringTag

  aform = app.GetForm('transaction/fRegisterCIF_Intro','fRegisterCIF_Intro',0)
  #SetToCenterForm(context.OwnerForm, aform.FormObject)
  aform.Show(app.CreateValues(['mode','new']))

def displayWithData(sender, context):
  app = context.OwnerForm.ClientApplication
  keyvalue = context.GetFieldValue('RegisterCIF.ID')
  kode_jenis_registercif = context.GetFieldValue('RegisterCIF.kode_jenis_registercif')

  formid, classname = GetFormInfoByCIFCode(kode_jenis_registercif)[:2]
  keyobjconst = 'PObj:%s#REGISTERCIF_ID=%d' % (classname,keyvalue)

  mode = sender.StringTag
  aform = app.GetFormWithData('transaction/'+formid,formid,0,keyobjconst,'uipRegisterCIF')
  #SetToCenterForm(context.OwnerForm, aform.FormObject)
  ea = aform.Show(app.CreateValues(['mode',mode]))

  if mode == 'auth':
    if ea == 1:
      # otorisasi berhasil
      #app.ShowMessage('Otorisasi berhasil.')
      context.DeleteRow()
    elif ea <> 2:
      # penghapusan berhasil
      #app.ShowMessage('Penolakan register berhasil.')
      context.DeleteRow()
