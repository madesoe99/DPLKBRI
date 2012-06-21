def zfill(s):
  #fungsi ini untuk menambahkan satu angka 0 pada string s
  #digunakan terutama untuk representasi penanggalan bagi hari / bulan
  #prekondisi: s haruslah literal string yang hanya berisi angka

  if len(s) == 1:
    s = '0' + s
  #selain berjumlah karakter sama dengan satu, tidak akan diutak-atik

  return s
#-----------------------------------------------------------------------

class qDaftarHistoriGiro:

  def __init__(self, formObj, parentForm):
    pass

  def FormShow(self):
    rShow = self.FormContainer.Show()

  def bTampilkanClick(self, sender):
    uipFilter = self.uipFilter

    awalTanggal = uipFilter.GetFieldValue('AwalTanggal')
    akhirTanggal = uipFilter.GetFieldValue('AkhirTanggal')
    #cek rentang tanggal filter
    if (awalTanggal[:3] > akhirTanggal[:3]):
      self.FormObject.ShowMessage('Rentang tanggal filter salah, mohon untuk dibetulkan dahulu.')
      return

    #set and display query
    self.SetAndDisplayQuery(uipFilter,awalTanggal,akhirTanggal)

  def SetAndDisplayQuery(self, uipFilter, awalTanggal, akhirTanggal):
    #set parameter OQL and show it
    query = self.FormObject.GetPanelByName('qHistoriGiroHarian')
    query.OQLText = 'select from HistoriGiroHarian '\
      '[Tanggal_Histori >= :tanggal_awal and Tanggal_Histori <= :tanggal_akhir]'\
      '(LMasterGiro.no_giro as Nomor_Giro_DPLK, '\
      'acc_giro as Kode_Akun_Giro, '\
      'Tanggal_Histori as Tanggal_Riwayat, '\
      'Sum_Nominal as Total_Nominal, '\
      'journal_blok_id as ID_Keterhubungan_Acc, '\
      'isReconciled$ as Status_Rekonsolidasi, '\
      'isTransactionProceed$ as Status_Pembuatan_Transaksi, '\
      'ID_HistoriGiroHarian as hidden_id, '\
      'self) then order by hidden_id;'

    #setting date untuk OQL: mm/dd/yyyy
    awalTanggal = '%s/%s/%d' % (zfill(str(awalTanggal[1])), \
      zfill(str(awalTanggal[2])),awalTanggal[0])
    akhirTanggal = '%s/%s/%d' % (zfill(str(akhirTanggal[1])), \
      zfill(str(akhirTanggal[2])),akhirTanggal[0])

    #set parameter OQL
    query.SetParameter('tanggal_awal',awalTanggal)
    query.SetParameter('tanggal_akhir',akhirTanggal)

    query.DisplayData()
