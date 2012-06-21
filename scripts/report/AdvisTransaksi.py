import sys, time, os, string

def ConstructReportHeader(config, oT, oFile):

  flagPen = 0
  oPar =  config.CreatePObjImplProxy('Parameter')
  #tentukan judul advis
  if oT.kode_jenis_transaksi == 'V':
    judulAdvis = 'Penarikan Dana Normal 30%'
  elif oT.kode_jenis_transaksi == 'W':
    judulAdvis = 'Penarikan Dana PHK'
  elif oT.kode_jenis_transaksi == 'J':
    if oT.kode_jns_manfaat == 'B':
      judulRinci = ' Normal'
    elif oT.kode_jns_manfaat == 'D':
      judulRinci = ' Dipercepat'
      oPar.key = 'PSN_CM_ALIH_<1TH'
      bParameter = oPar.numeric_value
      flagPen = 1
      
    elif oT.kode_jns_manfaat == 'C':
      judulRinci = ' Cacat'
    elif oT.kode_jns_manfaat == 'J':
      judulRinci = ' Janda / Anak'
    judulAdvis = 'Pengambilan Manfaat Pensiun' + judulRinci
  elif oT.kode_jenis_transaksi == 'H':
    judulAdvis = 'Pengalihan Ke DPLK Lain'
  elif oT.kode_jenis_transaksi == 'X' and oT.isPindahPaket == 'T':
    judulAdvis = 'Biaya Transaksi Pindah Paket Investasi'
  
  #load data nasabah
  oN = config.CreatePObjImplProxy('NasabahDPLK')
  oN.Key = oT.no_peserta

  #write file
  oFile.write('DPLK Bank Rakyat Indonesia')
  oFile.write('\nLembar Advis %s' % (judulAdvis))
  oFile.write('\n========================================================================')
  oFile.write('\n')
  oFile.write('\nNomor peserta        : %s' % (oN.no_peserta))
  oFile.write('\nNama lengkap         : %s' % (oN.nama_lengkap))
  oFile.write('\nTanggal lahir        : %s' % ('%s-%s-%d' % ( \
    string.zfill(str(oN.tanggal_lahir[2]),2),\
    string.zfill(str(oN.tanggal_lahir[1]),2),oN.tanggal_lahir[0])))
  oFile.write('\nTanggal transaksi    : %s' % ('%s-%s-%d' % ( \
    string.zfill(str(oT.tgl_transaksi[2]),2),\
    string.zfill(str(oT.tgl_transaksi[1]),2),oT.tgl_transaksi[0])))
  oFile.write('\nKode Paket Investasi : %s' % (oT.kode_paket_investasi))
  if oT.kode_jenis_transaksi == 'X' and oT.isPindahPaket == 'T':
    oFile.write('\n')
    oFile.write('\nPaket Investasi lama     : %s' % (oT.kode_paket_investasi))
    oFile.write('\nPaket Investasi saat ini : %s' % (oN.LRekeningDPLK.kode_paket_investasi))

  if flagPen == 1:
    if oT.saldo_peralihan_1th > 0:
       oFile.write('\nBiaya                : %s' % (config.FormatFloat(',0.0',oPar.numeric_value)))
       oFile.write('%')
  oFile.write('\n')

def ConstructReportDetails(config, oT, oFile):
  #tentukan jenis transaksi dan write file
  config.SendDebugMsg('advdet1')
  if oT.kode_jenis_transaksi == 'V':
    #penarikan dana 30%
    oP = config.CreatePObjImplProxy('RekeningDPLK')
    oP.Key = oT.no_peserta

    config.SendDebugMsg('advdet2')
    oFile.write('\nSaldo iuran awal  : Rp %20s' % (config.FormatFloat(',0.00',(oT.saldo_iuran_awal or 0.0))))
    oFile.write('\nSaldo pengembangan: Rp %20s' % (config.FormatFloat(',0.00',(oP.akum_dana_pengembangan or 0.0))))
    oFile.write('\nNominal penarikan : Rp %20s' % (config.FormatFloat(',0.00',(oT.jml_tarik or 0.0))))
    oFile.write('\nBiaya penarikan   : Rp %20s' % (config.FormatFloat(',0.00',(oT.biaya_tarik or 0.0))))
    oFile.write('\nPajak             : Rp %20s' % (config.FormatFloat(',0.00',(oT.pajak or 0.0))))
    oFile.write('\nBiaya lain        : Rp %20s' % (config.FormatFloat(',0.00',(oT.biaya_lain or 0.0))))
    oFile.write('\n------------------------------------------------------------------------')
    oFile.write('\nDana diterima     : Rp %20s' % (config.FormatFloat(',0.00',(oT.dana_diterima or 0.0))))
    oFile.write('\nSaldo iuran akhir : Rp %20s' % (config.FormatFloat(',0.00',(oT.saldo_iuran_akhir or 0.0))))
    config.SendDebugMsg('advdet3')    
  elif oT.kode_jenis_transaksi == 'W':
    #penarikan dana PHK
    oFile.write('\nSaldo iuran awal  : Rp %20s' % (config.FormatFloat(',0.00',oT.saldo_iuran_awal)))
    oFile.write('\nNominal penarikan : Rp %20s' % (config.FormatFloat(',0.00',oT.jml_tarik)))
    oFile.write('\nBiaya penarikan   : Rp %20s' % (config.FormatFloat(',0.00',oT.biaya_tarik)))
    oFile.write('\nPajak             : Rp %20s' % (config.FormatFloat(',0.00',oT.pajak)))
    oFile.write('\nBiaya lain        : Rp %20s' % (config.FormatFloat(',0.00',oT.biaya_lain)))
    oFile.write('\n------------------------------------------------------------------------')
    oFile.write('\nDana diterima     : Rp %20s' % (config.FormatFloat(',0.00',oT.dana_diterima)))
    oFile.write('\nSaldo iuran akhir : Rp %20s' % (config.FormatFloat(',0.00',oT.saldo_iuran_akhir)))
  elif oT.kode_jenis_transaksi == 'J':
    #pengambilan manfaat pensiun
    oFile.write('\nSaldo iuran pemberi kerja : Rp %20s' % (config.FormatFloat(',0.00',oT.saldo_iuran_pk)))
    oFile.write('\nSaldo iuran peserta       : Rp %20s' % (config.FormatFloat(',0.00',oT.saldo_iuran_pst)))
    oFile.write('\nSaldo pengembangan        : Rp %20s' % (config.FormatFloat(',0.00',oT.saldo_pengembangan)))
    oFile.write('\nSaldo peralihan           : Rp %20s' % (config.FormatFloat(',0.00',oT.saldo_peralihan)))
    oFile.write('\nSaldo jumlah dana         : Rp %20s' % (config.FormatFloat(',0.00',oT.saldo_jml_dana)))
    oFile.write('\nPengalihan dana < 1 thn   : Rp %20s' % (config.FormatFloat(',0.00',oT.saldo_peralihan_1th)))
    oFile.write('\nBiaya pencairan           : Rp %20s' % (config.FormatFloat(',0.00',oT.biaya_pencairan)))
    oFile.write('\nBiaya pengelolaan         : Rp %20s' % (config.FormatFloat(',0.00',oT.biaya_pengelolaan)))
    oFile.write('\nBiaya administrasi        : Rp %20s' % (config.FormatFloat(',0.00',oT.biaya_administrasi)))
    oFile.write('\nSaldo manfaat             : Rp %20s' % (config.FormatFloat(',0.00',oT.saldo_manfaat)))
    oFile.write('\nPajak                     : Rp %20s' % (config.FormatFloat(',0.00',oT.pajak)))
    oFile.write('\nManfaat setelah pajak     : Rp %20s' % (config.FormatFloat(',0.00',oT.manfaat_stlh_pajak)))
    oFile.write('\nManfaat tunai             : Rp %20s' % (config.FormatFloat(',0.00',oT.manfaat_tunai)))
    oFile.write('\nManfaat anuitas           : Rp %20s' % (config.FormatFloat(',0.00',oT.manfaat_anuitas)))
    oFile.write('\nBiaya lain                : Rp %20s' % (config.FormatFloat(',0.00',oT.biaya_lain)))
    oFile.write('\n------------------------------------------------------------------------')
    oFile.write('\nManfaat tunai diterima    : Rp %20s' % (config.FormatFloat(',0.00',oT.manfaat_tunai_diterima)))
  elif oT.kode_jenis_transaksi == 'H':
    #pengalihan ke DPLK lain
    oFile.write('\nSaldo iuran pemberi kerja : Rp %20s' % (config.FormatFloat(',0.00',oT.saldo_iuran_pk)))
    oFile.write('\nSaldo iuran peserta       : Rp %20s' % (config.FormatFloat(',0.00',oT.saldo_iuran_pst)))
    oFile.write('\nSaldo pengembangan        : Rp %20s' % (config.FormatFloat(',0.00',oT.saldo_pengembangan)))
    oFile.write('\nSaldo peralihan           : Rp %20s' % (config.FormatFloat(',0.00',oT.saldo_peralihan)))
    oFile.write('\nSaldo jumlah dana         : Rp %20s' % (config.FormatFloat(',0.00',oT.saldo_jml_dana)))
    oFile.write('\nBiaya administrasi        : Rp %20s' % (config.FormatFloat(',0.00',oT.biaya_administrasi)))
    oFile.write('\nBiaya pengalihan          : Rp %20s' % (config.FormatFloat(',0.00',oT.biaya_pindah)))
    oFile.write('\nSaldo dana dialihkan      : Rp %20s' % (config.FormatFloat(',0.00',oT.saldo_dana_dipindahkan)))
    oFile.write('\nBiaya lain                : Rp %20s' % (config.FormatFloat(',0.00',oT.biaya_lain)))
    oFile.write('\n------------------------------------------------------------------------')
    oFile.write('\nDana dialihkan            : Rp %20s' % (config.FormatFloat(',0.00',oT.dana_dialihkan)))
  elif oT.kode_jenis_transaksi == 'X' and oT.isPindahPaket == 'T':
    #biaya transaksi pindah paket investasi
    oFile.write('\nBiaya transaksi : Rp %20s' % (config.FormatFloat(',0.00',\
      abs(oT.mutasi_iuran_pst+oT.mutasi_iuran_pk+oT.mutasi_pengembangan+oT.mutasi_peralihan))))
  
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
  oFile.write('\n         Inputer data           Checker           Approver')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('\n         %s' \
    % (oU.UserName))
  oFile.write('\n')
  oFile.write('\n----------')
  oFile.write('\nSalinan advis yang ke-%d' % (oT.count_advis))
  oFile.write('\nTanggal entri data      : %s %s' % (entriDate, entriTime))
  oFile.write('\nTanggal pembuatan advis : %s %s' % (nowDate, nowTime))
  oFile.write('\nUser pembuat advis      : %s' % (config.SecurityContext.GetUserInfo()[1]))

def CreateAdvis(config, classTransaksi, idTransaksi):
#   config.SendDebugMsg(str(classTransaksi) + str(idTransaksi))
  o = config.CreatePObjImplProxy(classTransaksi)
  o.Key = idTransaksi
  
  config.BeginTransaction()
  try:
    #buat riwayat advis
    config.SendDebugMsg('adv1')
    oA = config.CreatePObject('AdvisHistory')
    oA.ID_Transaksi = idTransaksi
    oA.user_id = config.SecurityContext.UserID
    oA.terminal_id = config.SecurityContext.GetSessionInfo()[1]
    oA.print_date = config.Now()
    config.SendDebugMsg('adv2')    
    
    #inkremen count advis
    if o.count_advis == None or o.count_advis == '':
      #baru pertama kali print advis
      o.count_advis = 1
    else:
      #lewat 1x print advis
      o.count_advis = o.count_advis + 1
    config.SendDebugMsg('adv3')
      
    config.Commit()
  except:
    config.Rollback()
    raise

  tgltransaksi = '%d-%d-%d' % (o.tgl_transaksi[2],o.tgl_transaksi[1],o.tgl_transaksi[0])
  sBaseFileName = 'Advis_%s_%s_%s_#%d#%d.txt' % (classTransaksi, tgltransaksi, \
    o.no_peserta, o.count_advis, oA.advishistory_id)
  sFileName = config.UserHomeDirectory + sBaseFileName
  config.SendDebugMsg(sFileName)
  oFile = open(sFileName, 'w')

  config.SendDebugMsg('adv4')
  ConstructReportHeader(config, o, oFile)
  config.SendDebugMsg('adv5')
  ConstructReportDetails(config, o, oFile)
  config.SendDebugMsg('adv6')
  ConstructReportFooter(config, o, oFile)
  
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

  sBaseFileName = CreateAdvis(config, classTransaksi, idTransaksi)
  
  #return packet
  recRes = returnpacket.CreateDataPacketStructure('filename:string')
  recRes.filename = sBaseFileName

  return 1
