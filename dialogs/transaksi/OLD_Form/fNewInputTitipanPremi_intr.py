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
  uipN = sender.OwnerForm.GetUIPartByName('uipNasabah')
  uipRWU = sender.OwnerForm.GetUIPartByName('uipRekeningWU')
  uipP = sender.OwnerForm.GetUIPartByName('uipParameter')

  #cek kolektibilitas premi
  if uipN.KolektibilitasPremi == 'F':
    #pembayaran premi tidak lancar (masih ada hutang premi)
    if uipT.mutasi_premi in [None,''] or \
      uipT.mutasi_premi < uipP.PRESISI_ANGKA_FLOAT:
      form.ShowMessage('Nominal Mutasi Premi masih kosong atau 0! Mohon sekaligus juga '\
        'lunasi Kewajiban Premi yang belum terbayar sebesar Rp %0.2f.' % (uipN.KewajibanWasiatUmmat))
      return
    else:
      #cek nominal iuran premi dengan iuran premi seharusnya
      if uipT.mutasi_premi < (uipRWU.besar_premi + uipN.KewajibanWasiatUmmat):
        #nominal iuran peserta harus >= iuran peserta seharusnya
        sender.OwnerForm.ShowMessage('Nominal Mutasi Premi harus sama atau lebih besar dari '\
          'Besar Premi plus Kewajiban Premi yang belum terbayarkan!')
        return
  else:
    #pembayaran premi lancar
    if uipT.mutasi_premi in [None,''] or \
      uipT.mutasi_premi < uipP.PRESISI_ANGKA_FLOAT:
      form.ShowMessage('Nominal Mutasi Premi masih kosong atau 0! Mohon untuk diisi.')
      return
    else:
      #cek nominal iuran premi dengan iuran premi seharusnya
      if uipT.mutasi_premi < uipRWU.besar_premi:
        #nominal iuran peserta harus >= iuran peserta seharusnya
        sender.OwnerForm.ShowMessage('Nominal Mutasi Premi harus sama atau lebih besar dari Besar Premi!')
        return

  form.CommitBuffer()
  try:
    form.PostResult()
  except:
    raise
    
  #clear it and exit from it
  form.ResetAndClearData()
  sender.ExitAction = 1
