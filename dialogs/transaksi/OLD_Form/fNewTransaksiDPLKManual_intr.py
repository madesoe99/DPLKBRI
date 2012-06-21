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

  #cek value mutasi
  #if uipT.GetFieldValue('mutasi_iuran_pst') < uipP.PRESISI_ANGKA_FLOAT and \
  #  uipT.GetFieldValue('mutasi_iuran_pk') < uipP.PRESISI_ANGKA_FLOAT and \
  #  uipT.GetFieldValue('mutasi_pengembangan') < uipP.PRESISI_ANGKA_FLOAT and \
  #  uipT.GetFieldValue('mutasi_peralihan') < uipP.PRESISI_ANGKA_FLOAT:
  #  sender.OwnerForm.ShowMessage('Nilai mutasi masih nol semua! Mohon isi mutasi yang diinginkan.')
  #  return

  form.CommitBuffer()
  try:
    form.PostResult()
  except:
    raise

  #clear it and exit from it
  form.ResetAndClearData()
  sender.ExitAction = 1
