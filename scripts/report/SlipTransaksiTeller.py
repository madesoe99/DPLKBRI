import sys, time, os, string

def ConstructReportHeader(config, oT, oFile, idRNR):
  #tentukan judul slip
  if oT.ClassNameIs('IuranPeserta'):
    judulSlip = 'Iuran Peserta dan Titipan Premi'
  elif oT.ClassNameIs('IuranPendaftaran'):
    judulSlip = 'Biaya Pendaftaran'
  elif oT.ClassNameIs('TitipanPremi'):
    judulSlip = 'Titipan Premi'
  
  #cek apakah untuk kasus Pendaftaran awal atau Iuran Pertama
  if idRNR != 0:
    #load register nasabah rekening
    oN = config.CreatePObjImplProxy('RegisterNasabahRekening')
    oN.Key = idRNR
  else:    
    #load data nasabah
    oN = oT.LRekeningDPLK.LNasabahDPLK 
    
  #write file
  oFile.write('DPLK Bank Rakyat Indonesia')
  oFile.write('\nLembar Slip Transaksi %s' % (judulSlip))
  oFile.write('\n========================================================================')
  oFile.write('\n')
  oFile.write('\nNomor peserta     : %s' % (oN.no_peserta))
  oFile.write('\nNama lengkap      : %s' % (oN.nama_lengkap))
  oFile.write('\nTanggal transaksi : %s' % ('%s-%s-%d' % ( \
    string.zfill(str(oT.tgl_transaksi[2]),2),\
    string.zfill(str(oT.tgl_transaksi[1]),2),oT.tgl_transaksi[0])))
  oFile.write('\n')

def ConstructReportDetails(config, oT, oFile):
  #tentukan jenis transaksi dan write file
  if oT.ClassNameIs('IuranPeserta'):
    #iuran peserta    
    oFile.write('\nIuran peserta     : Rp %20s' % (config.FormatFloat(',0.00',oT.mutasi_iuran_pst)))
    #cek apakah peserta wasiat ummat
    if oT.ID_BatchPremi not in [None,0]:
      #batch premi tidak kosong, termasuk peserta wasiat ummat     
      oFile.write('\nTitipan premi     : Rp %20s' % (config.FormatFloat(',0.00',oT.titipan_premi)))
      oFile.write('\n------------------------------------------------------------------------')
      oFile.write('\nJumlah            : Rp %20s' % (config.FormatFloat(',0.00',oT.mutasi_iuran_pst+oT.titipan_premi)))
    else:
      #bukan peserta wasiat ummat
      oFile.write('\n------------------------------------------------------------------------')
      oFile.write('\nJumlah            : Rp %20s' % (config.FormatFloat(',0.00',oT.mutasi_iuran_pst)))
  elif oT.ClassNameIs('IuranPendaftaran'):
    #iuran pendaftaran
    oFile.write('\nBiaya pendaftaran : Rp %20s' % (config.FormatFloat(',0.00',oT.besar_biaya_daftar)))
    oFile.write('\n------------------------------------------------------------------------')
    oFile.write('\nJumlah            : Rp %20s' % (config.FormatFloat(',0.00',oT.besar_biaya_daftar)))
  elif oT.ClassNameIs('TitipanPremi'):
    #titipan premi
    oFile.write('\nTitipan premi     : Rp %20s' % (config.FormatFloat(',0.00',oT.mutasi_premi)))
    oFile.write('\n------------------------------------------------------------------------')
    oFile.write('\nJumlah            : Rp %20s' % (config.FormatFloat(',0.00',oT.mutasi_premi)))
    
def ConstructReportFooter(config, oT, oFile):
  entriDate = '%s-%s-%d' % (string.zfill(str(oT.tgl_sistem[2]),2), \
    string.zfill(str(oT.tgl_sistem[1]),2),oT.tgl_sistem[0])
  entriTime = '%s:%s:%s' % (string.zfill(str(oT.tgl_sistem[3]),2),\
    string.zfill(str(oT.tgl_sistem[4]),2),\
    string.zfill(str(oT.tgl_sistem[5]),2))
  nowDate = '%s-%s-%d' % (string.zfill(str(time.localtime()[2]),2),\
    string.zfill(str(time.localtime()[1]),2),time.localtime()[0])
  nowTime = '%s:%s:%s' % (string.zfill(str(time.localtime()[3]),2),\
    string.zfill(str(time.localtime()[4]),2),\
    string.zfill(str(time.localtime()[5]),2))

  oU = config.CreatePObjImplProxy('UserApp')
  oU.Key = oT.user_id
  
  #write file
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('\n            Teller')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('\n         %s' \
    % (oU.UserName))
  oFile.write('\n')
  oFile.write('\n----------')
  oFile.write('\nTanggal input data      : %s %s' % (entriDate, entriTime))
  oFile.write('\nTanggal pembuatan slip  : %s %s' % (nowDate, nowTime))
  oFile.write('\nUser pembuat slip       : %s' % (config.SecurityContext.GetUserInfo()[1]))

def ConstructReport(config, oT, oFile, idRNR):
  #persipaan semua data yang akan dicetak
  entriDate = '%s/%s/%d' % (string.zfill(str(oT.tgl_sistem[2]),2), \
    string.zfill(str(oT.tgl_sistem[1]),2),oT.tgl_sistem[0])
  entriTime = '%s:%s:%s' % (string.zfill(str(oT.tgl_sistem[3]),2),\
    string.zfill(str(oT.tgl_sistem[4]),2),\
    string.zfill(str(oT.tgl_sistem[5]),2))
  
  oU = config.CreatePObjImplProxy('UserApp')
  oU.Key = oT.user_id
  
  #get Nomor Core Banking
  oCBB = config.CreatePObjImplProxy('CoreBankingBatch')
  oCBB.SetKey('User_ID',oT.user_id)
  oCBB.SetKey('Tanggal',oT.tgl_sistem[2])
  oCBB.SetKey('Bulan',oT.tgl_sistem[1])
  oCBB.SetKey('Tahun',oT.tgl_sistem[0])
  
  #ambil objek nasabah, cek apakah untuk kasus Pendaftaran awal atau Iuran Pertama
  if idRNR != 0:
    #load register nasabah rekening
    oN = config.CreatePObjImplProxy('RegisterNasabahRekening')
    oN.Key = idRNR
    oPaketInvestasi = oN.LPaketInvestasi
  else:    
    #load data nasabah
    oN = oT.LRekeningDPLK.LNasabahDPLK
    oPaketInvestasi = oT.LRekeningDPLK.LPaketInvestasi 

  #ambil nomor rekening giro yang dipake (giro paket, premi dan pendaftaran)
  giroPremi = config.SysVarIntf.GetStringSysVar('GIROCOREBANKING', 'GiroPremi')
  giroPendaftaran = config.SysVarIntf.GetStringSysVar('GIROCOREBANKING', 'GiroPendaftaran')
  #ita ubah
  #giroPaket = oPaketInvestasi.no_giro
  giroPaket = config.SysVarIntf.GetStringSysVar('GIROCOREBANKING', 'GiroPenampungan')
  
  #tentukan jenis transaksi
  if oT.ClassNameIs('IuranPeserta'):
    #iuran peserta, ambil nomor giro paket
    oFile.write('%s(giro paket %s)-iuran peserta-IDR-%20s' % (giroPaket,\
      oPaketInvestasi.kode_paket_investasi,config.FormatFloat(',0.00',oT.mutasi_iuran_pst)))
    oFile.write('\n%s %s' % (oN.no_peserta,oN.nama_lengkap))
    
    #cek apakah peserta wasiat ummat
    if oT.ID_BatchPremi not in [None,0]:
      #batch premi tidak kosong, termasuk peserta wasiat ummat: ambil nomor giro premi      
      oFile.write('\n%s(giro premi)-titipan premi-IDR-%20s' % (giroPremi,\
        config.FormatFloat(',0.00',oT.titipan_premi)))
      oFile.write('\n%s %s' % (oN.no_peserta,oN.nama_lengkap))
      
    #cek pindah buku
    if oT.isPindahBuku == 'T':
      oFile.write('\npindah buku %s' % (oT.Rekening_Pindah_Buku))
    
  elif oT.ClassNameIs('IuranPendaftaran'):
    #iuran pendaftaran, ambil giro pendaftaran    
    oFile.write('%s(giro pendaftaran)-biaya pendaftaran-IDR-%20s' % (giroPendaftaran,\
      config.FormatFloat(',0.00',oT.besar_biaya_daftar)))
    oFile.write('\n%s %s' % (oN.no_peserta,oN.nama_lengkap))
  elif oT.ClassNameIs('TitipanPremi'):
    #titipan premi, ambil giro premi    
    oFile.write('%s(giro premi)-titipan premi-IDR-%20s' % (giroPremi,\
      config.FormatFloat(',0.00',oT.mutasi_premi)))
    oFile.write('\n%s %s' % (oN.no_peserta,oN.nama_lengkap))
  
    #cek pindah buku
    if oT.isPindahBuku == 'T':
      oFile.write('\npindah buku %s' % (oT.Rekening_Pindah_Buku))

  #write the end info
  oFile.write('\n%s(%s)-%s-%s' % (oCBB.No_Batch,oU.UserName,entriDate,entriTime))
  
def CreateSlip(config, classTransaksi, idTransaksi, idRNR):
  #idRNR = parameter untuk menandakan untuk pendaftaran awal dan iuran pertama 
  o = config.CreatePObjImplProxy(classTransaksi)
  o.Key = idTransaksi
  
  nowTime = '%s.%s.%s' % (string.zfill(str(time.localtime()[3]),2),\
    string.zfill(str(time.localtime()[4]),2),\
    string.zfill(str(time.localtime()[5]),2))
  tgltransaksi = '%d-%d-%d' % (o.tgl_transaksi[2],o.tgl_transaksi[1],o.tgl_transaksi[0])
  sBaseFileName = 'SlipTeller_%s_%s_%s_%s.txt' % (classTransaksi, tgltransaksi, \
    o.no_peserta, nowTime)
  sFileName = config.UserHomeDirectory + sBaseFileName
  oFile = open(sFileName, 'w')

  #ConstructReportHeader(config, o, oFile, idRNR)
  #ConstructReportDetails(config, o, oFile)
  #ConstructReportFooter(config, o, oFile)
  
  ConstructReport(config, o, oFile, idRNR)
  
  oFile.close()
  
  #set file read-only
  os.chmod(sFileName,333)

  return sBaseFileName

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  classTransaksi = parameter.FirstRecord.classtransaksi
  idTransaksi = parameter.FirstRecord.idtransaksi
  idRNR = parameter.FirstRecord.idRegisterNasabahRekening
  #bila idRNR != 0, berarti untuk kasus Pendaftaran Awal dan Iuran Pertama 

  sBaseFileName = CreateSlip(config, classTransaksi, idTransaksi, idRNR)
  
  #return packet
  recRes = returnpacket.CreateDataPacketStructure('filename:string')
  recRes.filename = sBaseFileName

  return 1
