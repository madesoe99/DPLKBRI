def kode_onexit(sender):     
  form = sender.OwnerForm                                         
  app = form.ClientApplication
                                 
  uipSubJnsTransLRInvestasi = form.GetUIPartByName('uipSubJnsTransLRInvestasi')  
  uipSubJnsTransLRInvestasi.Edit()
  
  res = app.ExecuteScript(
   'investasi/transaksi/invutils'
   , app.CreateValues(
       ['kode', uipSubJnsTransLRInvestasi.kode_subjns_LRInvestasi]
       , ['nama_field', 'kode_subjns_LRInvestasi']                
       , ['nama_tabel', 'SubJnsTransLRInvestasi']
     )
  )
  
  rec = res.FirstRecord
  if rec.ada:
    app.ShowMessage('Security type %s sudah ada' % uipSubJnsTransLRInvestasi.kode_subjns_LRInvestasi)
    uipSubJnsTransLRInvestasi.kode_subjns_LRInvestasi = None
    sender.SetFocus()
    
def btnOKClick(sender):
  form = sender.OwnerForm        
  uipSubJnsTransLRInvestasi = form.GetUIPartByName('uipSubJnsTransLRInvestasi')

  form.CommitBuffer()
           
  uipSubJnsTransLRInvestasi.Edit()
  uipSubJnsTransLRInvestasi.__SYSFLAG = 'N'
  form.PostResult()

  sender.ExitAction = 1

