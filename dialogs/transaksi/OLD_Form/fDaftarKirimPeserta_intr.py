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
  uipF = form.GetUIPartByName('uipFilter')
  uipF.Edit()

  #set and display query
  uipF.AwalTanggal = uipF.AkhirTanggal = form.ClientApplication.ModDateTime.Now()
  awalTanggal = uipF.GetFieldValue('AwalTanggal')
  akhirTanggal = uipF.GetFieldValue('AkhirTanggal')
  #SetAndDisplayQuery(form,uipF,awalTanggal,akhirTanggal)

def bTampilkanClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipFilter = form.GetUIPartByName('uipFilter')

  awalTanggal = uipFilter.GetFieldValue('AwalTanggal')
  akhirTanggal = uipFilter.GetFieldValue('AkhirTanggal')
  #cek rentang tanggal filter
  if (awalTanggal[:3] > akhirTanggal[:3]):
    sender.OwnerForm.ShowMessage('Rentang tanggal filter salah, mohon untuk dibetulkan dahulu.')
    return

  akhirTanggalPlus = app.ModDateTime.DecodeDate(
    app.ModDateTime.EncodeDate(
      akhirTanggal[0],akhirTanggal[1],akhirTanggal[2]
    ) + 1
  )

  #set and display query
  SetAndDisplayQuery(sender.OwnerForm,uipFilter,awalTanggal,akhirTanggalPlus)

def SetAndDisplayQuery(form, uipFilter, awalTanggal, akhirTanggal):
  #set parameter OQL and show it
  query = form.GetPanelByName('qKirimPeserta')
  query.OQLText = 'select from HistoriKirimPeserta '\
    '[Tanggal_Kirim >= :tanggal_awal and Tanggal_Kirim < :tanggal_akhir] '\
    '(Tanggal_Terdaftar, '\
    'Jumlah_Peserta, '\
    'Tanggal_Kirim, '\
    'User_ID, '\
    'ID_HistoriKirimPeserta, '\
    'self) then order by ID_HistoriKirimPeserta;'

  #setting date untuk OQL: mm/dd/yyyy
  #awalTanggal = uipFilter.GetFieldValue('AwalTanggal')
  #akhirTanggal = uipFilter.GetFieldValue('AkhirTanggal')

  awalTanggal = '%s/%s/%d' % (zfill(str(awalTanggal[1])), \
    zfill(str(awalTanggal[2])),awalTanggal[0])
  akhirTanggal = '%s/%s/%d' % (zfill(str(akhirTanggal[1])), \
    zfill(str(akhirTanggal[2])),akhirTanggal[0])

  #set parameter OQL
  query.SetParameter('tanggal_awal',awalTanggal)
  query.SetParameter('tanggal_akhir',akhirTanggal)

  query.DisplayData()

