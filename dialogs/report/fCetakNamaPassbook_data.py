moduleReport = None

import sys,string,datetime,time

def importModules(config):
  homeDir = config.GetHomeDir()
  sys.path.append(homeDir + '\script_modules')
  global moduleReport
  moduleReport = __import__('moduleReport')


def getDataNasabah(config,No_Peserta):
  Rekening = config.CreatePObjImplProxy('RekeningDPLK')
  Rekening.key = No_Peserta
  
  if Rekening.isnull:
     raise "\nPERINGATAN","Rekening DPLK Tidak Ditemukan"
     
  if Rekening.has_passbook <> 'T':
     raise "\nPERINGATAN","Rekening Tidak Memiliki Layanan Passbook"
     
  if Rekening.status_dplk == 'N':
     raise "\nPERINGATAN","Rekening Sudah Non Aktif"


  # Cari objek nasabah
  oNasabah = Rekening.LNasabahDPLK

  NamaNasabah = oNasabah.Nama_Lengkap
  AlamatNasabah     = oNasabah.Alamat_Surat_Jalan
  Alamat_RTRW     = oNasabah.Alamat_Surat_RTRW
  Alamat_Kelurahan = oNasabah.Alamat_Surat_Kelurahan
  Alamat_Kecamatan = oNasabah.Alamat_Surat_Kecamatan
  Alamat_Kota = oNasabah.Alamat_Surat_Kota
  Alamat_Propinsi = oNasabah.Alamat_Surat_Propinsi
  Alamat_Kodepos = oNasabah.Alamat_Surat_Kode_Pos
  Tgl_registrasi = oNasabah.tgl_registrasi
  #Cabang = Rekening.LBranchLocation.BranchName
  Tgl_pensiun = Rekening.tgl_pensiun
  
  # Dapat euy ... data nasabah dan alamatnya
  DataNasabah = {"Nama" : NamaNasabah,\
                "Alamat" : AlamatNasabah,\
                "RTRW" : Alamat_RTRW,\
                "Kelurahan" : Alamat_Kelurahan,\
                "Kecamatan" : Alamat_Kecamatan,\
                "Kota" : Alamat_Kota,\
                "Provinsi" : Alamat_Propinsi,\
                "KodePos" : Alamat_Kodepos,\
                "Tgl_pensiun" : Tgl_pensiun, \
                "Tgl_registrasi" : Tgl_registrasi \
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
  y , m , d = time.localtime()[:3]
  Tanggal_Cetak = str(d) + " " + MONTHS_SHORT_NAME[m-1] + " " + str(y)

  y , m , d = dictIdentitasNasabah['Tgl_pensiun'][:3]
  Tgl_pensiun = str(d) + " " + MONTHS_SHORT_NAME[m-1] + " " + str(y)

  y , m , d = dictIdentitasNasabah['Tgl_registrasi'][:3]
  Tgl_registrasi = str(d) + " " + MONTHS_SHORT_NAME[m-1] + " " + str(y)

  alamat = moduleReport.penggal(dictIdentitasNasabah['Alamat'] + ' ' + dictIdentitasNasabah['RTRW'] ,30)
  if len(alamat) < 2 :
     for i in range(2-len(alamat)):
         alamat.append('')



  #MarginLeft = 37 * ' '
  #MarginTop  = 4 * '\n'

  #MarginLeft = 30 * ' '
  #MarginTop  = 8 * '\n'

  MarginLeft = 36 * ' '
  MarginTop  = 5 * '\n'


  ReportData = chr(15) + MarginTop

  #ReportData += MarginLeft + dictIdentitasNasabah['Cabang'] +'\n'
  #ReportData += MarginLeft + ' ' +'\n'
  ReportData += MarginLeft + No_Peserta +'\n'
  ReportData += MarginLeft + ' ' +'\n'
  ReportData += MarginLeft + dictIdentitasNasabah['Nama'] +'\n'
  #ReportData += MarginLeft + ' ' +'\n'
  #ReportData += MarginLeft + alamat[0] +'\n'
  ReportData += MarginLeft + dictIdentitasNasabah['Alamat'] + ' '+ dictIdentitasNasabah['RTRW'] + '\n'
  #ReportData += MarginLeft + alamat[1] +'\n'
  ReportData += MarginLeft + dictIdentitasNasabah['Kelurahan'] + ' ' + dictIdentitasNasabah['Kecamatan'] +'\n'
  ReportData += MarginLeft + dictIdentitasNasabah['Kota'] + ' ' + dictIdentitasNasabah['Provinsi'] + ' - ' + dictIdentitasNasabah['KodePos']  +'\n'

  #Print Tanggal Valid
  ReportData += MarginLeft + ' ' +'\n'

  ReportData += '                                    Masa Kepesertaan : '+ Tgl_registrasi + ' - ' + Tgl_pensiun
  
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
           ['Alamat',dictIdentitasNasabah['Alamat']],\
           ['KodePos',dictIdentitasNasabah['KodePos']])


