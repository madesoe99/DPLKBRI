import com.ihsan.util.modman as modman

#TransactInv = modman.getModule(config, 'TransactInv')

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  id = parameter.FirstRecord.id

  oTransPiutangInvestasi = config.CreatePObjImplProxy('TransPiutangInvestasi')
  oTransPiutangInvestasi.Key = id
  oInvestasi = oTransPiutangInvestasi.LInvestasi

  config.BeginTransaction()
  try:
    oTransPiutangInvestasi.isCommitted = 'T'
    oTransPiutangInvestasi.tgl_otorisasi = config.Now()
    oTransPiutangInvestasi.user_id_auth = config.SecurityContext.userid
    oTransPiutangInvestasi.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]

    if oInvestasi.kode_jns_investasi == 'D':
      # deposito
      oTransPiutangInvestasi.no_bilyet = oInvestasi.no_bilyet
    elif oInvestasi.kode_jns_investasi == 'O':
      # obligasi
      #oObligasi = oInvestasi.CastAs('Obligasi')
      oObligasi = config.CreatePObjImplProxy('Obligasi')
      oObligasi.Key = oInvestasi.Id_Investasi
      oTransPiutangInvestasi.nama_investasi = oObligasi.nama_obligasi
    elif oInvestasi.kode_jns_investasi == 'R':
      # Reksadana
      #oReksadana = oInvestasi.CastAs('Reksadana')
      oReksadana = config.CreatePObjImplProxy('Reksadana')
      oReksadana.key = oInvestasi.id_Investasi
      oTransPiutangInvestasi.nama_investasi = oReksadana.nama_reksadana
    else:
      raise 'Kesalahan Otorisasi','Kode jenis investasi \'%s\' tidak dikenali.' % (str(oInvestasi.kode_jns_investasi))

    nom = oTransPiutangInvestasi.mutasi_debet - oTransPiutangInvestasi.mutasi_kredit
    oInvestasi.akum_nominal += nom
    oInvestasi.last_update = config.Now()

    TransactInv = modman.getModule(config, 'TransactInv')
    TransactInv.CreateRincianPokok(config, oInvestasi, nom)

    config.Commit()
  except:
    config.Rollback()
    raise

  return 1

