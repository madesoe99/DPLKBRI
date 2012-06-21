def FormShow(form, parameter):
  app = form.ClientApplication
  uipJenisRegisterCIF = form.GetUIPartByName('uipJenisRegisterCIF')
  
  uipJenisRegisterCIF.Edit()
  uipJenisRegisterCIF.user_id = app.UserID
  uipJenisRegisterCIF.last_update = app.ModDateTime.Now()

