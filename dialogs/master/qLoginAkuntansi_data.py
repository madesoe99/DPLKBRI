import sys

def FormGeneralSetData(uideflist, uiname, objdata):
  config = uideflist.Config
  uip = uideflist.uipParameter
  
  #dapetin dulu semua nama parameter
  sSQL = 'select Key_Parameter,Numeric_Value,Varchar_Value,Description from Parameter '\
    'order by Key_Parameter ASC'
  rSQL = config.CreateSQL(sSQL).RawResult
  
  rSQL.First()
  while not rSQL.Eof:
    rec = uip.Dataset.AddRecord()

    #set grid Parameter Aplikasi
    rec.Key_Parameter = rSQL.Key_Parameter
    rec.Description = rSQL.Description

    if rec.Key_Parameter == 'BATAS_TGL_TUTUP_BATCH':
      rec.Numeric_Value = rSQL.Numeric_Value
      rec.Varchar_Value = rSQL.Varchar_Value
      rec.ValueType = 0
    elif rSQL.Numeric_Value in [None,'']:
      rec.Varchar_Value = rSQL.Varchar_Value
      rec.ValueType = 1
    else:
      rec.Numeric_Value = rSQL.Numeric_Value
      rec.ValueType = 0
    
    rSQL.Next()

  return 0

def FormGeneralProcessData(uideflist, data):
  config = uideflist.Config

  try:
    uip = data.uipParameter
    for i in range(uip.RecordCount):
      if uip.GetRecord(i).__SYSFLAG == 'M':
        rec = uip.GetRecord(i)

        #debug code
        config.SendDebugMsg(rec.Key_Parameter)
        
        #simpan perubahan dalam DB
        oP = config.CreatePObjImplProxy('Parameter')
        oP.Key = rec.Key_Parameter
        if rec.ValueType == 0:
          #tipe angka
          oP.Numeric_Value = rec.Numeric_Value
        else:
          #tipe teks
          oP.Varchar_Value = rec.Varchar_Value
  except:
    raise '\nProses Error','\nPenyimpanan hasil perubahan Parameter Aplikasi gagal!'

  return 0
