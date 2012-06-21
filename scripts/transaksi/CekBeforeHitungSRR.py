def CekStatusBatch(config, tglHitung):
  jmlBatchNotYetClosed = 0

  #cek status batch (transaksi) dari tanggal ... (awal tahun???) sampai tglHitung
  sSQLBatch = 'select t.NO_BATCH from dbo.TRANSACTIONBATCH t \
               where t.BATCH_TYPE = \'T\' and t.BATCH_STATUS = \'O\' and \
                     t.TGL_USED > \'%d-01-01\' and t.TGL_USED <= \'%s\';' \
               % (tglHitung[0],'%d-%d-%d' % (tglHitung[0],tglHitung[1],tglHitung[2]))
  rSQLBatch = config.CreateSQL(sSQLBatch).RawResult
  
  if not rSQLBatch.Eof:
    jmlBatchNotYetClosed = rSQLBatch.RecordCount

  return jmlBatchNotYetClosed

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  y,m,d = config.ModLibUtils.DecodeDate(parameter.FirstRecord.tglhitung)
  tglHitung = [y,m,d]
  
  try:
    status = CekStatusBatch(config, tglHitung)
      
  except:
    raise
  
  returnpacket.CreateValues(['openbatch',status])

  return 1
