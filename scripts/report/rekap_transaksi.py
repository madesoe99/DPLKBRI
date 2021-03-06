import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi
import string

def ConstructReportHeader(config, jenis, strBulan, strTahun, oFile):
  if jenis == 'B':
    # BULANAN
    strJenis = 'REKAPITULASI TRANSAKSI BULANAN'
    strPeriode = 'PERIODE BULAN: %s %s' % (string.upper(strBulan), strTahun)
  else:
    # TAHUNAN
    strJenis = 'REKAPITULASI TRANSAKSI TAHUNAN'
    strPeriode = 'PERIODE TAHUN: %s' % (strTahun)

  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Rekapitulasi Transaksi</title>\n')
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Arial; line-height:100%; margin-top:0; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td colspan="4" height="20" style="border-left:medium none #000000; border-right:medium none #000000; border-top-style:none; border-top-width:medium; border-bottom-style:none; border-bottom-width:medium">\n')
  oFile.write('		<p align="center"><font size="3" color="#008000"><b>'+ strJenis +'</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" colspan="4" style="border-style: none; border-width: medium">\n')
  oFile.write('		<b><font color="#008000">'+ strPeriode +'</font></b></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="10%" align="center" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>NO</b></td>\n')
  oFile.write('		<td width="20%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>KODE</b></td>\n')
  oFile.write('		<td width="50%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>JENIS TRANSAKSI</b></td>\n')
  oFile.write('		<td width="20%" align="center" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>JUMLAH</b></td>\n')
  oFile.write('	</tr>\n')

def strSQLRekapTrans(config, jenis, intBulan, intTahun):
  if jenis == 'B':
    # BULANAN
    strFilter = \
      ' iscommitted = \'T\' and datepart(year,tgl_transaksi) = %d '\
      '  and  datepart(month,tgl_transaksi) = %d '\
      % (intTahun, intBulan)
  else:
    # TAHUNAN
    strFilter = \
      ' iscommitted = \'T\' and datepart(year,tgl_transaksi) = %d '\
      % (intTahun)
    
  strSQL = \
    'select j.kode_jenis_transaksi kode '\
    '  , nama_transaksi nama '\
    '  , isnull(sum(mutasi_peralihan) + sum(mutasi_pengembangan) + sum(mutasi_iuran_pst) + sum(mutasi_iuran_pk),0.0) sumTrans '\
    'from '\
    '(select kode_jenis_transaksi '\
    '  , nama_transaksi '\
    'from JenisTransaksiDPLK \
    where kode_jenis_transaksi not in (\'A\',\'B\')) as j '\
    'left outer join '\
    '(select id_transaksi '\
    '  , kode_jenis_transaksi '\
    '  , mutasi_peralihan '\
    '  , mutasi_pengembangan '\
    '  , mutasi_iuran_pst '\
    '  , mutasi_iuran_pk '\
    'from TransaksiDPLK '\
    'where '+ strFilter +') as t '\
    'on j.kode_jenis_transaksi = t.kode_jenis_transaksi '\
    'group by j.kode_jenis_transaksi '\
    '  , nama_transaksi'

#    '  , isnull(count(id_transaksi),0) nbOfTrans '\

  return strSQL  

def ConstructReportValues(config, strSQL, oFile):
  resSQL = config.CreateSQL(strSQL).RawResult

  no_urut = 0
  total = 0
  resSQL.First()
  while not resSQL.Eof:
    no_urut += 1

    if moduleapi.IsOddNumber(no_urut):
      bgcolor = '#EFEFEF'
    else:
      bgcolor = '#FFFFFF'

    #if resSQL.kode <> 'A':
    jumlah = moduleapi.FormatFloatStd(config, resSQL.sumTrans)
    #else:
    #  # pendaftaran peserta
    #  jumlah = str(resSQL.nbOfTrans)

    oFile.write('	<tr>\n')
    oFile.write('		<td width="10%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'">'+ str(no_urut) +'</td>\n')
    oFile.write('		<td width="20%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" align="center" bgcolor="'+ bgcolor +'">'+ resSQL.kode +'</td>\n')
    oFile.write('		<td width="50%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'">'+ resSQL.nama +'</td>\n')
    oFile.write('		<td width="20%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'">\n')
    oFile.write('		<p align="right">'+ jumlah +'</td>\n')
    oFile.write('	</tr>\n')

    total += resSQL.sumTrans

    resSQL.Next()

  return total

def ConstructReportTrailer(config, total, oFile):
  oFile.write('	<tr>\n')
  oFile.write('		<td width="80%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" colspan="3" bgcolor="#CC6699">\n')
  oFile.write('		<b>TOTAL</b></td>\n')
  oFile.write('		<td width="20%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, total) +'</b></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('</table>\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('</body>\n')
  oFile.write('\n')
  oFile.write('</html>\n')

def WriteToFile(config, parameter, oFile):
  bulan = parameter.FirstRecord.bulan
  tahun = parameter.FirstRecord.tahun
  if bulan == -999:
    jenis = 'T'
    strBulan = ''
  else:
    jenis = 'B'
    strBulan = moduleapi.IntMonthToStr(bulan)

  ConstructReportHeader(config, jenis, strBulan, str(tahun), oFile)
  sSQL = strSQLRekapTrans(config, jenis, bulan, tahun)
  config.SendDebugMsg(sSQL)
  total = ConstructReportValues(config, sSQL, oFile)
  ConstructReportTrailer(config, total, oFile)

def CreateReport(config, parameter, returnpacket):
  sBaseFileName = 'rekap_transaksi.htm'
  sFileName = config.UserHomeDirectory + sBaseFileName

  oFile = open(sFileName, 'w')
  WriteToFile(config, parameter, oFile)
  oFile.close()

  returnpacket.CreateValues(['filename',sBaseFileName])

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  CreateReport(config, parameter, returnpacket)

  return 1
