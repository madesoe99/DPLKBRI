import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi
import string

def ConstructReportHeader(config, strTanggalAwal, strTanggalAkhir, oFile):
  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Laporan Akumulasi Peserta Corporate</title>\n')
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Arial; line-height:100%; margin-top:0; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td colspan="7" height="20" style="border-left:medium none #000000; border-right:medium none #000000; border-top-style:none; border-top-width:medium; border-bottom-style:none; border-bottom-width:medium">\n')
  oFile.write('		<p align="center"><font size="3" color="#008000"><b>AKUMULASI DANA PERPAKET</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" colspan="7" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font color="#008000"><b>PERIODE '+ string.upper(strTanggalAwal) +' HINGGA '+ string.upper(strTanggalAkhir) +'</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="3%" align="center" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>NO</b></td>\n')
  oFile.write('		<td width="7%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>PAKET INVESTASI</b></td>\n')
  oFile.write('		<td width="9%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>AKUM DANA IURAN PST</b></td>\n')
  oFile.write('		<td width="9%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>AKUM DANA IURAN PK</b></td>\n')
  oFile.write('		<td width="9%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>AKUM DANA PENGEMBANGAN</b></td>\n')
  oFile.write('		<td width="9%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>AKUM DANA PERALIHAN</b></td>\n')
  oFile.write('		<td width="9%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>JUMLAH DANA</b></td>\n')
  oFile.write('	</tr>\n')


def strSQLSumValues(config, tgl_transaksi_awal, tgl_transaksi_akhir_plus):
  return \
    'select r.kode_paket_investasi '\
    '  , isnull(sum(t.MUTASI_IURAN_PK),0.0) as sumIuranPK '\
    '  , isnull(sum(t.MUTASI_IURAN_PST),0.0) as sumIuranPeserta '\
    '  , isnull(sum(t.MUTASI_PENGEMBANGAN),0.0) as sumPengembangan '\
    '  , isnull(sum(t.MUTASI_PERALIHAN),0.0) as sumPeralihan '\
    'from TRANSAKSIDPLK t, REKENINGDPLK r '\
    'where t.no_peserta = r.no_peserta '\
    '  and t.TGL_TRANSAKSI >= \'%s\' '\
    '  and t.TGL_TRANSAKSI < \'%s\' '\
    '  and r.status_dplk = \'A\' '\
    '  and t.ISCOMMITTED = \'T\' '\
    'group by r.kode_paket_investasi '\
    'order by r.kode_paket_investasi '\
    %(config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_awal)\
       , config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_akhir_plus)\
    )


def ConstructReportValues(config, strSQL, oFile):
  resSQL = config.CreateSQL(strSQL).RawResult

  no_urut = 0
  totdana = 0.0

  resSQL.First()
  while not resSQL.Eof:
  
    no_urut += 1

    if moduleapi.IsOddNumber(no_urut):
      bgcolor = '#EFEFEF'
    else:
      bgcolor = '#FFFFFF'


    akumiuranpst     = resSQL.sumIuranPeserta or 0.0
    akumiuranpk      = resSQL.sumIuranPK or 0.0
    akumpengembangan = resSQL.sumPengembangan or 0.0
    akumperalihan    = resSQL.sumPeralihan or 0.0
    
    totakum = (akumiuranpst + akumiuranpk + akumpengembangan + akumperalihan )
    totdana += totakum
    
    oFile.write('	<tr>\n')
    oFile.write('		<td width="3%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'" height="22">'+ str(no_urut) +'</td>\n')
    oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="center">'+ resSQL.kode_paket_investasi +'</td>\n')
    oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="right">'+moduleapi.FormatFloatStd(config, akumiuranpst, '-') +'</td>\n')
    oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="right">'+moduleapi.FormatFloatStd(config, akumiuranpk, '-') +'</td>\n')
    oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="right">'+moduleapi.FormatFloatStd(config, akumpengembangan, '-') +'</td>\n')
    oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="right">'+moduleapi.FormatFloatStd(config, akumperalihan, '-') +'</td>\n')
    oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="right">'+moduleapi.FormatFloatStd(config, totakum, '-') +'</td>\n')
    oFile.write('	</tr>\n')

    resSQL.Next()
    
  return totdana
    

def ConstructReportTrailer(config, totdana, oFile):
  oFile.write('	<tr>\n')
  oFile.write('		<td width="44%" colspan="6" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" colspan="6" bgcolor="#CC6699">\n')
  oFile.write('		<b>TOTAL DANA</b></td>\n')
  #oFile.write('		<td width="7%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  #oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totJmlTarik) +'</b></td>\n')
  #oFile.write('		<td width="7%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  #oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totBiayaNormal) +'</b></td>\n')
  #oFile.write('		<td width="7%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  #oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totBiayaPHK) +'</b></td>\n')
  #oFile.write('		<td width="7%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  #oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totPajak) +'</b></td>\n')
  #oFile.write('		<td width="7%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  #oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totNominalTarikAkhir) +'</b></td>\n')
  oFile.write('		<td width="9%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totdana) +'</b></td>\n')
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

  strSQL = strSQLSumValues(config, tgl_transaksi_awal, tgl_transaksi_akhir + 1)
  config.SendDebugMsg(strSQL)

  totdana = ConstructReportValues(config, strSQL, oFile)

  ConstructReportTrailer(
    config, totdana
    , oFile
  )

def CreateReport(config, parameter, returnpacket):
  sBaseFileName = 'Akumulasi Dana Perpaket.htm'
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

