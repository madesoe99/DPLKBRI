def FormShow(form, parameter):
  app = form.ClientApplication
  uipJenisPekerjaan = form.GetUIPartByName('uipJenisPekerjaan')
  
  uipJenisPekerjaan.Edit()
  uipJenisPekerjaan.user_id = app.UserID
  uipJenisPekerjaan.last_update = app.ModDateTime.Now()
  uipJenisPekerjaan.risk_flag = 'M'
