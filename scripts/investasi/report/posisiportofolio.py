import sys
import com.ihsan.util.modman as modman

NO_WIDTH = 30
JENIS_WIDTH = 200
PIHAK_WIDTH = 150
PERSEN_PIHAK_WIDTH = 50

def ConstructReportHeader(config, colwidth, colspan, strDateUntil, oFile):
  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Laporan Posisi Portofolio Investasi</title>\n')
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Arial; line-height:100%; margin-top:0; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')

  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="'+ str(colwidth) +'" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td colspan="'+ str(colspan) +'" height="20" style="border-left:medium none #000000; border-right:medium none #000000; border-top-style:none; border-top-width:medium; border-bottom-style:none; border-bottom-width:medium">\n')
  oFile.write('		<p align="center"><font size="3" color="#008000"><b>Dana Pensiun Lembaga \n')
  oFile.write('		Keuangan Muamalat</b></font><p align="center">\n')
  oFile.write('		<font size="3" color="#008000"><b>Laporan Posisi Portofolio Investasi</b></font><p align="center">\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="'+ str(colwidth) +'" colspan="'+ str(colspan) +'" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2" color="#008000"><b>per '+ strDateUntil +'</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="'+ str(NO_WIDTH) +'" align="center" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699" rowspan="3">\n')
  oFile.write('		<b><font size="2">NO</font></b></td>\n')
  oFile.write('		<font size="2">\n')
  oFile.write('		<td width="'+ str(JENIS_WIDTH) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699" rowspan="3">\n')
  oFile.write('		<font size="2">\n')
  oFile.write('		<b>JENIS INVESTASI</b></font></td>\n')

def resSQLPihakKetiga(config):
  strSQL = \
    'select kode_pihak_ketiga '\
    '  , nama_pihak_ketiga '\
    'from PihakKetiga '
  return config.CreateSQL(strSQL).RawResult

def resSQLJenisInvestasi(config):
  strSQL = \
    'select kode_jns_investasi '\
    '  , nama_jns_investasi '\
    'from JenisInvestasi '
  return config.CreateSQL(strSQL).RawResult

def resSQLTotJINominalInv(config, strDateUntilTmrwSQL, kode_jns_investasi):
  strSQL = \
    'select sum(mutasi_debet - mutasi_kredit) as totJINominal '\
    'from TransaksiInvestasi ti, Investasi i '\
    'where clsfTransaksiInvestasi = \'A\' '\
    '  and isCommitted = \'T\' '\
    '  and tgl_transaksi < \'%s\' '\
    '  and i.id_investasi = ti.id_investasi '\
    '  and i.kode_jns_investasi = \'%s\' '\
    % (strDateUntilTmrwSQL, kode_jns_investasi)
  return config.CreateSQL(strSQL).RawResult

def resSQLNominalInv(config, strDateUntilTmrwSQL, kode_pihak_ketiga, kode_jns_investasi):
  strSQL = \
    'select sum(mutasi_debet - mutasi_kredit) as nominal '\
    'from TransaksiInvestasi ti, Investasi i '\
    'where clsfTransaksiInvestasi = \'A\' '\
    '  and isCommitted = \'T\' '\
    '  and tgl_transaksi < \'%s\' '\
    '  and i.id_investasi = ti.id_investasi '\
    '  and i.kode_pihak_ketiga = \'%s\' '\
    '  and i.kode_jns_investasi = \'%s\' '\
    % (strDateUntilTmrwSQL, kode_pihak_ketiga, kode_jns_investasi)
  return config.CreateSQL(strSQL).RawResult

def ConstructPihakKetigaHeader(config, nbOfPihak, colspanPihak, groupPihakWidth, resSQLPK, oFile):
  oFile.write('		<td width="'+ str(groupPihakWidth) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699" colspan="'+ str(colspanPihak) +'">\n')
  oFile.write('		<font size="2"><b>Nama Pihak</b></font></td>\n')
  oFile.write('		</font>\n')
  oFile.write('	</tr>\n')

  oFile.write('	<tr>\n')

  lsPihakKetiga = []
  lsNominalPihakKetiga = []

  resSQLPK.First()
  while not resSQLPK.Eof:
    lsPihakKetiga.append(resSQLPK.kode_pihak_ketiga)
    lsNominalPihakKetiga.append(0.0)

    oFile.write('		<font size="2">\n')
    oFile.write('		<td width="'+  str(2 * PIHAK_WIDTH) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699" colspan="2">\n')
    oFile.write('		<font size="2"><b>'+ (resSQLPK.nama_pihak_ketiga or '&nbsp;') +'</b></font></td>\n')

    resSQLPK.Next()
  oFile.write('	</tr>\n')

  oFile.write('	<tr>\n')
  for i in range(nbOfPihak):
    oFile.write('		<font size="2">\n')
    oFile.write('		<td width="'+ str(PIHAK_WIDTH) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
    oFile.write('		<b><font size="2">Nilai Nominal</font></b></td>\n')
    oFile.write('		</font>\n')
    oFile.write('		<td width="'+ str(PERSEN_PIHAK_WIDTH) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
    oFile.write('		<b><font size="2">%</font></b></td>\n')
    oFile.write('		<font size="2">\n')
  oFile.write('	</tr>\n')

  return lsPihakKetiga, lsNominalPihakKetiga

def ConstructReportValues(config, lsPihakKetiga, lsNominalPihakKetiga, strDateUntilTmrwSQL, oFile):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  no_urut = 0
  sumAllNominal = 0.0
  sumNominalPerPK = 0.0

  resSQLJI = resSQLJenisInvestasi(config)
  resSQLJI.First()
  while not resSQLJI.Eof:
    no_urut += 1

    if moduleapi.IsOddNumber(no_urut):
      bgcolor = '#EFEFEF'
    else:
      bgcolor = '#FFFFFF'

    oFile.write('	<tr>\n')
    oFile.write('		<td width="'+ str(NO_WIDTH) +'" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'">\n')
    oFile.write('		<font size="2">'+ str(no_urut) +'</td>\n')
    oFile.write('		<td width="'+ str(JENIS_WIDTH) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'">\n')
    oFile.write('		<font size="2">'+ (resSQLJI.nama_jns_investasi or '&nbsp;') +'</font></td>\n')

    resSQLTJIN = resSQLTotJINominalInv(config, strDateUntilTmrwSQL, resSQLJI.kode_jns_investasi)
    totJINominal = 0.0
    if not resSQLTJIN.Eof:
      totJINominal = resSQLTJIN.totJINominal or 0.0

    sumAllNominal += totJINominal

    for kode_pihak_ketiga in lsPihakKetiga:
      resSQLNomInv = resSQLNominalInv(config, strDateUntilTmrwSQL, kode_pihak_ketiga, resSQLJI.kode_jns_investasi)
      resSQLNomInv.First()
      while not resSQLNomInv.Eof:
        nominal = resSQLNomInv.nominal or 0.0
        persen = 0.0
        if not moduleapi.IsApproxZero(totJINominal):
          persen = nominal * 100.0 / totJINominal

        strNominal = moduleapi.FormatFloatStd(config, nominal)
        strPersen = config.FormatFloat('0.##', persen)

        oFile.write('		<td width="'+ str(PIHAK_WIDTH) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'">\n')
        oFile.write('		<p align="right"><font size="2">'+ strNominal +'</font></td>\n')
        oFile.write('		<td width="'+ str(PERSEN_PIHAK_WIDTH) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'">\n')
        oFile.write('		<p align="right"><font size="2">'+ strPersen +'</font></td>\n')

        # update lsNominalPihakKetiga
        id = lsPihakKetiga.index(kode_pihak_ketiga)
        lsNominalPihakKetiga[id] += nominal

        resSQLNomInv.Next()

      # end while not resSQLNomInv.Eof

    # end for kode_pihak_ketiga in lsPihakKetiga

    oFile.write('	</tr>\n')

    resSQLJI.Next()
  # end while resSQLJI.Eof

  return sumAllNominal  

def ConstructReportTrailer(config, lsNominalPihakKetiga, sumAllNominal, oFile):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  oFile.write('	<tr>\n')
  oFile.write('		<td width="'+ str(NO_WIDTH) +'" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		&nbsp;</td>\n')
  oFile.write('		<td width="'+ str(JENIS_WIDTH) +'" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<p align="left"><b><font size="2">Total Penempatan</font></b></td>\n')

  for nominalPK in lsNominalPihakKetiga:
    persen = 0.0
    if not moduleapi.IsApproxZero(sumAllNominal):
      persen = nominalPK * 100.0 / sumAllNominal

    strNominalPK = moduleapi.FormatFloatStd(config, nominalPK)
    strPersen = config.FormatFloat('0.##', persen)

    oFile.write('		<td width="'+ str(PIHAK_WIDTH) +'" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
    oFile.write('		<font size="2">\n')
    oFile.write('		</font>\n')
    oFile.write('		</font>\n')
    oFile.write('		<b><font size="2">'+ strNominalPK +'</font></b></td>\n')
    oFile.write('		<td width="'+ str(PERSEN_PIHAK_WIDTH) +'" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
    oFile.write('		<b><font size="2">'+ strPersen +'</font></b></td>\n')

  oFile.write('	</tr>\n')
  oFile.write('</table>\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('</body>\n')
  oFile.write('\n')
  oFile.write('</html>\n')

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  dtDateUntil = parameter.FirstRecord.dateUntil
  dtDateUntilTmrw = dtDateUntil + 1

  sBaseFileName = 'posisi_portofolio.htm'
  sFileName = config.UserHomeDirectory + sBaseFileName
  oFile = open(sFileName, 'w')

  resSQLPK = resSQLPihakKetiga(config)
  nbOfPihak = resSQLPK.RecordCount

  colspanPihak = 2 * nbOfPihak
  pihakValWidth = PIHAK_WIDTH + PERSEN_PIHAK_WIDTH
  groupPihakWidth = nbOfPihak * pihakValWidth

  tableSpan = 2 + colspanPihak
  tableWidth = NO_WIDTH + JENIS_WIDTH + groupPihakWidth

  ConstructReportHeader(
    config
    , tableWidth
    , tableSpan
    , config.FormatDateTime('d mmmm yyyy', dtDateUntil)
    , oFile
  )
  lsPihakKetiga, lsNominalPihakKetiga = ConstructPihakKetigaHeader(
    config
    , nbOfPihak
    , colspanPihak
    , groupPihakWidth
    , resSQLPK
    , oFile
  )
  sumAllNominal = ConstructReportValues(config
    , lsPihakKetiga
    , lsNominalPihakKetiga
    , config.FormatDateTime('yyyy-mm-dd', dtDateUntilTmrw)
    , oFile
  )
  ConstructReportTrailer(config
    , lsNominalPihakKetiga
    , sumAllNominal
    , oFile
  )

  oFile.close()

  recRes = returnpacket.CreateDataPacketStructure('filename:string')
  recRes.filename = sBaseFileName
  
  #tambahan 
  sw = returnpacket.AddStreamWrapper()
  sw.LoadFromFile(sFileName)
  sw.MIMEType = config.AppObject.GetMIMETypeFromExtension(sFileName)

  return 1

