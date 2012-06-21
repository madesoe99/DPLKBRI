import sys
sys.path.append('c:/dafapp/dplk07/scripts/kakas')

import S_ImportTemplates

def FormGeneralSetData(uideflist, uiname, objdata):
  config = uideflist.config
  dsuipTL = uideflist.uipTemplateList.Dataset

  #ambil list of template yang tersedia
  dh = S_ImportTemplates.GetTemplateList(config)

  #cek apakah dataset kosong (tidak ada template yang di-load)
  if dh.Packet.DatasetCount > 0:
    #ada dataset yang terdefinisi
    dsTemplate = dh.Packet.GetDataset(0)

    #cek apakah record dsTemplate kosong atau ada isinya
    if dsTemplate.RecordCount > 0:
      #punya record, berarti ada file template yang di-load
      for i in range(dsTemplate.RecordCount):
        recTemplate = dsTemplate.GetRecord(i)

        #masukkan data packet dalam uipTL
        rec = dsuipTL.AddRecord()

        rec.NamaTemplate = recTemplate.namaTemplate
        rec.DeskripsiTemplate = recTemplate.deskripsiTemplate
        rec.TargetImport = recTemplate.targetClass
        #tidak perlu data deskripsi field dan deskripsi proses

  return 0
