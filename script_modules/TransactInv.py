import com.ihsan.util.modman as modman
modman.loadStdModules(globals(), 
  [
    "moduleapi"
  ]
)

def ListToFloatDate(config, LsInt) :
  y,m,d = LsInt[:3]
  return config.ModDateTime.EncodeDate(y,m,d)

def CreateSPI(config, nama, oInvestasi, oTransInduk, prof, kode_jenis_trinvestasi, Batch = '', tgltrans = ''):
# pendapatan (atau biaya) beli obligasi sebagai selisih dari nominal_jual
  if prof == 0.0 :
    return 0
  config.SendDebugMsg('SPI1:'+kode_jenis_trinvestasi)
  oSPI = config.CreatePObject('TransaksiSPInvestasi')
  oSPI.kode_jenis_trinvestasi = kode_jenis_trinvestasi
  config.SendDebugMsg('SPI12:'+str(oInvestasi.id_investasi))
  oSPI.LInvestasi = oInvestasi
  oSPI.nama_investasi = nama
  config.SendDebugMsg('SPI13:'+str(oInvestasi.kode_jns_investasi))
  if Batch == '' :
    oSPI.LTransactionBatch = oTransInduk.LTransactionBatch
  else :
    oSPI.LTransactionBatch = Batch
  oSPI.kode_jns_investasi = oInvestasi.kode_jns_investasi
  #oSPI.nominal = prof
  #oPendapatanObligasi.no_rekening = oRegisterObligasi.no_rekening

  config.SendDebugMsg('SPI2')
  if prof >= 0.0:
    # pendapatan
    oSPI.mutasi_debet = prof
    oSPI.mutasi_kredit = 0.0
  else:
    # biaya
    oSPI.mutasi_debet = 0.0
    oSPI.mutasi_kredit = -prof

  oSPI.isCommitted = 'T'

  config.SendDebugMsg('SPI3')
  if tgltrans == '' :
    oSPI.tgl_transaksi = moduleapi.DateTimeTupleToFloat(config, oTransInduk.tgl_transaksi)
    oSPI.LIndukTransaksiInvestasi = oTransInduk
    oSPI.user_id = oTransInduk.user_id
    oSPI.terminal_id = oTransInduk.terminal_id
  else :
    oSPI.tgl_transaksi = tgltrans
    oSPI.user_id = Batch.user_id_owner
    oSPI.terminal_id = Batch.terminal_id_create
    
  oSPI.tgl_sistem = config.Now()
  oSPI.tgl_otorisasi = config.Now()


  config.SendDebugMsg('SPI4')
  oSPI.user_id_auth = config.SecurityContext.userid
  oSPI.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]
  oSPI.no_bilyet = oInvestasi.no_bilyet
  
  oSPI.saldo_awal = (oInvestasi.akum_SPI or 0.0)
  oInvestasi.akum_SPI = oSPI.saldo_awal + prof
  config.SendDebugMsg('SPI5')
  return oSPI

def CreateSPINoBatch(config, nama, oInvestasi, oTransInduk, prof, kode_jenis_trinvestasi, tgltrans = ''):
# pendapatan (atau biaya) beli obligasi sebagai selisih dari nominal_jual
  if prof == 0.0 :
    return 0
  config.SendDebugMsg('SPI1:'+kode_jenis_trinvestasi)
  oSPI = config.CreatePObject('TransaksiSPInvestasi')
  oSPI.kode_jenis_trinvestasi = kode_jenis_trinvestasi
  config.SendDebugMsg('SPI12:'+str(oInvestasi.id_investasi))
  oSPI.LInvestasi = oInvestasi
  oSPI.nama_investasi = nama
  config.SendDebugMsg('SPI13:'+str(oInvestasi.kode_jns_investasi))
  oSPI.kode_jns_investasi = oInvestasi.kode_jns_investasi
  #oSPI.nominal = prof
  #oPendapatanObligasi.no_rekening = oRegisterObligasi.no_rekening

  config.SendDebugMsg('SPI2')
  if prof >= 0.0:
    # pendapatan
    oSPI.mutasi_debet = prof
    oSPI.mutasi_kredit = 0.0
  else:
    # biaya
    oSPI.mutasi_debet = 0.0
    oSPI.mutasi_kredit = -prof

  oSPI.isCommitted = 'T'

  config.SendDebugMsg('SPI3')
  if tgltrans == '' :
    oSPI.tgl_transaksi = moduleapi.DateTimeTupleToFloat(config, oTransInduk.tgl_transaksi)
    oSPI.LIndukTransaksiInvestasi = oTransInduk
    oSPI.user_id = oTransInduk.user_id
    oSPI.terminal_id = oTransInduk.terminal_id
  else :
    oSPI.tgl_transaksi = tgltrans
    oSPI.user_id = config.SecurityContext.userid
    oSPI.terminal_id = config.SecurityContext.GetSessionInfo()[1]
    
  oSPI.tgl_sistem = config.Now()
  oSPI.tgl_otorisasi = config.Now()

  config.SendDebugMsg('SPI4')
  oSPI.user_id_auth = config.SecurityContext.userid
  oSPI.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]
  oSPI.no_bilyet = oInvestasi.no_bilyet
  
  oSPI.saldo_awal = (oInvestasi.akum_SPI or 0.0)
  oInvestasi.akum_SPI = oSPI.saldo_awal + prof
  config.SendDebugMsg('SPI5')
  return oSPI
  
def CreatePNI(config, nama, oInvestasi, oTransInduk, prof, kode_jenis_trinvestasi, Batch = '', tgltrans = ''):
# pendapatan (atau biaya) beli obligasi sebagai selisih dari nominal_jual
  if prof == 0.0 :
    return 0
  oPNI = config.CreatePObject('TransaksiPNInvestasi')
  oPNI.kode_jenis_trinvestasi = kode_jenis_trinvestasi # pendapatan/biaya obligasi
  oPNI.LInvestasi = oInvestasi
  oPNI.nama_investasi = nama
  if Batch == '' :
    oPNI.LTransactionBatch = oTransInduk.LTransactionBatch
  else :
    oPNI.LTransactionBatch = Batch
  oPNI.kode_jns_investasi = oInvestasi.kode_jns_investasi
  #oPNI.nominal = prof
  #oPendapatanObligasi.no_rekening = oRegisterObligasi.no_rekening

  if prof >= 0.0:
    # pendapatan
    oPNI.mutasi_debet = 0.0
    oPNI.mutasi_kredit = prof
  else:
    # biaya
    oPNI.mutasi_debet = -prof
    oPNI.mutasi_kredit = 0.0

  oPNI.isCommitted = 'T'
  if tgltrans == '' :
    oPNI.tgl_transaksi = moduleapi.DateTimeTupleToFloat(config, oTransInduk.tgl_transaksi)
    oPNI.LIndukTransaksiInvestasi = oTransInduk
    oPNI.user_id = oTransInduk.user_id
    oPNI.terminal_id = oTransInduk.terminal_id
  else :
    oPNI.tgl_transaksi = tgltrans
    oPNI.user_id = Batch.user_id_owner
    oPNI.terminal_id = Batch.terminal_id_create
    
  oPNI.tgl_sistem = config.Now()
  oPNI.tgl_otorisasi = config.Now()
  oPNI.user_id_auth = config.SecurityContext.userid
  oPNI.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]
  oPNI.no_bilyet = oInvestasi.no_bilyet
  oPNI.LIndukTransaksiInvestasi = oTransInduk

  oPNI.saldo_awal = (oInvestasi.akum_PNI or 0.0)
  oInvestasi.akum_PNI = oPNI.saldo_awal + prof
  return oPNI

def CreatePNINoBatch(config, nama, oInvestasi, oTransInduk, prof, kode_jenis_trinvestasi, tgltrans = ''):
# pendapatan (atau biaya) beli obligasi sebagai selisih dari nominal_jual
  if prof == 0.0 :
    return 0
  oPNI = config.CreatePObject('TransaksiPNInvestasi')
  oPNI.kode_jenis_trinvestasi = kode_jenis_trinvestasi # pendapatan/biaya obligasi
  oPNI.LInvestasi = oInvestasi
  oPNI.nama_investasi = nama
  oPNI.kode_jns_investasi = oInvestasi.kode_jns_investasi
  #oPNI.nominal = prof
  #oPendapatanObligasi.no_rekening = oRegisterObligasi.no_rekening

  if prof >= 0.0:
    # pendapatan
    oPNI.mutasi_debet = 0.0
    oPNI.mutasi_kredit = prof
  else:
    # biaya
    oPNI.mutasi_debet = -prof
    oPNI.mutasi_kredit = 0.0

  oPNI.isCommitted = 'T'
  if tgltrans == '' :
    oPNI.tgl_transaksi = moduleapi.DateTimeTupleToFloat(config, oTransInduk.tgl_transaksi)
    oPNI.LIndukTransaksiInvestasi = oTransInduk
    oPNI.user_id = oTransInduk.user_id
    oPNI.terminal_id = oTransInduk.terminal_id
  else :
    oPNI.tgl_transaksi = tgltrans
    oPNI.user_id = config.SecurityContext.userid
    oPNI.terminal_id = config.SecurityContext.GetSessionInfo()[1]
    
  oPNI.tgl_sistem = config.Now()
  oPNI.tgl_otorisasi = config.Now()
  oPNI.user_id_auth = config.SecurityContext.userid
  oPNI.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]
  oPNI.no_bilyet = oInvestasi.no_bilyet
  oPNI.LIndukTransaksiInvestasi = oTransInduk

  oPNI.saldo_awal = (oInvestasi.akum_PNI or 0.0)
  oInvestasi.akum_PNI = oPNI.saldo_awal + prof
  return oPNI
  
def CreatePendapatanReksadana(config, oRedemptReksadana):
# pendapatan (atau biaya) redempt reksadana sebagai selisih dari NAB
# pendapatan diperoleh secara tunai, maka tidak menggunakan transpiutanglrinv
  
  oReksadana = oRedemptReksadana.LReksadana

  oPendapatanReksadana = config.CreatePObject('PendapatanReksadana')
  oPendapatanReksadana.kode_jenis_trinvestasi = 'R' # pendapatan/biaya redempt reksadana
  oPendapatanReksadana.LReksadana = oReksadana
  oPendapatanReksadana.LTransactionBatch = oRedemptReksadana.LTransactionBatch
  oPendapatanReksadana.kode_jns_investasi = oRedemptReksadana.kode_jns_investasi
  oPendapatanReksadana.tgl_transaksi = oRedemptReksadana.tgl_transaksi
  oPendapatanReksadana.nominal = oRedemptReksadana.profit
  oPendapatanReksadana.no_rekening = oRedemptReksadana.no_rekening

  if oRedemptReksadana.profit >= 0.0:
    # pendapatan
    oPendapatanReksadana.kode_subjns_LRInvestasi = 'C-PROF' # pendapatan reksadana
    oPendapatanReksadana.mutasi_debet = 0.0
    oPendapatanReksadana.mutasi_kredit = oRedemptReksadana.profit
  else:
    oPendapatanReksadana.kode_subjns_LRInvestasi = 'C-COST' # biaya reksadana
    oPendapatanReksadana.mutasi_debet = -oRedemptReksadana.profit
    oPendapatanReksadana.mutasi_kredit = 0.0

  oPendapatanReksadana.isCommitted = 'T'
  oPendapatanReksadana.nama_investasi = oReksadana.nama_reksadana
  oPendapatanReksadana.tgl_sistem = oRedemptReksadana.tgl_sistem
  oPendapatanReksadana.tgl_otorisasi = oRedemptReksadana.tgl_otorisasi
  oPendapatanReksadana.user_id = oRedemptReksadana.user_id
  oPendapatanReksadana.user_id_auth = oRedemptReksadana.user_id_auth
  oPendapatanReksadana.terminal_id = oRedemptReksadana.terminal_id
  oPendapatanReksadana.terminal_id_auth = oRedemptReksadana.terminal_id_auth

  # update saldo laba rugi
  oReksadana.akum_LR += oRedemptReksadana.profit
  oReksadana.akum_piutangLR -= oRedemptReksadana.profit
  
  TransactInv.CreateRincianBagiHasil(config, oReksadana, oRedemptReksadana.profit)
  return oPendapatanReksadana

def CreatePendapatanSaham(config, oRedemptSaham):
# pendapatan (atau biaya) redempt Saham sebagai selisih dari NAB
# pendapatan diperoleh secara tunai, maka tidak menggunakan transpiutanglrinv
  
  oSaham = oRedemptSaham.LSaham

  oPendapatanSaham = config.CreatePObject('PendapatanSaham')
  oPendapatanSaham.kode_jenis_trinvestasi = 'R' # pendapatan/biaya redempt Saham
  oPendapatanSaham.LSaham = oSaham
  oPendapatanSaham.LTransactionBatch = oRedemptSaham.LTransactionBatch
  oPendapatanSaham.kode_jns_investasi = oRedemptSaham.kode_jns_investasi
  oPendapatanSaham.tgl_transaksi = oRedemptSaham.tgl_transaksi
  oPendapatanSaham.nominal = oRedemptSaham.profit
  oPendapatanSaham.no_rekening = oRedemptSaham.no_rekening

  if oRedemptSaham.profit >= 0.0:
    # pendapatan
    oPendapatanSaham.kode_subjns_LRInvestasi = 'C-PROF' # pendapatan Saham
    oPendapatanSaham.mutasi_debet = 0.0
    oPendapatanSaham.mutasi_kredit = oRedemptSaham.profit
  else:
    oPendapatanSaham.kode_subjns_LRInvestasi = 'C-COST' # biaya Saham
    oPendapatanSaham.mutasi_debet = -oRedemptSaham.profit
    oPendapatanSaham.mutasi_kredit = 0.0

  oPendapatanSaham.isCommitted = 'T'
  oPendapatanSaham.nama_investasi = oSaham.nama_Saham
  oPendapatanSaham.tgl_sistem = oRedemptSaham.tgl_sistem
  oPendapatanSaham.tgl_otorisasi = oRedemptSaham.tgl_otorisasi
  oPendapatanSaham.user_id = oRedemptSaham.user_id
  oPendapatanSaham.user_id_auth = oRedemptSaham.user_id_auth
  oPendapatanSaham.terminal_id = oRedemptSaham.terminal_id
  oPendapatanSaham.terminal_id_auth = oRedemptSaham.terminal_id_auth

  # update saldo laba rugi
  oSaham.akum_LR += oRedemptSaham.profit
  oSaham.akum_piutangLR -= oRedemptSaham.profit
  
  TransactInv.CreateRincianBagiHasil(config, oSaham, oRedemptSaham.profit)
  return oPendapatanSaham
  
def CheckUpdateNAB (config, TglInput, oReksa) :
  Stat = False
  strSQL = 'Select * from HistNABReksadana \
          where id_investasi = %d and UserOto Is not Null \
          and NAB <> 0.0 order by HistNABReksadanaID desc ' \
          % oReksa.id_investasi
  rSQL = config.CreateSQL(strSQL).RawResult
  rSQL.First()
  if not rSQL.Eof :
    y,m,d = rSQL.Tgl_Penetapan[:3]
    TglUbah = config.ModDateTime.EncodeDate(y,m,d)
    if type(TglInput) != type(0.0) :
      y,m,d = TglInput[:3]
      TglInput = config.ModDateTime.EncodeDate(y,m,d)  
    Stat =  int(TglUbah) >= int(TglInput) 
  return Stat

def CheckUpdateNABSaham (config, TglInput, oSaham) :
  Stat = False
  strSQL = 'Select * from HistNABSaham \
          where id_investasi = %d and UserOto Is not Null \
          and NAB <> 0.0 order by HistNABSahamID desc ' \
          % oSaham.id_investasi
  rSQL = config.CreateSQL(strSQL).RawResult
  rSQL.First()
  if not rSQL.Eof :
    y,m,d = rSQL.Tgl_Penetapan[:3]
    TglUbah = config.ModDateTime.EncodeDate(y,m,d)
    if type(TglInput) != type(0.0) :
      y,m,d = TglInput[:3]
      TglInput = config.ModDateTime.EncodeDate(y,m,d)  
    Stat =  int(TglUbah) >= int(TglInput) 
  return Stat

def CheckUpdateUPReksa(config, TglInput, oReksa, mode) :
  Stat = False
  if mode :
    oLast = GetLastRedemt(config, oReksa)
  else :
    oLast = GetLastHistReksadana(config, oReksa)
  y,m,d = oLast.tgl_transaksi[:3]
  TglTrans = config.ModDateTime.EncodeDate(y,m,d)
  if type(TglInput) != type(0.0) :
    y,m,d = TglInput[:3]
    TglInput = config.ModDateTime.EncodeDate(y,m,d)  
  Stat =  int(TglTrans) == int(TglInput) 
  return Stat

def CheckUpdateUPSaham(config, TglInput, oReksa, mode) :
  Stat = False
  if mode :
    oLast = GetLastRedemtSaham(config, oReksa)
  else :
    oLast = GetLastHistSaham(config, oReksa)
  y,m,d = oLast.tgl_transaksi[:3]
  TglTrans = config.ModDateTime.EncodeDate(y,m,d)
  if type(TglInput) != type(0.0) :
    y,m,d = TglInput[:3]
    TglInput = config.ModDateTime.EncodeDate(y,m,d)  
  Stat =  int(TglTrans) == int(TglInput) 
  return Stat
  
def GetLastRedemt(config, oReksa) :
  strSQL = 'Select * from RedemptReksadana r, TransaksiInvestasi t \
            where id_investasi = %d and r.id_transaksiinvestasi = t.id_transaksiinvestasi\
            order by t.id_transaksiinvestasi desc ' \
            % oReksa.id_investasi
  
  rSQL = config.CreateSQL(strSQL).RawResult
  rSQL.First()
  oRR = config.CreatePObjImplProxy('RedemptReksadana')
  if rSQL.Eof :
    oRR.Key = 0
  else :
    oRR.Key = rSQL.id_transaksiinvestasi
   
  return oRR

def GetLastRedemtSaham(config, oSaham) :
  strSQL = 'Select * from RedemptSaham r, TransaksiInvestasi t \
            where id_investasi = %d and r.id_transaksiinvestasi = t.id_transaksiinvestasi\
            order by t.id_transaksiinvestasi desc ' \
            % oSaham.id_investasi
  config.SendDebugMsg('sSQL GetLastRedemtSaham = %s' % strSQL)
  rSQL = config.CreateSQL(strSQL).RawResult
  rSQL.First()
  oRR = config.CreatePObjImplProxy('RedemptSaham')
  if rSQL.Eof :
    oRR.Key = 0
  else :
    oRR.Key = rSQL.id_transaksiinvestasi
   
  return oRR
  
def GetLastHistReksadana(config, oReksa) :
  strSQL = 'Select * from SubscribeReksadana s, TransaksiInvestasi t \
            where id_investasi = %d and t.id_transaksiinvestasi = s.id_transaksiinvestasi \
            order by t.id_transaksiinvestasi desc ' \
            % oReksa.id_investasi
  rSQL = config.CreateSQL(strSQL).RawResult
  rSQL.First()
  oHR = config.CreatePObjImplProxy('SubscribeReksadana')
  oHR.Key = rSQL.id_transaksiinvestasi
   
  return oHR

def GetLastHistSaham(config, oSaham) :
  strSQL = 'Select * from SubscribeSaham s, TransaksiInvestasi t \
            where id_investasi = %d and t.id_transaksiinvestasi = s.id_transaksiinvestasi \
            order by t.id_transaksiinvestasi desc ' \
            % oSaham.id_investasi
  rSQL = config.CreateSQL(strSQL).RawResult
  rSQL.First()
  oHR = config.CreatePObjImplProxy('SubscribeSaham')
  oHR.Key = rSQL.id_transaksiinvestasi
   
  return oHR
  
def CreateRincianPokok(config, oInvestasi, nom) :
  strSQL = 'Select id_rincianinvestasi \
            From RincianInvestasi \
            where id_investasi = %d ' %   oInvestasi.id_investasi
  resSQL = config.CreateSQL(strSQL).RawResult
  resSQL.First()
  while not resSQL.Eof:
    oRincianInvestasi = config.CreatePObjImplProxy('RincianInvestasi')
    oRincianInvestasi.Key = resSQL.id_rincianinvestasi

    #Update Akumulasi Bagi Hasil berdasarkan proporsi
    oRincianInvestasi.Akum_Paket += oRincianInvestasi.proporsi * nom

    resSQL.Next()

def CreateRincianBagiHasil(config, oInvestasi, nom, Ajd = False) :
  strSQL = 'Select id_rincianinvestasi \
            From RincianInvestasi \
            where id_investasi = %d ' %   oInvestasi.id_investasi
  resSQL = config.CreateSQL(strSQL).RawResult
  resSQL.First()
  while not resSQL.Eof:
    oRincianInvestasi = config.CreatePObjImplProxy('RincianInvestasi')
    oRincianInvestasi.Key = resSQL.id_rincianinvestasi

    #Update Akumulasi Bagi Hasil berdasarkan proporsi
    if Ajd :
      oRincianInvestasi.Akum_LR_Paket = oRincianInvestasi.proporsi * nom
    else :
      oRincianInvestasi.Akum_LR_Paket += oRincianInvestasi.proporsi * nom

    resSQL.Next()
