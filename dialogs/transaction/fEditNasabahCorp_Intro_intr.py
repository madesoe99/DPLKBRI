def btnOKClick(sender):
  form = sender.OwnerForm
  uipNoData = form.GetUIPartByName('uipNoData')
  app = form.ClientApplication
  
  classname = 'NasabahDPLKCorporate'
  keyfield = 'KODE_NASABAH_CORPORATE'
  keyvalue = uipNoData.GetFieldValue('LPesertaKorporat.kode_nasabah_corporate')
  key = 'PObj:%s#%s=%s' % (classname, keyfield, keyvalue)
  
  aform = app.GetFormWithData('transaction/fRegistrasiCorp','fRegistrasiCorp',0,key,'uipNasabahDPLKCorporate')
  ea = aform.Show(app.CreateValues(['mode','editdoc']))
  
  if ea == 1:
    # eaQuitOK
    sender.ExitAction = 1
  else:
    uipNoData.Edit()
    uipNoData.SetFieldValue('LPesertaKorporat.kode_nasabah_corporate',None)
    uipNoData.SetFieldValue('LPesertaKorporat.nama_perusahaan',None)
    
    form.GetControlByName('pData.LPesertaKorporat').SetFocus()
