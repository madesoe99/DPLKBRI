def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)
  
  oDeposito = config.AccessPObject(parameter.FirstRecord.key)
  strSQL = \
    'select id_investasi '\
    'from TransaksiInvestasi '\
    'where id_investasi = %d; '\
    % (oDeposito.id_investasi)
  resSQL = config.CreateSQL(strSQL).RawResult
  if resSQL.Eof :
    oDeposito.status = 'B'
    oDeposito.last_update = config.Now()
    oDeposito.user_id = config.SecurityContext.UserID
    oDeposito.terminal_id = config.SecurityContext.InitIP
  else :
    raise Exception, '\nPERINGATAN: Deposito sudah memiliki transaksi, tidak bisa di batalkan'
  
  return 1

