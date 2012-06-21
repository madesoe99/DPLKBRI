## PENTING !!! ##
## ASUMSI: TGL_TRANSAKSI UNTUK SEMUA TRANSAKSIDPLK ADALAH BULAT KECUALI TRANSAKSIBAGIHASIL (KODE_JENIS_TRANSAKSI = 'G') ##

import sys, time
sys.path.append('c:/dafapp/dplk07/script_modules')

import transaksiapi, moduleapi

def CreateObjekTBH(config, idbghasil, idBatch, noPeserta, ekivRate, \
  srrKumulatifPeserta, tgl_akhir_hitung):
  y,m,d = time.localtime()[:3]
  oTBH = config.CreatePObject('TransaksiBagiHasil')
  oTBH.kode_jenis_transaksi = 'G'
  oTBH.idbghasil = idbghasil
  oTBH.ID_TransactionBatch = idBatch
  oTBH.no_peserta = noPeserta
  oTBH.mutasi_iuran_pk = oTBH.mutasi_iuran_pst = oTBH.mutasi_peralihan = 0.0
  oTBH.mutasi_pengembangan = ekivRate * srrKumulatifPeserta
  oTBH.terminal_id = oTBH.terminal_id_auth = \
    config.SecurityContext.GetSessionInfo()[1]

  # tanggal transaksi berdasarkan tanggal hari ini
  #oTBH.tgl_transaksi = config.ModLibUtils.EncodeDate(y,m,d)

  # tanggal transaksi berdasarkan tanggal batch
  oTransactionBatch = oTBH.LTransactionBatch

##  oTransactionBatch = config.CreatePObjImplProxy('TransactionBatch')
##  config.SendDebugMsg('c0')
##  oTransactionBatch.Key = idBatch

  config.SendDebugMsg('c1')
#   oTBH.tgl_transaksi = oTBH.tgl_otorisasi = moduleapi.DateTimeTupleToFloat(config, oTransactionBatch.tgl_used)
  # sesuai tanggal akhir srrcalc
  oTBH.tgl_transaksi = oTBH.tgl_otorisasi = moduleapi.DateTimeTupleToFloat(config, tgl_akhir_hitung)
  config.SendDebugMsg('c2')

  oTBH.tgl_sistem = config.Now()
  oTBH.user_id = oTBH.user_id_auth = config.SecurityContext.UserID
  oTBH.branch_code = config.SecurityContext.GetUserInfo()[4]
  oTBH.isCommitted = 'T'
  oTBH.keterangan = 'Transaksi bagihasil %d-%d-%d peserta %s' % (d,m,y,noPeserta)
  config.SendDebugMsg('d')

  #assgin kode paket investasinya
  transaksiapi.SetPaketInvestasi(config, oTBH)
  config.SendDebugMsg('e')

  oRekeningDPLK = oTBH.LRekeningDPLK
  oRekeningDPLK.akum_dana_pengembangan += oTBH.mutasi_pengembangan

  return 1

def CreateTransaksiBagiHasil(config, idbghasil, ekivRate, sWhere, idBatch, \
  totalHariSRRKumulatif, tgl_akhir_hitung):
  y,m,d = time.localtime()[:3]

  #ambil terlebih dahulu peserta yang tergabung dalam SRRCalcRincian yang didefinisikan
  #dalam sWhere
  sSQL = 'select h.NO_PESERTA, h.SRR, s.TOTAL_HARI_SRR \
          from HISTORISRR h, SRRCALC s, SRRCALCRINCIAN sr \
          where (%s) and h.ID_SRRCALCRINCIAN = sr.ID_SRRCALCRINCIAN and \
          sr.ID_SRRCALC = s.ID_SRRCALC \
          order by h.NO_PESERTA, h.ID_SRRCALCRINCIAN' % (sWhere)
  rSQL = config.CreateSQL(sSQL).RawResult

##  progress = config.ProgressTracker
##  progress.ProgressLevel2()

  minimalBagiHasil = moduleapi.GetMinimalSRRBagiHasil(config)

  srrKumulatifPeserta = 0.0
  lastNoPeserta = rSQL.no_peserta
  rSQL.First()
  while not rSQL.Eof:

##    progress.SetProgressInfo2(2, 'Memproses peserta %s...' % (lastNoPeserta))

    if lastNoPeserta == rSQL.no_peserta:
      #peserta masih sama, hitung srr kumulatif peserta
      srrKumulatifPeserta += rSQL.srr * (rSQL.total_hari_SRR / totalHariSRRKumulatif)
    else:
      #peserta berbeda, buat objek transaksi bagi hasil untuk lastNoPeserta
      #jika SRR peserta memenuhi minimal bagi hasil
      config.SendDebugMsg('bef CreateObjekTBH1')
      if srrKumulatifPeserta >= minimalBagiHasil:
        config.SendDebugMsg('bef CreateObjekTBH11')
        CreateObjekTBH(config, idbghasil, idBatch, lastNoPeserta, ekivRate, \
          srrKumulatifPeserta, tgl_akhir_hitung)

      #switching: handling untuk peserta berikutnya 
      #(set lastNoPeserta dan srrKumulatifPeserta untuk peserta berikutnya) 
      lastNoPeserta = rSQL.no_peserta
      srrKumulatifPeserta = rSQL.srr * (rSQL.total_hari_SRR / totalHariSRRKumulatif)

    rSQL.Next()

  #HANDLING KHUSUS UNTUK LAST ITEM TERLOOPING
  config.SendDebugMsg('bef CreateObjekTBH2')
  #jika SRR peserta memenuhi minimal bagi hasil
  if srrKumulatifPeserta >= minimalBagiHasil:
    CreateObjekTBH(config, idbghasil, idBatch, lastNoPeserta, ekivRate, \
      srrKumulatifPeserta, tgl_akhir_hitung)

  return 1

def CreateBagiHasil(config, listSRRCalcRincian, laba, kodePaketInvestasi, \
  totalHariSRRKumulatif, idBatch, tgl_akhir_hitung):

  #buat objek BagiHasil
  oBH = config.CreatePObject('BagiHasil')

  #buat objek SRRCalc_BagiHasil sesuai dengan listSRRCalcRincian
  srrKumulatif = 0.0
  sWhere = ''
  for SRRCalcRincian in listSRRCalcRincian:
    oSCBH = config.CreatePObject('SRRCalcBagiHasil')
    oSCBH.idbghasil = oBH.idbghasil
    oSCBH.ID_SRRCalcRincian = SRRCalcRincian[0]
    # srrKumulatif = total srr * (total hari srr/totalHariSRRKumulatif)
    srrKumulatif = SRRCalcRincian[1] * (SRRCalcRincian[2] / totalHariSRRKumulatif)

    #string berikut dipakai saat CreateTransaksiBagiHasil
    if sWhere == '':
      sWhere = ' h.ID_SRRCALCRINCIAN = %d' % (SRRCalcRincian[0])
    else:
      #bila SRR yang terlibat bagi hasil lebih dari satu
      sWhere += ' or h.ID_SRRCALCRINCIAN = %d' % (SRRCalcRincian[0])

  #lengkapi properti objek BagiHasil
  oBH.kode_paket_investasi = kodePaketInvestasi
  if not moduleapi.IsApproxZero(srrKumulatif):
    # srrKumulatif tidak nol
    oBH.indeks = laba / srrKumulatif
  else:
    oBH.indeks = 0.0
  oBH.status_posting = 'F'
  oBH.keuntungan_dibagikan = laba 
  oBH.tgl_bagi_hasil = config.Now()
  config.SendDebugMsg('cbh1')

  #buat Transaksi BagiHasil untuk tiap peserta yang terlist dalam SRRCalcRincian
  CreateTransaksiBagiHasil(config, oBH.idbghasil, oBH.indeks, sWhere, idBatch, \
    totalHariSRRKumulatif, tgl_akhir_hitung)

  return 1

def Main(config, idSRRCalc, idBatch, dataset):
  config.SendDebugMsg('bhm1')
  #ambil dulu peserta yang tercatat sebagai peserta dalam perhitungan SRR Calc
  #cek bila ada peserta yang berubah status menjadi "Non Aktif"
  #pengecekan MENGABAIKAN pemilihan KODE PAKET INVESTASI 
  #bila ada yang berstatus "Non Aktif", Raise untuk hitung ulang secara manual
  #atau proses dihitungkan secara otomatis oleh sistem??
  sSQLCek = 'select h.NO_PESERTA \
             from SRRCALC s, SRRCALCRINCIAN sr, HISTORISRR h, REKENINGDPLK r \
             where s.STATUS_BAGIHASIL = \'F\' and \
                   s.ID_SRRCALC <= %d and sr.ID_SRRCALC = s.ID_SRRCALC and \
                   h.ID_SRRCALCRINCIAN = sr.ID_SRRCALCRINCIAN and \
                   r.no_peserta = h.NO_PESERTA and \
                   (r.STATUS_DPLK = \'N\' or r.STATUS_DPLK = \'S\')' \
             % (idSRRCalc)
  rSQLCek = config.CreateSQL(sSQLCek).RawResult

  config.SendDebugMsg('bhm2')
  if not rSQLCek.Eof:
    #terdapat peserta yang Non Aktif
    raise '\nPERINGATAN','Dalam hasil Perhitungan SRR yang dipakai untuk Bagi Hasil,'\
      'terdapat peserta yang SEKARANG telah berstatus NON AKTIF. Hal ini menyebabkan proses'\
      'Bagi Hasil menjadi tidak valid. Untuk itu, 1) hapus semua hasil perhitungan SRR.'\
      '2) Selanjutnya, lakukan perhitungan ulang SRR.'

##  progress = config.ProgressTracker
##  progress.ProgressLevel1()

  config.BeginTransaction()
  try:
    #set Parameter BATAS_TGL_TUTUP_BATCH dengan tanggal Akhir SRR Calc yang dipakai
    oSC = config.CreatePObjImplProxy('SRRCalc')
    oSC.Key = idSRRCalc
    tgl_akhir_hitung = oSC.tgl_akhir_hitung

    config.SendDebugMsg('bhm3')
    #lakukan proses bagi hasil per paket investasi
    for j in range(dataset.RecordCount):
      config.SendDebugMsg('bhm4')
      recPI = dataset.GetRecord(j)
      kodePaketInvestasi = recPI.kodePaket
      laba = recPI.laba

##      progress.SetProgressInfo2(1, 'Memproses Paket Investasi %s...: ' % (kodePaketInvestasi))

      #cek SRR sebelumnya yang status_bagihasil masih false (kode paket investasinya sama)
      #klo ada, ikutan diambil untuk perhitungan bagi hasil
      sSQL = 'select sr.ID_SRRCALCRINCIAN, sr.TOTAL_SRR, s.TOTAL_HARI_SRR \
              from SRRCALC s, SRRCALCRINCIAN sr \
              where s.STATUS_BAGIHASIL = \'F\' and \
                    s.ID_SRRCALC <= %d and \
                    s.ID_SRRCALC = sr.ID_SRRCALC and \
                    sr.KODE_PAKET_INVESTASI = \'%s\';' \
              % (idSRRCalc, kodePaketInvestasi)
      config.SendDebugMsg('sql srrcal: '+ str(sSQL))
      rSQL = config.CreateSQL(sSQL).RawResult

      #inisialisasi data
      rSQL.First()
      totalHariSRRKumulatif = 0
      listSRRCalcRincian = []

      config.SendDebugMsg('bhm5')
      while not rSQL.Eof:   
        #tambahkan SRRCalc dalam listSRRCalc
        listSRRCalcRincian += [[rSQL.ID_SRRCALCRINCIAN,rSQL.total_srr,rSQL.total_hari_SRR]]        
        totalHariSRRKumulatif += rSQL.total_hari_SRR

        rSQL.Next()

      config.SendDebugMsg('bhm6')
      if listSRRCalcRincian != []:
        #proses bagi hasil untuk paket investasi yang ada hasil perhitungan SRR
        CreateBagiHasil(config, listSRRCalcRincian, laba, kodePaketInvestasi, \
          totalHariSRRKumulatif, idBatch, tgl_akhir_hitung)

    config.SendDebugMsg('bhm7')
    #update status bagi hasil untuk semua SRRCalc yang dibagi hasilkan
    sSQLUpdate = 'update SRRCALC set STATUS_BAGIHASIL = \'T\' where ID_SRRCALC <= %d \
                 and STATUS_BAGIHASIL = \'F\'' \
                 % (idSRRCalc)
    rSQLUpdate = config.ExecSQL(sSQLUpdate)

    config.SendDebugMsg('bhm8')
    #set Parameter BATAS_TGL_TUTUP_BATCH dengan tanggal Akhir SRR Calc yang dipakai
    oP = config.CreatePObjImplProxy('Parameter')
    oP.Key = 'BATAS_TGL_TUTUP_BATCH'
    y,m,d = tgl_akhir_hitung[:3]
    tgl_akhir_plus = config.ModLibUtils.EncodeDate(y, m, d) + 1
#     y, m, d, h, n, s, z = tgl_akhir_hitung[:7]
#     tgl_akhir_plus = config.ModLibUtils.EncodeDate(y, m, d) + config.ModLibUtils.EncodeTime(h, n, s, z)
    oP.Numeric_Value = tgl_akhir_plus
    y,m,d = config.ModLibUtils.DecodeDate(tgl_akhir_plus)[:3]
    oP.Varchar_Value = '%d-%d-%d' % (d,m,y)

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
  idSRRCalc = parameter.__Info.GetRecord(0).idSRRCalc
  idBatch = parameter.__Info.GetRecord(0).idBatch
  dsPaketInvestasi = parameter.__PaketInvestasi

  consoleID = 'HitungBagiHasil_' + str(pid)

  sJobName = 'Proses Bagi Hasil. TaskID = %s' % (pid)
  app.WriteConsole(sJobName + ': mulai berlangsung\r\n')
  try:
    app.CreateConsole(consoleID, 'progress')
    try:
      app.SwitchDefaultConsole(consoleID)

      #main task right here
      Main(config, idSRRCalc, idBatch, dsPaketInvestasi)

      app.WriteConsole(sJobName + ': telah selesai\r\n')
    finally:
      app.CloseConsole(consoleID)
  except:
    app.WriteConsole(sJobName + ': Error\r\n' + str(sys.exc_info()[1]) + '\r\n')
    raise
