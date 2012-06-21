import com.ihsan.util.modman as modman

#moduleapi = modman.getModule(config, 'moduleapi')

def CreateTransPiutangInvestasi(config, oReksadana, oBagiHasilReksadana):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  oTransPiutangInvestasi = config.CreatePObject('TransPiutangInvestasi')
  oTransPiutangInvestasi.LInvestasi = oReksadana
  oTransPiutangInvestasi.nama_investasi = oReksadana.nama_reksadana
  oTransPiutangInvestasi.LTransactionBatch = oBagiHasilReksadana.LTransactionBatch
  oTransPiutangInvestasi.kode_jns_investasi = 'C'
  oTransPiutangInvestasi.kode_jenis_trinvestasi = 'L' # bagi hasil reksadana
  oTransPiutangInvestasi.tgl_transaksi = moduleapi.DateTimeTupleToFloat(config, oBagiHasilReksadana.tgl_transaksi)

  oTransPiutangInvestasi.mutasi_debet = 0.0
  oTransPiutangInvestasi.mutasi_kredit = oReksadana.akum_nominal - oBagiHasilReksadana.NAB * oReksadana.unit_penyertaan

  oTransPiutangInvestasi.isCommitted = 'T'

  oTransPiutangInvestasi.tgl_sistem = config.Now()
  oTransPiutangInvestasi.tgl_otorisasi = config.Now()
  oTransPiutangInvestasi.user_id = oReksadana.user_id
  oTransPiutangInvestasi.user_id_auth = oReksadana.user_id_auth
  oTransPiutangInvestasi.terminal_id = oReksadana.terminal_id
  oTransPiutangInvestasi.terminal_id_auth = oReksadana.terminal_id_auth

def CreateHistNABReksadana(config, oBagiHasilReksadana):
  oHistNABReksadana = config.CreatePObject('HistNABReksadana')
  oHistNABReksadana.NAB = oBagiHasilReksadana.NAB
  oHistNABReksadana.tgl_penetapan = config.Now()
  oHistNABReksadana.LReksadana = oBagiHasilReksadana.LReksadana

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  id = parameter.FirstRecord.id

  oBagiHasilReksadana = config.CreatePObjImplProxy('BagiHasilReksadana')
  oBagiHasilReksadana.Key = id
  oReksadana = oBagiHasilReksadana.LReksadana

  config.BeginTransaction()
  try:
    CreateTransPiutangInvestasi(config, oReksadana, oBagiHasilReksadana)

    oBagiHasilReksadana.isCommitted = 'T'
    oBagiHasilReksadana.tgl_otorisasi = config.Now()
    oBagiHasilReksadana.user_id_auth = config.SecurityContext.userid
    oBagiHasilReksadana.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]
    oBagiHasilReksadana.no_bilyet = oReksadana.no_bilyet

    oReksadana.akum_nominal = oBagiHasilReksadana.NAB * oReksadana.unit_penyertaan
    oReksadana.akum_LR += oBagiHasilReksadana.nominal_bagi_hasil
    oReksadana.NAB_awal = oBagiHasilReksadana.NAB
    oReksadana.NAB = oBagiHasilReksadana.NAB
    oReksadana.nominal_jual = oBagiHasilReksadana.nominal_jual
    oReksadana.last_update = config.Now()

    CreateHistNABReksadana(config, oBagiHasilReksadana)

    config.Commit()
  except:
    config.Rollback()
    raise

  return 1

