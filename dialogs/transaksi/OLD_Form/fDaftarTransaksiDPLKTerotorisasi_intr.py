def zfill(s):
  #fungsi ini untuk menambahkan satu angka 0 pada string s
  #digunakan terutama untuk representasi penanggalan bagi hari / bulan
  #prekondisi: s haruslah literal string yang hanya berisi angka
  
  if len(s) == 1:
    s = '0' + s
  #selain berjumlah karakter sama dengan satu, tidak akan diutak-atik

  return s
#-----------------------------------------------------------------------
def FormShow(form, parameter):
  uip = form.GetUIPartByName('uipUserInfo')
  uipFilter = form.GetUIPartByName('uipFilter')
  
  if uip.isBackOffice:
    #matikan lookup branch
    form.GetControlByName('pFilter.LBranch').Enabled = 0
    
def bTampilkanClick(sender):
  uip = sender.OwnerForm.GetUIPartByName('uipUserInfo')
  uipFilter = sender.OwnerForm.GetUIPartByName('uipFilter')

  awalTanggal = uipFilter.GetFieldValue('AwalTanggal')
  akhirTanggal = uipFilter.GetFieldValue('AkhirTanggal')

  #cek branch code
  if uipFilter.GetFieldValue('LBranch.branch_code') == None or \
    uipFilter.GetFieldValue('LBranch.branch_code') == '':
    sender.OwnerForm.ShowMessage('Kode dan Nama Cabang belum dipilih, mohon untuk dipilih dahulu!')
    return

  #cek rentang tanggal filter
  if (awalTanggal[:3] > akhirTanggal[:3]):
    sender.OwnerForm.ShowMessage('Rentang tanggal filter salah, mohon untuk dibetulkan dahulu.')
    return

  #Daftar transaksi DPLK biasa sudah terotorisasi
  #sementara pake nama variable yang agak aneh
  sNotAuthCondition = 'isCommitted = \'T\' and'

  if uip.isBackOffice:
    #bakcoffice user
    sCondition = 'branch_code = \'%s\' and' % (uip.BranchCode)
  else:
    #maybe ROOT or ADMIN user
    sCondition = 'branch_code = \'%s\' and' \
      % (uipFilter.GetFieldValue('LBranch.branch_code'))

  #set parameter OQL and show it
  query = sender.OwnerForm.GetPanelByName('qTransaksi')
  query.OQLText = 'select from TransaksiDPLK [%s %s ' \
    'tgl_transaksi >= :tanggal_awal and tgl_transaksi <= :tanggal_akhir] ' \
    '(tgl_transaksi as Tanggal_Transaksi, ' \
    'no_peserta as Nomor_Peserta, ' \
    'LJenisTransaksiDPLK.nama_transaksi as Kode_Jenis_Transaksi, ' \
    'branch_code as Kode_Cabang, ' \
    'isCommitted as Status_Otorisasi, ' \
    'tgl_otorisasi as Tanggal_Otorisasi, ' \
    'keterangan as Keterangan, ' \
    'LTransactionBatch.ID_TransactionBatch as idbatch, ' \
    'LTransactionBatch.no_batch as nobatch, ' \
    'ID_Transaksi,' \
    'kode_jenis_transaksi as hidden_kode_Jenis_Transaksi, ' \
    'self) then order by Tanggal_Transaksi;' % (sCondition, sNotAuthCondition)

  #setting date untuk OQL: mm/dd/yyyy
  awalTanggal = '%s/%s/%d' % (zfill(str(awalTanggal[1])), \
    zfill(str(awalTanggal[2])),awalTanggal[0])

  akhirTanggal = '%s/%s/%d' % (zfill(str(akhirTanggal[1])), \
    zfill(str(akhirTanggal[2])),akhirTanggal[0])
  
  query.SetParameter('tanggal_awal',awalTanggal)
  query.SetParameter('tanggal_akhir',akhirTanggal)
  
  query.DisplayData()
