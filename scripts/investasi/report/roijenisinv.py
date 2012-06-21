import sys
import com.ihsan.util.modman as modman

#moduleapi = modman.getModule(config, 'moduleapi')

def ConstructReportHeader(config, strDateFrom, strDateUntil, oFile):
  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>ROI per Jenis Investasi</title>\n')
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Arial; line-height:100%; margin-top:0; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td colspan="4" height="20" style="border-left:medium none #000000; border-right:medium none #000000; border-top-style:none; border-top-width:medium; border-bottom-style:none; border-bottom-width:medium">\n')
  oFile.write('		<p align="center"><font size="3" color="#008000"><b>ROI PER JENIS \n')
  oFile.write('		INVESTASI</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" colspan="4" style="border-style: none; border-width: medium">\n')
  oFile.write('		<b><font color="#008000" size="2">'+ strDateFrom +' - '+ strDateUntil +'</font></b></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="10%" align="center" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b><font size="2">NO</font></b></td>\n')
  oFile.write('		<font size="2">\n')
  oFile.write('		<td width="50%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b><font size="2">JENIS INVESTASI</font></b></td>\n')
  oFile.write('		<td width="20%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b><font size="2">NILAI HASIL INVESTASI<br>\n')
  oFile.write('		(Rp)</font></b></td>\n')
  oFile.write('		</font>\n')
  oFile.write('		<td width="20%" align="center" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b><font size="2">ROI<br>\n')
  oFile.write('		(%)</font></b></td>\n')
  oFile.write('	</tr>\n')

def resSQLHasilInv(config, strDateFromSQL, strDateUntilTmrwSQL):
  strSQL = \
    'select sum(mutasi_kredit - mutasi_debet) as hasil '\
    '  , j.kode_jns_investasi '\
    '  , j.nama_jns_investasi '\
    'from '\
    '  (select mutasi_debet '\
    '    , mutasi_kredit '\
    '    , kode_jns_investasi '\
    '  from TransaksiInvestasi '\
    '  where clsfTransaksiInvestasi = \'C\' '\
    '  and isCommitted = \'T\' '\
    '  and tgl_transaksi >= \'%s\' '\
    '  and tgl_transaksi < \'%s\' '\
    '  ) ti '\
    'right outer join '\
    '  (select kode_jns_investasi '\
    '    , nama_jns_investasi '\
    '  from JenisInvestasi '\
    '  ) j on ti.kode_jns_investasi = j.kode_jns_investasi '\
    'group by j.kode_jns_investasi '\
    '  , j.nama_jns_investasi '\
    'order by j.kode_jns_investasi '\
    % (strDateFromSQL
       , strDateUntilTmrwSQL
    )
  return config.CreateSQL(strSQL).RawResult

def resSQLNominalInv(config, strDateFromSQL, strDateUntilTmrwSQL):
  strSQL = \
    'select sum(mutasi_debet - mutasi_kredit) as nominal '\
    '  , j.kode_jns_investasi '\
    '  , j.nama_jns_investasi '\
    'from TransaksiInvestasi ti, JenisInvestasi j '\
    'where clsfTransaksiInvestasi = \'A\' '\
    '  and isCommitted = \'T\' '\
    '  and tgl_transaksi >= \'%s\' '\
    '  and tgl_transaksi < \'%s\' '\
    '  and j.kode_jns_investasi = ti.kode_jns_investasi '\
    'group by j.kode_jns_investasi '\
    '  , j.nama_jns_investasi '\
    'order by j.kode_jns_investasi '\
    % (strDateFromSQL
       , strDateUntilTmrwSQL
    )
  return config.CreateSQL(strSQL).RawResult

def ConstructReportValues(config, strDateFromSQL, strDateUntilTmrwSQL, oFile):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  resSQLHslInv = resSQLHasilInv(config, strDateFromSQL, strDateUntilTmrwSQL)
  resSQLNomInv = resSQLNominalInv(config, strDateFromSQL, strDateUntilTmrwSQL)

  no_urut = 0
  totHasil = 0.0

  resSQLNomInv.First()
  resSQLHslInv.First()
  
  nomStop = 0
  while not resSQLHslInv.Eof:
    no_urut += 1

    if moduleapi.IsOddNumber(no_urut):
      bgcolor = '#EFEFEF'
    else:
      bgcolor = '#FFFFFF'

    hasil = 0.0
    strHasil = '0'
    nominal = 0.0
    strROI = '0'

    if not nomStop:

      strJenis = resSQLHslInv.nama_jns_investasi or '&nbsp;'
      hasil = resSQLHslInv.hasil or 0.0
      strHasil = moduleapi.FormatFloatStd(config, hasil)
      nominal = resSQLNomInv.nominal or 0.0
      strROI = '0'

      if resSQLNomInv.kode_jns_investasi == resSQLHslInv.kode_jns_investasi:

        if not moduleapi.IsApproxZero(nominal):
          #hasil = resSQLHslInv.hasil or 0.0
          strROI = config.FormatFloat('0.##', hasil * 100.0 / nominal)

        resSQLNomInv.Next()

    else:

      # nomStop
      strJenis = resSQLHslInv.nama_jns_investasi or '&nbsp;'
      hasil = resSQLHslInv.hasil or 0.0
      strHasil = moduleapi.FormatFloatStd(config, hasil)

    # end if not nomStop

    oFile.write('	<tr>\n')
    oFile.write('		<td width="10%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'">\n')
    oFile.write('		<font size="2">'+ str(no_urut) +'</font></td>\n')
    oFile.write('		<td width="50%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'"><font size="2">'+ strJenis +'</font></td>\n')
    oFile.write('		<td width="20%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'"><font size="2">\n')
    oFile.write('		<p align="right">'+ strHasil +'</font></td>\n')
    oFile.write('		<td width="20%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'">\n')
    oFile.write('		<font size="2"><p align="center">'+ strROI +'</font></td>\n')
    oFile.write('	</tr>\n')

    totHasil += hasil

    resSQLHslInv.Next()

  return totHasil

def ConstructReportTrailer(config, totHasil, oFile):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  oFile.write('	<tr>\n')
  oFile.write('		<td width="60%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" colspan="2" bgcolor="#CC6699">\n')
  oFile.write('		<b><font size="2">TOTAL</font></b><font size="3"></td>\n')
  oFile.write('		<td width="20%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<font size="2">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totHasil) +'</b></font></td>\n')
  oFile.write('		<td width="20%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		&nbsp;</td>\n')
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

  sBaseFileName = 'roi_per_jenisinv.htm'
  sFileName = config.UserHomeDirectory + sBaseFileName
  oFile = open(sFileName, 'w')

  ConstructReportHeader(
    config
    , config.FormatDateTime('d mmmm yyyy', dtDateFrom)
    , config.FormatDateTime('d mmmm yyyy', dtDateUntil)
    , oFile
  )

  totHasil = ConstructReportValues(
    config
    , config.FormatDateTime('yyyy-mm-dd', dtDateFrom)
    , config.FormatDateTime('yyyy-mm-dd', dtDateUntilTmrw)
    , oFile
  )

  ConstructReportTrailer(config, totHasil, oFile)

  oFile.close()

  recRes = returnpacket.CreateDataPacketStructure('filename:string')
  recRes.filename = sBaseFileName

  #tambahan stream wrapper
  sw = returnpacket.AddStreamWrapper()
  sw.LoadFromFile(sFileName)
  sw.MIMEType = config.AppObject.GetMIMETypeFromExtension(sFileName)

  return 1

