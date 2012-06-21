import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi
import string

def ConstructReportHeader(config, isDipercepat, tanggal_pensiun_awal, tanggal_pensiun_akhir, oFile):
  strDipercepat = ''
  if isDipercepat:
    strDipercepat = ' Dipercepat'

  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Masa Pensiun'+ strDipercepat +'</title>\n')
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Arial; line-height:100%; margin-top:0; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td colspan="9" height="20" style="border-left:medium none #000000; border-right:medium none #000000; border-top-style:none; border-top-width:medium; border-bottom-style:none; border-bottom-width:medium">\n')
  oFile.write('		<p align="center"><font size="3" color="#008000"><b>LAPORAN MASA PENSIUN'+ string.upper(strDipercepat) +'</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" colspan="9" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font color="#008000"><b>PERIODE</b></font> <b><font color="#008000">'+ string.upper(config.FormatDateTime('d mmmm yyyy',tanggal_pensiun_awal)) +' \n')
  oFile.write('		HINGGA '+ string.upper(config.FormatDateTime('d mmmm yyyy',tanggal_pensiun_akhir)) +'</font></b></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="5%" align="center" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699" rowspan="2">\n')
  oFile.write('		<p style="margin-top: 0; margin-bottom: 0"><b>NO</b></td>\n')
  oFile.write('		<td width="10%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699" rowspan="2">\n')
  oFile.write('		<p style="margin-top: 0; margin-bottom: 0"><b>NO. PESERTA</b></td>\n')
  oFile.write('		<td width="25%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699" rowspan="2">\n')
  oFile.write('		<p style="margin-top: 0; margin-bottom: 0"><b>NAMA LENGKAP</b></td>\n')
  oFile.write('		<td width="10%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<p style="margin-top: 0; margin-bottom: 0"><b>TANGGAL</b></p>\n')
  oFile.write('		<p style="margin-top: 0; margin-bottom: 0"><b>LAHIR</b></p>\n')
  oFile.write('		</td>\n')
  oFile.write('		<td width="10%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<p style="margin-top: 0; margin-bottom: 0"><b>TANGGAL</b></p>\n')
  oFile.write('		<p style="margin-top: 0; margin-bottom: 0"><b>PENSIUN</b></p>\n')
  oFile.write('		<p style="margin-top: 0; margin-bottom: 0"><b>DIPERCEPAT</b></td>\n')
  oFile.write('		<td width="10%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<p style="margin-top: 0; margin-bottom: 0"><b>TANGGAL</b></p>\n')
  oFile.write('		<p style="margin-top: 0; margin-bottom: 0"><b>PENSIUN</b></td>\n')
  oFile.write('		<td width="10%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699" rowspan="2">\n')
  oFile.write('		<p style="margin-top: 0; margin-bottom: 0"><b>AKUMULASI</b></p>\n')
  oFile.write('		<p style="margin-top: 0; margin-bottom: 0"><b>IURAN</b></td>\n')
  oFile.write('		<td width="10%" align="center" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699" rowspan="2">\n')
  oFile.write('		<p style="margin-top: 0; margin-bottom: 0"><b>AKUMULASI</b></p>\n')
  oFile.write('		<p style="margin-top: 0; margin-bottom: 0"><b>PENGALIHAN</b></td>\n')
  oFile.write('		<td width="10%" align="center" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699" rowspan="2">\n')
  oFile.write('		<p style="margin-top: 0; margin-bottom: 0"><b>AKUMULASI</b></p>\n')
  oFile.write('		<p style="margin-top: 0; margin-bottom: 0"><b>PENGEMBANGAN</b></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="30%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#CC6699" colspan="3">\n')
  oFile.write('		<p align="center"><b>(DD/MM/YYYY)</b></td>\n')
  oFile.write('	</tr>\n')

def strSQLMasaPensiun(config, isDipercepat, tanggal_pensiun_awal, tanggal_pensiun_akhir_plus):
  strTglDipercepat = ''
  if isDipercepat:
    strTglDipercepat = '_dipercepat'

  return \
    'select n.no_peserta '\
    '  , isnull(nama_lengkap,\'\') nama_lengkap '\
    '  , isnull(tanggal_lahir, \'\') tanggal_lahir '\
    '  , isnull(tgl_pensiun_dipercepat, \'\') tgl_pensiun_dipercepat '\
    '  , isnull(tgl_pensiun, \'\') tgl_pensiun '\
    '  , isnull(akum_dana_iuran_pk, 0.0) akum_dana_iuran_pk '\
    '  , isnull(akum_dana_iuran_pst, 0.0) akum_dana_iuran_pst '\
    '  , isnull(akum_dana_peralihan, 0.0) akum_dana_peralihan '\
    '  , isnull(akum_dana_pengembangan, 0.0) akum_dana_pengembangan '\
    'from nasabahdplk n, rekeningdplk r '\
    'where n.no_peserta = r.no_peserta '\
    '  and tgl_pensiun%s >= \'%s\' '\
    '  and tgl_pensiun%s < \'%s\' '\
    'order by n.no_peserta'\
    % (strTglDipercepat\
       , config.FormatDateTime('yyyy-mm-dd',tanggal_pensiun_awal)\
       , strTglDipercepat\
       , config.FormatDateTime('yyyy-mm-dd',tanggal_pensiun_akhir_plus))

def ConstructReportValues(config, strSQL, oFile):
  resSQL = config.CreateSQL(strSQL).RawResult

  no_urut = 0
  totAkumIuran = 0.0
  totAkumPeralihan = 0.0
  totAkumPengembangan = 0.0
  resSQL.First()
  while not resSQL.Eof:
    no_urut += 1

    if moduleapi.IsOddNumber(no_urut):
      bgcolor = '#EFEFEF'
    else:
      bgcolor = '#FFFFFF'

    akumIuran = resSQL.akum_dana_iuran_pk + resSQL.akum_dana_iuran_pst
    strAkumIuran = moduleapi.FormatFloatStd(config, akumIuran)
    strAkumPeralihan = moduleapi.FormatFloatStd(config, resSQL.akum_dana_peralihan)
    strAkumPengembangan = moduleapi.FormatFloatStd(config, resSQL.akum_dana_pengembangan)

    if resSQL.tanggal_lahir <> '':
      strTglLahir = config.FormatDateTime('dd/mm/yyyy',moduleapi.DateTimeTupleToFloat(config, resSQL.tanggal_lahir))
    else:
      strTglLahir = ''

    if resSQL.tgl_pensiun_dipercepat <> '':
      strTglPensiunDipercepat = config.FormatDateTime('dd/mm/yyyy',moduleapi.DateTimeTupleToFloat(config, resSQL.tgl_pensiun_dipercepat))
    else:
      strTglPensiunDipercepat = ''

    if resSQL.tgl_pensiun <> '':
      strTglPensiun = config.FormatDateTime('dd/mm/yyyy',moduleapi.DateTimeTupleToFloat(config, resSQL.tgl_pensiun))
    else:
      strTglPensiun = ''

    oFile.write('	<tr>\n')
    oFile.write('		<td width="5%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'">'+ str(no_urut) +'</td>\n')
    oFile.write('		<td width="10%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'">\n')
    oFile.write('		<p align="center">'+ resSQL.no_peserta +'</td>\n')
    oFile.write('		<td width="25%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'">'+ resSQL.nama_lengkap +'</td>\n')
    oFile.write('		<td width="10%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" align="center">\n')
    oFile.write('		<p align="center">'+ strTglLahir +'</td>\n')
    oFile.write('		<td width="10%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" align="center">'+ strTglPensiunDipercepat +'</td>\n')
    oFile.write('		<td width="10%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" align="center">'+ strTglPensiun +'</td>\n')
    oFile.write('		<td width="10%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'">\n')
    oFile.write('		<p align="right">'+ strAkumIuran +'</td>\n')
    oFile.write('		<td width="10%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'">\n')
    oFile.write('		<p align="right">'+ strAkumPeralihan +'</td>\n')
    oFile.write('		<td width="10%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'">'+ strAkumPengembangan +'</td>\n')
    oFile.write('	</tr>\n')

    totAkumIuran += akumIuran
    totAkumPeralihan += resSQL.akum_dana_peralihan
    totAkumPengembangan += resSQL.akum_dana_pengembangan

    resSQL.Next()

  return (totAkumIuran, totAkumPeralihan, totAkumPengembangan)

def ConstructReportTrailer(config, totAkumIuran, totAkumPeralihan, totAkumPengembangan, oFile):
  oFile.write('	<tr>\n')
  oFile.write('		<td width="70%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" colspan="6" bgcolor="#CC6699">\n')
  oFile.write('		<b>TOTAL</b></td>\n')
  
  oFile.write('		<td width="10%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totAkumIuran) +'</b></td>\n')
  oFile.write('		<td width="10%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totAkumPeralihan) +'</b></td>\n')
  oFile.write('		<td width="10%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totAkumPengembangan) +'</b></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('</table>\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('</body>\n')
  oFile.write('\n')
  oFile.write('</html>\n')

def WriteToFile(config, parameter, oFile):
  tanggal_pensiun_awal = parameter.FirstRecord.tanggal_pensiun_awal
  tanggal_pensiun_akhir = parameter.FirstRecord.tanggal_pensiun_akhir
  isDipercepat = parameter.FirstRecord.isDipercepat

  ConstructReportHeader(config, isDipercepat, tanggal_pensiun_awal, tanggal_pensiun_akhir, oFile)
  strSQL = strSQLMasaPensiun(config, isDipercepat, tanggal_pensiun_awal, tanggal_pensiun_akhir + 1)
  totAkumIuran, totAkumPeralihan, totAkumPengembangan = ConstructReportValues(config, strSQL, oFile)[:3]
  ConstructReportTrailer(config, totAkumIuran, totAkumPeralihan, totAkumPengembangan, oFile)

def CreateReport(config, parameter, returnpacket):
  sBaseFileName = 'saldo_iuran_pst.htm'
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
