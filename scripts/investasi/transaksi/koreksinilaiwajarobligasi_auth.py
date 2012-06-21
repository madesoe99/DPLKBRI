import com.ihsan.util.modman as modman

#moduleapi = modman.getModule(config, 'moduleapi')
#TransactInv = modman.getModule(config, 'TransactInv')

def CreateTransPiutangLRInvestasi(config, oPendapatanObligasi):
  moduleapi = modman.getModule(config, 'moduleapi')
  oTransPiutangLRInvestasi = config.CreatePObject('TransPiutangLRInvestasi')
  
  oTransPiutangLRInvestasi.LInvestasi = oPendapatanObligasi.LObligasi
  oTransPiutangLRInvestasi.nama_investasi = oPendapatanObligasi.LObligasi.nama_obligasi
  oTransPiutangLRInvestasi.kode_jns_investasi = oPendapatanObligasi.LObligasi.kode_jns_investasi
  oTransPiutangLRInvestasi.kode_jenis_trinvestasi = 'N' # pendapatan obligasi
  oTransPiutangLRInvestasi.tgl_transaksi = moduleapi.DateTimeTupleToFloat(config, oPendapatanObligasi.tgl_transaksi)
  if oPendapatanObligasi.nominal > 0.0 :
    oTransPiutangLRInvestasi.mutasi_debet = oPendapatanObligasi.nominal
    oTransPiutangLRInvestasi.mutasi_kredit = 0.0
  else :
    oTransPiutangLRInvestasi.mutasi_debet = 0.0
    oTransPiutangLRInvestasi.mutasi_kredit = -oPendapatanObligasi.nominal
  oTransPiutangLRInvestasi.isCommitted = 'T'

  oTransPiutangLRInvestasi.tgl_sistem = moduleapi.DateTimeTupleToFloat(config, oPendapatanObligasi.tgl_sistem)
  oTransPiutangLRInvestasi.tgl_otorisasi = moduleapi.DateTimeTupleToFloat(config, oPendapatanObligasi.tgl_otorisasi)
  oTransPiutangLRInvestasi.user_id = oPendapatanObligasi.user_id
  oTransPiutangLRInvestasi.user_id_auth = oPendapatanObligasi.user_id_auth
  oTransPiutangLRInvestasi.terminal_id = oPendapatanObligasi.terminal_id
  oTransPiutangLRInvestasi.terminal_id_auth = oPendapatanObligasi.terminal_id_auth

  oTransPiutangLRInvestasi.LTransLRInvestasi = oPendapatanObligasi

def CreateTransPiutangInvestasi(config, oPendapatanObligasi):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  oTransPiutangInvestasi = config.CreatePObject('TransPiutangInvestasi')
  
  oTransPiutangInvestasi.LInvestasi = oPendapatanObligasi.LObligasi
  oTransPiutangInvestasi.nama_investasi = oPendapatanObligasi.LObligasi.nama_obligasi
  oTransPiutangInvestasi.kode_jns_investasi = oPendapatanObligasi.LObligasi.kode_jns_investasi
  oTransPiutangInvestasi.kode_jenis_trinvestasi = 'N' # pendapatan obligasi
  oTransPiutangInvestasi.tgl_transaksi = moduleapi.DateTimeTupleToFloat(config, oPendapatanObligasi.tgl_transaksi)
  if oPendapatanObligasi.nominal > 0.0 :
    oTransPiutangInvestasi.mutasi_debet = oPendapatanObligasi.nominal
    oTransPiutangInvestasi.mutasi_kredit = 0.0
  else :
    oTransPiutangInvestasi.mutasi_debet = 0.0
    oTransPiutangInvestasi.mutasi_kredit = -oPendapatanObligasi.nominal
  
  oTransPiutangInvestasi.isCommitted = 'T'

  oTransPiutangInvestasi.tgl_sistem = moduleapi.DateTimeTupleToFloat(config, oPendapatanObligasi.tgl_sistem)
  oTransPiutangInvestasi.tgl_otorisasi = moduleapi.DateTimeTupleToFloat(config, oPendapatanObligasi.tgl_otorisasi)
  oTransPiutangInvestasi.user_id = oPendapatanObligasi.user_id
  oTransPiutangInvestasi.user_id_auth = oPendapatanObligasi.user_id_auth
  oTransPiutangInvestasi.terminal_id = oPendapatanObligasi.terminal_id
  oTransPiutangInvestasi.terminal_id_auth = oPendapatanObligasi.terminal_id_auth

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  id = parameter.FirstRecord.id
  TransactInv = modman.getModule(config, 'TransactInv')

  oPendapatanObligasi = config.CreatePObjImplProxy('PendapatanObligasi')
  oPendapatanObligasi.Key = id
  oObligasi = config.CreatePObjImplProxy('Obligasi')
  oObligasi.Key = oPendapatanObligasi.id_investasi
  ##oObligasi = oPendapatanObligasi.LObligasi
  
  config.BeginTransaction()
  try:
    oPendapatanObligasi.nama_investasi = oObligasi.nama_obligasi
    oPendapatanObligasi.isCommitted = 'T'
    oPendapatanObligasi.tgl_otorisasi = config.Now()
    oPendapatanObligasi.user_id_auth = config.SecurityContext.userid
    oPendapatanObligasi.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]
    oPendapatanObligasi.kode_subjns_LRInvestasi = 'B-KNW' # pendapatan obligasi dari kupon

    akum = oObligasi.akum_nominal
    oObligasi.akum_nominal = oPendapatanObligasi.nominal + oObligasi.Harga_pari
    profObl = oObligasi.akum_nominal-akum

    if profObl != 0.0 :
      TransactInv.CreateSPINoBatch(config, oObligasi.nama_obligasi, oObligasi, oPendapatanObligasi, profObl,'N')
      TransactInv.CreateSPINoBatch(config, oObligasi.nama_obligasi, oObligasi, oPendapatanObligasi, profObl,'N')

      #CreateTransPiutangInvestasi(config, oPendapatanObligasi)
      # tidak perlu buat transpiutanglrinvestasi,
      # karena pendapatan obligasi diperoleh secara tunai
  
      #oObligasi.akum_piutangLR += oPendapatanObligasi.nominal
      
      #oObligasi.akum_LR += oPendapatanObligasi.nominal
      #TransactInv.CreateRincianBagiHasil(config, oObligasi, oPendapatanObligasi.nominal)
      
      #akum nominal sama dengan total dari persentase


      TransactInv.CreateRincianPokok(config, oObligasi, oPendapatanObligasi.nominal-akum)
      oObligasi.last_update = config.Now()
      
    oPendapatanObligasi.mutasi_kredit = 0.0
    oPendapatanObligasi.mutasi_debet = 0.0
    
    config.Commit()
  except:
    config.Rollback()
    raise

  return 1

