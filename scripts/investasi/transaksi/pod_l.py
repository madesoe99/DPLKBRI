# pod_l.py
# menjalankan proses akhir hari
# - melakukan rollover semua deposito yang ARO
# - menutup semua deposito yang bukan ARO dan bukan konfirmasi (yang statusnya pindah buku)
# - melakukan kapitalisir semua deposito ARO yang treatment-nya kapitalisir

import com.ihsan.util.modman as modman

#moduleapi = modman.getModule(config, 'moduleapi')
#rolloverinv_auth = modman.getModule(config, 'rolloverinv_auth')

def resSelectDeposito(config, strToday):
  # select deposito jatuh tempo yang treatment pokoknya ARO atau pindah buku (tutup langsung)

  strSQL = \
    'select i.id_investasi, tgl_jatuh_tempo '\
    'from Deposito d, Investasi i '\
    'where d.id_investasi = i.id_investasi '\
    '  and i.status = \'T\' '\
    '  and (d.treatmentPokok in (\'A\', \'P\')) '\
    '  and datediff(day, tgl_jatuh_tempo, \'%s\') >= 0 '\
    % (strToday)
  return config.CreateSQL(strSQL).RawResult

def CreateRolloverDeposito(config, oDeposito, ID_TransactionBatch):
  # rollover untuk deposito yang berstatus ARO

  oRolloverDeposito = config.CreatePObject('RolloverDeposito')
  oRolloverDeposito.LDeposito = oDeposito
  oRolloverDeposito.no_bilyet = oDeposito.no_bilyet
  oRolloverDeposito.kode_jns_investasi = oDeposito.kode_jns_investasi
  oRolloverDeposito.kode_jenis_trinvestasi = 'F' # rollover
  oRolloverDeposito.ID_TransactionBatch = ID_TransactionBatch
  oRolloverDeposito.lakukan_kapitalisir = oDeposito.kapitalisir_rollover
  oRolloverDeposito.tgl_transaksi = config.Now()
  oRolloverDeposito.isCommitted = 'T'

  oRolloverDeposito.mutasi_debet = oDeposito.akum_piutangLR
  oRolloverDeposito.mutasi_kredit = 0.0

  oRolloverDeposito.tgl_sistem = config.Now()
  oRolloverDeposito.tgl_otorisasi = config.Now()
  oRolloverDeposito.user_id = config.SecurityContext.userid
  oRolloverDeposito.user_id_auth = config.SecurityContext.userid
  oRolloverDeposito.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oRolloverDeposito.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]

  return oRolloverDeposito

def CreateTutupDeposito(config, oDeposito, ID_TransactionBatch):
  oTutupDeposito = config.CreatePObject('TutupDeposito')
  oTutupDeposito.LDeposito = oDeposito
  oTutupDeposito.no_bilyet = oDeposito.no_bilyet
  oTutupDeposito.kode_jns_investasi = oDeposito.kode_jns_investasi
  oTutupDeposito.kode_jenis_trinvestasi = 'C' # tutup deposito
  oTutupDeposito.ID_TransactionBatch = ID_TransactionBatch
  oTutupDeposito.tgl_transaksi = config.Now()
  oTutupDeposito.isCommitted = 'T'

  # set nomor rekening pencairan
  oTutupDeposito.no_rekening = oDeposito.no_rekening

  oTutupDeposito.mutasi_debet = 0.0
  oTutupDeposito.mutasi_kredit = oTutupDeposito.LDeposito.akum_nominal

  oTutupDeposito.biaya = 0.0
  oTutupDeposito.penalti = 0.0
  oTutupDeposito.isPenalti = 'F'

  oTutupDeposito.tgl_sistem = config.Now()
  oTutupDeposito.tgl_otorisasi = config.Now()
  oTutupDeposito.user_id = config.SecurityContext.userid
  oTutupDeposito.user_id_auth = config.SecurityContext.userid
  oTutupDeposito.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oTutupDeposito.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]

  oDeposito.akum_nominal = 0.0
  oDeposito.status = 'F'

def DAFLongScriptMain(config, parameter, pid, monfilename):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # pid: Process ID of this script
  # monfilename: Monitor file name to store status

  moduleapi = modman.getModule(config, 'moduleapi')
  rolloverinv_auth = modman.getModule(config, 'rolloverinv_auth')
  
  appObj = config.GetAppObject()
  appObj.WriteConsole('\r\n===================')
  appObj.WriteConsole('\r\nMulai POD Investasi %s.' % (config.FormatDateTime('d-m-yyyy hh:nn:ss', config.Now())))
  appObj.WriteConsole('\r\nBatch Investasi: %s' % (str(parameter.FirstRecord.ID_TransactionBatch)))

  config.BeginTransaction()
  try:
    resSQL = resSelectDeposito(config, config.FormatDateTime('yyyy-mm-dd', config.Now()))
    nbOfDoc = resSQL.RecordCount
    resSQL.First()
    i = 1
    while not resSQL.Eof:

      oDeposito = config.CreatePObjImplProxy('Deposito')
      oDeposito.Key = resSQL.id_investasi

      oJenisInvestasi = config.CreatePObjImplProxy('JenisInvestasi')
      oJenisInvestasi.Key = oDeposito.kode_jns_investasi
      jenisInv = ''
      if not oJenisInvestasi.IsNull:
        jenisInv = oJenisInvestasi.nama_jns_investasi

      ##jenisInv = oDeposito.LRincianPaketInvestasi.LJenisInvestasi.nama_jns_investasi
      appObj.WriteConsole('\r\nPemrosesan %d dari %d: %s %s' % (i, nbOfDoc, jenisInv or '', oDeposito.no_bilyet or ''))

      if oDeposito.treatmentPokok == 'A':
        # ARO
        appObj.WriteConsole('\r\n  Rollover')
        moduleapi.AdvanceJatuhTempo(config, oDeposito)
        if oDeposito.kapitalisir_rollover == 'T':
          appObj.WriteConsole(' Kapitalisir')
          # kapitalisir bagi hasil
          # menambah akum nominal (piutang investasi)
          oRolloverDeposito = CreateRolloverDeposito(config, oDeposito, parameter.FirstRecord.ID_TransactionBatch)
          # mengurangi akum piutangLR (piutang pendapatan)
          rolloverinv_auth.CreateTransPiutangLRInvestasi(config, 1, oDeposito, parameter.FirstRecord.ID_TransactionBatch, oRolloverDeposito)
          # update nilai2 akumulasi di deposito
          oDeposito.akum_nominal += oDeposito.akum_piutangLR
        else:
          appObj.WriteConsole(' Non-Kapitalisir')
          # mengurangi akum piutangLR (piutang pendapatan)
          rolloverinv_auth.CreateTransPiutangLRInvestasi(config, 0, oDeposito, parameter.FirstRecord.ID_TransactionBatch)
      else:
        # resSQL.treatmentPokok == 'P'
        # treatmentPokok == pindah buku
        # tutup deposito
        appObj.WriteConsole('\r\n  Tutup Deposito')
        CreateTutupDeposito(config, oDeposito, parameter.FirstRecord.ID_TransactionBatch)

      oDeposito.akum_piutangLR = 0.0
      oDeposito.last_update = config.Now()

      resSQL.Next()
      i += 1

    # end while

    config.Commit()
    appObj.WriteConsole('\r\nPOD berhasil.')
  except:
    config.Rollback()
    appObj.WriteConsole('\r\nPOD gagal: '+ str(sys.exc_info()[1]))
    raise

  appObj.WriteConsole('\r\n===================')

  #return 1
