def FormShow(form, parameter):
  app = form.ClientApplication
  uipJenisPekerjaan = form.GetUIPartByName('uipJenisPekerjaan')
  
  uipJenisPekerjaan.Edit()
  uipJenisPekerjaan.user_id = app.UserID
  uipJenisPekerjaan.last_update = app.ModDateTime.Now()
  #if uipJenisPekerjaan.risk_flag in [None]
    #uipJenisPekerjaan.risk_flag = 'M'

