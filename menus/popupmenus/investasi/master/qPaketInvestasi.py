def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def mnuNewClick(sender, context):
  app = context.OwnerForm.ClientApplication
  formid = sender.StringTag

  #aform = app.GetForm('investasi/master/'+formid,formid,0)
  aform = app.GetFormWithData('investasi/master/'+formid,formid,0,'x','x')
  SetToCenterForm(context.OwnerForm, aform.FormObject)
  aform.Show()

def displayWithData(sender, context):
  app = context.OwnerForm.ClientApplication
  key = context.KeyObjConst
  formid = sender.StringTag
  aform = app.GetFormWithData('investasi/master/'+formid,formid,0,key,'uipPaketInvestasi')
  SetToCenterForm(context.OwnerForm, aform.FormObject)
  aform.Show()

def mnuDeleteClick(sender, context):
  app = context.OwnerForm.ClientApplication
  try:
    dlg = app.ConfirmDialog('Anda yakin menghapus %s?' \
      % (context.GetFieldValue('PaketInvestasi.Nama_Paket_Investasi')))
    if dlg:
      #cek status aktif paket investasi
      if context.GetFieldValue('PaketInvestasi.isAktif') in ['T','true','True']:
        #paket investasi masih aktif, tidak boleh dihapus
        app.ShowMessage('Penghapusan tidak dibolehkan! Paket Investasi masih aktif (digunakan).')
      else:
        kode_paket_investasi = context.GetFieldValue('PaketInvestasi.Kode_Paket_Investasi')

        app.ExecuteScript('investasi/master/paketinvestasi_del',\
          app.CreateValues(['kode_paket_investasi',kode_paket_investasi])\
        )
        context.DeleteRow()
  finally:
    app = None

  return 1

