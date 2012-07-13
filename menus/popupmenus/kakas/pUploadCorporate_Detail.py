def ShowFormData(sender, context):
  form = context.Ownerform
  app = form.ClientApplication
  formid = '%s_Edit' % form.FormClassName
  
  key = context.KeyObjConst
  ph = app.CreateValues(['key', key])
  form = app.CreateForm('kakas/'+formid, formid, 0, ph, None)
  form.Show(sender.StringTag)
