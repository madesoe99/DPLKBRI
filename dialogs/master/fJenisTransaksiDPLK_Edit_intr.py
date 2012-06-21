def FormShow(form, parameter):
  app = form.ClientApplication
  uipJenisTransaksiDPLK = form.GetUIPartByName('uipJenisTransaksiDPLK')
  
  uipJenisTransaksiDPLK.Edit()
  uipJenisTransaksiDPLK.user_id = app.UserID
  uipJenisTransaksiDPLK.last_update = app.ModDateTime.Now()

