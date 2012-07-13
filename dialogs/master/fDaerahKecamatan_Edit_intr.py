def FormShow(form, parameter):
  app = form.ClientApplication
  uipDaerahKecamatan = form.GetUIPartByName('uipDaerahKecamatan')

  uipDaerahKecamatan.Edit()
  uipDaerahKecamatan.user_id = app.UserID
  uipDaerahKecamatan.last_update = app.ModDateTime.Now()

