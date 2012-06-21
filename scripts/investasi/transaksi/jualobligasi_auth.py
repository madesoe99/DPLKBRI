import com.ihsan.util.modman as modman

#moduleapi = modman.getModule(config, 'moduleapi')
#TransactInv = modman.getModule(config, 'TransactInv')

def SetJualObligasi(config, oJualObligasi):
  # set nilai2 transaksi obligasi
  oObl = config.CreatePObjImplProxy('Obligasi')
  oObl.Key = oJualObligasi.id_investasi
  
  oJualObligasi.isCommitted = 'T'
  oJualObligasi.tgl_otorisasi = config.Now()
  oJualObligasi.user_id_auth = config.SecurityContext.userid
  oJualObligasi.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]
  oJualObligasi.nama_investasi = oObl.nama_obligasi#oJualObligasi.LObligasi.nama_obligasi

def CreatePendapatanTutupObligasi(config, oJualObligasi):
  # pendapatan (atau biaya) tutup obligasi sebagai selisih dari nominal_jual
  # pendapatan diperoleh secara tunai, maka tidak menggunakan transpiutanglrinv
  moduleapi = modman.getModule(config, 'moduleapi')
  
  oObl = config.CreatePObjImplProxy('Obligasi')
  oObl.Key = oJualObligasi.id_investasi
  
  oPendapatanObligasi = config.CreatePObject('PendapatanObligasi')
  oPendapatanObligasi.kode_jenis_trinvestasi = 'J' # pendapatan/biaya jual obligasi
  oPendapatanObligasi.LInvestasi = oJualObligasi.LObligasi
  oPendapatanObligasi.kode_jns_investasi = oJualObligasi.kode_jns_investasi
  oPendapatanObligasi.tgl_transaksi = moduleapi.DateTimeTupleToFloat(config, oJualObligasi.tgl_transaksi)
  oPendapatanObligasi.nominal = oJualObligasi.profit
  oPendapatanObligasi.no_rekening = oJualObligasi.no_rekening

  if oJualObligasi.profit >= 0.0:
    # pendapatan
    oPendapatanObligasi.kode_subjns_LRInvestasi = 'B-PROF' # biaya obligasi capital gain
    oPendapatanObligasi.mutasi_debet = 0.0
    oPendapatanObligasi.mutasi_kredit = oJualObligasi.profit
  else:
    oPendapatanObligasi.kode_subjns_LRInvestasi = 'B-COST' # biaya obligasi
    oPendapatanObligasi.mutasi_debet = -oJualObligasi.profit
    oPendapatanObligasi.mutasi_kredit = 0.0

  oPendapatanObligasi.isCommitted = 'T'
  oPendapatanObligasi.nama_investasi = oObl.nama_obligasi#oJualObligasi.LObligasi.nama_obligasi
  oPendapatanObligasi.tgl_sistem = moduleapi.DateTimeTupleToFloat(config, oJualObligasi.tgl_sistem)
  oPendapatanObligasi.tgl_otorisasi = moduleapi.DateTimeTupleToFloat(config, oJualObligasi.tgl_otorisasi)
  oPendapatanObligasi.user_id = oJualObligasi.user_id
  oPendapatanObligasi.user_id_auth = oJualObligasi.user_id_auth
  oPendapatanObligasi.terminal_id = oJualObligasi.terminal_id
  oPendapatanObligasi.terminal_id_auth = oJualObligasi.terminal_id_auth
  #oPendapatanObligasi.no_bilyet = oJualObligasi.LObligasi.no_bilyet

  # update saldo laba rugi
  oObligasi = oJualObligasi.LObligasi
  oObligasi.akum_LR += oJualObligasi.profit

  return oPendapatanObligasi

#Create Pendapatan dari harga beli
def CreatePendapatanObligasi(config, oObligasi, oJualObligasi, profObl):
  # pendapatan (atau biaya) beli obligasi sebagai selisih dari nominal_jual
  moduleapi = modman.getModule(config, 'moduleapi')

  oPendapatanObligasi = config.CreatePObject('PendapatanObligasi')
  oPendapatanObligasi.kode_jenis_trinvestasi = 'K' # pendapatan/biaya obligasi
  oPendapatanObligasi.LInvestasi = oObligasi
  oPendapatanObligasi.nama_investasi = oObligasi.nama_obligasi
  oPendapatanObligasi.kode_jns_investasi = oObligasi.kode_jns_investasi
  oPendapatanObligasi.nominal = profObl
  oPendapatanObligasi.no_rekening = oJualObligasi.no_rekening

  if profObl >= 0.0:
    # pendapatan
    oPendapatanObligasi.kode_subjns_LRInvestasi = 'B-PROF' # pendapatan obligasi capital gain
    oPendapatanObligasi.mutasi_debet = 0.0
    oPendapatanObligasi.mutasi_kredit = profObl
  else:
    # biaya
    oPendapatanObligasi.kode_subjns_LRInvestasi = 'B-COST' # biaya obligasi
    oPendapatanObligasi.mutasi_debet = -profObl
    oPendapatanObligasi.mutasi_kredit = 0.0

  oPendapatanObligasi.isCommitted = 'T'
  oPendapatanObligasi.tgl_transaksi = moduleapi.DateTimeTupleToFloat(config, oObligasi.tgl_buka)
  oPendapatanObligasi.tgl_sistem = config.Now()
  oPendapatanObligasi.tgl_otorisasi = config.Now()
  oPendapatanObligasi.user_id = oObligasi.user_id
  oPendapatanObligasi.user_id_auth = oObligasi.user_id_auth
  oPendapatanObligasi.terminal_id = oObligasi.terminal_id
  oPendapatanObligasi.terminal_id_auth = oObligasi.terminal_id_auth
  oPendapatanObligasi.no_bilyet = oObligasi.no_bilyet

  oObligasi.akum_LR += profObl

  return oPendapatanObligasi

# biaya tutup obligasi
def CreateBiayaObligasi(config, oJualObligasi):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  oTransLRInvestasi = config.CreatePObject('TransLRInvestasi')
  oTransLRInvestasi.nama_investasi = oJualObligasi.LObligasi.nama_obligasi
  oTransLRInvestasi.LInvestasi = oJualObligasi.LObligasi
  oTransLRInvestasi.kode_jns_investasi = oJualObligasi.kode_jns_investasi
  oTransLRInvestasi.kode_jenis_trinvestasi = 'D' # biaya obligasi
  oTransLRInvestasi.kode_subjns_LRInvestasi = 'B-COST' # biaya obligasi
  oTransLRInvestasi.tgl_transaksi = moduleapi.DateTimeTupleToFloat(config, oJualObligasi.tgl_transaksi)
  oTransLRInvestasi.mutasi_debet = oJualObligasi.biaya
  oTransLRInvestasi.mutasi_kredit = 0.0
  oTransLRInvestasi.isCommitted = 'T'

  oTransLRInvestasi.tgl_sistem = moduleapi.DateTimeTupleToFloat(config, oJualObligasi.tgl_sistem)
  oTransLRInvestasi.tgl_otorisasi = moduleapi.DateTimeTupleToFloat(config, oJualObligasi.tgl_otorisasi)
  oTransLRInvestasi.user_id = oJualObligasi.user_id
  oTransLRInvestasi.user_id_auth = oJualObligasi.user_id_auth
  oTransLRInvestasi.terminal_id = oJualObligasi.terminal_id
  oTransLRInvestasi.terminal_id_auth = oJualObligasi.terminal_id_auth
  #oTransLRInvestasi.no_bilyet = oJualObligasi.LObligasi.no_bilyet

  oObligasi = oJualObligasi.LObligasi
  oObligasi.akum_LR -= oJualObligasi.biaya
  
  return oTransLRInvestasi

def CreateTransPiutangLRInvestasi(config, oJualObligasi):
  # buat piutang lr investasi
  moduleapi = modman.getModule(config, 'moduleapi')

  oTransPiutangLRInvestasi = config.CreatePObject('TransPiutangLRInvestasi')
  oTransPiutangLRInvestasi.LInvestasi = oJualObligasi.LInvestasi
  oTransPiutangLRInvestasi.nama_investasi = oJualObligasi.LObligasi.nama_obligasi
  oTransPiutangLRInvestasi.kode_jns_investasi = oJualObligasi.kode_jns_investasi
  oTransPiutangLRInvestasi.kode_jenis_trinvestasi = 'J' # jual obligasi
  oTransPiutangLRInvestasi.tgl_transaksi = moduleapi.DateTimeTupleToFloat(config, oJualObligasi.tgl_transaksi)
  oTransPiutangLRInvestasi.mutasi_debet = 0.0
  oTransPiutangLRInvestasi.mutasi_kredit = oJualObligasi.LObligasi.akum_piutangLR
  oTransPiutangLRInvestasi.isCommitted = 'T'

  oTransPiutangLRInvestasi.tgl_sistem = moduleapi.DateTimeTupleToFloat(config, oJualObligasi.tgl_sistem)
  oTransPiutangLRInvestasi.tgl_otorisasi = moduleapi.DateTimeTupleToFloat(config, oJualObligasi.tgl_otorisasi)
  oTransPiutangLRInvestasi.user_id = oJualObligasi.user_id
  oTransPiutangLRInvestasi.user_id_auth = oJualObligasi.user_id_auth
  oTransPiutangLRInvestasi.terminal_id = oJualObligasi.terminal_id
  oTransPiutangLRInvestasi.terminal_id_auth = oJualObligasi.terminal_id_auth
  oTransPiutangLRInvestasi.nama_investasi = oTransPiutangLRInvestasi.LObligasi.nama_obligasi

  oTransPiutangLRInvestasi.LJualObligasi = oJualObligasi

  return oTransPiutangLRInvestasi

def CloseInvestasi(config, oJualObligasi):
  moduleapi = modman.getModule(config, 'moduleapi')
  oInvestasi = oJualObligasi.LInvestasi

  oInvestasi.status = 'F'
  oInvestasi.tgl_tutup = moduleapi.DateTimeTupleToFloat(config, oJualObligasi.tgl_transaksi)
  oInvestasi.akum_nominal = oJualObligasi.nominal_jual
  oInvestasi.akum_piutangLR = 0.0
  oInvestasi.last_update = config.Now()

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  id = parameter.FirstRecord.id
  moduleapi = modman.getModule(config, 'moduleapi')
  TransactInv = modman.getModule(config, 'TransactInv')

  oJualObligasi = config.CreatePObjImplProxy('JualObligasi')
  oJualObligasi.Key = id

  config.BeginTransaction()
  try:
    SetJualObligasi(config, oJualObligasi)
    oObligasi = oJualObligasi.LObligasi
    #margin = oObligasi.harga_pari - oObligasi.harga_beli
    #if not moduleapi.IsApproxZero(margin) :
    #  CreatePendapatanObligasi(config, oObligasi, oJualObligasi, margin)
    
    #buat transaksi SPI
    profObl = oJualObligasi.nominal_jual - oObligasi.akum_nominal
    TransactInv.CreateSPINoBatch(config, oObligasi.nama_obligasi, oObligasi, oJualObligasi, profObl,'N')
    TransactInv.CreatePNINoBatch(config, oObligasi.nama_obligasi, oObligasi, oJualObligasi, profObl,'N')

    TransactInv.CreateRincianPokok(config, oObligasi, profObl)
    if not moduleapi.IsApproxZero(oJualObligasi.profit):
      # buat pendapatan (atau biaya) tutup obligasi dari selisih nominal_jual
      CreatePendapatanTutupObligasi(config, oJualObligasi)
      TransactInv.CreateSPINoBatch(config, oObligasi.nama_obligasi, oObligasi, oJualObligasi, -oObligasi.akum_SPI,'J')
      TransactInv.CreatePNINoBatch(config, oObligasi.nama_obligasi, oObligasi, oJualObligasi, -oObligasi.akum_PNI,'J')
    #if oJualObligasi.biaya > 0.0:
    #  # biaya tutup obligasi secara tunai (tanpa piutanglrinv)
    #  CreateBiayaObligasi(config, oJualObligasi)

    # trans piutang lr investasi, memindahkan akumulasi piutang pendapatan
    # jika nilai akum tersebut ada
    # tidak ada transaksi obligasi yang menghasilkan piutang pendapatan (akum_piutangLR)
    #if not moduleapi.IsApproxZero(oJualObligasi.LObligasi.akum_piutangLR):
    #  CreateTransPiutangLRInvestasi(config, oJualObligasi)

    # tutup investasi (set status)
    CloseInvestasi(config, oJualObligasi)

    config.Commit()
  except:
    config.Rollback()
    raise

  return 1

