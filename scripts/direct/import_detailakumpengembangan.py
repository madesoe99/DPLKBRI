import dafsys

config = dafsys.OpenConfig('c:/dafapp/dplk07/default.cfg')
config.BeginTransaction()
try:
  sSQL = 'SELECT no_peserta, kode_paket_investasi, akum_dana_pengembangan \
  FROM REKENINGDPLK \
  WHERE STATUS_DPLK = \'A\' '
  rSQL = config.CreateSQL(sSQL).RawResult
  print 'peserta : ' + rSQL.no_peserta
  while not rSQL.Eof:    
    kode_paket = rSQL.kode_paket_investasi
    sSQLJenisInvest = 'SELECT kode_jns_investasi, maks_proporsi \
    FROM RINCIANPAKETINVESTASI\
    WHERE kode_paket_investasi = \'%s\' ' % (kode_paket)
    rSQLJenisInvest = config.CreateSQL(sSQLJenisInvest).RawResult
    while not rSQLJenisInvest.Eof:
      print 'peserta : ' + rSQL.no_peserta + ' - ' + kode_paket + ' - ' + rSQLJenisInvest.kode_jns_investasi + ' - ' + str(rSQLJenisInvest.maks_proporsi)
      # akum = rSQLJenisInvest.maks_proporsi / 100 * rSQL.akum_dana_pengembangan      
      if rSQLJenisInvest.kode_jns_investasi == 'D':
          akum = rSQL.akum_dana_pengembangan
      else:
          akum = 0
          sSQL = 'INSERT INTO DETAILAKUMPENGEMBANGAN \
	  (no_peserta, kode_paket_investasi, kode_jns_investasi, Nilai_Akumulasi) \
	  VALUES (\'%s\',\'%s\',\'%s\',%f) ' % \
	  (rSQL.no_peserta, kode_paket, rSQLJenisInvest.kode_jns_investasi, akum)
          config.ExecSQL(sSQL)
      # oDetailAkum = config.CreatePObject('DetailAkumPengembangan')
      # oDetailAkum.no_peserta            = rSQL.no_peserta
      # oDetailAkum.kode_paket_investasi  = kode_paket
      # oDetailAkum.kode_jns_investasi    = rSQLJenisInvest.kode_jns_investasi
      # oDetailAkum.Nilai_Akumulasi       = akum
      
      rSQLJenisInvest.Next()    
    rSQL.Next()
  config.Commit()
except:
  config.Rollback()
  raise
