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
  uipF.StatusBagiHasil = 'A'
  uipF.AwalTanggal = uipF.AkhirTanggal = form.ClientApplication.ModDateTime.Now()
  awalTanggal = uipF.GetFieldValue('AwalTanggal')
  akhirTanggal = uipF.GetFieldValue('AkhirTanggal')
  #SetAndDisplayQuery(form,uipF,awalTanggal,akhirTanggal)

def bTampilkanClick(sender):
  uipFilter = sender.OwnerForm.GetUIPartByName('uipFilter')

  awalTanggal = uipFilter.GetFieldValue('AwalTanggal')
  akhirTanggal = uipFilter.GetFieldValue('AkhirTanggal')
  #cek rentang tanggal filter
  if (awalTanggal[:3] > akhirTanggal[:3]):
    sender.OwnerForm.ShowMessage('Rentang tanggal filter salah, mohon untuk dibetulkan dahulu.')
    return

  #set and display query
  SetAndDisplayQuery(sender.OwnerForm,uipFilter,awalTanggal,akhirTanggal)

def SetAndDisplayQuery(form, uipFilter, awalTanggal, akhirTanggal):
  #set parameter OQL and show it
  query = form.GetPanelByName('qSRRCalc')
  query.OQLText = 'select from SRRCalc '\
    '[(0 = :NeedStatus or status_bagihasil = :StatusBagiHasil) and '\
    'tgl_create >= :tanggal_awal and tgl_create <= :tanggal_akhir] '\
    '(tgl_mulai_hitung, '\
    'tgl_akhir_hitung, '\
    'status_bagihasil$, '\
    'user_id_create, '\
    'tgl_create, '\
    'ID_SRRCalc, '\
    'self) then order by ID_SRRCalc;'

  #setting date untuk OQL: mm/dd/yyyy
  #awalTanggal = uipFilter.GetFieldValue('AwalTanggal')
  #akhirTanggal = uipFilter.GetFieldValue('AkhirTanggal')

  awalTanggal = '%s/%s/%d' % (zfill(str(awalTanggal[1])), \
    zfill(str(awalTanggal[2])),awalTanggal[0])
  akhirTanggal = '%s/%s/%d' % (zfill(str(akhirTanggal[1])), \
    zfill(str(akhirTanggal[2])),akhirTanggal[0])

  #set parameter OQL
  if uipFilter.StatusBagiHasil == 'A':
    #semua status bagi hasil ditampilkan
    query.SetParameter('NeedStatus',0)
  else:
    #hanya menampilkan status False atau True
    query.SetParameter('NeedStatus',1)
  
  query.SetParameter('StatusBagiHasil',uipFilter.StatusBagiHasil)
  query.SetParameter('tanggal_awal',awalTanggal)
  query.SetParameter('tanggal_akhir',akhirTanggal)

  query.DisplayData()

