def FormShow(form, parameter):
  uipT = form.GetUIPartByName('uipTransaksi')
  
  #set batch transaksi
  uipT.Edit()
  uipT.SetFieldValue('LTransactionBatch.ID_TransactionBatch', \
    parameter.FirstRecord.idbatch)
  uipT.SetFieldValue('LTransactionBatch.no_batch', \
    parameter.FirstRecord.nobatch)
  form.GetControlByName('pDataTransaksi.LTransactionBatch').Enabled = 0

  #set branch code untuk transaction batch
  uipT.TB_BranchCode = parameter.FirstRecord.branchcode

  #disable tanggal transaksi, supaya diset dengan tanggal pakai batch
  uipT.tgl_transaksi = parameter.FirstRecord.tglpakai
  form.GetControlByName('pDataTransaksi.tgl_transaksi').Enabled = 0

def bSimpanClick(sender):
  form = sender.OwnerForm
  uipT = sender.OwnerForm.GetUIPartByName('uipTransaksi')
  uipP = sender.OwnerForm.GetUIPartByName('uipParameter')

  #cek nominal mutasi premi
  if uipT.mutasi_premi == None or uipT.mutasi_premi == '' or \
    uipT.mutasi_premi < uipP.PRESISI_ANGKA_FLOAT:
    form.ShowMessage('Nominal Mutasi Premi masih kosong atau 0! Mohon untuk diisi.')
    return

  form.CommitBuffer()
  try:
    form.PostResult()
  except:
    raise
    
  #clear it and exit from it
  form.ResetAndClearData()
  sender.ExitAction = 1
