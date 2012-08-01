def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def mnuNewClick(sender, context):
  app = context.OwnerForm.ClientApplication
  formID = sender.StringTag
  form = app.CreateForm('transaction/'+formID, formID, 0, None, None)
  form.Show(app.CreateValues(['mode','new']))

def displayWithData(sender, context):
  formID = 'fRegistrasi_testPrint'
  mode = sender.StringTag
  #aform = app.GetFormWithData('transaction/'+formid,formid,0,key,'uipRegisterNasabahRekening')
  if context.KeyObjConst not in ['', 0]:
    app = context.OwnerForm.ClientApplication
    ph = app.CreateValues(['key', context.KeyObjConst])
    if ph in [None, ""]:
      app.ShowMessage('Data tidak ditemukan')
      return
    
    frm = app.CreateForm('transaction/'+formID, formID, 0, ph, None)
    SetToCenterForm(context.OwnerForm, frm.FormObject)
    ea = frm.Show(app.CreateValues(['mode',mode]))
    
    if mode == 'auth':
      if ea == 1:
        # otorisasi berhasil
        #app.ShowMessage('Otorisasi berhasil.')
        context.DeleteRow()
      elif ea not in [2, None]:
        # penghapusan berhasil
        #app.ShowMessage('Penolakan register berhasil.')
        context.DeleteRow()

def mnuPaymentClick(sender, context):
  app = context.OwnerForm.ClientApplication
  
  #cek status biaya daftar peserta (sudah bayar pendaftaran atau belum)
  if context.GetFieldValue('RegisterNasabahRekening.STATUS_BIAYA_DAFTAR') == 'T':
    app.ShowMessage('Peserta sudah membayar Biaya Pendaftaran.\nSelanjutnya silahkan lakukan approval.')
    return
  
  try:
    dlg = app.ConfirmDialog('Anda akan melakukan pembayaran Biaya Pendaftaran '\
      'untuk peserta %s %s?' % (context.GetFieldValue('RegisterNasabahRekening.no_peserta'),\
      context.GetFieldValue('RegisterNasabahRekening.nama_lengkap')))
      
    if dlg:
      ph = app.CreateValues(['key', context.KeyObjConst])
      aform = app.CreateForm('transaction/fRegistrationPayment',\
        'fRegistrationPayment',0,ph, None)
      #SetToCenterForm(context.OwnerForm, aform.FormObject)
      ea = aform.Show()
      #app.ShowMessage(str(ea))      
      if ea == 1:
        # eaQuitOK
        #app.ShowMessage('Biaya Pendaftaran telah dibayar.')
        #set Status_biaya_daftar di query menjadi T (true)
        context.SetFieldValue('RegisterNasabahRekening.STATUS_BIAYA_DAFTAR', 'T')
      else:
        #app.ShowMessage('Pembayaran Biaya Pendaftaran dibatalkan.')
        pass
  finally:
    app = None

  return 1
