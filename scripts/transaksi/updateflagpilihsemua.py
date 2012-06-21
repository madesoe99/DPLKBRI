
def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  rec = parameter.FirstRecord
  kode_cbg = rec.kode_cbg
  tgl_awal = rec.tgl_awal
  tgl_akhir = rec.tgl_akhir
  flag = rec.flag
  config.BeginTransaction()
  try:
    sSQL = 'UPDATE TransaksiDPLK \
    SET Flag_Pilih = \'%s\' \
    FROM TransaksiDPLK t, TransactionBatch b \
    WHERE t.ID_TransactionBatch = b.ID_TransactionBatch AND \
    t.branch_code = \'%s\' AND \
    batch_sub_type <> \'T\' AND \
    IsCommitted <> \'T\' AND \
    tgl_transaksi >= \'%s\' AND tgl_transaksi <= \'%s\' ' \
    % (flag, kode_cbg, tgl_awal, tgl_akhir)
    n = config.ExecSQL(sSQL)
    config.Commit()
  except:
    config.Rollback()
    raise

  returnpacket.CreateValues(['n', n])
  
  return 1
