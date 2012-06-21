import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi

def RolloverInvestasi(config, oTransPiutangInvestasi):
  oInvestasi = oTransPiutangInvestasi.LInvestasi
  oDeposito = oInvestasi.CastAs('Deposito')
  moduleapi.AdvanceJatuhTempo(config, oDeposito)

def SetTransPiutangInvestasi(config, oTransPiutangInvestasi):
  oTransPiutangInvestasi.isCommitted = 'T'
  oTransPiutangInvestasi.tgl_otorisasi = config.Now()
  oTransPiutangInvestasi.user_id_auth = config.SecurityContext.userid
  oTransPiutangInvestasi.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]
  oTransPiutangInvestasi.no_bilyet = oTransPiutangInvestasi.LInvestasi.no_bilyet

def CreateTransPiutangLRInvestasi(config, isKapitalisir, oDeposito, ID_TransactionBatch, oRolloverDeposito = None):
  # mengurangi piutang pendapatan
  oTransPiutangLRInvestasi = config.CreatePObject('TransPiutangLRInvestasi')
  oTransPiutangLRInvestasi.LInvestasi = oDeposito
  oTransPiutangLRInvestasi.no_bilyet = oDeposito.no_bilyet
  oTransPiutangLRInvestasi.ID_TransactionBatch = ID_TransactionBatch
  oTransPiutangLRInvestasi.kode_jns_investasi = 'D' # rollover investasi
  oTransPiutangLRInvestasi.kode_jenis_trinvestasi = 'F' # rollover investasi
  oTransPiutangLRInvestasi.tgl_transaksi = config.Now()
  oTransPiutangLRInvestasi.isCommitted = 'T'

  # menolkan akum_piutangLR di objek investasi melalui mutasi kredit senilai tersebut
  oTransPiutangLRInvestasi.mutasi_debet = 0.0
  oTransPiutangLRInvestasi.mutasi_kredit = oDeposito.akum_piutangLR

  oTransPiutangLRInvestasi.tgl_sistem = config.Now()
  oTransPiutangLRInvestasi.tgl_otorisasi = config.Now()
  oTransPiutangLRInvestasi.user_id = config.SecurityContext.userid
  oTransPiutangLRInvestasi.user_id_auth = config.SecurityContext.userid
  oTransPiutangLRInvestasi.terminal_id = config.SecurityContext.GetSessionInfo()[1]
  oTransPiutangLRInvestasi.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]

  if isKapitalisir:
    oTransPiutangLRInvestasi.LTransPiutangInvestasi = oRolloverDeposito

  return oTransPiutangLRInvestasi

def KapitalisirInvestasi(config, oDeposito, oRolloverDeposito):
  CreateTransPiutangLRInvestasi(config, 1, oDeposito, oRolloverDeposito.ID_TransactionBatch, oRolloverDeposito)

  oDeposito.akum_nominal += (oDeposito.akum_piutangLR or 0.0)
  oDeposito.akum_piutangLR = 0.0

  strSQL = 'Select id_rincianinvestasi \
            From RincianInvestasi \
            where id_investasi = %d ' %   oDeposito.id_investasi
  resSQL = config.CreateSQL(strSQL).RawResult
  resSQL.First()
  while not resSQL.Eof:
    oRincianDeposito = config.CreatePObjImplProxy('RincianDeposito')
    oRincianDeposito.Key = resSQL.id_rincianinvestasi

    #Update Akumulasi Nominal berdasarkan proporsi
    oRincianDeposito.Akum_Paket += oDeposito.akum_nominal * oRincianDeposito.proporsi
    oRincianDeposito.Akum_LR_Paket = 0.0

    resSQL.Next()


def RolloverNonKapitalisir(config, oDeposito, oRolloverDeposito):
  CreateTransPiutangLRInvestasi(config, 0, oDeposito, oRolloverDeposito.ID_TransactionBatch)

  # tidak ada transaksi kapitalisir,
  # artinya tidak ada penambahan ke pokok
  oRolloverDeposito.Delete()

  oDeposito.akum_piutangLR = 0.0

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  id = parameter.FirstRecord.id

  oTransPiutangInvestasi = config.CreatePObjImplProxy('TransPiutangInvestasi')
  oTransPiutangInvestasi.Key = id
  
  oInvestasi = oTransPiutangInvestasi.LInvestasi
  oDeposito = oInvestasi.CastAs('Deposito')
  if oDeposito.tgl_jatuh_tempo > config.Now() :
     raise '\nPERINGATAN','Deposito belum jatuh tempo'
  config.BeginTransaction()
  try:
    RolloverInvestasi(config, oTransPiutangInvestasi)
    if parameter.FirstRecord.isKapitalisir:
      SetTransPiutangInvestasi(config, oTransPiutangInvestasi)
      KapitalisirInvestasi(config, oDeposito, oTransPiutangInvestasi)
    else:
      RolloverNonKapitalisir(config, oDeposito, oTransPiutangInvestasi)

    oDeposito.last_update = config.Now()

    config.Commit()
  except:
    config.Rollback()
    raise

  return 1

