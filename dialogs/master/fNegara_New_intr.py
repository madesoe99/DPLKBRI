def FormShow(form, parameter):
  app = form.ClientApplication
  uipNegara = form.GetUIPartByName('uipNegara')
  
  uipNegara.Edit()
  uipNegara.user_id = app.UserID
  uipNegara.last_update = app.ModDateTime.Now()
  uipNegara.risk_flag = 'M'
