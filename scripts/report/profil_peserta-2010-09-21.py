import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi
import string

def GetValuesFromKlasifikasi(config, klasifikasi):
  if klasifikasi == 'J':
    info = 'Jenis Usaha'
    code = 'Kode Jenis Usaha'
    name = 'Nama Jenis Usaha'
    strSQL = \
      'select k.kode_jenis_usaha kode, k.nama_jenis_usaha nama, count(n.no_peserta) jumlah '\
      'from jenisusaha k, nasabahdplk n, rekeningdplk r '\
      'where n.no_peserta = r.no_peserta '\
      '  and k.kode_jenis_usaha = n.kode_jenis_usaha '\
      '  and r.status_dplk = \'A\' '\
      'group by k.kode_jenis_usaha, k.nama_jenis_usaha'
  elif klasifikasi == 'D':
    info = 'Daerah Asal'
    code = 'Kode Propinsi'
    name = 'Nama Propinsi'
    strSQL = \
      'select k.kode_propinsi kode, k.nama_propinsi nama, count(n.no_peserta) jumlah '\
      'from daerahasal k, nasabahdplk n, rekeningdplk r '\
      'where n.no_peserta = r.no_peserta '\
      '  and k.kode_propinsi = n.kode_propinsi '\
      '  and r.status_dplk = \'A\' '\
      'group by k.kode_propinsi, k.nama_propinsi'
  elif klasifikasi == 'K':
    info = 'Kepemilikan'
    code = 'Kode Kepemilikan'
    name = 'Keterangan'
    strSQL = \
      'select k.kode_pemilikan kode, k.keterangan nama, count(n.no_peserta) jumlah '\
      'from kepemilikan k, nasabahdplk n, rekeningdplk r '\
      'where n.no_peserta = r.no_peserta '\
      '  and k.kode_pemilikan = n.kode_pemilikan '\
      '  and r.status_dplk = \'A\' '\
      'group by k.kode_pemilikan, k.keterangan'
  elif klasifikasi == 'E':
    info = 'Kelompok'
    code = 'Kode Kelompok'
    name = 'Nama Kelompok'
    strSQL = \
      'select k.kode_kelompok kode, k.nama_kelompok nama, count(n.no_peserta) jumlah '\
      'from kelompok k, nasabahdplk n, rekeningdplk r '\
      'where k.kode_kelompok = n.kode_kelompok '\
      '  and r.status_dplk = \'A\' '\
      'group by k.kode_kelompok, k.nama_kelompok'
  else:
    raise 'Kesalahan Klasifikasi','Klasifikasi tidak dikenal.'

  return [info, code, name, strSQL]  

def ConstructReportHeader(config, valKlasifikasi, oFile):
  info, code, name = valKlasifikasi[:3]

  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Profil Peserta Menurut '+ info +'</title>\n')
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Arial; line-height:100%; margin-top:0; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td colspan="4" height="20" style="border-left:medium none #000000; border-right:medium none #000000; border-top-style:none; border-top-width:medium; border-bottom-style:none; border-bottom-width:medium">\n')
  oFile.write('		<p align="center"><b><font size="3" color="#008000">PROFIL PESERTA MENURUT '+ string.upper(info) +'</font></b></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" colspan="4" style="border-style: none; border-width: medium">&nbsp;</td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="10%" align="center" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699"><b>NO</b></td>\n')
  oFile.write('		<td width="20%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699"><b>'+ string.upper(code) +'</b></td>\n')
  oFile.write('		<td width="50%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699"><b>'+ string.upper(name) +'</b></td>\n')
  oFile.write('		<td width="20%" align="center" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699"><b>JUMLAH</b></td>\n')
  oFile.write('	</tr>\n')

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

    oFile.write('	<tr>\n')
    oFile.write('		<td width="10%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'">'+ str(no_urut) +'</td>\n')
    oFile.write('		<td width="20%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" align="center" bgcolor="'+ bgcolor +'">'+ resSQL.kode +'</td>\n')
    oFile.write('		<td width="50%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'">'+ resSQL.nama +'</td>\n')
    oFile.write('		<td width="20%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'">\n')
    oFile.write('		<p align="right">'+ str(resSQL.jumlah) +'</td>\n')
    oFile.write('	</tr>\n')

    total += resSQL.jumlah

    resSQL.Next()

  return total    

def ConstructReportTrailer(config, total, oFile):
  oFile.write('	<tr>\n')
  oFile.write('		<td width="80%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" colspan="3" bgcolor="#CC6699">\n')
  oFile.write('		<b>TOTAL</b></td>\n')
  oFile.write('		<td width="20%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ str(total) +'</b></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('</table>\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('</body>\n')
  oFile.write('\n')
  oFile.write('</html>\n')

def WriteToFile(config, parameter, oFile):
  klasifikasi = parameter.FirstRecord.klasifikasi

  valKlasifikasi = GetValuesFromKlasifikasi(config, klasifikasi)
  ConstructReportHeader(config, valKlasifikasi, oFile)
  total = ConstructReportValues(config, valKlasifikasi[3], oFile)
  ConstructReportTrailer(config, total, oFile)

def CreateReport(config, parameter, returnpacket):
  sBaseFileName = 'profil_peserta.htm'
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

