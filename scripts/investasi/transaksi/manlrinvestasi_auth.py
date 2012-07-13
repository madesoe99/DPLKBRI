import com.ihsan.util.modman as modman

#TransactInv = modman.getModule(config, 'TransactInv')

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  id = parameter.FirstRecord.id

  oTransLRInvestasi = config.CreatePObjImplProxy('TransLRInvestasi')
  oTransLRInvestasi.Key = id
  oInvestasi = oTransLRInvestasi.LInvestasi

  config.BeginTransaction()
  try:
    oTransLRInvestasi.isCommitted = 'T'
    oTransLRInvestasi.tgl_otorisasi = config.Now()
    oTransLRInvestasi.user_id_auth = config.SecurityContext.userid
    oTransLRInvestasi.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]

    if oInvestasi.kode_jns_investasi == 'D':
      # deposito
      oTransLRInvestasi.no_bilyet = oInvestasi.no_bilyet
      oTransLRInvestasi.nama_investasi = oInvestasi.no_bilyet
    elif oInvestasi.kode_jns_investasi == 'O':
      # obligasi
      #oObligasi = oInvestasi.CastAs('Obligasi')
      oObligasi = config.CreatePObjImplProxy('Obligasi')
      oObligasi.Key = oInvestasi.Id_Investasi
      oTransLRInvestasi.nama_investasi = oObligasi.nama_obligasi
    elif oInvestasi.kode_jns_investasi == 'R':
      # Reksadana
      #oReksadana = oInvestasi.CastAs('Reksadana')
      oReksadana = config.CreatePObjImplProxy('Reksadana')
      oReksadana.key = oInvestasi.id_Investasi
      oTransLRInvestasi.nama_investasi = oReksadana.nama_reksadana
    else:
      raise Exception, 'Kesalahan Otorisasi' + 'Kode jenis investasi \'%s\' tidak dikenali.' % (str(oInvestasi.kode_jns_investasi))

    nom = oTransLRInvestasi.mutasi_kredit - oTransLRInvestasi.mutasi_debet
    oInvestasi.akum_LR += nom
    oInvestasi.last_update = config.Now()

    TransactInv = modman.getModule(config, 'TransactInv')
    TransactInv.CreateRincianBagiHasil(config, oInvestasi, nom)
    
    config.Commit()
  except:
    config.Rollback()
    raise

  return 1

