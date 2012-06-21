def FormShow(form, parameter):
  app = form.ClientApplication
  uipSumberDana = form.GetUIPartByName('uipSumberDana')
  
  uipSumberDana.Edit()
  uipSumberDana.user_id = app.UserID
  uipSumberDana.last_update = app.ModDateTime.Now()

