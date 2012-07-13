import sys

def FormGeneralSetData(uideflist, uiname, objdata):
  config = uideflist.Config
  uip = uideflist.uipGLInterface
  
  #dapetin dulu semua nama parameter
  sSQL = 'select * from GLInterface order by account_code ASC'
  rSQL = config.CreateSQL(sSQL).RawResult
  
  rSQL.First()
  while not rSQL.Eof:
    rec = uip.Dataset.AddRecord()

    #set grid Parameter Aplikasi
    rec.intf_code = rSQL.intf_code
    rec.description = rSQL.description
    rec.account_code = rSQL.account_code
    rec.user_id = rSQL.user_id
    rec.last_update = config.ModLibUtils.EncodeDate(rSQL.last_update[0],\
      rSQL.last_update[1],rSQL.last_update[2])

    rSQL.Next()

  return 0

def FormGeneralProcessData(uideflist, data):
  config = uideflist.Config

  try:
    uip = data.uipGLInterface
    for i in range(uip.RecordCount):
      if uip.GetRecord(i).__SYSFLAG in ['M','N']:
        rec = uip.GetRecord(i)

        if uip.GetRecord(i).__SYSFLAG == 'M':
          #modify existing record
          o = config.CreatePObjImplProxy('GLInterface')
          o.Key = rec.intf_code
        elif uip.GetRecord(i).__SYSFLAG == 'N':
          #create new record
          o = config.CreatePObject('GLInterface')
          o.intf_code = rec.intf_code

        #simpan perubahan field lain dalam DB
        o.description = rec.description
        o.account_code = rec.account_code
        o.user_id = config.SecurityContext.InitUser
        o.last_update = config.ModLibUtils.Now()
  except:
    raise Exception, '\nProses Error' + 'Penyimpanan hasil perubahan Parameter Akuntansi gagal!'

  return 0
