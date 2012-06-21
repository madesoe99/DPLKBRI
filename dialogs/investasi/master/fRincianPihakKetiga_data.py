def OnSetData_uipPihakKetiga (uipPihakKetiga) :
  uideflist = uipPihakKetiga.UIDefList
  config = uideflist.config
  uip = uideflist.GetPClassUIByName('uipRincianPK')
  lsjns = ''
  kodePK = uipPihakKetiga.Dataset.GetRecord(0).kode_pihak_ketiga
  
  strSQL = 'select * from rincianpihakketiga where kode_pihak_ketiga = \'%s\' ' \
    % kodePK

  rSQL = config.CreateSQL(strSQL).RawResult
  rSQL.First()
  while not rSQL.Eof :
    rec = uip.Dataset.AddRecord()
    rec.kode_jns_investasi = rSQL.kode_jns_investasi
    rec.kode_pihak_ketiga = rSQL.kode_pihak_ketiga
    rec.acc_investasi = rSQL.acc_investasi
    rec.acc_pendapatan = rSQL.acc_pendapatan
    rec.acc_beban = rSQL.acc_beban
    rec.acc_pendapatan = rSQL.acc_pendapatan
    rec.acc_piut_pendapatan = rSQL.acc_piut_pendapatan
    rec.acc_penjualan = rSQL.acc_penjualan
    
    rSQL.Next()
  strSQL = 'select * from JenisInvestasi '
  strSQL += 'where kode_jns_investasi not in ( \
    select kode_jns_investasi from rincianpihakketiga where kode_pihak_ketiga = \'%s\') ' \
    % kodePK

  rSQL = config.CreateSQL(strSQL).RawResult
  rSQL.First()
  while not rSQL.Eof :
    rec = uip.Dataset.AddRecord()
    rec.kode_jns_investasi = rSQL.kode_jns_investasi
    rec.kode_pihak_ketiga = kodePK

    rSQL.Next()

  return 1

def OnBeginProcessData (uideflist, AData) :
  config = uideflist.Config
  uData = AData.uipRincianPK
  for i in range(uData.RecordCount) :
    if uData.GetRecord(i).kode_jns_investasi not in (None, '') :
      oRincianPK = config.CreatePObjImplProxy('RincianPihakKetiga')
      oRincianPK.SetKey('kode_jns_investasi',uData.GetRecord(i).kode_jns_investasi)
      oRincianPK.SetKey('kode_pihak_ketiga',uData.GetRecord(i).kode_pihak_ketiga)
      if oRincianPK.IsNull :
        oRincianPK = config.CreatePObject('RincianPihakKetiga')
        oRincianPK.kode_jns_investasi = uData.GetRecord(i).kode_jns_investasi
        oRincianPK.kode_pihak_ketiga = uData.GetRecord(i).kode_pihak_ketiga
      oRincianPK.acc_investasi = uData.GetRecord(i).acc_investasi
      oRincianPK.acc_pendapatan = uData.GetRecord(i).acc_pendapatan
      oRincianPK.acc_beban = uData.GetRecord(i).acc_beban
      oRincianPK.acc_pendapatan = uData.GetRecord(i).acc_pendapatan
      oRincianPK.acc_piut_pendapatan = uData.GetRecord(i).acc_piut_pendapatan
      oRincianPK.acc_penjualan = uData.GetRecord(i).acc_penjualan

  return 0
