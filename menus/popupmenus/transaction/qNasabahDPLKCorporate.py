def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def mnuNewClick(sender, context):
  app = context.OwnerForm.ClientApplication
  formid = sender.StringTag

  aform = app.CreateForm('transaction/'+formid,formid,0,None,None)
  #aform = app.GetFormWithData('transaction/'+formid,formid,0,'x','x')
  #SetToCenterForm(context.OwnerForm, aform.FormObject)
  aform.Show(app.CreateValues(['mode','new']))

def displayWithDataX(sender, context):
  app = context.OwnerForm.ClientApplication
  key = context.KeyObjConst
  ph = app.CreateValues(['key', key])
  
  frm = app.CreateForm('transaction/fCorporateParams', 'fCorporateParams', 0, ph, None)
  frm.Show()

def displayWithData(sender, context):
  app = context.OwnerForm.ClientApplication
  key = context.KeyObjConst
  mode = sender.StringTag

  if mode == 'viewmember':
    formid = 'fCorporateMember'
  elif mode <> 'editdoc':
    formid = 'fNasabahDPLKCorporate'
  else:
    formid = 'fRegistrasiCorp'

  #aform = app.GetFormWithData('transaction/'+formid,formid,0,key,uipart)
  aform = app.GetFormWithData('transaction/'+formid,formid,0,key,'uipNasabahDPLKCorporate')
  #SetToCenterForm(context.OwnerForm, aform.FormObject)
  aform.Show(app.CreateValues(['mode',mode]))

def mnuDeleteClick(sender, context):
  app = context.OwnerForm.ClientApplication
  try:
    dlg = app.ConfirmDialog('Anda yakin menghapus data perusahaan: %s?' \
      % (context.GetFieldValue('NasabahDPLKCorporate.nama_perusahaan')))
    if dlg:
      app = context.OwnerForm.ClientApplication
      ph = app.CreateValues(['key', context.KeyObjConst])
      ph = app.ExecuteScript('S_SetFlag.DeleteNasabahKorporat', ph)

      rec = ph.FirstRecord
      if rec.IsErr:
        raise Exception, '\n\nPERINGATAN\n%s' % rec.ErrMsg
      else:
        app.ShowMessage('Data nasabah korporat telah dihapus')
        #app.DeletePObj(key)
        context.DeleteRow()
  finally:
    app = None

  return 1

