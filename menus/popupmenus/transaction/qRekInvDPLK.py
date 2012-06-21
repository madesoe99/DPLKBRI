def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def mnuNewClick(sender, context):
  app = context.OwnerForm.ClientApplication
  formid = sender.StringTag
  intTag = sender.NumberTag
  
  ph = None
  mode = 'new'
  if intTag == 1:
    no_peserta = context.GetFieldValue('RekInvDPLK.No_Peserta')
    ph = app.CreateValues(['mode', 'exist_nasabah'], ['no_peserta', no_peserta])
    mode = 'new_pesertaexisting'
    
  #aform = app.GetFormWithData('transaction/'+formid,formid,0,'x','x')
  aform = app.CreateForm('transaction/'+formid, formid, 0, ph, None)
  #aform = app.GetForm('transaction/'+formid,formid,0)
  #SetToCenterForm(context.OwnerForm, aform.FormObject)
  aform.Show(app.CreateValues(['mode',mode]))
  
def displayWithData(sender, context):
  app = context.OwnerForm.ClientApplication
  key = context.KeyObjConst
  mode = sender.StringTag

  if mode == 'view':
    # view data nasabahdplk/RekInvDPLK
    formid = 'fRekInvDPLK'
    uipart = 'uipRekInvDPLK'
  elif mode == 'viewhistori':
    formid = 'fHistoriNasabahRekening'
    uipart = 'uipNasabahDPLK'
  else:
    # edit data umum nasabahdplk/RekInvDPLK
    formid = 'fEditNasabahRekening'
    uipart = 'uipRegisterCIF'

  if key not in ['', 0]:
    ph = app.CreateValues(['key', key])
    if ph in [None, ""]:
      app.ShowMessage('Data tidak ditemukan')
      return
    
    aform = app.GetFormWithData('transaction/'+formid, formid, 0, key, uipart)
    #SetToCenterForm(context.OwnerForm, aform.FormObject)
    aform.Show(app.CreateValues(['mode',mode]))
    
    #frm = app.CreateForm('transaction/'+formid, formid, 0, ph, None)
    #SetToCenterForm(context.OwnerForm, frm.FormObject)
    #frm.Show(app.CreateValues(['mode',mode]))
  
def mnuHistoriClick(sender, context):
  #if checkIsInactive(context):
  #  return
  
  app = context.OwnerForm.ClientApplication
  key = context.KeyObjConst
  formid = sender.StringTag
  ph = app.CreateValues(['key', key])

  #aform = app.GetFormWithData('transaction/'+formid, formid, 0, key, 'uipNasabahDPLK')
  aform = app.CreateForm('transaction/'+formid, formid, 0, ph, None)
  #SetToCenterForm(context.OwnerForm, aform.FormObject)
  aform.Show()

def GetFormInfoByCIFCode(kode_jenis_registercif):
  if kode_jenis_registercif == 'A':
    return ['fRegisterUbahAlamat','NasabahDPLK']
  elif kode_jenis_registercif == 'D':
    return ['fRegisterAutodebet','RekInvDPLK']
  elif kode_jenis_registercif == 'I':
    return ['fRegisterIuran','RekInvDPLK']
  elif kode_jenis_registercif == 'K':
    return ['fRegisterStatusKerja','NasabahDPLK']
  elif kode_jenis_registercif == 'N':
    return ['fRegisterAnuitas','RekInvDPLK']
  elif kode_jenis_registercif == 'P':
    return ['fRegisterPindahPaketInvestasi','RekInvDPLK']
  elif kode_jenis_registercif == 'U':
    return ['fRegisterWasiatUmmat','RekInvDPLK']
  elif kode_jenis_registercif == 'W':
    return ['fRegisterAhliWaris','NasabahDPLK']
  elif kode_jenis_registercif == 'Z':
    #return ['fEditNasabahRekening','NasabahDPLK']
    raise Exception, '\n\nPERHATIAN!\nMohon maaf masih dalam tahap pengembangan'
  else:
    raise Exception,'\n\nGetFormInfoByCIFCode Error\nKode jenis Register CIF tidak dikenali.'

def displayWithDataSpecific(sender, context):
  app = context.OwnerForm.ClientApplication
  kode_jenis_registercif = sender.StringTag

  formid, classname = GetFormInfoByCIFCode(kode_jenis_registercif)[:2]
  keyvalue = context.GetFieldValue('RekInvDPLK.no_rekening')
  key = 'PObj:%s#NO_REKENING=%s' % (classname, keyvalue)

  aform = app.GetFormWithData('transaction/'+formid,formid,0,key,'uipMaster')
  #SetToCenterForm(context.OwnerForm, aform.FormObject)
  aform.Show(app.CreateValues(['mode','new']))

def mnuDeleteClick(sender, context):
  app = context.OwnerForm.ClientApplication

  try:
    dlg = app.ConfirmDialog('Anda yakin akan menghapus data rekening ini?')
    if dlg:
      app = context.OwnerForm.ClientApplication
      ph = app.CreateValues(['key', context.KeyObjConst])
      ph = app.ExecuteScript('S_SetFlag.DeleteRekInvDPLK', ph)

      rec = ph.FirstRecord
      if rec.IsErr:
        raise Exception, '\n\nPERINGATAN\n%s' % rec.ErrMsg
      else:
        app.ShowMessage('Rekening DPLK telah dihapus')
        #app.DeletePObj(key)
        context.DeleteRow()
  finally:
    app = None

  return 1

def mnuStatemenClick(sender, context):
  app = context.OwnerForm.ClientApplication
  f = app.CreateForm('report/fStatemenIndividual', 'report/fStatemenIndividual', 0,
    app.CreateValues(['no_rekening', context.GetFieldValue('RekInvDPLK.no_rekening')]), None)
  f.FormContainer.Show()

