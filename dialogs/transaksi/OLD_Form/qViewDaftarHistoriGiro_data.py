def FormGeneralSetDataEx(uideflist, parameter):
  config = uideflist.config
  recP = uideflist.uipParameter.Dataset.AddRecord()

  oHGH = config.CreatePObjImplProxy('HistoriGiroHarian')
  oHGH.Key = parameter.FirstRecord.keyID
  
  #simpan kode ID_HistoriGiroHarian
  recP.hidden_id = parameter.FirstRecord.keyID
  recP.no_giro = oHGH.LMasterGiro.no_giro
  recP.acc_giro = oHGH.acc_giro
  recP.sum_nominal = oHGH.Sum_Nominal

  return 0
