def FormShow(form, parameter):
  uipTransaksi = form.GetUIPartByName('uipTransaksi')
  uipNasabah = form.GetUIPartByName('uipNasabah')
  uipTransaksi.Edit()
  uipNasabah.Edit()

  #set batch transaksi
  uipTransaksi.SetFieldValue('LTransactionBatch.ID_TransactionBatch', \
    parameter.FirstRecord.idbatch)
  uipTransaksi.SetFieldValue('LTransactionBatch.no_batch', \
    parameter.FirstRecord.nobatch)
  form.GetControlByName('pTransaksi.LTransactionBatch').Enabled = 0

  #set branch code untuk transaction batch
  uipTransaksi.TB_BranchCode = parameter.FirstRecord.branchcode
  form.GetControlByName('pTransaksi.TB_BranchCode').Enabled = 0

  #disable tanggal transaksi, supaya diset dengan tanggal pakai batch
  uipTransaksi.tgl_transaksi = parameter.FirstRecord.tglpakai
  form.GetControlByName('pTransaksi.tgl_transaksi').Enabled = 0

def bSimpanClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipTransaksi = form.GetUIPartByName('uipTransaksi')

  #checking kode dplk dan nomor DPLK lain
  if uipTransaksi.GetFieldValue('LLDP.kode_dp') in [None,''] or \
    uipTransaksi.no_dplk_lain in [None,'']:
    form.ShowMessage('Kode DPLK lain atau Nomor DPLK lain ' \
      'belum terisi, mohon diisi dahulu.')
    return

  form.CommitBuffer()
  try:
    form.PostResult()
  except:
    raise
    
  sender.ExitAction = 1
