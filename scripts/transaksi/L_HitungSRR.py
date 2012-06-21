## PENTING !!! ##
## ASUMSI: TGL_TRANSAKSI UNTUK SEMUA TRANSAKSIDPLK ADALAH BULAT KECUALI TRANSAKSIBAGIHASIL (KODE_JENIS_TRANSAKSI = 'G') ##

import sys
sys.path.append('c:/dafapp/dplk/script_modules')

import moduleapi

def isEmptySRRCalc(config):
  sSQL = 'select ID_SRRCalc from SRRCalc;'
  rSQL = config.CreateSQL(sSQL).RawResult
  #1 berarti kosong, 0 berarti isi
  return rSQL.Eof

def isEmptyHistoriSRR(config):
  sSQL = 'select ID_HISTORISRR from HISTORISRR;'
  rSQL = config.CreateSQL(sSQL).RawResult

  #1 berarti kosong, 0 berarti isi
  return rSQL.Eof

def GetRecentSaldoAkhir(config, noPeserta):
  sSQL = 'select top 1 h.SALDO_AKHIR_SRR from HISTORISRR h \
    where h.NO_PESERTA = \'%s\' order by h.ID_HISTORISRR DESC;' \
    % (noPeserta)
  rSQL = config.CreateSQL(sSQL).RawResult

  saldo_akhir_SRR = 0.0
  if not rSQL.Eof:
    saldo_akhir_SRR = rSQL.Saldo_Akhir_SRR

  config.SendDebugMsg(noPeserta+'|recent_saldo_akhir:'+str(saldo_akhir_SRR))
  
  return saldo_akhir_SRR

def HitungSRRPeserta(config, emptyHistoriSRR, totalDeltaSaldo, noPeserta):
  #cek tabel historisrr
  if emptyHistoriSRR:
    #historisrr kosong, berarti pertama kali ngitung SRR: nothing todo
    saldo_akhir_SRR = 0.0
  else:
    #sudah ada isi: cek HistoriSRR peserta
    #tidak ketemu, saldo_akhir_srr_akhirnya berarti 0 (belum pernah dihitung SRR-nya)
    #ketemu, pake (saldo_akhir_srr_akhir * totalHari) sebagai penambah untuk SRR peserta 
    saldo_akhir_SRR = GetRecentSaldoAkhir(config, noPeserta)

  srrPeserta = saldo_akhir_SRR + totalDeltaSaldo
  
  config.SendDebugMsg(noPeserta+'|totalDeltaSaldo:'+str(totalDeltaSaldo))
  config.SendDebugMsg(noPeserta+'|srrPeserta:'+str(srrPeserta))
  
  return srrPeserta, saldo_akhir_SRR

def resJumlahPeserta(config, tglAkhir):
  #ambil jumlah peserta aktif sampai dengan tglAkhir (recent date)
  #perbaikan: restriksi tanggal registrasi dicabut
  sSQLJumlah = 'select count(no_peserta) as JumlahPeserta \
          from REKENINGDPLK \
          where STATUS_DPLK = \'A\';'
#   sSQLJumlah = 'select count(n.no_peserta) as JumlahPeserta \
#           from NASABAHDPLK n, REKENINGDPLK r \
#           where r.STATUS_DPLK = \'A\' and \
#                 n.no_peserta = r.no_peserta;'
#           % ('%d-%d-%d' % (tglAkhir[0],tglAkhir[1],tglAkhir[2]))
#                 n.tgl_registrasi < DateAdd(d,1,\'%s\') and \
  return config.CreateSQL(sSQLJumlah).RawResult

def resTransPeserta(config, tglAwalProses, tglAkhir):
  #ambil semua transaksi terotorisasi milik peserta aktif yang tanggal 
  #tgl_transaksinya dari rentang tglAwalProses - tglAkhir
  #tglAwalProses bulat dan tidak termasuk yang diproses (>)
  #kode_paket_investasi berdasarkan paket peserta tersebut
  #perbaikan: restriksi tanggal registrasi dicabut
  sSQL = 'select r.no_peserta, r.kode_paket_investasi, t.TGL_TRANSAKSI, \
          	t.MUTASI_IURAN_PK, t.MUTASI_IURAN_PST, \
            t.MUTASI_PENGEMBANGAN, t.MUTASI_PERALIHAN \
        	from TRANSAKSIDPLK t, REKENINGDPLK r \
        	where t.ISCOMMITTED = \'T\' \
        		and STATUS_DPLK = \'A\' \
        	  and r.no_peserta = t.no_peserta \
        		and t.TGL_TRANSAKSI > \'%s\' \
        		and t.TGL_TRANSAKSI < DateAdd(d,1,\'%s\') \
          order by r.kode_paket_investasi, r.no_peserta; ' \
          % ('%d-%d-%d' % (tglAwalProses[0], tglAwalProses[1], tglAwalProses[2])
            , '%d-%d-%d' % (tglAkhir[0], tglAkhir[1], tglAkhir[2])
          )
  config.SendDebugMsg('transpeserta: '+ sSQL)
  return config.CreateSQL(sSQL).RawResult

def resNonTransPeserta(config, tglAwalProses, tglAkhir):
  # ambil peserta
  # yang masih aktif dan terdaftar selambatnya tglAkhir
  # yang tidak melakukan transaksi selama rentang srr yang dipilih
  #perbaikan: restriksi tanggal registrasi dicabut
  sSQL = 'select r.no_peserta, kode_paket_investasi \
    from REKENINGDPLK r \
    where STATUS_DPLK = \'A\' \
    	and r.no_peserta not in \
    (select no_peserta \
    from TransaksiDPLK \
    where ISCOMMITTED = \'T\' \
    	and TGL_TRANSAKSI > \'%s\' \
    	and TGL_TRANSAKSI < DateAdd(d,1,\'%s\') \
    ) \
    order by kode_paket_investasi; ' \
    % ('%d-%d-%d' % (tglAwalProses[0],tglAwalProses[1],tglAwalProses[2])
      , '%d-%d-%d' % (tglAkhir[0],tglAkhir[1],tglAkhir[2])
    )
#   sSQL = 'select r.no_peserta, kode_paket_investasi \
#     from NASABAHDPLK n, REKENINGDPLK r \
#     where r.no_peserta = n.no_peserta \
#     	and STATUS_DPLK = \'A\' \
#     	and r.no_peserta not in \
#     (select no_peserta \
#     from TransaksiDPLK \
#     where ISCOMMITTED = \'T\' \
#     	and TGL_TRANSAKSI > \'%s\' \
#     	and TGL_TRANSAKSI < DateAdd(d,1,\'%s\') \
#     ) \
#     order by kode_paket_investasi; ' \
#     % ('%d-%d-%d' % (tglAwalProses[0],tglAwalProses[1],tglAwalProses[2])
#       , '%d-%d-%d' % (tglAkhir[0],tglAkhir[1],tglAkhir[2])
#     )
#     	and tgl_registrasi < DateAdd(d,1,\'%s\') \
#   config.SendDebugMsg('nontranspeserta: '+ sSQL)
  return config.CreateSQL(sSQL).RawResult

def CreateHistoriSRR(config, lastNoPeserta, lastID_SRRCalcRincian, saldoAkhir, srrPeserta):
  oHS = config.CreatePObject('HistoriSRR')
  oHS.no_peserta = lastNoPeserta
  oHS.ID_SRRCalcRincian = lastID_SRRCalcRincian
#   oHS.saldo_akhir_srr = (oR.akum_dana_iuran_pk or 0.0) + (oR.akum_dana_iuran_pst or 0.0) + \
#     (oR.akum_dana_pengembangan or 0.0) + (oR.akum_dana_peralihan or 0.0)
  oHS.saldo_akhir_srr = saldoAkhir
  oHS.srr = srrPeserta

  return oHS

def CreateSRRCalcRincian(config, ID_SRRCalc, kode_paket_investasi):
  oSCR = config.CreatePObject('SRRCalcRincian')
  oSCR.ID_SRRCalc = ID_SRRCalc
  oSCR.kode_paket_investasi = kode_paket_investasi
  oSCR.total_srr = 0.0

  return oSCR

def Main(config, tglAwalProses, tglAwal, tglAkhir, needSaving):
  rSQLJumlah = resJumlahPeserta(config, tglAkhir)

  rSQL = resTransPeserta(config, tglAwalProses, tglAkhir)

  # ambil peserta yang tidak bertransaksi
  rSQLNonTrans = resNonTransPeserta(config, tglAwalProses, tglAkhir)
  rSQLNonTrans.First()

#   progress = config.ProgressTracker
#   progress.ProgressLevel1()
  
  #inisialisasi data

  TotalDana = 1.0
  i = 0
  n = rSQLJumlah.JumlahPeserta
  totalDeltaSaldo = totalSRRPaket = srrPeserta = SumSRRPaket = sumMutasi = 0.0

  recentTglSRR = config.ModLibUtils.EncodeDate(tglAkhir[0],tglAkhir[1],tglAkhir[2])
  lastTglSRR = config.ModLibUtils.EncodeDate(tglAwal[0],tglAwal[1],tglAwal[2])
  totalHari = recentTglSRR - lastTglSRR + 1

  if (not rSQL.Eof) and (rSQLNonTrans.Eof or (rSQL.kode_paket_investasi <= rSQLNonTrans.kode_paket_investasi)):
    lastPaketInvestasi = rSQL.kode_paket_investasi 
    rProses = rSQL
  elif not rSQLNonTrans.Eof:
    # rSQL.kode_paket_investasi > rSQLNonTrans.kode_paket_investasi
    lastPaketInvestasi = rSQLNonTrans.kode_paket_investasi 
    rProses = rSQLNonTrans
  else:
    raise 'Kesalahan Rentang Tanggal','\nData peserta maupun data transaksi tidak ditemukan.'
  lastNoPeserta = rProses.no_peserta

  #buat objek-objek yang diperlukan
  oR = config.CreatePObjImplProxy('RekeningDPLK')

  #sebelum buat SRR Calc, cek status isi tabel SRR Calc dahulu
  #1 berarti kosong, 0 berarti isi
  emptySRRCalc = isEmptySRRCalc(config)
  emptyHistoriSRR = isEmptyHistoriSRR(config)

  recentTimeSRR = config.ModLibUtils.CutTime(config.Now())
  if moduleapi.IsApproxZero(recentTimeSRR):
    # perhitungan srr dilasanakan tidak jauh dari setelah jam 00:00
    recentTimeSRR += config.ModLibUtils.EncodeTime(0, 1, 0, 0) # tambah satu menit 

  oSC = config.CreatePObject('SRRCalc')
  oSC.tgl_mulai_hitung = lastTglSRR
  oSC.tgl_akhir_hitung = recentTglSRR + recentTimeSRR
  oSC.total_hari_SRR = int(totalHari)
  oSC.status_bagihasil = 'F'
  oSC.status_rebond = 'F'
  oSC.tgl_create = config.Now()
  oSC.user_id_create = config.SecurityContext.UserID

  #buat SRRCalcRincian, rincian objek SRR Calc di atas
  oSCR = CreateSRRCalcRincian(config, oSC.ID_SRRCalc, lastPaketInvestasi)
  lastID_SRRCalcRincian = oSCR.ID_SRRCalcRincian
  
  minimalBagiHasil = moduleapi.GetMinimalSRRBagiHasil(config)

  config.BeginTransaction()
  try:
    stop = 0
    while not stop:
      prefProses = rProses
      if rProses == rSQL:
        #hitung delta saldonya dari total Mutasi dan deltaWaktu
        totalMutasi = (rSQL.MUTASI_IURAN_PK or 0.0) + (rSQL.MUTASI_IURAN_PST or 0.0) + \
          (rSQL.MUTASI_PENGEMBANGAN or 0.0) + (rSQL.MUTASI_PERALIHAN or 0.0)
        config.SendDebugMsg(rProses.no_peserta+'|main_tot_mutasi:'+str(totalMutasi))

        tglTransaksi = config.ModLibUtils.EncodeDate(rSQL.tgl_transaksi[0],\
          rSQL.tgl_transaksi[1],rSQL.tgl_transaksi[2])

        # ambil element karena tidak bisa langsung membandingkan list dan tuple
        yTrans, mTrans, dTrans = rSQL.tgl_transaksi[:3]
        # bandingkan antar list
        if [yTrans, mTrans, dTrans] != tglAwalProses:
          deltaWaktu = recentTglSRR - tglTransaksi + 1
        else:
          # perlakuan khusus jika tanggal transaksi == tglAwalProses (transaksi bagi hasil bulan sebelumnya)
          deltaWaktu = recentTglSRR - tglTransaksi

        deltaSaldo = totalMutasi * (deltaWaktu / totalHari)
        config.SendDebugMsg(rProses.no_peserta+'|main_deltaSaldo:'+str(deltaSaldo))
      else:
        # rProses == rSQLNonTrans
        totalMutasi = 0.0
        deltaSaldo = 0.0

      if rProses.kode_paket_investasi == lastPaketInvestasi:
        #kode paket investasi masih sama, cek kesamaan no peserta
        if rProses.no_peserta == lastNoPeserta:
          #paket investasi dan no peserta SAMA: tambahkan delta saldo ke total delta saldo
          sumMutasi += totalMutasi
          totalDeltaSaldo += deltaSaldo
          config.SendDebugMsg(rProses.no_peserta+'|main_sumMutasi:'+str(sumMutasi))
          config.SendDebugMsg(rProses.no_peserta+'|main_totalDeltaSaldo:'+str(totalDeltaSaldo))
        else:
          #paket investasi SAMA, no peserta berbeda: lakukan switching proses
          oR.Key = lastNoPeserta

          #hitung SRR untuk last Peserta
          srrPeserta, saldo_akhir_SRR = HitungSRRPeserta(config, emptyHistoriSRR, totalDeltaSaldo, \
            lastNoPeserta)

          #simpan: Saldo saat SRR, SRR, tanggal SRR lastNoPeserta dalam Histori SRR 
          CreateHistoriSRR(config, lastNoPeserta, lastID_SRRCalcRincian, sumMutasi + saldo_akhir_SRR, srrPeserta)
          sumMutasi = totalMutasi

          #tambahkan SRR peserta dalam totalSRR paket investasi yang masih SAMA
          #jika SRR peserta kurang dari minimal bagi hasil, maka srr tidak dianggap sebagai bagian dari totalsrrpaket
          if srrPeserta >= minimalBagiHasil:
            totalSRRPaket += srrPeserta

          #switch total delta saldo untuk peserta lain, lastNoPeserta
          lastNoPeserta = rProses.no_peserta
          totalDeltaSaldo = deltaSaldo

          #inkremen counter peserta
          i += 1
      else:
        #kode paket investasi telah BERUBAH, otomatis no peserta juga BERUBAH
        oR.Key = lastNoPeserta

        #PROSESI SRR PESERTA (YANG JUGA IKUT BERUBAH)
        #hitung SRR untuk last Peserta
        srrPeserta, saldo_akhir_SRR = HitungSRRPeserta(config, emptyHistoriSRR, totalDeltaSaldo, \
          lastNoPeserta)

        #simpan: Saldo saat SRR, SRR, tanggal SRR lastNoPeserta dalam Histori SRR 
        CreateHistoriSRR(config, lastNoPeserta, lastID_SRRCalcRincian, sumMutasi + saldo_akhir_SRR, srrPeserta)
        sumMutasi = totalMutasi

        #tambahkan SRR peserta dalam totalSRR paket investasi yang masih SAMA
        #jika SRR peserta kurang dari minimal bagi hasil, maka srr tidak dianggap sebagai bagian dari totalsrrpaket
        if srrPeserta >= minimalBagiHasil:
          totalSRRPaket += srrPeserta

        #simpan Total SRR untuk last paket investasi di SRR Calc
        oSCR.total_srr = totalSRRPaket

        #switch totalSRRPaket, totalSaldo
        totalSRRPaket = 0.0
        totalDeltaSaldo = deltaSaldo

        #buatkan lagi SRR Calc Rincian untuk Paket Investasi berikutnya
        oSCR = CreateSRRCalcRincian(config, oSC.ID_SRRCalc, rProses.kode_paket_investasi)
        lastID_SRRCalcRincian = oSCR.ID_SRRCalcRincian

        lastNoPeserta = rProses.no_peserta
        lastPaketInvestasi = rProses.kode_paket_investasi

        #inkremen counter peserta
        i += 1

      rProses.Next()
      # cek eof
      if rProses.Eof:
        # pindah ke result sql lain
        if rProses == rSQL:
          rProses = rSQLNonTrans
        else:
          rProses = rSQL
      elif rProses.kode_paket_investasi != lastPaketInvestasi:
        # not rProses.Eof
        # cek lagi urutan paket investasi
        if (not rSQL.Eof) and (rSQLNonTrans.Eof or (rSQL.kode_paket_investasi <= rSQLNonTrans.kode_paket_investasi)):
          rProses = rSQL
        else:
          # rSQL.kode_paket_investasi > rSQLNonTrans.kode_paket_investasi
          rProses = rSQLNonTrans

      # evaluasi nilai berhenti
      stop = rProses.Eof # rSQL.Eof and rSQLNonTrans.Eof

    # end while

    #HANDLING KHUSUS UNTUK LAST ITEM TERLOOPING, SIMPAN SEMUA DATA--------------
    oR.Key = lastNoPeserta

    #hitung SRR untuk last Peserta
    srrPeserta, saldo_akhir_SRR = HitungSRRPeserta(config, emptyHistoriSRR, totalDeltaSaldo, \
      lastNoPeserta)

    #simpan: Saldo saat SRR, SRR, tanggal SRR lastNoPeserta dalam Histori SRR 
    CreateHistoriSRR(config, lastNoPeserta, lastID_SRRCalcRincian, sumMutasi + saldo_akhir_SRR, srrPeserta)

    #tambahkan SRR peserta dalam totalSRR paket investasi yang masih SAMA
    #jika SRR peserta kurang dari minimal bagi hasil, maka srr tidak dianggap sebagai bagian dari totalsrrpaket
    if srrPeserta >= minimalBagiHasil:
      totalSRRPaket += srrPeserta

    #simpan Total SRR untuk last paket investasi di SRR Calc
    oSCR.total_srr = totalSRRPaket
    #---------------------------------------------------------------------------

    config.Commit()  
  except:
    config.Rollback()
    raise    

  return 1

def CekRentangHitungSRR(config, tglAwal, tglAkhir):
  strSQL = \
    'select top 1 ID_SRRCalc \
    from SRRCalc \
    where \
      ((tgl_mulai_hitung <= \'%s\' \
      and \'%s\' <= tgl_akhir_hitung) \
      or \
      (tgl_mulai_hitung <= \'%s\' \
      and \'%s\' <= tgl_akhir_hitung)) \
      or \
      (\'%s\' < tgl_mulai_hitung \
      and tgl_akhir_hitung < \'%s\'); '\
    % ('%d-%d-%d' % (tglAwal[0],tglAwal[1],tglAwal[2])
      , '%d-%d-%d' % (tglAwal[0],tglAwal[1],tglAwal[2])
      , '%d-%d-%d' % (tglAkhir[0],tglAkhir[1],tglAkhir[2])
      , '%d-%d-%d' % (tglAkhir[0],tglAkhir[1],tglAkhir[2])
      , '%d-%d-%d' % (tglAwal[0],tglAwal[1],tglAwal[2])
      , '%d-%d-%d' % (tglAkhir[0],tglAkhir[1],tglAkhir[2])
    )
  resSQL = config.CreateSQL(strSQL).RawResult
  resSQL.First()
  if not resSQL.Eof:
    raise 'Kesalahan Rentang Tanggal\r\n', 'Rentang tanggal tidak boleh beririsan dari perhitungan srr yang sudah dilakukan.'

def DAFLongScriptMain(config, parameter, pid, monfilename):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # pid: Process ID of this script
  # monfilename: Monitor file name to store status
#   import rpdb2; rpdb2.start_embedded_debugger("000")

  app = config.AppObject
  needSaving = parameter.FirstRecord.code

  y,m,d = config.ModLibUtils.DecodeDate(parameter.FirstRecord.tglawal)
  tglAwal = [y,m,d]

  # tglAwalProses adalah tanggal awal dikurangi 1 hari
  # digunakan untuk pembatasan transaksi yang akan diproses
  # yaitu lebih dari tglAwalProses
  y,m,d = config.ModLibUtils.DecodeDate(parameter.FirstRecord.tglawal-1)
  tglAwalProses = [y,m,d]

  y,m,d = config.ModLibUtils.DecodeDate(parameter.FirstRecord.tglakhir)
  tglAkhir = [y,m,d]

  consoleID = 'HitungSRR_' + str(pid)

  sJobName = 'Penghitungan SRR. TaskID = %s' % (pid)
  app.WriteConsole(sJobName + ': mulai berlangsung\r\n')
  try:
    app.CreateConsole(consoleID, 'progress')
    try:
      app.SwitchDefaultConsole(consoleID)

      CekRentangHitungSRR(config, tglAwal, tglAkhir)
      
      #main task right here
      Main(config, tglAwalProses, tglAwal, tglAkhir, needSaving)

      app.WriteConsole(sJobName + ': telah selesai\r\n')
    finally:
      app.CloseConsole(consoleID)
  except:
    app.WriteConsole(sJobName + ': Error\r\n' + str(sys.exc_info()[1]) + '\r\n')
    raise
