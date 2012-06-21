def FormAfterProcessServerData (sender, operation_id, datapacket):
  part = sender.GetUIPartByName('menulist')
  part.First()
  
  return 1

def bSelect_Click (sender):
  try:
    form = sender.OwnerForm
    app = form.ClientApplication

    uipart = form.GetUIPartByName('menulist')
    editor = app.GetFormWithData('userman/edit_menu', 'edit_menu', 0, uipart.menu_name, 'menu_name')
    editor.Show()
  finally:
    uipart = None
    editor = None
    form = None
    app = None
