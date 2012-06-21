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
    
  #set parameter pajak tarik dana
  recPTD = uideflist.uipPajakTarikDana.Dataset.AddRecord()
  recPTD.Batas1 = config.SysVarIntf.GetFloatSysVar('PAJAKTARIKDANA','Batas1')
  recPTD.Batas2 = config.SysVarIntf.GetFloatSysVar('PAJAKTARIKDANA','Batas2')
  recPTD.Batas3 = config.SysVarIntf.GetFloatSysVar('PAJAKTARIKDANA','Batas3')
  recPTD.Batas4 = config.SysVarIntf.GetFloatSysVar('PAJAKTARIKDANA','Batas4')
  recPTD.Batas5 = config.SysVarIntf.GetFloatSysVar('PAJAKTARIKDANA','Batas5')
  
  recPTD.PersenBatas1 = config.SysVarIntf.GetFloatSysVar('PAJAKTARIKDANA','PersenBatas1')
  recPTD.PersenBatas2 = config.SysVarIntf.GetFloatSysVar('PAJAKTARIKDANA','PersenBatas2')
  recPTD.PersenBatas3 = config.SysVarIntf.GetFloatSysVar('PAJAKTARIKDANA','PersenBatas3')
  recPTD.PersenBatas4 = config.SysVarIntf.GetFloatSysVar('PAJAKTARIKDANA','PersenBatas4')
  recPTD.PersenBatas5 = config.SysVarIntf.GetFloatSysVar('PAJAKTARIKDANA','PersenBatas5')

  #set parameter pajak ambil manfaat
  recPAM = uideflist.uipPajakAmbilManfaat.Dataset.AddRecord()
  recPAM.Batas1 = config.SysVarIntf.GetFloatSysVar('PAJAKAMBILMANFAAT','Batas1')
  recPAM.Batas2 = config.SysVarIntf.GetFloatSysVar('PAJAKAMBILMANFAAT','Batas2')
  recPAM.Batas3 = config.SysVarIntf.GetFloatSysVar('PAJAKAMBILMANFAAT','Batas3')
  recPAM.Batas4 = config.SysVarIntf.GetFloatSysVar('PAJAKAMBILMANFAAT','Batas4')
  recPAM.Batas5 = config.SysVarIntf.GetFloatSysVar('PAJAKAMBILMANFAAT','Batas5')

  recPAM.PersenBatas1 = config.SysVarIntf.GetFloatSysVar('PAJAKAMBILMANFAAT','PersenBatas1')
  recPAM.PersenBatas2 = config.SysVarIntf.GetFloatSysVar('PAJAKAMBILMANFAAT','PersenBatas2')
  recPAM.PersenBatas3 = config.SysVarIntf.GetFloatSysVar('PAJAKAMBILMANFAAT','PersenBatas3')
  recPAM.PersenBatas4 = config.SysVarIntf.GetFloatSysVar('PAJAKAMBILMANFAAT','PersenBatas4')
  recPAM.PersenBatas5 = config.SysVarIntf.GetFloatSysVar('PAJAKAMBILMANFAAT','PersenBatas5')

  #set parameter timezone
  recTZ = uideflist.uipTimeZone.Dataset.AddRecord()
  recTZ.isTimeZoneUsed = config.SysVarIntf.GetStringSysVar('TIMEZONE','UseTimeZone')
  recTZ.TimeZoneServer = config.SysVarIntf.GetStringSysVar('TIMEZONE','TimeZoneServer')
  recTZ.SelisihMenitBaratTengah = config.SysVarIntf.GetIntSysVar('TIMEZONE','SelisihMenitBaratTengah')
  recTZ.SelisihMenitBaratTimur = config.SysVarIntf.GetIntSysVar('TIMEZONE','SelisihMenitBaratTimur')
  recTZ.SelisihMenitTengahTimur = config.SysVarIntf.GetIntSysVar('TIMEZONE','SelisihMenitTengahTimur')
  recTZ.AwalJamKerja = config.SysVarIntf.GetIntSysVar('TIMEZONE','AwalJamKerja')
  recTZ.AwalMenitKerja = config.SysVarIntf.GetIntSysVar('TIMEZONE','AwalMenitKerja')
  recTZ.AkhirJamKerja = config.SysVarIntf.GetIntSysVar('TIMEZONE','AkhirJamKerja')
  recTZ.AkhirMenitKerja = config.SysVarIntf.GetIntSysVar('TIMEZONE','AkhirMenitKerja')
  
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
          
    #simpan parameter pajak penarikan dana
    recPTD = data.uipPajakTarikDana.GetRecord(0)
    config.SysVarIntf.SetFloatSysVar('PAJAKTARIKDANA','Batas1',recPTD.Batas1)
    config.SysVarIntf.SetFloatSysVar('PAJAKTARIKDANA','Batas2',recPTD.Batas2)
    config.SysVarIntf.SetFloatSysVar('PAJAKTARIKDANA','Batas3',recPTD.Batas3)
    config.SysVarIntf.SetFloatSysVar('PAJAKTARIKDANA','Batas4',recPTD.Batas4)
    config.SysVarIntf.SetFloatSysVar('PAJAKTARIKDANA','Batas5',recPTD.Batas5)

    config.SysVarIntf.SetFloatSysVar('PAJAKTARIKDANA','PersenBatas1',recPTD.PersenBatas1)
    config.SysVarIntf.SetFloatSysVar('PAJAKTARIKDANA','PersenBatas2',recPTD.PersenBatas2)
    config.SysVarIntf.SetFloatSysVar('PAJAKTARIKDANA','PersenBatas3',recPTD.PersenBatas3)
    config.SysVarIntf.SetFloatSysVar('PAJAKTARIKDANA','PersenBatas4',recPTD.PersenBatas4)
    config.SysVarIntf.SetFloatSysVar('PAJAKTARIKDANA','PersenBatas5',recPTD.PersenBatas5)

    #simpan parameter pajak pengambilan manfaat
    recPAM = data.uipPajakAmbilManfaat.GetRecord(0)
    config.SysVarIntf.SetFloatSysVar('PAJAKAMBILMANFAAT','Batas1',recPAM.Batas1)
    config.SysVarIntf.SetFloatSysVar('PAJAKAMBILMANFAAT','Batas2',recPAM.Batas2)
    config.SysVarIntf.SetFloatSysVar('PAJAKAMBILMANFAAT','Batas3',recPAM.Batas3)
    config.SysVarIntf.SetFloatSysVar('PAJAKAMBILMANFAAT','Batas4',recPAM.Batas4)
    config.SysVarIntf.SetFloatSysVar('PAJAKAMBILMANFAAT','Batas5',recPAM.Batas5)

    config.SysVarIntf.SetFloatSysVar('PAJAKAMBILMANFAAT','PersenBatas1',recPAM.PersenBatas1)
    config.SysVarIntf.SetFloatSysVar('PAJAKAMBILMANFAAT','PersenBatas2',recPAM.PersenBatas2)
    config.SysVarIntf.SetFloatSysVar('PAJAKAMBILMANFAAT','PersenBatas3',recPAM.PersenBatas3)
    config.SysVarIntf.SetFloatSysVar('PAJAKAMBILMANFAAT','PersenBatas4',recPAM.PersenBatas4)
    config.SysVarIntf.SetFloatSysVar('PAJAKAMBILMANFAAT','PersenBatas5',recPAM.PersenBatas5)

    #simpan parameter timezone
    recTZ = data.uipTimeZone.GetRecord(0)
    config.SysVarIntf.SetStringSysVar('TIMEZONE','UseTimeZone',recTZ.isTimeZoneUsed)
    config.SysVarIntf.SetStringSysVar('TIMEZONE','TimeZoneServer',recTZ.TimeZoneServer)

    config.SysVarIntf.SetIntSysVar('TIMEZONE','SelisihMenitBaratTengah',recTZ.SelisihMenitBaratTengah)
    config.SysVarIntf.SetIntSysVar('TIMEZONE','SelisihMenitBaratTimur',recTZ.SelisihMenitBaratTimur)
    config.SysVarIntf.SetIntSysVar('TIMEZONE','SelisihMenitTengahTimur',recTZ.SelisihMenitTengahTimur)

    config.SysVarIntf.SetIntSysVar('TIMEZONE','AwalJamKerja',recTZ.AwalJamKerja)
    config.SysVarIntf.SetIntSysVar('TIMEZONE','AwalMenitKerja',recTZ.AwalMenitKerja)
    config.SysVarIntf.SetIntSysVar('TIMEZONE','AkhirJamKerja',recTZ.AkhirJamKerja)
    config.SysVarIntf.SetIntSysVar('TIMEZONE','AkhirMenitKerja',recTZ.AkhirMenitKerja)

  except:
    raise '\nProses Error','Penyimpanan hasil perubahan Parameter Aplikasi gagal!'

  return 0
