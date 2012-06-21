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

  #cek nominal iuran pendaftaran
  if uipT.GetFieldValue('besar_biaya_daftar') == None or \
    uipT.GetFieldValue('besar_biaya_daftar') == '' or \
    uipT.GetFieldValue('besar_biaya_daftar') < uipP.PRESISI_ANGKA_FLOAT:
    sender.OwnerForm.ShowMessage('Nominal besar biaya daftar masih kosong atau 0! Mohon untuk diisi.')
    return
  elif abs(uipT.GetFieldValue('besar_biaya_daftar') - \
    uipT.GetFieldValue('DefaultIuranPendaftaran')) > uipP.PRESISI_ANGKA_FLOAT:
    sender.OwnerForm.ShowMessage('Besar biaya daftar harus sama dengan default iuran pendaftaran.')
    return

  form.CommitBuffer()
  try:
    form.PostResult()
  except:
    raise

  #clear it and exit from it
  form.ResetAndClearData()
  sender.ExitAction = 1
