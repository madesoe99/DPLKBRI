moduleReport = None

import sys,string,datetime,time

def importModules(config):
  homeDir = config.GetHomeDir()
  sys.path.append(homeDir + '\script_modules')
  global moduleReport
  moduleReport = __import__('moduleReport')


def strSQLWasiatUmmatId(config, No_Peserta):
  return \
    'select REKENINGWASIATUMMAT_ID '\
    'from REKENINGWASIATUMMAT '\
    'where NO_PESERTA = \'%s\' '\
     %( No_Peserta )

def getDataNasabah(config,No_Peserta):
  Rekening = config.CreatePObjImplProxy('RekeningDPLK')
  Rekening.key = No_Peserta

  strSQLId = strSQLWasiatUmmatId(config, No_Peserta)

  resSQLId = config.CreateSQL(strSQLId).RawResult
  resSQLId.First()

  RekeningWU = config.CreatePObjImplProxy('RekeningWasiatUmmat')
  RekeningWU.key = resSQLId.rekeningwasiatummat_id

  if Rekening.isnull:
     raise Exception, "\nPERINGATAN" + "Rekening DPLK Tidak Ditemukan"
     
  if Rekening.has_passbook <> 'T':
     raise Exception, "\nPERINGATAN" + "Rekening Tidak Memiliki Layanan Passbook"

  # Cari objek nasabah
  oNasabah = Rekening.LNasabahDPLK

  NamaNasabah       = oNasabah.Nama_Lengkap
  y, m, d           = oNasabah.tanggal_lahir[:3]
  TglLahir          = '%s/%s/%s'% (str(d).zfill(2), str(m).zfill(2), str(y))
  NomorPolis        = RekeningWU.no_polis
  y, m, d           = RekeningWU.tgl_akseptasi[:3]
  TglMulaiAkseptasi = '%s/%s/%s'% (str(d).zfill(2), str(m).zfill(2), str(y))
  y, m ,d           = RekeningWU.tgl_akseptasi[:3]
  TglMulaiPerjanjian= '%s/%s/%s'% (str(d).zfill(2), str(m).zfill(2), str(y))
  y, m ,d           = RekeningWU.tgl_berakhir[:3]
  TglAkhirPerjanjian= '%s/%s/%s'% (str(d).zfill(2), str(m).zfill(2), str(y))
  SetoranPerbulan   = config.FormatFloat('#,##0.00',Rekening.iuran_pst)
  ManfaatTakaful    = config.FormatFloat('#,##0.00',RekeningWU.manfaat_asuransi)
  PremiPerbulan     = config.FormatFloat('#,##0.00',RekeningWU.besar_premi)

  # Dapat euy ... data nasabah dan detail asuransi
  
  DataNasabah = {"Nama" : NamaNasabah,\
                 "TglLahir" : TglLahir,\
                 "NomorPolis" : NomorPolis,\
                 "TglMulaiAkseptasi" : TglMulaiAkseptasi,\
                 "TglMulaiPerjanjian" : TglMulaiPerjanjian,\
                 "TglAkhirPerjanjian" : TglAkhirPerjanjian,\
                 "SetoranPerbulan" : SetoranPerbulan,\
                 "ManfaatTakaful" : ManfaatTakaful,
                 "PremiPerbulan" : PremiPerbulan \
                }
                
  return DataNasabah


def ConstructReport(config,No_Peserta):
  # --- Fungsi untuk mennyusun report nama nasabah untuk passbook
  # --- ReturnValue = string
  # --- FORMAT ini digunakan jika Print menggunakan PRFILE

  MONTHS_SHORT_NAME = ('Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agt', 'Sept', 'Okt', 'Nov', 'Des')

  
  # Run Function getDataNasabah
  dictIdentitasNasabah = getDataNasabah(config,No_Peserta)
  
  # Start Construct Report
  #y , m , d = time.localtime()[:3]
  #Tanggal_Cetak = str(d) + " " + MONTHS_SHORT_NAME[m-1] + " " + str(y)
  #alamat = moduleReport.penggal(dictIdentitasNasabah['Alamat'] + ' ' + dictIdentitasNasabah['RTRW'] ,30)
  #if len(alamat) < 2 :
  #   for i in range(2-len(alamat)):
   #      alamat.append('')


  ### Original
  #MarginLeft  = 30 * ' '
  #MarginLeft1 = 50 * ' '
  #MarginTop   = 10 * '\n'

  #ReportData = chr(15) + MarginTop

  #ReportData += MarginLeft + dictIdentitasNasabah['NomorPolis'] +'\n'
  #ReportData += MarginLeft + '\n'
  #ReportData += MarginLeft1 + No_Peserta +'\n'
  #ReportData += MarginLeft + '\n'
  #ReportData += MarginLeft + '\n'
  #ReportData += MarginLeft + No_Peserta +'\n'
  #ReportData += MarginLeft + dictIdentitasNasabah['Nama'] +'\n'
  #ReportData += MarginLeft + No_Peserta +'\n'
  #ReportData += MarginLeft + '\n'
  #ReportData += MarginLeft + dictIdentitasNasabah['TglLahir'] +'\n'
  #ReportData += MarginLeft + dictIdentitasNasabah['TglMulaiAkseptasi'] +'\n'
  #ReportData += MarginLeft + dictIdentitasNasabah['TglMulaiPerjanjian'] +'\n'
  #ReportData += MarginLeft + dictIdentitasNasabah['TglAkhirPerjanjian'] +'\n'
  #ReportData += MarginLeft + No_Peserta +'\n'
  #ReportData += MarginLeft + dictIdentitasNasabah['SetoranPerbulan'] +'\n'
  #ReportData += MarginLeft + dictIdentitasNasabah['ManfaatTakaful'] +'\n'
  #ReportData += MarginLeft + dictIdentitasNasabah['PremiPerbulan'] +'\n'

  #Print Tanggal Cetak
  #ReportData += 16 * '\n'
  #ReportData += 45 * ' ' + Tanggal_Cetak

  #################
  
  MarginLeft  = 60 * ' '
  MarginLeft1 = 105 * ' '
  MarginTop   = 9 * '\n'

  ReportData = chr(15) + MarginTop

  #ReportData += MarginLeft + dictIdentitasNasabah['NomorPolis'] +'\n'
  ReportData += MarginLeft + '\n'
  ReportData += MarginLeft1 + No_Peserta +'\n'
  #ReportData += MarginLeft + '\n'
  #ReportData += MarginLeft + '\n'
  ReportData += MarginLeft + '\n'
  #ReportData += MarginLeft + '\n'
  #ReportData += MarginLeft + '\n'
  #ReportData += MarginLeft + '\n'
  ReportData += MarginLeft + '\n'
  ReportData += MarginLeft + No_Peserta +'\n'
  ReportData += MarginLeft + dictIdentitasNasabah['Nama'] +'\n'
  #ReportData += MarginLeft + '\n'
  ReportData += MarginLeft + No_Peserta +'\n'
  #ReportData += MarginLeft + '\n'
  ReportData += MarginLeft + dictIdentitasNasabah['TglLahir'] +'\n'
  #ReportData += MarginLeft + '\n'
  ReportData += MarginLeft + dictIdentitasNasabah['TglMulaiAkseptasi'] +'\n'
  ReportData += MarginLeft + dictIdentitasNasabah['TglMulaiPerjanjian'] +'\n'
  ReportData += MarginLeft + dictIdentitasNasabah['TglAkhirPerjanjian'] +'\n'
  #ReportData += MarginLeft + '\n'
  ReportData += MarginLeft + No_Peserta +'\n'
  ReportData += MarginLeft + dictIdentitasNasabah['SetoranPerbulan'] +'\n'
  ReportData += MarginLeft + dictIdentitasNasabah['ManfaatTakaful'] +'\n'
  ReportData += MarginLeft + dictIdentitasNasabah['PremiPerbulan'] +'\n'

  #Print Tanggal Cetak
  ReportData += 16 * '\n'
  #ReportData += 45 * ' ' + Tanggal_Cetak


  return ReportData


def CetakNamaPassbook(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  importModules(config)
  param = parameter.FirstRecord
  
  sBaseFileName = 'NamaPassbook.txt'

  sFileName = config.UserHomeDirectory + sBaseFileName

  oFile = open(sFileName,'w')

  # Construct ReportData
  oFile.write(ConstructReport(config,param.No_Peserta))
  oFile.close()

  sw = returnpacket.AddStreamWrapper()
  sw.LoadFromFile(sFileName)
  sw.MIMEType = config.AppObject.GetMIMETypeFromExtension(sFileName)

  return 1


def LookUpDataNasabah(config,parameter,returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)
    
  # Run Function getDataNasabah
  dictIdentitasNasabah = getDataNasabah(config,parameter.FirstRecord.No_Peserta)
  
  recRes = returnpacket.CreateValues(['Nama',dictIdentitasNasabah['Nama']],\
           ['TglLahir',dictIdentitasNasabah['TglLahir']],\
           ['NomorPolis',dictIdentitasNasabah['NomorPolis']],\
           ['TglMulaiAkseptasi',dictIdentitasNasabah['TglMulaiAkseptasi']],\
           ['TglMulaiPerjanjian',dictIdentitasNasabah['TglMulaiPerjanjian']],\
           ['TglAkhirPerjanjian',dictIdentitasNasabah['TglAkhirPerjanjian']],\
           ['SetoranPerbulan',dictIdentitasNasabah['SetoranPerbulan']],\
           ['ManfaatTakaful',dictIdentitasNasabah['ManfaatTakaful']],\
           ['PremiPerbulan',dictIdentitasNasabah['PremiPerbulan']])


