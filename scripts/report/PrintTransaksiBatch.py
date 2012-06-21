import sys, time, os

def ConstructReportHeader(config, oTB, oFile):
  tipeBatch = {'R':'Registration','T':'Transaction','P':'Premi','I':'Investment'}
  subTipeBatch = {'T':'Batch Teller','M':'Batch Manual'}
  statusBatch = {'O':'Open','C':'Closed'}

  #write file
  oFile.write('DPLK Bank Rakyat Indonesia')
  oFile.write('\nDaftar Transaksi Isi Batch')
  oFile.write('\n========================================================================')
  oFile.write('\n')
  oFile.write('\nNomor Batch     : %s' % (oTB.no_batch))
  oFile.write('\nTipe Batch      : %s' % (tipeBatch[oTB.batch_type]))
  oFile.write('\nSub Tipe Batch  : %s' % (subTipeBatch[oTB.batch_sub_type]))
  oFile.write('\nTanggal Buat    : %s' % ('%s-%s-%d' % ( \
    str(oTB.tgl_create[2]).zfill(2),\
    str(oTB.tgl_create[1]).zfill(2),oTB.tgl_create[0])))
  oFile.write('\nTanggal Pakai   : %s' % ('%s-%s-%d' % ( \
    str(oTB.tgl_used[2]).zfill(2),\
    str(oTB.tgl_used[1]).zfill(2),oTB.tgl_used[0])))
  oFile.write('\nStatus Batch    : %s' % (statusBatch[oTB.batch_status]))
  oFile.write('\n')

def ConstructReportDetails(config, oTB, oFile):
  #tentukan list transaksi berdasarkan jenis batchnya
  if oTB.batch_type == 'R':
    listTransaksi = oTB.Ls_IuranPendaftaran
    stringJudul = 'Nomor Peserta\tKode Cabang\t' \
      'Biaya Pendaftaran\tStatus Otorisasi\tKeterangan'
  elif oTB.batch_type == 'T':
    listTransaksi = oTB.Ls_TransaksiDPLK
    stringJudul = 'Kode Jenis Transaksi\tNomor Peserta\tKode Cabang\t' \
      'Mutasi Iuran PK\t  Mutasi Iuran Peserta\t  Mutasi Pengembangan\t Mutasi Peralihan\t' \
      'Status Otorisasi\tKeterangan'
  elif oTB.batch_type == 'P':
    listTransaksi = oTB.Ls_TransaksiPremi
    stringJudul = 'Nama Transaksi\tKode Cabang\t' \
      'Mutasi Premi\tDebet\tStatus Otorisasi\tKeterangan'
  elif oTB.batch_type == 'I':
    listTransaksi = oTB.Ls_TransaksiInvestasi
    stringJudul = 'Nomor Bilyet\tKelompok Transaksi\tKode Jenis Transaksi\t' \
      'Mutasi Debet\tMutasi Kredit\tStatus Otorisasi'
    
  #judul untuk tabel list transaksi
  oFile.write('\n%s' % (stringJudul))
  oFile.write('\n')
  
  #looping sambil write to file
  listTransaksi.First()
  while not listTransaksi.EndOfList:
    oTransaksi = listTransaksi.CurrentElement
    
    if oTB.batch_type == 'R':
      oFile.write('\n%s\t%s\t%20s\t%s\t%s' % (oTransaksi.no_peserta, oTransaksi.branch_code, \
        config.FormatFloat(',0.00',oTransaksi.besar_biaya_daftar), \
        oTransaksi.isCommitted, oTransaksi.keterangan ))
    elif oTB.batch_type == 'T':
      oFile.write('\n%10s\t%20s\t%5s\t%20s\t%20s\t%20s\t%17s\t%15s\t%s' % (oTransaksi.kode_jenis_transaksi, \
        oTransaksi.no_peserta, oTransaksi.branch_code, \
        config.FormatFloat(',0.00',oTransaksi.mutasi_iuran_pk), \
        config.FormatFloat(',0.00',oTransaksi.mutasi_iuran_pst), \
        config.FormatFloat(',0.00',oTransaksi.mutasi_pengembangan), \
        config.FormatFloat(',0.00',oTransaksi.mutasi_peralihan), \
        oTransaksi.isCommitted, oTransaksi.keterangan))
    elif oTB.batch_type == 'P':
      oFile.write('\n%s\t%s\t%20s\t%s\t%s\t%s' % (oTransaksi.jenis_transaksi, \
        oTransaksi.branch_code, config.FormatFloat(',0.00',oTransaksi.mutasi_premi), \
        oTransaksi.isDebet, oTransaksi.isCommitted, oTransaksi.keterangan))
    elif oTB.batch_type == 'I':
      oFile.write('\n%s\t%s\t%s\t%20s\t%20s\t%s' % (oTransaksi.no_bilyet, \
      oTransaksi.clsfTransaksiInvestasi, oTransaksi.kode_jenis_trinvestasi, \
      config.FormatFloat(',0.00',oTransaksi.mutasi_debet), \
      config.FormatFloat(',0.00',oTransaksi.mutasi_kredit), oTransaksi.isCommitted))
    
    listTransaksi.Next()
    
def ConstructReportFooter(config, oTB, oFile):
  nowDate = '%s-%s-%d' % (str(time.localtime()[2]).zfill(2),\
    str(time.localtime()[1]).zfill(2),time.localtime()[0])
  nowTime = '%s:%s:%s' % (str(time.localtime()[3]).zfill(2),\
    str(time.localtime()[4]).zfill(2),\
    str(time.localtime()[5]).zfill(2))

  #write file
  oFile.write('\n')
  oFile.write('\n----------')
  oFile.write('\nTanggal mencetak : %s %s' % (nowDate, nowTime))
  oFile.write('\nUser pencetak    : %s' % (config.SecurityContext.GetUserInfo()[1]))

def CreateSlip(config, idBatch):
  o = config.CreatePObjImplProxy('TransactionBatch')
  o.Key = idBatch
  
  nowTime = '%s.%s.%s' % (str(time.localtime()[3]).zfill(2),\
    str(time.localtime()[4]).zfill(2),\
    str(time.localtime()[5]).zfill(2))
  tgltransaksi = '%d-%d-%d' % (o.tgl_used[2],o.tgl_used[1],o.tgl_used[0])
  sBaseFileName = 'TransaksiBatch_%s_%s_%s.txt' % (tgltransaksi, \
    o.no_batch, nowTime)
  sFileName = config.UserHomeDirectory + sBaseFileName
  oFile = open(sFileName, 'w')

  ConstructReportHeader(config, o, oFile)
  ConstructReportDetails(config, o, oFile)
  ConstructReportFooter(config, o, oFile)
  
  oFile.close()
  
  #set file read-only
  os.chmod(sFileName,333)

  return sBaseFileName

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  idBatch = parameter.FirstRecord.idbatch
  sBaseFileName = CreateSlip(config, idBatch)
  
  #return packet
  recRes = returnpacket.CreateDataPacketStructure('filename:string')
  recRes.filename = sBaseFileName

  return 1
