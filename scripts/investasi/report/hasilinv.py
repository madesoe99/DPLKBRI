import sys
import com.ihsan.util.modman as modman

PERKIRAAN_WIDTH = 150
JENIS_WIDTH = 150
TOTAL_WIDTH = 150

def ConstructReportHeader(config, colwidth, colspan, strDateFrom, strDateUntil, oFile):
  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Hasil Investasi</title>\n')
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Arial; line-height:100%; margin-top:0; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="'+ str(colwidth) +'" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td colspan="'+ str(colspan) +'" height="20" style="border-left:medium none #000000; border-right:medium none #000000; border-top-style:none; border-top-width:medium; border-bottom-style:none; border-bottom-width:medium">\n')
  oFile.write('		<p align="center"><font size="3" color="#008000"><b>Dana Pensiun Lembaga \n')
  oFile.write('		Keuangan Muamalat</b></font><p align="center">\n')
  oFile.write('		<font size="3" color="#008000"><b>Laporan Hasil Investasi</b></font>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="'+ str(colwidth) +'" colspan="'+ str(colspan) +'" style="border-style: none; border-width: medium">\n')
  oFile.write('		<p align="left"><font size="2" color="#008000"><b>'+ strDateFrom +'-'+ strDateUntil +'</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<font size="2">\n')
  oFile.write('		<td width="'+ str(PERKIRAAN_WIDTH) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699" rowspan="2">\n')
  oFile.write('		<font size="2"><b>Perkiraan</b></font></td>\n')

def resSQLJenisInvestasi(config):
  strSQL = \
    'select kode_jns_investasi '\
    '  , nama_jns_investasi '\
    'from JenisInvestasi '
  return config.CreateSQL(strSQL).RawResult

def resSQLHasilInv(config, strDateFromSQL, strDateUntilTmrwSQL, kode_jns_investasi):
  strSQL = \
    'select sum(mutasi_kredit) as pendapatan '\
    '  , sum(mutasi_debet) as beban '\
    'from TransaksiInvestasi ti, Investasi i '\
    'where clsfTransaksiInvestasi = \'C\' '\
    '  and isCommitted = \'T\' '\
    '  and tgl_transaksi >= \'%s\' '\
    '  and tgl_transaksi < \'%s\' '\
    '  and i.id_investasi = ti.id_investasi '\
    '  and i.kode_jns_investasi = \'%s\' '\
    % (strDateFromSQL, strDateUntilTmrwSQL, kode_jns_investasi)
  config.SendDebugMsg(strSQL)
  return config.CreateSQL(strSQL).RawResult

def ConstructJenisInvHeader(config, colspanHasil, hasilWidth, resSQLJI, oFile):
  oFile.write('		<td width="'+ str(hasilWidth) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699" colspan="'+ str(colspanHasil) +'">\n')
  oFile.write('		<font size="2"><b>Hasil Investasi</b></font></td>\n')
  oFile.write('		</font>\n')
  oFile.write('		<td width="'+ str(TOTAL_WIDTH) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699" rowspan="2">\n')
  oFile.write('		<font size="2"><b>TOTAL</b></font></td>\n')
  oFile.write('	</tr>\n')

  oFile.write('	<tr>\n')

  lsJenisInvestasi = []
  lsPendapatan = []
  lsBiaya = []

  resSQLJI.First()
  while not resSQLJI.Eof:
    lsJenisInvestasi.append(resSQLJI.kode_jns_investasi)
    lsPendapatan.append(0.0)
    lsBiaya.append(0.0)

    oFile.write('		<font size="2">\n')
    oFile.write('		<td width="'+ str(JENIS_WIDTH) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
    oFile.write('		<font size="2">\n')
    oFile.write('		<b>'+ (resSQLJI.nama_jns_investasi or '&nbsp;') +'</b></font></td>\n')

    resSQLJI.Next()
  oFile.write('	</tr>\n')

  return lsJenisInvestasi, lsPendapatan, lsBiaya

def ConstructReportValues(config, lsJenisInvestasi, lsPendapatan, lsBiaya, strDateFromSQL, strDateUntilTmrwSQL, oFile):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  lsHasil = []
  sumAllNominal = 0.0

  # loop pertama untuk pendapatan
  sumPendapatan = 0.0
  oFile.write('	<tr>\n')
  oFile.write('		<td width="'+ str(PERKIRAAN_WIDTH) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#EFEFEF">\n')
  oFile.write('		<font size="2">Pendapatan Investasi</font></td>\n')
  i = 0
  for kode_jns_investasi in lsJenisInvestasi:

    resSQLHI = resSQLHasilInv(config, strDateFromSQL, strDateUntilTmrwSQL, kode_jns_investasi)
    resSQLHI.First()
    pendapatan = 0.0
    strPendapatan = '0'
    if not resSQLHI.Eof:
      pendapatan = resSQLHI.pendapatan or 0.0
      strPendapatan = moduleapi.FormatFloatStd(config, pendapatan)

    oFile.write('		<td width="'+ str(JENIS_WIDTH) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#EFEFEF" align="right">\n')
    oFile.write('		<font size="2">'+ strPendapatan +'</font></td>\n')

    lsPendapatan[i] += pendapatan
    beban = resSQLHI.beban or 0.0
    lsBiaya[i] += beban
    lsHasil.append(pendapatan - beban)

    sumPendapatan += pendapatan
    i += 1

  oFile.write('		<td width="'+ str(TOTAL_WIDTH) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#EFEFEF" align="right">\n')
  oFile.write('		<font size="2">'+ moduleapi.FormatFloatStd(config, sumPendapatan) +'</font></td>\n')
  oFile.write('	</tr>\n')

  sumAllNominal += sumPendapatan

  # loop kedua untuk beban
  sumBiaya = 0.0
  oFile.write('	<tr>\n')
  oFile.write('		<td width="'+ str(PERKIRAAN_WIDTH) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#EFEFEF">\n')
  oFile.write('		<font size="2">Beban Investasi</font></td>\n')

  for j in range(len(lsJenisInvestasi)):
    beban = lsBiaya[j]
    strBeban = moduleapi.FormatFloatStd(config, beban)

    oFile.write('		<td width="'+ str(JENIS_WIDTH) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#EFEFEF" align="right">\n')
    oFile.write('		<font size="2">'+ strBeban +'</font></td>\n')

    sumBiaya += beban

  oFile.write('		<td width="'+ str(TOTAL_WIDTH) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#EFEFEF" align="right">\n')
  oFile.write('		<font size="2">'+ moduleapi.FormatFloatStd(config, sumBiaya) +'</font></td>\n')
  oFile.write('	</tr>\n')

  sumAllNominal = sumPendapatan - sumBiaya

  return lsHasil, sumAllNominal

def ConstructReportTrailer(config, lsHasil, sumAllNominal, oFile):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  oFile.write('	<tr>\n')

  oFile.write('		<td width="'+ str(PERKIRAAN_WIDTH) +'" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<p align="left"><font size="2"><b>Hasil Usaha Investasi</b></font></td>\n')

  for hasil in lsHasil:
    oFile.write('		<td width="'+ str(JENIS_WIDTH) +'" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
    oFile.write('		</font>\n')
    oFile.write('		<b><font size="2">'+ moduleapi.FormatFloatStd(config, hasil) +'</font></b></td>\n')

  oFile.write('		<td width="'+ str(TOTAL_WIDTH) +'" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b><font size="2">'+ moduleapi.FormatFloatStd(config, sumAllNominal) +'</font></b></td>\n')

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

  dtDateFrom = parameter.FirstRecord.dateFrom
  dtDateUntil = parameter.FirstRecord.dateUntil
  dtDateUntilTmrw = dtDateUntil + 1

  sBaseFileName = 'hasil_investasi.htm'
  sFileName = config.UserHomeDirectory + sBaseFileName
  oFile = open(sFileName, 'w')

  resSQLJI = resSQLJenisInvestasi(config)
  nbOfJI = resSQLJI.RecordCount

  colspanHasil = nbOfJI
  hasilWidth = colspanHasil * JENIS_WIDTH

  tableSpan = 1 + colspanHasil + 1
  tableWidth = PERKIRAAN_WIDTH + hasilWidth + TOTAL_WIDTH

  ConstructReportHeader(
    config
    , tableWidth
    , tableSpan
    , config.FormatDateTime('d mmmm yyyy', dtDateFrom)
    , config.FormatDateTime('d mmmm yyyy', dtDateUntil)
    , oFile
  )
  lsJenisInvestasi, lsPendapatan, lsBiaya = ConstructJenisInvHeader(
    config
    , colspanHasil
    , hasilWidth
    , resSQLJI
    , oFile
  )
  lsHasil, sumAllNominal = ConstructReportValues(config
    , lsJenisInvestasi
    , lsPendapatan
    , lsBiaya
    , config.FormatDateTime('yyyy-mm-dd', dtDateFrom)
    , config.FormatDateTime('yyyy-mm-dd', dtDateUntilTmrw)
    , oFile
  )
  ConstructReportTrailer(config
    , lsHasil
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
