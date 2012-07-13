## PENTING !!! ##
## ASUMSI: TGL_TRANSAKSI UNTUK SEMUA TRANSAKSIDPLK ADALAH BULAT KECUALI TRANSAKSIBAGIHASIL (KODE_JENIS_TRANSAKSI = 'G') ##

import sys, time
sys.path.append('c:/dafapp/dplk07/script_modules')

import transaksiapi, moduleapi

INV_REKSADANA = ['R']

def CreateObjekTBH(config, idbghasil, idBatch, noPeserta, ekivRate, \
  srrKumulatifPeserta, tgl_akhir_hitung, kode_jns_investasi, baghas_peserta):
  
  y,m,d = tgl_akhir_hitung[:3]
  oTBH = config.CreatePObject('TransaksiBagiHasil')
  oTBH.kode_jenis_transaksi = 'G'
  oTBH.idbghasil = idbghasil
  oTBH.ID_TransactionBatch = idBatch
  oTBH.no_peserta = noPeserta
  oTBH.mutasi_iuran_pk = oTBH.mutasi_iuran_pst = oTBH.mutasi_peralihan = 0.0
  if kode_jns_investasi in INV_REKSADANA:
	oTBH.mutasi_pengembangan = baghas_peserta	
  else:
	oTBH.mutasi_pengembangan = ekivRate * srrKumulatifPeserta
	config.SendDebugMsg(noPeserta+'|'+str(oTBH.mutasi_pengembangan))
  oTBH.terminal_id = oTBH.terminal_id_auth = \
    config.SecurityContext.GetSessionInfo()[1]

  # tanggal transaksi berdasarkan tanggal hari ini
  #oTBH.tgl_transaksi = config.ModLibUtils.EncodeDate(y,m,d)

  # tanggal transaksi berdasarkan tanggal batch
  oTransactionBatch = oTBH.LTransactionBatch

##  oTransactionBatch = config.CreatePObjImplProxy('TransactionBatch')
##  oTransactionBatch.Key = idBatch

  nama_jenis_investasi = moduleapi.GetNamaJenisInvestasi(config, kode_jns_investasi)
#   oTBH.tgl_transaksi = oTBH.tgl_otorisasi = moduleapi.DateTimeTupleToFloat(config, oTransactionBatch.tgl_used)
  # sesuai tanggal akhir srrcalc
  oTBH.tgl_transaksi = oTBH.tgl_otorisasi = moduleapi.DateTimeTupleToFloat(config, tgl_akhir_hitung)
  oTBH.tgl_sistem = config.Now()
  oTBH.user_id = oTBH.user_id_auth = config.SecurityContext.UserID
  oTBH.branch_code = config.SecurityContext.GetUserInfo()[4]
  oTBH.isCommitted = 'T'
  oTBH.keterangan = 'Transaksi bagihasil %s %d-%d-%d peserta %s' % (nama_jenis_investasi,d,m,y,noPeserta)

  #assgin kode paket investasinya
  transaksiapi.SetPaketInvestasi(config, oTBH)

  oRekeningDPLK = oTBH.LRekeningDPLK
  oDetailAkumPengembangan = config.CreatePObjImplProxy('DetailAkumPengembangan')
  oDetailAkumPengembangan.SetKey('no_peserta',noPeserta)
  oDetailAkumPengembangan.SetKey('kode_paket_investasi', oRekeningDPLK.kode_paket_investasi)
  oDetailAkumPengembangan.SetKey('kode_jns_investasi', kode_jns_investasi)  
  
  #oRekeningDPLK.akum_dana_pengembangan += oTBH.mutasi_pengembangan
  oDetailAkumPengembangan.Nilai_Akumulasi += oTBH.mutasi_pengembangan   
  if oDetailAkumPengembangan.Nilai_Akumulasi < 0:
      oRekeningDPLK.akum_dana_iuran_pst += oDetailAkumPengembangan.Nilai_Akumulasi
      oRekeningDPLK.akum_dana_pengembangan += oTBH.mutasi_pengembangan - oDetailAkumPengembangan.Nilai_Akumulasi
      oDetailAkumPengembangan.Nilai_Akumulasi = 0
      if oRekeningDPLK.akum_dana_iuran_pst < 0:
          oRekeningDPLK.akum_dana_iuran_pk += oRekeningDPLK.akum_dana_iuran_pst
          oRekeningDPLK.akum_dana_iuran_pst = 0
          if oRekeningDPLK.akum_dana_iuran_pk < 0:
              oRekeningDPLK.akum_dana_peralihan += oRekeningDPLK.akum_dana_iuran_pk
              oRekeningDPLK.akum_dana_iuran_pk = 0
  else:
    oRekeningDPLK.akum_dana_pengembangan += oTBH.mutasi_pengembangan 
	
  return 1

def CreateTransaksiBagiHasil(config, idbghasil, ekivRate, sWhere, idBatch, \
  totalHariSRRKumulatif, tgl_akhir_hitung, kode_jns_investasi):
  y,m,d = time.localtime()[:3]

  #ambil terlebih dahulu peserta yang tergabung dalam SRRCalcRincian yang didefinisikan
  #dalam sWhere
  sSQL = 'select h.NO_PESERTA, h.SRR, s.TOTAL_HARI_SRR \
          from HISTORISRR h, SRRCALC s, SRRCALCRINCIAN sr \
          where (%s) and h.ID_SRRCALCRINCIAN = sr.ID_SRRCALCRINCIAN and \
          sr.ID_SRRCALC = s.ID_SRRCALC \
          order by h.NO_PESERTA, h.ID_SRRCALCRINCIAN' % (sWhere)
  rSQL = config.CreateSQL(sSQL).RawResult  
  minimalBagiHasil = moduleapi.GetMinimalSRRBagiHasil(config)

  srrKumulatifPeserta = 0.0
  lastNoPeserta = rSQL.no_peserta
  rSQL.First()
  while not rSQL.Eof:    
    if lastNoPeserta == rSQL.no_peserta:
      #peserta masih sama, hitung srr kumulatif peserta
      srrKumulatifPeserta += rSQL.srr * (rSQL.total_hari_SRR / totalHariSRRKumulatif)
    else:
      #peserta berbeda, buat objek transaksi bagi hasil untuk lastNoPeserta
      #jika SRR peserta memenuhi minimal bagi hasil
      if srrKumulatifPeserta >= minimalBagiHasil:
        CreateObjekTBH(config, idbghasil, idBatch, lastNoPeserta, ekivRate, \
          srrKumulatifPeserta, tgl_akhir_hitung, kode_jns_investasi, 0)

      #switching: handling untuk peserta berikutnya 
      #(set lastNoPeserta dan srrKumulatifPeserta untuk peserta berikutnya) 
      lastNoPeserta = rSQL.no_peserta
      srrKumulatifPeserta = rSQL.srr * (rSQL.total_hari_SRR / totalHariSRRKumulatif)

    rSQL.Next()

  #HANDLING KHUSUS UNTUK LAST ITEM TERLOOPING
  #jika SRR peserta memenuhi minimal bagi hasil
  config.SendDebugMsg('lastNoPeserta|srrKumulatifPeserta=%s|%s'%(str(lastNoPeserta),str(srrKumulatifPeserta)))
  if srrKumulatifPeserta >= minimalBagiHasil:
    CreateObjekTBH(config, idbghasil, idBatch, lastNoPeserta, ekivRate, \
      srrKumulatifPeserta, tgl_akhir_hitung, kode_jns_investasi, 0)

  return 1

def CreateBagiHasil(config, listSRRCalcRincian, laba, kodePaketInvestasi, \
  kode_jns_investasi, totalHariSRRKumulatif, idBatch, tgl_akhir_hitung):

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
  oBH.kode_jns_investasi = kode_jns_investasi
  if not moduleapi.IsApproxZero(srrKumulatif):
    # srrKumulatif tidak nol
    oBH.indeks = laba / srrKumulatif
  else:
    oBH.indeks = 0.0
  oBH.status_posting = 'F'
  oBH.keuntungan_dibagikan = laba 
  oBH.tgl_bagi_hasil = config.Now()

  #buat Transaksi BagiHasil untuk tiap peserta yang terlist dalam SRRCalcRincian
  CreateTransaksiBagiHasil(config, oBH.idbghasil, oBH.indeks, sWhere, idBatch, \
  totalHariSRRKumulatif, tgl_akhir_hitung, kode_jns_investasi)

  return 1
  
def CreateBagiHasil2(config, laba, total_dana_paket, kodePaketInvestasi, kode_jns_investasi):
  #buat objek BagiHasil
  oBH = config.CreatePObject('BagiHasil')
  oBH.kode_paket_investasi = kodePaketInvestasi
  oBH.kode_jns_investasi = kode_jns_investasi
  if not moduleapi.IsApproxZero(total_dana_paket):
    oBH.indeks = laba / total_dana_paket
  else:
    oBH.indeks = 0.0
  oBH.status_posting = 'F'
  oBH.keuntungan_dibagikan = laba 
  oBH.tgl_bagi_hasil = config.Now()
  
  return oBH  
  
def Main(config, idSRRCalc, idBatch, dataset):
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

  if not rSQLCek.Eof:
    #terdapat peserta yang Non Aktif
    raise Exception, '\nPERINGATAN','Dalam hasil Perhitungan SRR yang dipakai untuk Bagi Hasil + '\
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
    tgl_mulai_hitung = oSC.tgl_mulai_hitung
    #lakukan proses bagi hasil per paket investasi
    for j in range(dataset.RecordCount):
      recPI = dataset.GetRecord(j)
      kodePaketInvestasi = recPI.kodePaket
      laba = recPI.laba
      kode_jns_investasi = recPI.kode_jns_investasi
      y,m,d = tgl_akhir_hitung[:3]
      yy,mm,dd = tgl_mulai_hitung[:3]
	  
      tgl_mulai = config.ModLibUtils.EncodeDate(yy, mm, dd)
      str_tgl_mulai = config.FormatDateTime('yyyy-mm-dd', tgl_mulai)

      tgl_akhir = config.ModLibUtils.EncodeDate(y, m, d)
      tgl_akhir_plus = config.ModLibUtils.EncodeDate(y, m, d) + 1
	  
      tgl_baghas = config.FormatDateTime('yyyy-mm-dd', tgl_akhir)
      tgl_baghas_plus = config.FormatDateTime('yyyy-mm-dd', tgl_akhir_plus)
      if laba <> 0:
	    if kode_jns_investasi in INV_REKSADANA:
		  total_dana_paket = moduleapi.GetTotalDanaPaket(config, str_tgl_mulai, kodePaketInvestasi)		  
		  sSQL = 'SELECT no_peserta \
		  FROM RekeningDPLK \
		  WHERE kode_paket_investasi = \'%s\' \
		  AND status_dplk = \'A\'' % (kodePaketInvestasi)
		  rSQL = config.CreateSQL(sSQL).RawResult
		  rSQL.First()
		  oBH = CreateBagiHasil2(config, laba, total_dana_paket, kodePaketInvestasi, kode_jns_investasi)
		  while not rSQL.Eof:
                      total_dana_peserta = moduleapi.GetTotalDanaPeserta(config, str_tgl_mulai, kodePaketInvestasi, rSQL.no_peserta)
                      baghas_peserta = (total_dana_peserta / total_dana_paket) * laba
                      CreateObjekTBH(config, oBH.idbghasil, idBatch, rSQL.no_peserta, 0, 0, \
					  tgl_akhir_hitung, kode_jns_investasi, baghas_peserta)
                      rSQL.Next()
	    else:
              #cek SRR sebelumnya yang status_bagihasil masih false (kode paket investasinya sama)
              #klo ada, ikutan diambil untuk perhitungan bagi hasil
              sSQL = 'select sr.ID_SRRCALCRINCIAN, sr.TOTAL_SRR, s.TOTAL_HARI_SRR \
              from SRRCALC s, SRRCALCRINCIAN sr \
              where s.STATUS_BAGIHASIL = \'F\' and s.ID_SRRCALC <= %d \
              and s.ID_SRRCALC = sr.ID_SRRCALC and sr.KODE_PAKET_INVESTASI = \'%s\';'\
			  % (idSRRCalc, kodePaketInvestasi)
              rSQL = config.CreateSQL(sSQL).RawResult
              #inisialisasi data
              rSQL.First()
              totalHariSRRKumulatif = 0
              listSRRCalcRincian = []

              while not rSQL.Eof:   
              #tambahkan SRRCalc dalam listSRRCalc
                  listSRRCalcRincian += [[rSQL.ID_SRRCALCRINCIAN,rSQL.total_srr,rSQL.total_hari_SRR]]        
                  totalHariSRRKumulatif += rSQL.total_hari_SRR
                  rSQL.Next()
                  if listSRRCalcRincian != []:
                      #proses bagi hasil untuk paket investasi yang ada hasil perhitungan SRR
                      CreateBagiHasil(config, listSRRCalcRincian, laba, kodePaketInvestasi, \
                                      kode_jns_investasi, totalHariSRRKumulatif, idBatch, tgl_akhir_hitung)

    #update status bagi hasil untuk semua SRRCalc yang dibagi hasilkan
    sSQLUpdate = 'update SRRCALC set STATUS_BAGIHASIL = \'T\' where ID_SRRCALC <= %d \
                 and STATUS_BAGIHASIL = \'F\'' \
                 % (idSRRCalc)
    rSQLUpdate = config.ExecSQL(sSQLUpdate)

    #set Parameter BATAS_TGL_TUTUP_BATCH dengan tanggal Akhir SRR Calc yang dipakai
    oP = config.CreatePObjImplProxy('Parameter')
    oP.Key = 'BATAS_TGL_TUTUP_BATCH'
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
#   import rpdb2; rpdb2.start_embedded_debugger("000")
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
