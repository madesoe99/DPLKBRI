def kode_onexit(sender):     
  form = sender.OwnerForm                                         
  app = form.ClientApplication
                                 
  uipJenisReksadana = form.GetUIPartByName('uipJenisReksadana')  
  uipJenisReksadana.Edit()
  
  res = app.ExecuteScript(
   'investasi/transaksi/invutils'
   , app.CreateValues(
       ['kode', uipJenisReksadana.kode_jns_reksadana]
       , ['nama_field', 'kode_jns_reksadana']                
       , ['nama_tabel', 'JenisReksadana']
     )
  )
  
  rec = res.FirstRecord
  if rec.ada:
    app.ShowMessage('Jenis reksadana %s sudah ada' % uipJenisReksadana.kode_jns_reksadana)
    uipJenisReksadana.kode_jns_reksadana = None
    sender.SetFocus()
    
def btnOKClick(sender):
  form = sender.OwnerForm
  uipJenisReksadana = form.GetUIPartByName('uipJenisReksadana')

  #cek isian field yang harus diisi
  if (uipJenisReksadana.kode_jns_reksadana) in [None,'']:
    form.ShowMessage('Kode Jenis Reksadana wajib diisi!')
    return
    
  form.CommitBuffer()
  try:
    uipJenisReksadana.Edit()
    uipJenisReksadana.__SYSFLAG = 'N'
    form.PostResult()
    sender.ExitAction = 1
  except:
    raise
