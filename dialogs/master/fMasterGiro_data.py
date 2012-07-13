import sys

def FormGeneralSetData(uideflist, uiname, objdata):
  config = uideflist.Config
  uip = uideflist.uipMasterGiro
  
  #dapetin dulu semua nama parameter
  sSQL = 'select * from MasterGiro order by acc_giro ASC'
  rSQL = config.CreateSQL(sSQL).RawResult
  
  rSQL.First()
  while not rSQL.Eof:
    rec = uip.Dataset.AddRecord()

    #set grid Parameter Aplikasi
    rec.acc_giro = rSQL.acc_giro
    rec.no_giro = rSQL.no_giro
    rec.acc_histori_giro = rSQL.acc_histori_giro

    rSQL.Next()

  return 0

#kode ini sudah tidak dipakai, tidak dihapus untuk reserve code
def FormGeneralProcessData(uideflist, data):
  config = uideflist.Config

  try:
    uip = data.uipMasterGiro
    for i in range(uip.RecordCount):
      if uip.GetRecord(i).__SYSFLAG in ['M','N']:
        rec = uip.GetRecord(i)

        if uip.GetRecord(i).__SYSFLAG == 'M':
          #modify existing record
          o = config.CreatePObjImplProxy('MasterGiro')
          o.Key = rec.acc_giro
        elif uip.GetRecord(i).__SYSFLAG == 'N':
          #create new record
          o = config.CreatePObject('MasterGiro')
          o.acc_giro = rec.acc_giro

        #simpan perubahan field lain dalam DB
        o.no_giro = rec.no_giro
        o.acc_histori_giro = rec.acc_histori_giro
  except:
    raise Exception, '\nProses Error' + '\nPenyimpanan hasil perubahan Master Giro gagal!'

  return 0
