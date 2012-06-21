def FormShow(form, parameter):
  app = form.ClientApplication
  uipOperationCode = form.GetUIPartByName('uipOperationCode')
  
  uipOperationCode.Edit()
  uipOperationCode.user_id = app.UserID
  uipOperationCode.last_update = app.ModDateTime.Now()

