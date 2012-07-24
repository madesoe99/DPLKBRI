def showForm(sender, context):
  app = context.OwnerForm.ClientApplication
  mode = sender.StringTag
  
  ph = None
  formid = 'fMasterKartuDPLK'
  if mode == 'edit':  
    key = context.KeyObjConst
    ph = app.CreateValues(['key', key])
    formid = 'fMasterKartuDPLK_Edit'
  
  form = app.CreateForm('transaction/'+formid, formid, 0, ph, None)
  form.Show(mode)

