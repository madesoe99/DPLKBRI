def FormShow(form, parameter):
  app = form.ClientApplication
  uipDaerahAsal = form.GetUIPartByName('uipDaerahAsal')

  uipDaerahAsal.Edit()
  uipDaerahAsal.user_id = app.UserID
  uipDaerahAsal.last_update = app.ModDateTime.Now()

