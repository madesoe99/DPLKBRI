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
  uipF.StatusPosting = 'A'
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
  query = form.GetPanelByName('qBagiHasil')
  query.OQLText = 'select from BagiHasil '\
    '[(0 = :NeedStatus or status_posting = :StatusPosting) and '\
    'tgl_bagi_hasil >= :tanggal_awal '\
    'and tgl_bagi_hasil <= :tanggal_akhir] '\
    '(tgl_bagi_hasil, '\
    'kode_paket_investasi, '\
    'kode_jns_investasi, '\
    'status_posting, '\
    'keuntungan_dibagikan, '\
    'indeks, '\
    'idbghasil, '\
    'self) then order by idbghasil;'

  #setting date untuk OQL: mm/dd/yyyy
  #awalTanggal = uipFilter.GetFieldValue('AwalTanggal')
  #akhirTanggal = uipFilter.GetFieldValue('AkhirTanggal')

  awalTanggal = '%s/%s/%d' % (zfill(str(awalTanggal[1])), \
    zfill(str(awalTanggal[2])),awalTanggal[0])
  akhirTanggal = '%s/%s/%d' % (zfill(str(akhirTanggal[1])), \
    zfill(str(akhirTanggal[2])),akhirTanggal[0])

  #set parameter OQL
  if uipFilter.StatusPosting == 'A':
    #semua status bagi hasil ditampilkan
    query.SetParameter('NeedStatus',0)
  else:
    #hanya menampilkan status False atau True
    query.SetParameter('NeedStatus',1)
  
  query.SetParameter('StatusPosting',uipFilter.StatusPosting)
  query.SetParameter('tanggal_awal',awalTanggal)
  query.SetParameter('tanggal_akhir',akhirTanggal)

  query.DisplayData()

