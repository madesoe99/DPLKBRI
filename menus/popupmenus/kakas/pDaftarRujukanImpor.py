def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

def mnuNewClick(sender, context):
  app = context.OwnerForm.ClientApplication
  formid = sender.Name

  aform = app.GetForm('kakas/'+formid,formid,0)
  #SetToCenterForm(context.OwnerForm, aform.FormObject)
  aform.Show(app.CreateValues(['mode',sender.StringTag]))

def displayWithData(sender, context):
  app = context.OwnerForm.ClientApplication
  uipTL = context.OwnerForm.GetUIPartByName('uipTemplateList')
  parameter = app.CreateValues(['namaTemplate',uipTL.NamaTemplate],\
    ['mode',sender.StringTag])
  
  formid = sender.Name
  aform = app.GetFormWithParameters('kakas/'+formid,formid,0,parameter)
  #SetToCenterForm(context.OwnerForm, aform.FormObject)
  aform.Show(app.CreateValues(['mode',sender.StringTag]))

def mnuDeleteClick(sender, context):
  app = context.OwnerForm.ClientApplication
  uipTL = context.OwnerForm.GetUIPartByName('uipTemplateList')
  parameter = app.CreateValues(['NamaFungsi','DeleteTemplate'],\
    ['NamaTemplate',uipTL.NamaTemplate])
  try:
    dlg = app.ConfirmDialog('Anda yakin menghapus Rujukan (template) ini?')
    if dlg:
      #hapus file template dengan menggunakan script
      dh = app.ExecuteScript('kakas/S_ImportTemplates',parameter)
      if dh.FirstRecord.deleteSucceed:
        app.ShowMessage('Rujukan (template) berhasil dihapus.')
      else:
        app.ShowMessage('Rujukan (template) TIDAK BERHASIL dihapus. '\
          'Bisa jadi Rujukan tidak ditemukan atau sudah dihapus. Mohon dicek dengan '\
          'me-refresh daftar Rujukan (template) terlebih dahulu.')
  finally:
    app = None

  return 1

