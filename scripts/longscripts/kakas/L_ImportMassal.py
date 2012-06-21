import com.ihsan.lib.bulkdatareader as reader
import com.ihsan.utils as utils
import com.ihsan.lib.trace as trace
import pyFlexcel
import sys, time, string

def LoadTemplateFile(config, fileName):
  fileName = config.GetHomeDir() + 'ImportTemplates\\'+ fileName
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
  
def LoadUploadFile(config, filename):
  try:
    #get file yang telah di-upload ke server 
    sfile = config.UserHomeDirectory + utils.ExtractFileName(filename)
    
    #open it
    workbook = pyFlexcel.Open(sfile)
    
    #cek eksistensi worksheet
    if not workbook.IsWorksheetExist('DataImpor'):
        raise '','Worksheet DataImpor tidak ditemukan! \
          \nWorksheet tempat data akan diimpor harus bernama DataImpor.'
    
    #activing worksheet
    workbook.ActivateWorksheet('DataImpor')    
  except:
    raise

  return workbook
  
def LoadDeskripsiField(config, dsDeskripsiField):
  dict = {}
  try:
    for i in range(dsDeskripsiField.RecordCount):
      recDF = dsDeskripsiField.GetRecord(i)
      dict[recDF.namaField] = [recDF.tipeField, recDF.lookupField]  
  except:
    raise

  return dict

def checkingField(config, dictDeskripsiField, workBookXLS):
  
  try:
    #load nama kolom dan posisi kolom workBookXLS dalam dictionary
    i = 1
    dictKolomField = {}
    namaKolom = workBookXLS.GetCellValue(1, i)
    while (namaKolom != None) and (str(namaKolom).strip().replace(' ','') != ''):
      #add nama kolom dalam dictionary sebagai key, urutan kolom sebagai value
      dictKolomField[i] = str(namaKolom)
      
      #inkremen
      i += 1
      namaKolom = workBookXLS.GetCellValue(1, i)
    #end while
  
    #proses checking nama kolom dengan nama field pada template
    fieldNotInColumn = []
    for key in dictDeskripsiField.keys():
      if key not in dictKolomField.values():
        #masukkan field template yang tidak terdapat di kolom workBookXLS
        fieldNotInColumn.append(key)
        
    if fieldNotInColumn != []:
      #terdapat field template yang tidak terdefinisi dalam kolom workBookXLS
      raise '','Kolom/field data berikut tidak ditemukan pada file upload:\n' + \
        str(fieldNotInColumn)
  except:
    raise

  return dictKolomField

def GetRow(config, workBookXLS, row, jumlahKolom, dictDeskripsiField, dictKolomField):
  currentRowValue = []

  #cek sel(row,1) kosong atau tidak
  if workBookXLS.GetCellValue(row, 1) != None and \
    str(workBookXLS.GetCellValue(row, 1)).strip() != '':
    #bukan sel yang kosong
    for j in range(jumlahKolom):
      #cek tipe value dalam kolom / cell tersebut (dimulai dari kolom 1)
      tipeKolom = dictDeskripsiField[dictKolomField[j+1]][0]
      
      #disesuaikan dengan 4 predefined tipe default 
      if tipeKolom == 'string':
        valueKolom = str(workBookXLS.GetCellValue(row,j+1))
      elif tipeKolom == 'integer':
        valueKolom = int(workBookXLS.GetCellValue(row,j+1))
      elif tipeKolom == 'float':
        valueKolom = float(workBookXLS.GetCellValue(row,j+1))
      elif tipeKolom == 'datetime':
        #format tanggal yang valid: DD/MM/YYYY, separator default '/'
        #tanggal dikonversi menjadi tuple 
        d,m,y = str(workBookXLS.GetCellValue(row,j+1)).split('/')
        valueKolom = [int(y),int(m),int(d),0,0,0,0,0,0]
      else:
        raise '','Tipe %s tidak terdefinisi sebagai tipe kolom field!' % (tipeKolom)
        
      #value dalam tuple terurut kolom (berdasarkan index)
      currentRowValue.append(valueKolom)

  return currentRowValue

def Main(config, uploadFileName, templateFile):

  app = config.AppObject
  #baca konfigurasi file template
  dh = LoadTemplateFile(config, templateFile) 
  recInfoTemplate = dh.Packet.GetDatasetByName('__InfoTemplate').GetRecord(0)
  dsDeskripsiField = dh.Packet.GetDatasetByName('__DeskripsiField')
  
  #load dataset deskripsi field template ke dalam bentuk dictionary
  #format: 'NamaField:[TipeField,LookupField]'
  dictDeskripsiField = LoadDeskripsiField(config,dsDeskripsiField)
  
  #load worksheet yang akan diimpor pada file .xls yang telah di-upload
  workBookXLS = LoadUploadFile(config, uploadFileName)
  
  #cocokkan field file template dengan kolom yang ada di file .xls
  #format: 'NomorKolom (mulai angka 1):NamaKolom'
  dictKolomField = checkingField(config, dictDeskripsiField, workBookXLS)
  
  #persiapkan progress tracker
#   pt = config.ProgressTracker
#   pt.ProgressLevel1()
#   pt.SetProgressInfo2(1, 'Mulai memproses data...')
  
  config.BeginTransaction()
  try:
    #baca file .xls berisi data yang akan diimpor (semua checking telah dilewati)
    #ambil 1 row (ASUMSI mulai dari row 2, row 1 untuk nama kolom)
    jumlahKolom = len(dictKolomField)
    i = 2
    
    #kasus elemen pertama
    currentRowValue = GetRow(config, workBookXLS, i, jumlahKolom, \
      dictDeskripsiField, dictKolomField)
    
    while currentRowValue != []:
      #currentRowValue tidak kosong
      
      #PROSESI IMPOR DATA
      
      #inkremen
      i += 1
      currentRowValue = GetRow(config, workBookXLS, i, jumlahKolom, \
        dictDeskripsiField, dictKolomField)
      if i % 10 == 0 : 
        app.ConWriteln('baris ke %d terproses' % i,'status')
    #end while
    
    config.Commit()
  except:
    config.Rollback()
    raise
  
  return 1

def DAFLongScriptMain(config, parameter, pid, monfilename):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # pid: Process ID of this script
  # monfilename: Monitor file name to store status

  app = config.AppObject
  uploadFileName = parameter.FirstRecord.uploadFileName
  templateFile = parameter.FirstRecord.templateFile

  consoleID = 'ImportMassal_' + str(pid)
  sJobName = 'Impor Data Massal. TaskID = %s' % (pid)
  #app.WriteConsole(sJobName + ': mulai berlangsung\r\n')
  
  #fileLog = open(config.GetHomeDir()[:-1]+'trackedtasks/'+consoleID,'w')
  app.ConWriteln(sJobName + ': mulai berlangsung', monfilename)
  try:
    #app.CreateConsole(consoleID, 'progress')
    try:
      #app.SwitchDefaultConsole(consoleID)      
            
      #main task right here
      Main(config, uploadFileName, templateFile)

      #app.WriteConsole(sJobName + ': telah selesai\r\n')
      app.ConWriteln(sJobName + ': telah selesai',monfilename)
    finally:
      #app.CloseConsole(consoleID)
      pass#fileLog.close()
  except:
    #app.WriteConsole(sJobName + ': Error\r\n' + str(sys.exc_info()[1]) + '\r\n')
    app.ConWriteln(sJobName + 'Error\r\n'+ + str(sys.exc_info()[1]) + '\r\n', monfilename)
    raise
    
  return 0
