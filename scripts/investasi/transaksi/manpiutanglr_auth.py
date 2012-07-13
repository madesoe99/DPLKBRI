import com.ihsan.util.modman as modman

#moduleapi = modman.getModule(config, 'moduleapi')
#TransactInv = modman.getModule(config, 'TransactInv')

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  id = parameter.FirstRecord.id

  oTransPiutangLRInvestasi = config.CreatePObjImplProxy('TransPiutangLRInvestasi')
  oTransPiutangLRInvestasi.Key = id
  oInvestasi = oTransPiutangLRInvestasi.LInvestasi

  config.BeginTransaction()
  try:
    oTransPiutangLRInvestasi.isCommitted = 'T'
    oTransPiutangLRInvestasi.tgl_otorisasi = config.Now()
    oTransPiutangLRInvestasi.user_id_auth = config.SecurityContext.userid
    oTransPiutangLRInvestasi.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]

    if oInvestasi.kode_jns_investasi == 'D':
      # deposito
      oTransPiutangLRInvestasi.no_bilyet = oInvestasi.no_bilyet
      oTransPiutangLRInvestasi.nama_investasi = oInvestasi.no_bilyet
    elif oInvestasi.kode_jns_investasi == 'O':
      # obligasi
      oObligasi = oInvestasi.CastAs('Obligasi')
      oTransPiutangLRInvestasi.nama_investasi = oObligasi.nama_obligasi
    elif oInvestasi.kode_jns_investasi == 'R':
      # Reksadana
      oReksadana = oInvestasi.CastAs('Reksadana')
      oTransPiutangLRInvestasi.nama_investasi = oReksadana.nama_reksadana
    else:
      raise Exception, 'Kesalahan Otorisasi' + 'Kode jenis investasi \'%s\' tidak dikenali.' % (str(oInvestasi.kode_jns_investasi))

    nom = oTransPiutangLRInvestasi.mutasi_debet - oTransPiutangLRInvestasi.mutasi_kredit
    oInvestasi.akum_piutangLR += nom
    oInvestasi.last_update = config.Now()

    TransactInv = modman.getModule(config, 'TransactInv')
    TransactInv.CreateRincianBagiHasil(config, oInvestasi, nom)

    config.Commit()
  except:
    config.Rollback()
    raise

  return 1

