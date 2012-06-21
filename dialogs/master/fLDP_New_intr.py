def FormShow(form, parameter):
  app = form.ClientApplication
  uipLDP = form.GetUIPartByName('uipLDP')
  
  uipLDP.Edit()
  uipLDP.jenis_dp = 'B'
  uipLDP.user_id = app.UserID
  uipLDP.last_update = app.ModDateTime.Now()

