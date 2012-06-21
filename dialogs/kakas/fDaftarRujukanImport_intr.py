def FormShow(form, parameter):
  uipTL = form.GetUIPartByName('uipTemplateList')
  uipTL.First()

def btnRefreshClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipTL = form.GetUIPartByName('uipTemplateList')
  
  try:
    dh = app.ExecuteScript('kakas/S_ImportTemplates',\
      app.CreateValues(['NamaFungsi','GetTemplateList'],['NamaTemplate','']))

    #cek apakah dataset kosong (tidak ada template yang terdefinisi)
    if dh.Packet.DatasetCount > 0:
      #ada dataset yang terdefinisi
      dsTemplate = dh.Packet.GetDataset(0)

      #cek apakah record dsTemplate kosong atau ada isinya
      if dsTemplate.RecordCount > 0:
        #punya record, berarti ada file template yang di-load

        uipTL.ClearData()
        for i in range(dsTemplate.RecordCount):
          rec = dsTemplate.GetRecord(i)
          
          uipTL.Append()
          uipTL.NamaTemplate = rec.namaTemplate
          uipTL.DeskripsiTemplate = rec.deskripsiTemplate
          uipTL.TargetImport = rec.targetClass
          uipTL.Post()

        uipTL.First()
    else:
      form.ShowMessage('Tidak ada Rujukan (Template) untuk impor data massal yang terdefinisi.')

  finally:
    form = app = None
