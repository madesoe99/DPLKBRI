import sys, os

def DeleteTemplate(config, NamaTemplate):
  fileName = config.GetHomeDir() + 'ImportTemplates\\'+ \
    NamaTemplate.rstrip().lstrip().replace(' ','')
  try:
    #cek fileName.def dan fileName.dat
    if os.access(fileName+'.def', os.F_OK) and \
      os.access(fileName+'.dat', os.F_OK):
      #kedua file .dat dan .def bisa diakses, hapus kedua file tersebut
      os.remove(fileName+'.def')
      os.remove(fileName+'.dat')
      deleteSucceed = 1
    else:
      deleteSucceed = 0  
  except:
    raise
    
  ph = config.AppObject.CreateValues(['deleteSucceed',deleteSucceed]) 

  return ph
  
def GetTemplateList(config):
  try:  
    #ambil semua file .def yang ada di direktori ImportTemplate
    templateDir = config.GetHomeDir() + 'ImportTemplates\\'
    listOfFile = os.listdir(templateDir)
    
    #buat definisi packet untuk dikirimkan lagi ke client
    phTemplateList = config.AppObject.CreatePacket()
    rPacket = phTemplateList.Packet        
    rPacket.AddDataPacketStructureEx('__InfoTemplate', \
      'namaTemplate:string;deskripsiTemplate:string;' \
      'targetClass:string;processScript:string;processFunction:string;')
    rPacket.BuildAllStructure()

    if listOfFile != []:
      #bukan direktori kosong (ada file template terdefinisi)
      listOfFile.sort()
        
      #siapkan dataset dalam rPacket
      dsIT = rPacket.AddNewDataset('__InfoTemplate')

      #buat data packet yang akan menampung hasil serialisasi string file
      phTemplate = config.AppObject.CreatePacket()
      packet = phTemplate.Packet
      
      for fileName in listOfFile:
        #ambil struktur dan isi data packet yang tersimpan di file
        #hanya proses file .def (abaikan .dat, kecuali waktu list dir bisa filtering)
        if os.path.splitext(fileName)[1]=='.def':
          #cek dulu apakah ada pasangan filenya .dat
          defFileFullPath = templateDir + os.path.splitext(fileName)[0] + '.def'
          datFileFullPath = templateDir + os.path.splitext(fileName)[0] + '.dat'

          if os.access(datFileFullPath, os.F_OK):
            #file .dat ditemukan, isi packet dengan isi file .dat
            try:
              f = open(defFileFullPath,'r')
              sDefinition = f.read()
              f.close()
  
              f = open(datFileFullPath,'r')
              sData = f.read()
              f.close()              
            except:
              raise
            
            #masukkan string dalam packet
            packet.SetSerializationString(sDefinition,sData)
            
            #buat record baru untuk dataset __InfoTemplate dalam rPacket
            rec = dsIT.AddRecord()
            
            #ambil data yang berasal dari dataset __InfoTemplate packet
            recPacket = packet.GetDatasetByName('__InfoTemplate').GetRecord(0)
            
            rec.namaTemplate = recPacket.namaTemplate
            rec.deskripsiTemplate = recPacket.deskripsiTemplate
            rec.targetClass = recPacket.targetClass
            rec.processScript = recPacket.processScript
            rec.processFunction = recPacket.processFunction            
            #tidak perlu mengambil data deskripsiFields
            
          else:
            #file .dat tidak ditemukan, sementara abaikan proses mengisi packet
            pass
      
  except:
    raise 'GetTemplateList error', str(sys.exc_info()[1])
    
  return phTemplateList 

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  NamaFungsi = parameter.FirstRecord.NamaFungsi
  NamaTemplate = parameter.FirstRecord.NamaTemplate 

  try:
    if NamaFungsi == 'GetTemplateList':
      #ambil semua list template
      dh = GetTemplateList(config)
    elif NamaFungsi == 'DeleteTemplate':
      #hapus file template tertentu
      dh = DeleteTemplate(config, NamaTemplate)
      
    #copy struktur dan data, lalu implemen ke returnpacket
    sSerial = dh.Packet.GetSerializationString()
    returnpacket.SetSerializationString(sSerial[0], sSerial[1])

  except:
    raise

  return 1
