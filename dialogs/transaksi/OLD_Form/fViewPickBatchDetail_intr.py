class fViewPickBatchDetail:

  def __init__(self, formObj, parentForm):
    pass
  
  def FormShow(self):
    uipTB = self.uipTransactionBatch

    #choose the right listName/table name
    if uipTB.batch_type == 'R':
      #registrasi
      tableName = 'IuranPendaftaran'
      columnString = 'tgl_transaksi,no_peserta,isCommitted$ as status_otorisasi,branch_code,'\
        'keterangan,ID_Transaksi,self'
    elif uipTB.batch_type == 'T':
      #transaksi DPLK
      tableName = 'TransaksiDPLK'
      columnString = 'tgl_transaksi,kode_jenis_transaksi,LJenisTransaksiDPLK.nama_transaksi,'\
      'no_peserta,isCommitted$ as status_otorisasi,branch_code,keterangan,ID_Transaksi,self'
    elif uipTB.batch_type == 'I':
      #transaksi Investasi
      tableName = 'TransaksiInvestasi'
      columnString = 'tgl_transaksi,no_bilyet,clsfTransaksiInvestasi as kelompok_transaksi,'\
      'kode_jenis_trinvestasi as kode_jenis_transaksi,'\
      'isCommitted$ as status_otorisasi,id_transaksiinvestasi as ID_Transaksi,self'
    else:
      #uipTB.batch_type == 'P': premi
      tableName = 'TransaksiPremi'
      columnString = 'tgl_transaksi,jenis_transaksi$,isCommitted$ as status_otorisasi,branch_code,'\
        'keterangan,ID_Transaksi,self'

    #set OQL text and show it
    query = self.qTransaksi
    query.OQLText = 'select from %s [ID_TransactionBatch = %d] (%s) ' \
      'then order by tgl_transaksi;' \
      % (tableName, uipTB.ID_TransactionBatch, columnString)

    query.DisplayData()
    rShow = self.FormContainer.Show()
