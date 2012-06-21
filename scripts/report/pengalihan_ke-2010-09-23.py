import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi
import string

def ConstructReportHeader(config, strTanggalAwal, strTanggalAkhir, oFile):
  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Laporan Pengalihan Ke</title>\n')
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Arial; line-height:100%; margin-top:0; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td colspan="7" height="20" style="border-left:medium none #000000; border-right:medium none #000000; border-top-style:none; border-top-width:medium; border-bottom-style:none; border-bottom-width:medium">\n')
  oFile.write('		<p align="center"><font size="3" color="#008000"><b>LAPORAN PENGALIHAN KE </b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" colspan="7" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font color="#008000"><b>PERIODE '+ string.upper(strTanggalAwal) +' HINGGA '+ string.upper(strTanggalAkhir) +'</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="5%" align="center" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>NO</b></td>\n')
  oFile.write('		<td width="10%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<p style="margin-top: 0; margin-bottom: 0"><b>TGL. TRANSAKSI</b></p>\n')
  oFile.write('		<p style="margin-top: 0; margin-bottom: 0"><b>(DD/MM/YYYY)</b></td>\n')
  oFile.write('		<td width="10%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>NO. PESERTA</b></td>\n')
  oFile.write('		<td width="20%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>NAMA LENGKAP</b></td>\n')
  oFile.write('		<td width="10%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>JUMLAH DANA</b></td>\n')
  oFile.write('		<td width="10%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>BIAYA PINDAH</b></td>\n')
  oFile.write('		<td width="10%" align="center" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>BIAYA ADMINISTRASI</b></td>\n')
  oFile.write('		<td width="10%" align="center" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>BIAYA PENGELOLAAN</b></td>\n')
  oFile.write('		<td width="10%" align="center" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>BIAYA LAIN</b></td>\n')
  oFile.write('		<td width="10%" align="center" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>DANA DIALIHKAN</b></td>\n')
  oFile.write('		<td width="15%" align="center" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>DP TUJUAN</b></td>\n')
  oFile.write('	</tr>\n')

def strSQLDaftarTransaksi(config, tgl_transaksi_awal, tgl_transaksi_akhir_plus):

  return \
    'select isnull(tgl_transaksi,\'\') tgl_transaksi '\
    '  , n.no_peserta '\
    '  , isnull(nama_lengkap,\'\') nama_lengkap '\
    '  , t.tgl_transaksi '\
    '  , b.saldo_jml_dana '\
    '  , b.biaya_pindah '\
    '  , b.biaya_administrasi '\
    '  , b.biaya_pengelolaan '\
    '  , b.biaya_lain '\
    '  , b.dana_dialihkan '\
    '  , b.kode_dp '\
    'from TransaksiDPLK t '\
    '  , NasabahDPLK n '\
    '  , PengalihanKeDPLKLain b '\
    'where t.isCommitted = \'T\' '\
    '  and t.tgl_transaksi >= \'%s\' '\
    '  and t.tgl_transaksi < \'%s\' '\
    '  and t.id_transaksi = b.id_transaksi '\
    '  and t.no_peserta = n.no_peserta '\
    '  and t.kode_jenis_transaksi = \'H\' '\
    'order by tgl_transaksi '\
    % (config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_awal)\
       , config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_akhir_plus)\
       )


def ConstructReportValues(config, strSQL, oFile):
  resSQL = config.CreateSQL(strSQL).RawResult

  no_urut = 0
  
  totSaldoJmlDana = 0.0
  totBiayaPindah = 0.0
  totBiayaAdministrasi = 0.0
  totBiayaPengelolaan = 0.0
  totBiayaLain = 0.0
  totDanaDialihkan = 0.0


  resSQL.First()

  while not resSQL.Eof:
    no_urut += 1

    if moduleapi.IsOddNumber(no_urut):
      bgcolor = '#EFEFEF'
    else:
      bgcolor = '#FFFFFF'

    if resSQL.tgl_transaksi <> '':
      strTglTransaksi = config.FormatDateTime('dd/mm/yyyy',moduleapi.DateTimeTupleToFloat(config, resSQL.tgl_transaksi))
    else:
      strTglTransaksi = ''

    oFile.write('	<tr>\n')
    oFile.write('		<td width="5%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'">'+ str(no_urut) +'</td>\n')
    oFile.write('		<td width="10%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" >\n')
    oFile.write('		<p align="center">'+ strTglTransaksi +'</td>\n')
    oFile.write('		<td width="10%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" >\n')
    oFile.write('		<p align="center">'+ resSQL.no_peserta +'</td>\n')
    oFile.write('		<td width="20%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" >'+ resSQL.nama_lengkap +'</td>\n')
    oFile.write('		<td width="10%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" >\n')
    oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, resSQL.saldo_jml_dana) +'</td>\n')
    oFile.write('		<td width="10%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" >\n')
    oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, resSQL.biaya_pindah) +'</td>\n')
    oFile.write('		<td width="10%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'" >\n')
    oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, resSQL.biaya_administrasi) +'</td>\n')
    oFile.write('		<td width="10%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'" >\n')
    oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, resSQL.biaya_pengelolaan) +'</td>\n')
    oFile.write('		<td width="10%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'" >\n')
    oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, resSQL.biaya_lain) +'</td>\n')
    oFile.write('		<td width="10%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'" >\n')
    oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, resSQL.dana_dialihkan) +'</td>\n')
    oFile.write('		<td width="15%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'" >\n')
    oFile.write('		<p align="left">'+ resSQL.kode_dp +'</td>\n')
    oFile.write('	</tr>\n')

    totSaldoJmlDana += resSQL.saldo_jml_dana
    totBiayaPindah += resSQL.biaya_pindah
    totBiayaAdministrasi += resSQL.biaya_administrasi
    totBiayaPengelolaan += resSQL.biaya_pengelolaan
    totBiayaLain += resSQL.biaya_lain
    totDanaDialihkan += resSQL.dana_dialihkan
    
    resSQL.Next()

  return totSaldoJmlDana,totBiayaPindah,totBiayaAdministrasi,totBiayaPengelolaan,totBiayaLain,totDanaDialihkan

def ConstructReportTrailer(config, totSaldoJmlDana, totBiayaPindah, totBiayaAdministrasi, totBiayaPengelolaan, totBiayaLain, totDanaDialihkan, oFile):
  oFile.write('	<tr>\n')
  oFile.write('		<td width="85%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" colspan="4" bgcolor="#CC6699">\n')
  oFile.write('		<b>TOTAL</b></td>\n')
  oFile.write('		<td width="10%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totSaldoJmlDana) +'</b></td>\n')
  oFile.write('		<td width="10%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totBiayaPindah) +'</b></td>\n')
  oFile.write('		<td width="10%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totBiayaAdministrasi) +'</b></td>\n')
  oFile.write('		<td width="10%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totBiayaPengelolaan) +'</b></td>\n')
  oFile.write('		<td width="10%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totBiayaLain) +'</b></td>\n')
  oFile.write('		<td width="10%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totDanaDialihkan) +'</b></td>\n')
  oFile.write('		<td width="10%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b> &nbsp; </b></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('</table>\n')
  oFile.write('<p>&nbsp;</p>\n')
  oFile.write('<table border="2" width="100%" id="table4" style="border-width: 0px; border-collapse:collapse" bordercolorlight="#000000" bordercolordark="#000000">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td align="right" style="border-left-style: none; border-left-width: medium; border-right-style: none; border-right-width: medium; border-top-style: none; border-top-width: medium; border-bottom-style: solid; border-bottom-width: 1px">\n')
  oFile.write('		Dicetak tanggal '+ config.FormatDateTime('d mmmm yyyy', config.Now()) +'</td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td style="border-left-style: none; border-left-width: medium; border-right-style: none; border-right-width: medium; border-top-style: solid; border-top-width: 1px; border-bottom-style: none; border-bottom-width: medium"></td>\n')
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
  
  strTanggalAwal = config.FormatDateTime('dd mmmm yyyy',tgl_transaksi_awal)
  strTanggalAkhir = config.FormatDateTime('dd mmmm yyyy',tgl_transaksi_akhir)
  ConstructReportHeader(config, strTanggalAwal, strTanggalAkhir, oFile)

  strSQL = strSQLDaftarTransaksi(config, tgl_transaksi_awal, tgl_transaksi_akhir + 1)
  config.SendDebugMsg(strSQL)
  totSaldoJmlDana,totBiayaPindah,totBiayaAdministrasi,totBiayaPengelolaan,totBiayaLain,totDanaDialihkan = ConstructReportValues(config, strSQL, oFile)
  ConstructReportTrailer(
   config,
   totSaldoJmlDana,
   totBiayaPindah,
   totBiayaAdministrasi,
   totBiayaPengelolaan,
   totBiayaLain,
   totDanaDialihkan, oFile)

def CreateReport(config, parameter, returnpacket):
  sBaseFileName = 'Laporan_Pengalihan_Ke.htm'
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

