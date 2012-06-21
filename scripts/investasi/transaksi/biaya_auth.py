import com.ihsan.util.modman as modman

#TransactInv = modman.getModule(config, 'TransactInv')

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)
  recReksa = parameter.uipReksadana.GetRecord(0)
  modeOto = recReksa.ModeOto

  id = parameter.uipTransLRInvestasi.GetRecord(0).id_transaksiinvestasi

  oTransLRInvestasi = config.CreatePObjImplProxy('TransLRInvestasi')
  oTransLRInvestasi.Key = id
  oInvestasi = oTransLRInvestasi.LInvestasi

  config.BeginTransaction()
  try:
    if modeOto :
      oTransLRInvestasi.isCommitted = 'T'
      oTransLRInvestasi.tgl_otorisasi = config.Now()
      oTransLRInvestasi.user_id_auth = config.SecurityContext.userid
      oTransLRInvestasi.terminal_id_auth = config.SecurityContext.GetSessionInfo()[1]

      nom = oTransLRInvestasi.mutasi_kredit - oTransLRInvestasi.mutasi_debet
      oInvestasi.akum_LR += nom
      oInvestasi.last_update = config.Now()

      TransactInv = modman.getModule(config, 'TransactInv')
      TransactInv.CreateRincianBagiHasil(config, oInvestasi, nom)
    else :
      oTransLRInvestasi.Delete()
    config.Commit()
  except:
    config.Rollback()
    raise

  return 1

