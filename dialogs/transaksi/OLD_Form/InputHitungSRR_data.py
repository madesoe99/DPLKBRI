def FormGeneralSetData(uideflist, uiname, objdata):
  config = uideflist.config
  uipInput = uideflist.uipInput
  recInput = uipInput.Dataset.AddRecord()

  recInput.TanggalAkhir = recInput.TanggalHariIni = config.Now()
  
  #cek parameter BATAS_TGL_TUTUP_BATCH
  oP = config.CreatePObjImplProxy('Parameter')
  oP.Key = 'PRESISI_ANGKA_FLOAT'
  presisiFloat = oP.Numeric_Value

  oP.Key = 'BATAS_TGL_TUTUP_BATCH'
  
  if oP.Numeric_Value > presisiFloat:
    #berarti sudah pernah melakukan penghitungan SRR
    recInput.TanggalAwal = oP.Numeric_Value
  
  return 0
