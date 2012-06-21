def mnuShowModal(sender, app):
  form_id = sender.Name
  group_id = sender.StringTag
  form = app.GetForm(group_id+'/'+form_id, form_id, 0)

  form.Show(app.CreateValues(['code',sender.NumberTag]))
  
def mnuShowModalWithData(sender, app):
  form_id = sender.Name
  group_id = sender.StringTag
  form = app.GetFormWithData(group_id+'/'+form_id, form_id, 0, 'x', 'x')

  form.Show(app.CreateValues(['code',sender.NumberTag]))
