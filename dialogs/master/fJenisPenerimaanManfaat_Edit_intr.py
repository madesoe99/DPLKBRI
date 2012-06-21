def FormShow(form, parameter):
  app = form.ClientApplication
  uipJenisPenerimaanManfaat = form.GetUIPartByName('uipJenisPenerimaanManfaat')

  uipJenisPenerimaanManfaat.Edit()
  uipJenisPenerimaanManfaat.user_id = app.UserID
  uipJenisPenerimaanManfaat.last_update = app.ModDateTime.Now()

