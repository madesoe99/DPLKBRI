def FormShow(form, parameter):
  app = form.ClientApplication
  uipDaerahKota = form.GetUIPartByName('uipDaerahKota')

  uipDaerahKota.Edit()
  uipDaerahKota.user_id = app.UserID
  uipDaerahKota.last_update = app.ModDateTime.Now()

