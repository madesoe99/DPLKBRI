def FormShow(form, parameter):
  app = form.ClientApplication
  uipJenisUsaha = form.GetUIPartByName('uipJenisUsaha')
  
  uipJenisUsaha.Edit()
  uipJenisUsaha.user_id = app.UserID
  uipJenisUsaha.last_update = app.ModDateTime.Now()
  #if uipJenisUsaha.risk_flag in [None]:
  #  uipJenisUsaha.risk_flag = 'M'

