import sys
import com.ihsan.lib.trace as trace
sys.path.append('c:/dafapp/dplk07/script_modules')

# global variabel
RECONCILE_DIR = 'c:/dafapp/dplk07/file_reconcile/'

def SavePacket(config, rowList, oHistoriGiroHarian):
  # sususan rowList: 0-Nomor_Batch, 1-Id_Detil_Transaksi, 2-RefBiller, 3-VAPrefix,
  # 4-VANumber, 5-Nomor_Rekening, 6-Jenis_Mutasi, 7-Nilai_Mutasi, 8-Kode_Cabang,
  # 9-Keterangan

  #buat objek HistoriGiro
  oHG = config.CreatePObject('HistoriGiro')
  oHG.acc_giro = oHistoriGiroHarian.acc_giro
  oHG.ID_HistoriGiroHarian = oHistoriGiroHarian.ID_HistoriGiroHarian
  oHG.Nomor_Batch_CoreBanking = rowList[0] or ''
  oHG.Nomor_Urut = rowList[1] or ''
  oHG.Nomor_Referensi = rowList[1] or ''
  oHG.Kode_Mnemonic = rowList[6] or ''
  oHG.Nominal = float(rowList[7]) or 0.0
  oHG.Transaksi_Peserta = 0 # sd tgl 10 mei pasti dr kiblat, bkn dr aplikasi
  oHG.isTransaksiCreated = 'F'
  oHG.Nomor_Peserta = rowList[4]
  oHG.Keterangan = rowList[9]

def Main(config, dtTglTransaksi):
  try:    
    #ambil info semua giro DPLK dan masukkan ke dictNoGiro
    sSQL = "SELECT acc_giro, acc_histori_giro, no_giro \
            FROM MasterGiro \
            ORDER by acc_giro"
    rSQL = config.CreateSQL(sSQL).RawResult
    dictNoGiro = {}
    rSQL.First()
    while not rSQL.Eof:
      dictNoGiro[rSQL.no_giro] = [rSQL.acc_giro, rSQL.acc_histori_giro]
      rSQL.Next()
    # end while
    
    tglRekon = config.ModLibUtils.DecodeDate(dtTglTransaksi)
    tglRekon = str(tglRekon[2]) + '-' + str(tglRekon[1]) + '-' + str(tglRekon[0])
    listObjectHGHCreated = {}
    # ambil file reconcile
    try:
      fOpen = open(RECONCILE_DIR+'DplkRekon-'+str(tglRekon)+'.txt','r')
      s = fOpen.readline()
      while s != '':
        s = s[:-1] # menghilangkan tanda '\n' di akhir string 
        rowList = s.split('|')
        # sususan rowList: 0-Nomor_Batch, 1-Id_Detil_Transaksi, 2-RefBiller, 3-VAPrefix,
        # 4-VANumber, 5-Nomor_Rekening, 6-Jenis_Mutasi, 7-Nilai_Mutasi, 8-Kode_Cabang,
        # 9-Keterangan

        # cek objek HistoriGiroHarian
        if not listObjectHGHCreated.has_key(rowList[5]):
          # objek HistoriGiroHarian untuk Nomor Rekening belum dibuatkan
          # buat objek HistoriGiroHarian
          oHGH = config.CreatePObject('HistoriGiroHarian')
          oHGH.Tanggal_Histori = dtTglTransaksi
          oHGH.acc_giro = dictNoGiro[rowList[5]][0]
          oHGH.isReconciled = oHGH.isTransactionProceed = 'F'

          # flush to database
          config.FlushUpdates()
          
          # tambahkan objek HGH dalam listObjectHGHCreated
          listObjectHGHCreated[rowList[5]] = oHGH

        else:
          # objek HistoriGiroHarian sudah dibuat, akses objeknya
          oHGH = listObjectHGHCreated[rowList[5]]
          
        # buat objek HistoriGiro
        SavePacket(config, rowList, oHGH)
        
        # next file content
        s = fOpen.readline()
      
    finally:
      fOpen.close()

  except:
    raise

  return 1

def UpdateNominalSum(config, dtTglTransaksi):
  y,m,d = config.ModLibUtils.DecodeDate(dtTglTransaksi)[:3]
  sSQL = 'update HISTORIGIROHARIAN \
          set HISTORIGIROHARIAN.SUM_NOMINAL = \
              (select x.snk-x.snd as sum_nominal \
               from (select sum_kredit.ID_HISTORIGIROHARIAN, \
                            isnull(sum_kredit.sum_nominal_kredit,0.0) as snk, \
                            isnull(sum_debit.sum_nominal_debit,0.0) as snd \
                     from (select SUM(hg.NOMINAL) as sum_nominal_kredit, \
                                  hg.ID_HISTORIGIROHARIAN \
                           from HISTORIGIRO hg \
                           where hg.KODE_MNEMONIC = \'C\' \
                           group by hg.ID_HISTORIGIROHARIAN) as sum_kredit \
                          full outer join \
                          (select SUM(hg.NOMINAL) as sum_nominal_debit, \
                                  hg.ID_HISTORIGIROHARIAN \
                           from HISTORIGIRO hg \
                           where hg.KODE_MNEMONIC = \'D\' \
                           group by hg.ID_HISTORIGIROHARIAN) as sum_debit \
                          on sum_debit.ID_HISTORIGIROHARIAN = \
                          sum_kredit.ID_HISTORIGIROHARIAN) as x \
               where x.ID_HISTORIGIROHARIAN = HISTORIGIROHARIAN.ID_HISTORIGIROHARIAN) \
          where HISTORIGIROHARIAN.TANGGAL_HISTORI = \'%s\'' \
          % ('%d-%d-%d' % (y,m,d))
  rSQL = config.ExecSQL(sSQL)

  return 1

def GetHistoriGiro(conn, Nomor_Rekening, Tgl_Transaksi):
  query = "SELECT to_char(A.Id_Detil_Transaksi) as Id_Detil_Transaksi, \
  A.Keterangan, A.Jenis_Mutasi, \
  to_char(A.Nilai_Mutasi) as Nilai_Mutasi, \
  A.Nomor_Referensi, C.Nomor_Batch \
  FROM \
  HistDetilTransaksi A,\
  HistTransaksi B,\
  BatchTransaksi C\
  WHERE A.Id_Transaksi = B.Id_Transaksi \
  AND B.Id_Batch_Transaksi = C.Id_Batch_Transaksi \
  AND A.Nomor_Rekening = '%s' \
  AND A.Tanggal_Transaksi = '%s' \
  ORDER BY \
  A.Id_Detil_Transaksi ASC" % (Nomor_Rekening, Tgl_Transaksi)

  trace.udp_trace(query)
  rHistori = conn.GetQuery(query)    
  
  return rHistori

def DAFLongScriptMain(config, parameter, pid, monfilename):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # pid: Process ID of this script
  # monfilename: Monitor file name to store status

  #import rpdb2; rpdb2.start_embedded_debugger("000")

  app = config.AppObject
  dtTglTransaksi = parameter.FirstRecord.tglTransaksi
  y,m,d = config.ModLibUtils.DecodeDate(dtTglTransaksi)
  tTglTransaksi = [y,m,d]
  
  consoleID = 'GetHistoriGiro_' + str(pid)

  sJobName = '%s. TaskID = %s' % ('Ambil Riwayat Giro DPLK',pid)
  app.WriteConsole(sJobName + ': mulai berlangsung\r\n')
  try:
    app.CreateConsole(consoleID, 'progress')
    try:
      app.SwitchDefaultConsole(consoleID)

      #main task right here
      config.BeginTransaction()
      try:
        Main(config, dtTglTransaksi)
        config.FlushUpdates()
        UpdateNominalSum(config, dtTglTransaksi)

        config.Commit()
      except:
        config.Rollback()
        raise

      app.WriteConsole(sJobName + ': telah selesai\r\n')
    finally:
      app.CloseConsole(consoleID)
  except:
    app.WriteConsole(sJobName + ': Error\r\n' + str(sys.exc_info()[1]) + '\r\n')
    raise
