def FormShow(form, parameter):
  app = form.ClientApplication
  uipKepemilikan = form.GetUIPartByName('uipKepemilikan')
  
  uipKepemilikan.Edit()
  uipKepemilikan.user_id = app.UserID
  uipKepemilikan.last_update = app.ModDateTime.Now()

