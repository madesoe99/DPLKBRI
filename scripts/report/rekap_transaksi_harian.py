import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi
import string

def ConstructReportHeader(config, strTglAwal, strTglAkhir, oFile):
  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Rekapitulasi Transaksi Harian</title>\n')
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Arial; line-height:100%; margin-top:0; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td colspan="4" height="20" style="border-left:medium none #000000; border-right:medium none #000000; border-top-style:none; border-top-width:medium; border-bottom-style:none; border-bottom-width:medium">\n')
  oFile.write('		<p align="center"><font size="3" color="#008000"><b>REKAPITULASI TRANSAKSI HARIAN</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" colspan="4" style="border-style: none; border-width: medium">\n')
  oFile.write('		<b><font color="#008000">PERIODE '+ string.upper(strTglAwal) +' HINGGA '+ string.upper(strTglAkhir) +'</font></b></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="10%" align="center" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>NO</b></td>\n')
  oFile.write('		<td width="20%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>KODE</b></td>\n')
  oFile.write('		<td width="30%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>JENIS TRANSAKSI</b></td>\n')
  oFile.write('		<td width="20%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>JUMLAH DATA</b></td>\n')
  oFile.write('		<td width="20%" align="center" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>JUMLAH</b></td>\n')
  oFile.write('	</tr>\n')

def strSQLRekapTrans(config, tglAwal, tglAkhirPlus):
  #'  , count(j.kode_jenis_transaksi) jmldata '\
  strSQL = \
    'select j.kode_jenis_transaksi kode '\
    '  , isnull(nama_transaksi,\'\') nama '\
    '  , count(distinct(t.no_peserta)) jmldata '\
    '  , isnull(sum(mutasi_peralihan + mutasi_pengembangan + mutasi_iuran_pst + mutasi_iuran_pk),0.0) sumTrans '\
    'from '\
    '(select kode_jenis_transaksi '\
    '  , nama_transaksi '\
    'from JenisTransaksiDPLK '\
    'where kode_jenis_transaksi not in (\'A\',\'B\')) as j '\
    'left outer join '\
    '(select id_transaksi '\
    '  , no_peserta '\
    '  , kode_jenis_transaksi '\
    '  , mutasi_peralihan '\
    '  , mutasi_pengembangan '\
    '  , mutasi_iuran_pst '\
    '  , mutasi_iuran_pk '\
    'from TransaksiDPLK '\
    'where tgl_transaksi >= \'%s\' '\
    '  and tgl_transaksi < \'%s\' '\
    '  and ISCOMMITTED = \'T\' '\
    ') as t '\
    'on j.kode_jenis_transaksi = t.kode_jenis_transaksi '\
    'group by j.kode_jenis_transaksi '\
    '  , nama_transaksi' \
    % (config.FormatDateTime('yyyy-mm-dd',tglAwal)\
       , config.FormatDateTime('yyyy-mm-dd',tglAkhirPlus))

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
    jumlahdata = str(resSQL.jmldata)

    if jumlah == '0':
       jumlahdata = '-'
       jumlah = '-'
       


    #else:
    #  # pendaftaran peserta
    #  jumlah = str(resSQL.nbOfTrans)

    oFile.write('	<tr>\n')
    oFile.write('		<td width="10%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'">'+ str(no_urut) +'</td>\n')
    oFile.write('		<td width="20%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" align="center" bgcolor="'+ bgcolor +'">'+ resSQL.kode +'</td>\n')
    oFile.write('		<td width="30%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'">'+ resSQL.nama +'</td>\n')
    oFile.write('		<td width="20%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'">\n')
    oFile.write('		<p align="right">'+ jumlahdata +'</td>\n')
    oFile.write('		<td width="20%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'">\n')
    oFile.write('		<p align="right">'+ jumlah +'</td>\n')
    oFile.write('	</tr>\n')

    total += resSQL.sumTrans

    resSQL.Next()

  return total

def ConstructReportTrailer(config, total, oFile):
  oFile.write('	<tr>\n')
  oFile.write('		<td width="80%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" colspan="4" bgcolor="#CC6699">\n')
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
  tgl_transaksi_awal = parameter.FirstRecord.tanggal_awal
  tgl_transaksi_akhir = parameter.FirstRecord.tanggal_akhir

  strTglAwal = config.FormatDateTime('dd mmmm yyyy',tgl_transaksi_awal)
  strTglAkhir = config.FormatDateTime('dd mmmm yyyy',tgl_transaksi_akhir)
  ConstructReportHeader(config, strTglAwal, strTglAkhir, oFile)
  total = ConstructReportValues(config, strSQLRekapTrans(config, tgl_transaksi_awal, tgl_transaksi_akhir + 1), oFile)
  ConstructReportTrailer(config, total, oFile)

def CreateReport(config, parameter, returnpacket):
  sBaseFileName = 'rekap_transaksi_harian.htm'
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
