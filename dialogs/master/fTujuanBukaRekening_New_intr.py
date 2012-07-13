def FormShow(form, parameter):
  app = form.ClientApplication
  uipTujuanBukaRekening = form.GetUIPartByName('uipTujuanBukaRekening')
  
  uipTujuanBukaRekening.Edit()
  uipTujuanBukaRekening.user_id = app.UserID
  uipTujuanBukaRekening.last_update = app.ModDateTime.Now()

