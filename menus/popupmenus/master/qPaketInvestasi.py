def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def mnuNewClick(sender, context):
  app = context.OwnerForm.ClientApplication
  formid = sender.StringTag

  aform = app.GetForm('master/'+formid,formid,0)
  SetToCenterForm(context.OwnerForm, aform.FormObject)
  aform.Show()

def displayWithData(sender, context):
  app = context.OwnerForm.ClientApplication
  key = context.KeyObjConst
  formid = sender.StringTag
  aform = app.GetFormWithData('master/'+formid,formid,0,key,'uipPaketInvestasi')
  SetToCenterForm(context.OwnerForm, aform.FormObject)
  aform.Show()

def mnuDeleteClick(sender, context):
  app = context.OwnerForm.ClientApplication
  try:
    dlg = app.ConfirmDialog('Anda yakin menghapus Paket Investasi ini?')
    if dlg:
      kode_paket_investasi = context.GetFieldValue('PaketInvestasi.kode_paket_investasi')

      app.ExecuteScript('master/paketinvestasi_del',\
        app.CreateValues(['kode_paket_investasi',kode_paket_investasi])\
      )
      #app.ShowMessage('Data was succesfully deleted')
      context.DeleteRow()
  finally:
    app = None

  return 1

