def showForm(sender, context):
  app = context.OwnerForm.ClientApplication
  mode = sender.StringTag
  
  ph = None
  if mode == 'edit':  
    key = context.KeyObjConst
    ph = app.CreateValues(['key', key])
  
  form = app.CreateForm('transaction/fMasterKartuDPLK', 'fMasterKartuDPLK', 0, ph, None)
  form.Show(mode)

