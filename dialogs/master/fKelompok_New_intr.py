def FormShow(form, parameter):
  app = form.ClientApplication
  uipKelompok = form.GetUIPartByName('uipKelompok')
  
  uipKelompok.Edit()
  uipKelompok.user_id = app.UserID
  uipKelompok.last_update = app.ModDateTime.Now()

