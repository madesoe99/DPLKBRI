import sys, re
import dafdb
import com.ihsan.lib.trace as trace
sys.path.append('c:/dafapp/dplk07/script_modules')
import confKiblat
import moduleapi as mod
kiblatConfFile = confKiblat.kiblatConfFile
kiblatConfLiab = confKiblat.kiblatConfLiab

def SavePacket(config, rHistori, oHistoriGiroHarian, acc_giro):
  rHistori.First()
  while not rHistori.Eof():
    #buat objek HistoriGiro
    oHG = config.CreatePObject('HistoriGiro')
    oHG.acc_giro = acc_giro
    oHG.ID_HistoriGiroHarian = oHistoriGiroHarian.ID_HistoriGiroHarian
    batch = rHistori.GetFieldValue('Nomor_Batch') or ''
    oHG.Nomor_Batch_CoreBanking =  batch[:30]
#     oHG.Nomor_Urut = rHistori.GetFieldValue('Id_Detil_Transaksi') or ''
    noref = rHistori.GetFieldValue('Nomor_Referensi') or ''
    if noref[0:3]=='DP_':
      oHG.Nomor_Urut = noref
    else:
      oHG.Nomor_Urut = rHistori.GetFieldValue('Id_Detil_Transaksi') or ''      
    #oHG.Nomor_Urut = (noref + '|' + str(rHistori.GetFieldValue('Id_Detil_Transaksi')))[:50]
    oHG.Nomor_Referensi = noref[:20] 
    oHG.Kode_Mnemonic = rHistori.GetFieldValue('Jenis_Mutasi') or ''
    oHG.Nominal = float(rHistori.GetFieldValue('Nilai_Mutasi')) or 0.0
    if rHistori.GetFieldValue('IsBillerTransaction') == 'T' or (noref[0:3]=='DP_'):
      oHG.Transaksi_Peserta = 1
    else:
      oHG.Transaksi_Peserta = 0
    oHG.isTransaksiCreated = 'F'
    
    #proses nomor peserta (lebih baik pake Regex)
    ket = rHistori.GetFieldValue('Keterangan') or ''
    if re.search('[0-9]+', ket):
      r = re.search('[0-9]+', ket)
      if len(r.group()) == 10:
        nomrek = r.group()
        ket = ket.replace(nomrek, '')
        if re.search('[0-9]+', ket):
          r = re.search('[0-9]+', ket)
          if len(r.group()) == 11:
            oHG.Nomor_Peserta = r.group()
      elif len(r.group()) == 11:
        oHG.Nomor_Peserta = r.group()

    oHG.Keterangan = ket
    rHistori.Next()

def Main(config, dtTglTransaksi):
  try:    
    conn = dafdb.getDBConnection(kiblatConfFile, kiblatConfLiab)
    conn.Connect()    
  
    #ambil info semua giro DPLK
    sSQL = "SELECT acc_giro, acc_histori_giro, no_giro \
            FROM MasterGiro \
            ORDER by acc_giro"
    rSQL = config.CreateSQL(sSQL).RawResult
    rSQL.First()
    while not rSQL.Eof:
      oraTglTransaksi = mod.FormatDateOracle(config.ModLibUtils.DecodeDate(dtTglTransaksi)) 
      rHistori = GetHistoriGiro(conn, rSQL.no_giro, oraTglTransaksi)
      config.SendDebugMsg(rSQL.no_giro)
      if not rHistori.Eof():
        #buat objek oHistoriGiroHarian
        oHGH = config.CreatePObject('HistoriGiroHarian')
        oHGH.Tanggal_Histori = dtTglTransaksi
        oHGH.acc_giro = rSQL.acc_giro
        oHGH.isReconciled = oHGH.isTransactionProceed = 'F'
        config.FlushUpdates()
        SavePacket(config, rHistori, oHGH, rSQL.acc_giro)
  
      rSQL.Next()
    
  finally:
    conn.Disconnect()
  
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
  A.Nomor_Referensi, C.Nomor_Batch, \
  A.IsBillerTransaction \
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
#   import rpdb2; rpdb2.start_embedded_debugger("000")
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
