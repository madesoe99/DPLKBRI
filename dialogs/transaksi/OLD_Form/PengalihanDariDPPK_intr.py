def FormShow(form, parameter):
  uipTransaksi = form.GetUIPartByName('uipTransaksi')
  uipNasabah = form.GetUIPartByName('uipNasabah')
  uipTransaksi.Edit()
  uipNasabah.Edit()

  #set akumulasi dana dan nama paket investasi
  uipNasabah.SetFieldValue('DanaPk', \
    uipNasabah.GetFieldValue('LRekeningDPLK.akum_dana_iuran_pk'))
  uipNasabah.SetFieldValue('DanaPst', \
    uipNasabah.GetFieldValue('LRekeningDPLK.akum_dana_iuran_pst'))
  uipNasabah.SetFieldValue('DanaPengembangan', \
    uipNasabah.GetFieldValue('LRekeningDPLK.akum_dana_pengembangan'))
  uipNasabah.SetFieldValue('DanaPeralihan', \
    uipNasabah.GetFieldValue('LRekeningDPLK.akum_dana_peralihan'))
  uipNasabah.SetFieldValue('PaketInvestasi', \
    uipNasabah.GetFieldValue('LRekeningDPLK.LPaketInvestasi.nama_paket_investasi'))

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

  #checking kode dppk dan nomor DPPK lain
  if uipTransaksi.GetFieldValue('LLDP.kode_dp') in [None,''] or \
    uipTransaksi.no_dplk_lain in [None,'']:
    form.ShowMessage('Nama DPPK lain atau Nomor DPPK lain ' \
      'belum terisi, mohon diisi dahulu.')
    return

  form.CommitBuffer()
  try:
    form.PostResult()
  except:
    raise
    
  sender.ExitAction = 1
