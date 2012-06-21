def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  id = parameter.FirstRecord.id

  oSRRCalc = config.CreatePObjImplProxy('SRRCalc')
  oSRRCalc.Key = id

  config.BeginTransaction()
  try:
    #delete terlebih dahulu Ls_HistoriSRR yang ada di SRRCalcRincian
    lsSRRCalcRincian = oSRRCalc.Ls_SRRCalcRincian 
    lsSRRCalcRincian.First()
    while not lsSRRCalcRincian.EndOfList:
      oSRRCalcRincian = lsSRRCalcRincian.CurrentElement
      oSRRCalcRincian.Ls_HistoriSRR.DeleteAllPObjs()
      
      lsSRRCalcRincian.Next()
    
    oSRRCalc.Ls_SRRCalcRincian.DeleteAllPObjs()
    oSRRCalc.Delete()

    config.Commit()
  except:
    config.Rollback()
    raise

  return 1
