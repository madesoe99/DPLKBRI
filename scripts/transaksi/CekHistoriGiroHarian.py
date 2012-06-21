def CekHistoriGiroHarian(config, tTglTransaksi):
  sSQL = 'select ID_HistoriGiroHarian,isReconciled,isTransactionProceed,journal_blok_id '\
    'from HistoriGiroHarian '\
    'where Tanggal_Histori = \'%s\'' % ('%d-%d-%d' % (tTglTransaksi[0],\
    tTglTransaksi[1],tTglTransaksi[2]))
  rSQL = config.CreateSQL(sSQL).RawResult
  
  isAllReconciled = isAllTransactionProceed = 1
  isAllConverted2Journal = 0
  isExist = not rSQL.Eof
  rSQL.First()
  while not rSQL.Eof:
    if rSQL.isReconciled == 'F':
      isAllReconciled = 0
    if rSQL.isTransactionProceed == 'F':
      isAllTransactionProceed = 0
    if rSQL.journal_blok_id not in [None,'',0]:
      isAllConverted2Journal = 1
  
    rSQL.Next()
  
  return [isExist, isAllReconciled, isAllTransactionProceed, \
    isAllConverted2Journal]
  
def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  dtTglTransaksi = parameter.FirstRecord.tglTransaksi
  tTglTransaksi = config.ModLibUtils.DecodeDate(dtTglTransaksi)
  
  try:
    result = CekHistoriGiroHarian(config, tTglTransaksi)      
  except:
    raise
  
  returnpacket.CreateValues(['isExist',result[0]],\
    ['isAllReconciled',result[1]],\
    ['isAllTransactionProceed',result[2]],\
    ['isAllConverted2Journal',result[3]])

  return 1
