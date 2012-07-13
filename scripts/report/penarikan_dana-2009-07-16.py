import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi
import string

def ConstructReportHeader(config, strTanggalAwal, strTanggalAkhir, oFile):
  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Laporan Penarikan Dana</title>\n')
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Arial; line-height:100%; margin-top:0; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td colspan="12" height="20" style="border-left:medium none #000000; border-right:medium none #000000; border-top-style:none; border-top-width:medium; border-bottom-style:none; border-bottom-width:medium">\n')
  oFile.write('		<p align="center"><font size="3" color="#008000"><b>PENARIKAN DANA (PENARIKAN \n')
  oFile.write('		30% DAN PHK)</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" colspan="12" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font color="#008000"><b>PERIODE '+ string.upper(strTanggalAwal) +' HINGGA '+ string.upper(strTanggalAkhir) +'</b></font></td>\n')
  oFile.write('	</tr>\n')

  oFile.write('	<tr>\n')
  oFile.write('		<td width="2%" align="center" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>NO</b></td>\n')
  oFile.write('		<td width="15%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>NAMA LENGKAP</b></td>\n')
  oFile.write('		<td width="7%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>NO. PESERTA</b></td>\n')
  oFile.write('		<td width="9%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<p style="margin-top: 0; margin-bottom: 0"><b>TGL. TRANSAKSI</b></p>\n')
  oFile.write('		<p style="margin-top: 0; margin-bottom: 0"><b>(DD/MM/YY)</b></td>\n')
  oFile.write('		<td width="7%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>SALDO IURAN</b></td>\n')
  oFile.write('		<td width="4%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>JENIS</b></td>\n')
  oFile.write('		<td width="7%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>NOMINAL PENARIKAN</b></td>\n')
  oFile.write('		<td width="7%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>BIAYA 1%</b></td>\n')
  oFile.write('		<td width="7%" align="center" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>BIAYA 2.5% PHK</b></td>\n')
  oFile.write('		<td width="7%" align="center" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>PAJAK</b></td>\n')
  oFile.write('		<td width="7%" align="center" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>NOMINAL</b></td>\n')
  oFile.write('		<td width="21%" align="center" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>KETERANGAN</b></td>\n')
  oFile.write('	</tr>\n')

def strSQLDaftarTransaksi(config, tgl_transaksi_awal, tgl_transaksi_akhir_plus):
  return \
    'select isnull(tgl_transaksi,\'\') tgl_transaksi '\
    '  , r.no_peserta '\
    '  , isnull(mutasi_iuran_pk + mutasi_iuran_pst + mutasi_pengembangan + mutasi_peralihan,0.0) mutasi '\
    '  , kode_jenis_transaksi '\
    '  , ID_Transaksi '\
    '  , t.Keterangan '\
    'from TransaksiDPLK t '\
    '  , RekeningDPLK r '\
    'where t.isCommitted = \'T\' '\
    '  and tgl_transaksi >= \'%s\' '\
    '  and tgl_transaksi < \'%s\' '\
    '  and t.no_peserta = r.no_peserta '\
    '  and kode_jenis_transaksi in (\'V\', \'W\') '\
    'order by tgl_transaksi; '\
    % (config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_awal)\
       , config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_akhir_plus)\
    )

def ConstructReportValues(config, strSQL, oFile):
  resSQL = config.CreateSQL(strSQL).RawResult

  no_urut = 0

  totJmlTarik = 0.0
  totBiayaNormal = 0.0
  totBiayaPHK = 0.0
  totPajak = 0.0
  totNominalTarikAkhir = 0.0
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
      
    biayaNormal = 0.0
    biayaPHK = 0.0
    if resSQL.kode_jenis_transaksi == 'V':
      # penarikan dana 30%
      oPenarikan = config.CreatePObjImplProxy('PenarikanDanaNormal')
      oPenarikan.Key = resSQL.ID_Transaksi

      jenisPenarikan = '30%'

      biayaNormal = oPenarikan.biaya_tarik or 0.0
      strBiayaNormal = moduleapi.FormatFloatStd(config, biayaNormal, '-')
      strBiayaPHK = '-'
    elif resSQL.kode_jenis_transaksi == 'W':
      # penarikan dana PHK
      oPenarikan = config.CreatePObjImplProxy('PenarikanDanaPHK')
      oPenarikan.Key = resSQL.ID_Transaksi

      jenisPenarikan = 'PHK'

      biayaPHK = oPenarikan.biaya_tarik or 0.0
      strBiayaNormal = '-'
      strBiayaPHK = moduleapi.FormatFloatStd(config, biayaPHK, '-')
    else:
      raise Exception, 'Kesalahan Kode Jenis Transaksi' +  '\nKode jenis transaksi \'%s\' tidak dikenali sebagai transaksi penarikan dana.' % (str(resSQL.kode_jenis_transaksi))

    saldo_iuran_awal = oPenarikan.saldo_iuran_awal or 0.0
    jml_tarik = oPenarikan.jml_tarik or 0.0
    pajak = oPenarikan.pajak or 0.0
    nominalTarikAkhir = jml_tarik - biayaPHK - pajak

    oFile.write('	<tr>\n')
    oFile.write('		<td width="2%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'" height="22">'+ str(no_urut) +'</td>\n')
    oFile.write('		<td width="15%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">'+ oPenarikan.LRekeningDPLK.LNasabahDPLK.nama_lengkap +'</td>\n')
    oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="center">'+ oPenarikan.no_peserta +'</td>\n')
    oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="center">'+ strTglTransaksi +'</td>\n')
    oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, saldo_iuran_awal, '-') +'</td>\n')
    oFile.write('		<td width="4%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="center">'+ jenisPenarikan +'</td>\n')
    oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, jml_tarik, '-') +'</td>\n')
    oFile.write('		<td width="7%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="right">'+ strBiayaNormal +'</td>\n')
    oFile.write('		<td width="7%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		'+ strBiayaPHK +'</td>\n')
    oFile.write('		<td width="7%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		'+ moduleapi.FormatFloatStd(config, pajak, '-') +'</td>\n')
    oFile.write('		<td width="7%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		'+ moduleapi.FormatFloatStd(config, nominalTarikAkhir, '-') +'</td>\n')
    oFile.write('		<td width="21%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">'+ (resSQL.Keterangan or '&nbsp;') +'</td>\n')
    oFile.write('	</tr>\n')

    totJmlTarik += jml_tarik
    totBiayaNormal += biayaNormal
    totBiayaPHK += biayaPHK
    totPajak += pajak
    totNominalTarikAkhir += nominalTarikAkhir

    resSQL.Next()

  return totJmlTarik, totBiayaNormal, totBiayaPHK, totPajak, totNominalTarikAkhir

def ConstructReportTrailer(config, totJmlTarik, totBiayaNormal, totBiayaPHK, totPajak, totNominalTarikAkhir, oFile):
  oFile.write('	<tr>\n')
  oFile.write('		<td width="44%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" colspan="6" bgcolor="#CC6699">\n')
  oFile.write('		<b>TOTAL</b></td>\n')
  oFile.write('		<td width="7%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totJmlTarik) +'</b></td>\n')
  oFile.write('		<td width="7%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totBiayaNormal) +'</b></td>\n')
  oFile.write('		<td width="7%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totBiayaPHK) +'</b></td>\n')
  oFile.write('		<td width="7%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totPajak) +'</b></td>\n')
  oFile.write('		<td width="7%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totNominalTarikAkhir) +'</b></td>\n')
  oFile.write('		<td width="21%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		&nbsp;</td>\n')
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
  totJmlTarik, totBiayaNormal, totBiayaPHK, totPajak, totNominalTarikAkhir = ConstructReportValues(config, strSQL, oFile)
  ConstructReportTrailer(config, totJmlTarik, totBiayaNormal, totBiayaPHK, totPajak, totNominalTarikAkhir, oFile)

def CreateReport(config, parameter, returnpacket):
  sBaseFileName = 'penarikan_dana.htm'
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

