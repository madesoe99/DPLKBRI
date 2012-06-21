def mnuShowModalWithData(sender, context):
  app = context.OwnerForm.ClientApplication
  form_id = sender.Name
  group_id = sender.StringTag
  form = app.GetFormWithData(group_id+'/'+form_id, form_id, 0, \
    context.KeyObjConst, 'uipSRRCalc')

  form.Show(app.CreateValues(['code',sender.NumberTag]))

def mnuHapusClick(sender, context):
  app = context.OwnerForm.ClientApplication
  
  #cek status bagi hasil SRR
  if context.GetFieldValue('SRRCalc.status_bagihasil') in ['true','T']:
    app.ShowMessage('PERINGATAN!\n\nSaldo Rata-rata yang sudah dibagihasilkan'\
      '\n(Status Bagi Hasil True) tidak boleh dihapus.')
    return
  
  try:
    dlg = app.ConfirmDialog('Anda yakin akan menghapus data hasil perhitungan SRR ini?')
    if dlg:
      idSRRCalc = context.GetFieldValue('SRRCalc.ID_SRRCalc')
      app.ExecuteScript('transaksi/DeleteSRRCalc',app.CreateValues(['id',idSRRCalc]))
      context.DeleteRow()
  finally:
    app = None

  return 1
