import sys, os

def UpdateDataTemplateFile(config, fileName, dataString):
  try:
    #cek filename.dat
    if os.access(fileName+'.dat', os.F_OK):
      f = open(fileName+'.dat','w')
      f.write(dataString)
      f.close()

  except:
    raise '\nUpdate Data File Template Error', str(sys.exc_info()[1])

  return 1

def SaveTemplateFile(config, fileName, definitionString, dataString):
  try:
    #cek kemungkinan nama file sama (cukup file .def saja)
    if not os.access(fileName+'.def', os.F_OK):
      #file tidak ada yang sama, buat file .def
      f = open(fileName+'.def','w+')
      f.write(definitionString)
      f.close()

      if not os.access(fileName+'.dat', os.F_OK):
        #buat file .dat
        f = open(fileName+'.dat','w+')
        f.write(dataString)
        f.close()
      else:
        raise '','File %s.dat terduplikasi!' % (fileName)
    else:
      #file ada, akan terjadi duplikasi
      raise '','Nama file template tidak boleh sama!'

  except:
    raise '\nPenyimpanan File Template Error', str(sys.exc_info()[1])

  return 1

def LoadTemplateFile(config, fileName):
  try:
    #cek fileName.def dan fileName.dat
    if os.access(fileName+'.def', os.F_OK) and \
      os.access(fileName+'.dat', os.F_OK):
      #kedua file .dat dan .def bisa diakses, masukkan dalam packet
      f = open(fileName+'.def','r')
      sDefinition = f.read()
      f.close()

      f = open(fileName+'.dat','r')
      sData = f.read()
      f.close()

      #masukkan string dalam packet
      ph = config.AppObject.CreatePacket()
      packet = ph.Packet
      packet.SetSerializationString(sDefinition,sData)
    else:
      raise '','Salah satu file template %s (.def atau .dat) tidak ditemukan!'

  except:
    raise '\nLoading File Template Error', str(sys.exc_info()[1])

  return ph

def FormGeneralSetDataEx(uideflist, parameter):
  config = uideflist.config
  
  #load informasi template dari file
  fileName = config.GetHomeDir() + 'ImportTemplates\\'+ \
    parameter.FirstRecord.namaTemplate.rstrip().lstrip().replace(' ','')
  dh = LoadTemplateFile(config, fileName)
  
  #isikan dataset InfoTemplate dalam uipTemplate
  recIT = dh.Packet.GetDatasetByName('__InfoTemplate').GetRecord(0)
  
  recT = uideflist.uipTemplate.Dataset.AddRecord()
  recT.NamaTemplate = recIT.namaTemplate
  recT.DeskripsiTemplate = recIT.deskripsiTemplate
  recT.TargetImport = recIT.targetClass
  recT.ScriptProses = recIT.processScript
  recT.FungsiProses = recIT.processFunction
  
  #isikan dataset DeskripsiField dalam uipDeskripsiField
  dsDF = dh.Packet.GetDatasetByName('__DeskripsiField')
  for i in range(dsDF.RecordCount):
    recDF = dsDF.GetRecord(i)
    
    recGrid = uideflist.uipDeskripsiField.Dataset.AddRecord()
    recGrid.NamaField = recDF.namaField
    recGrid.TipeField = recDF.tipeField
    recGrid.LookupClass = recDF.lookupClass
    recGrid.LookupField = recDF.lookupField

  return 0
  
def FormGeneralProcessData(uideflist, data):
  config = uideflist.Config
  recT = data.uipTemplate.GetRecord(0)

  try:
    fileName = config.GetHomeDir() + 'ImportTemplates\\'+ \
      recT.NamaTemplate.rstrip().lstrip().replace(' ','')
    if recT.mode == 'new':
      uipDF = data.uipDeskripsiField

      #mode New, bikin paket baru
      ph = config.AppObject.CreatePacket()
      packet = ph.Packet
      
      packet.AddDataPacketStructureEx('__DeskripsiField', \
        'namaField:string;tipeField:string;lookupClass:string;lookupField:string;')
      packet.AddDataPacketStructureEx('__InfoTemplate', \
        'namaTemplate:string;deskripsiTemplate:string;' \
        'targetClass:string;processScript:string;processFunction:string;')
      packet.BuildAllStructure()
      
      #packet diisi dengan data dari form
      dsIT = packet.AddNewDataset('__InfoTemplate')
      recIT = dsIT.AddRecord()
      recIT.namaTemplate = recT.NamaTemplate.rstrip().lstrip()
      recIT.deskripsiTemplate = recT.DeskripsiTemplate
      recIT.targetClass = recT.TargetImport
      recIT.processScript = recT.ScriptProses
      recIT.processFunction = recT.FungsiProses
      
      #looping grid untuk isi dataset __DeskripsiField
      dsDF = packet.AddNewDataset('__DeskripsiField')
      for i in range(uipDF.RecordCount):
        rec = uipDF.GetRecord(i)
        
        recDF = dsDF.AddRecord()
        recDF.namaField = rec.NamaField
        recDF.tipeField = rec.TipeField
        recDF.lookupClass = rec.LookupClass
        recDF.lookupField = rec.LookupField
        
      #serialisasi paket dan simpan packet dalam file
      sSerialPaket = packet.GetSerializationString()
      
      #nama file packet menggunakan nama template
      SaveTemplateFile(config, fileName, sSerialPaket[0], sSerialPaket[1])

    elif recT.mode == 'edit':
      #mode edit, cek flag isGridEdited
      if recT.__SYSFLAG == 'M' or recT.isGridEdited:
        uipDF = data.uipDeskripsiField
        
        #template diedit, load paket (struktur dan paket) dari file
        dh = LoadTemplateFile(config, fileName)

        #cek apakah InfoTemplate yang dimodifikasi
        if recT.__SYSFLAG == 'M':
          #ada yang berubah, langsung timpa semuanya saja
          recIT = dh.Packet.GetDatasetByName('__InfoTemplate').GetRecord(0)
          recIT.namaTemplate = recT.NamaTemplate.rstrip().lstrip()
          recIT.deskripsiTemplate = recT.DeskripsiTemplate
          recIT.targetClass = recT.TargetImport
          recIT.processScript = recT.ScriptProses
          recIT.processFunction = recT.FungsiProses

        #cek apakah ada DeskripsiField yang berubah
        #paling mudah hapus dataset DeskripsiField lama, buatkan yang baru
        dh.Packet.DeleteDataset('__DeskripsiField')
        dsDF = dh.Packet.AddNewDataset('__DeskripsiField')
        
        for i in range(uipDF.RecordCount):
          rec = uipDF.GetRecord(i)

          recDF = dsDF.AddRecord()
          recDF.namaField = rec.NamaField
          recDF.tipeField = rec.TipeField
          recDF.lookupClass = rec.LookupClass
          recDF.lookupField = rec.LookupField

        #serialisasi paket dan simpan packet dalam file
        sSerialPaket = dh.Packet.GetSerializationString()

        #update file .dat
        UpdateDataTemplateFile(config, fileName, sSerialPaket[1])

  except:
    raise '\nProses Error', str(sys.exc_info()[1])

  return 0
