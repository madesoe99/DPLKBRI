def GetFormInfoByCIFCode(kode_jenis_registercif):
  if kode_jenis_registercif == 'A':
    return ['fRegisterUbahAlamat','NasabahDPLK']
  elif kode_jenis_registercif == 'I':
    return ['fRegisterIuran','RekeningDPLK']
  elif kode_jenis_registercif == 'K':
    return ['fRegisterStatusKerja','NasabahDPLK']
  elif kode_jenis_registercif == 'W':
    return ['fRegisterAhliWaris','NasabahDPLK']
  elif kode_jenis_registercif == 'Z':
    return ['fEditNasabahRekening','NasabahDPLK']
  else:
    raise 'GetFormInfoByCIFCode Error','Kode jenis Register CIF tidak dikenali.'

def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top
  
def JenisRegisterCIFAfterLookup(sender, linkui):
  form = sender.OwnerForm
  uipNoData = form.GetUIPartByName('uipNoData')
  
  kode_jenis_registercif = uipNoData.GetFieldValue('LJenisRegisterCIF.kode_jenis_registercif')
  if (kode_jenis_registercif == 'U') or (kode_jenis_registercif == 'N'):
    uipNoData.SetFieldValue('LJenisRegisterCIF.kode_jenis_registercif',None)
    uipNoData.SetFieldValue('LJenisRegisterCIF.nama_jenis_registercif',None)
    form.GetControlByName('pData.LJenisRegisterCIF').SetFocus()

def btnOKClick(sender):
  form = sender.OwnerForm
  uipNoData = form.GetUIPartByName('uipNoData')
  app = form.ClientApplication

  form.CommitBuffer()
  form.PostResult()

  formid, classname = GetFormInfoByCIFCode(uipNoData.GetFieldValue('LJenisRegisterCIF.kode_jenis_registercif'))[:2]
  keyvalue = uipNoData.GetFieldValue('LPeserta.no_peserta')
  key = 'PObj:%s#NO_PESERTA=%s' % (classname, keyvalue)

  aform = app.GetFormWithData('transaction/'+formid,formid,0,key,'uipMaster')
  #SetToCenterForm(form, aform.FormObject)
  ea = aform.Show(app.CreateValues(['mode','new']))

  if ea == 1:
    # eaQuitOK
    sender.ExitAction = 1
  else:
    # bersihkan form
    uipNoData.Edit()
    uipNoData.SetFieldValue('LPeserta.no_peserta',None)
    uipNoData.SetFieldValue('LPeserta.nama_lengkap',None)
    uipNoData.SetFieldValue('LJenisRegisterCIF.kode_jenis_registercif',None)
    uipNoData.SetFieldValue('LJenisRegisterCIF.nama_jenis_registercif',None)
    form.GetControlByName('pData.LPeserta').SetFocus()

