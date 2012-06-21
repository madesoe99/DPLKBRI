def mnuCetakIsiBatchClick(sender, context):
  app = context.OwnerForm.ClientApplication

  try:
    idBatch = context.GetFieldValue('TransactionBatch.hidden_idbatch')

    res = app.ExecuteScript('report/PrintTransaksiBatch',\
      app.CreateValues(['idbatch',idBatch]))
    app.DownloadItem(res.FirstRecord.filename,'v')
    
  finally:
    app = None

  return 1

def mnuBukaBatchClick(sender, context):
  app = context.OwnerForm.ClientApplication

  #cek status batch terlebih dahulu
  if context.GetFieldValue('TransactionBatch.Status_Batch') == 'Buka':
    app.ShowMessage('Batch Transaksi masih terbuka! Pembukaan hanya berlaku untuk Batch yang sudah berstatus Tutup.')
    return
    
  #cek parameter batas tanggal tutup batch
  uipP = context.OwnerForm.GetUIPartByName('uipParameter')
  if uipP.BATAS_TGL_TUTUP_BATCH >= uipP.PRESISI_ANGKA_FLOAT:
    #parameter BATAS_TGL_TUTUP_BATCH ada isinya, cek batas tanggalnya
    y1,m1,d1 = context.GetFieldValue('TransactionBatch.Tanggal_Pakai')[:3]
    tglPakaiBatch = app.ModDateTime.EncodeDate(y1,m1,d1)
    
    if tglPakaiBatch <= uipP.BATAS_TGL_TUTUP_BATCH:
      y,m,d = app.ModDateTime.DecodeDate(uipP.BATAS_TGL_TUTUP_BATCH)
      app.ShowMessage('PERINGATAN!\n\nBatch Transaksi dengan tanggal pakai '\
        'sebelum tanggal %d-%d-%d\nTIDAK DIPERKENANKAN untuk dibuka kembali.' % (d,m,y))
      return

  try:
    batch_no = context.GetFieldValue('TransactionBatch.Nomor_Batch')
    hidden_idbatch = context.GetFieldValue('TransactionBatch.hidden_idbatch')
    
    if app.ConfirmDialog('Apakah Anda yakin akan membuka kembali Batch Transaksi bernomor %s?' % (batch_no)):
      #status Batch jadikan 'closed'
      dh = app.ExecuteScript('transaksi/OpenClosedBatch', \
        app.CreateValues(['idbatch',hidden_idbatch]))

      if dh.FirstRecord.status:
        context.SetFieldValue('TransactionBatch.Status_Batch', 'Buka')
        app.ShowMessage('Batch Transaksi nomor %s berhasil dibuka kembali.' % (batch_no))
  finally:
    app = None

  return 1
  
def mnuTutupBatchClick(sender, context):
  app = context.OwnerForm.ClientApplication

  #cek status batch terlebih dahulu
  if context.GetFieldValue('TransactionBatch.Status_Batch') == 'Tutup':
    app.ShowMessage('Batch Transaksi telah ditutup! Penutupan hanya berlaku untuk Batch yang masih berstatus Buka.')
    return

  try:
    batch_no = context.GetFieldValue('TransactionBatch.Nomor_Batch')
    hidden_idbatch = context.GetFieldValue('TransactionBatch.hidden_idbatch')

    if app.ConfirmDialog('Apakah Anda yakin akan menutup Batch Transaksi bernomor %s?' % (batch_no)):
      #status Batch jadikan 'closed'
      dh = app.ExecuteScript('transaksi/CloseAllOpenBatch', \
        app.CreateValues(['idbatch',hidden_idbatch],['tglpakai','']))

      if not dh.FirstRecord.status:
        #status bernilai 0, semua transaksi sudah terotorisasi
        context.SetFieldValue('TransactionBatch.Status_Batch', 'Tutup')
        app.ShowMessage('Batch nomor %s berhasil ditutup.' % (batch_no))
      else:
        #status bernilai != 0, masih ada transaksi belum terotorisasi
        jenisBatch = context.GetFieldValue('TransactionBatch.Tipe_Batch')
        if jenisBatch == 'Premi':
          nama_transaksi = 'Transaksi Premi '
        elif jenisBatch == 'Transaction':
          nama_transaksi = 'Transaksi DPLK '
        elif jenisBatch == 'Registration':
          nama_transaksi = 'Iuran Pendaftaran '
        elif jenisBatch == 'Investment':
          nama_transaksi = 'Transaksi Investasi '

        app.ShowMessage('PERINGATAN!\n\nMasih ada %d transaksi dalam Batch ' \
          'nomor %s yang belum terotorisasi. Silahkan lihat dalam Daftar %s Belum ' \
          'Terotorisasi.' % (dh.FirstRecord.status,batch_no,nama_transaksi))
        
  finally:
    app = None

  return 1

#event click umum---------------------------------------------------------------

#aturan NumberTag
# 0 mode new: untuk new manual batch, new spesific batch
# 1 mode view: untuk Lihat detil batch

#konvesnsi
def mnuShowModal(sender, context):
  app = context.OwnerForm.ClientApplication
  
  form_id = sender.Name
  group_id = sender.StringTag
  form = app.FindForm(form_id)
  if form == None:
    form = app.GetForm(group_id+'/'+form_id, form_id, 0)

  form.Show(app.CreateValues(['code',sender.NumberTag]))

def mnuShowModalWithData(sender, context):
  app = context.OwnerForm.ClientApplication
  ShowDataPacket = app.CreateValues(['code',sender.NumberTag])
  
  if sender.NumberTag == 0:
    #mode New
    key = 'x'
    uipName = 'x'
  elif sender.NumberTag == 1:
    #mode View
    key = context.KeyObjConst
    uipName = 'uipTransactionBatch'
    ShowDataPacket = app.CreateValues(['nopeserta','kosong'], \
      ['nobatch',context.GetFieldValue('TransactionBatch.Nomor_Batch')])

  form_id = sender.Name
  group_id = sender.StringTag
  form = app.GetFormWithData(group_id+'/'+form_id, form_id, 0, key, uipName)

  form.Show(ShowDataPacket)

