def FormShow(form, parameter):
  app = form.ClientApplication
  uipJenisJabatan = form.GetUIPartByName('uipJenisJabatan')
  
  uipJenisJabatan.Edit()
  uipJenisJabatan.user_id = app.UserID
  uipJenisJabatan.last_update = app.ModDateTime.Now()
  uipJenisJabatan.risk_flag = 'M'
