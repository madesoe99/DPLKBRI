def FormShow(form, parameter):
  uip = form.GetUIPartByName('uipUserInfo')
  uipTB = form.GetUIPartByName('uipTransactionBatch')
  
  #cek parameter dari form InputSingle
  if parameter.FirstRecord.nopeserta == 'InputSingle':
    #View Batch dari form Input, bukan dari daftar
    #reserved untuk keperluan masa mendatang
    pass

  #choose the right listName/table name
  if uipTB.batch_type == 'R':
    #registrasi
    tableName = 'IuranPendaftaran'
    columnString = 'tgl_transaksi,no_peserta,branch_code,besar_biaya_daftar as biaya_pendaftaran,'\
      'isCommitted$ as status_otorisasi,keterangan,ID_Transaksi,self'
  elif uipTB.batch_type == 'T':
    #transaksi DPLK
    tableName = 'TransaksiDPLK'
    columnString = 'tgl_transaksi,kode_jenis_transaksi,LJenisTransaksiDPLK.nama_transaksi,'\
    'no_peserta,branch_code,mutasi_iuran_pk as iuran_pemberi_kerja,mutasi_iuran_pst as '\
    'iuran_peserta,mutasi_pengembangan as pengembangan,mutasi_peralihan as peralihan,'\
    'isCommitted$ as status_otorisasi,keterangan,ID_Transaksi,'\
    'LTransactionBatch.batch_sub_type$ as sub_tipe_batch,self'
  elif uipTB.batch_type == 'I':
    #transaksi Investasi
    tableName = 'TransaksiInvestasi'
    columnString = 'tgl_transaksi,no_bilyet,clsfTransaksiInvestasi as kelompok_transaksi,'\
    'kode_jenis_trinvestasi as kode_jenis_transaksi,mutasi_debet,mutasi_kredit,'\
    'isCommitted$ as status_otorisasi,id_transaksiinvestasi as ID_Transaksi,self'
  else:
    #uipTB.batch_type == 'P': premi
    tableName = 'TransaksiPremi'
    columnString = 'tgl_transaksi,jenis_transaksi$,branch_code,mutasi_premi,'\
      'isDebet as debet,isCommitted$ as status_otorisasi,keterangan,ID_Transaksi,self'

  #buat OQLText sesuai user
  if uip.isTeller:
    #teller user
    sCondition = 'user_id = \'%s\' and ' % (uip.UserIDOwner)
  elif uip.isBackOffice and uipTB.batch_type != 'I':
    #bakcoffice user (kecuali untuk transaksi investasi)
    sCondition = 'branch_code = \'%s\' and ' % (uip.BranchCode)
  else:
    #maybe ROOT or ADMIN user
    sCondition = ''

  #set OQL text and show it
  query = form.GetPanelByName('qTransaksi')
  query.OQLText = 'select from %s [%s ID_TransactionBatch = %d] (%s) ' \
    'then order by tgl_transaksi;' \
    % (tableName, sCondition, uipTB.ID_TransactionBatch, columnString)
    
  query.DisplayData()
  
  #cek apakah query mempunyai data
  if not query.HasData:
    #non aktifkan bPrint
    form.GetControlByName('pButton.bPrint').Enabled = 0

def bPrintClick(bPrint):
  app = bPrint.OwnerForm.ClientApplication
  uipTB = bPrint.OwnerForm.GetUIPartByName('uipTransactionBatch')

  try:
    res = app.ExecuteScript('report/PrintTransaksiBatch',\
      app.CreateValues(['idbatch',uipTB.ID_TransactionBatch]))
    app.DownloadItem(res.FirstRecord.filename,'v')
  except:
    app = None
    raise
