import time, string

def FormGeneralSetData(uideflist, uiname, objdata):
  config = uideflist.config
  uipPI = uideflist.uipPaketInvestasi

  #ambil info semua Paket Investasi yang terdaftar
  sOQL = 'select from RincianPaketInvestasi '\
    '[LPaketInvestasi.isAktif = \'T\']'\
    '(kode_paket_investasi,'\
    'LPaketInvestasi.nama_paket_investasi, '\
    'LJenisInvestasi.kode_jns_investasi,'\
    'LJenisInvestasi.nama_jns_investasi,'\
    'maks_proporsi,self)'\
    'then order by kode_paket_investasi;'

  iOQL = config.OQLEngine.CreateOQL(sOQL)
  iOQL.Active = 1
  rOQL = iOQL.RawResult

  rOQL.First()
  while not rOQL.Eof:
    recPI = uipPI.Dataset.AddRecord()
    recPI.kode_paket_investasi = rOQL.kode_paket_investasi
    recPI.nama_paket_investasi = rOQL.nama_paket_investasi
    recPI.kode_jns_investasi = rOQL.kode_jns_investasi
    recPI.nama_jns_investasi = rOQL.nama_jns_investasi
    recPI.maks_proporsi = rOQL.maks_proporsi
    recPI.NominalProfit = 0.0

    rOQL.Next()
    
  #set parameter
  recInput = uideflist.uipInput.Dataset.AddRecord()

  oP = config.CreatePObjImplProxy('Parameter')
  oP.Key = 'PRESISI_ANGKA_FLOAT'
  recInput.PRESISI_ANGKA_FLOAT = oP.Numeric_Value
  
  today = time.localtime()[:3]
  recInput.Today = '%s/%s/%d' % (string.zfill(str(today[1]),2), \
    string.zfill(str(today[2]),2),today[0])
  
  return 0
