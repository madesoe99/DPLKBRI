import sys
import string
import com.ihsan.util.modman as modman

def ConstructReportHeader(config, strTanggalAwal, strTanggalAkhir, oFile):
  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Laporan Perolehan Peserta</title>\n')
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Arial; line-height:100%; margin-top:0; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td colspan="8" height="20" style="border-left:medium none #000000; border-right:medium none #000000; border-top-style:none; border-top-width:medium; border-bottom-style:none; border-bottom-width:medium">\n')
  oFile.write('		<p align="center"><font size="3" color="#008000"><b>HISTORI HASIL INVESTASI</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" colspan="11" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font color="#008000"><b>PERIODE '+ string.upper(strTanggalAwal) +' HINGGA '+ string.upper(strTanggalAkhir) +'</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="3%" align="center" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>NO</b></td>\n')
  oFile.write('		<td width="9%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>KODE PIHAK III</b></td>\n')
  oFile.write('		<td width="18%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>NAMA PIHAK III</b></td>\n')
  oFile.write('		<td width="7%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>NO BILYET</b></td>\n')
  oFile.write('		<td width="9%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>TGL BUKA</b></td>\n')
  #oFile.write('		<td width="9%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  #oFile.write('		<b>TGL TUTUP</b></td>\n')
  oFile.write('		<td width="9%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>NOMINAL PEMBUKAAN</b></td>\n')
  oFile.write('		<td width="9%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>TGL BAG HAS</b></td>\n')
  oFile.write('		<td width="9%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>HASIL INVESTASI</b></td>\n')
  oFile.write('		<td width="9%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>NISBAH</b></td>\n')
 # oFile.write('		<td width="9%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
 # oFile.write('		<b>STATUS</b></td>\n')
  oFile.write('		<td width="9%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>KETERANGAN</b></td>\n')

  oFile.write('	</tr>\n')


def strSQLPihakKetiga(config, kode_pihak_ketiga):
  return \
    'select nama_pihak_ketiga '\
    '  from pihakketiga '\
    '  where kode_pihak_ketiga = \'%s\' ;'\
    % (kode_pihak_ketiga)
  
def strSQLHistHslInv(config, tgl_transaksi_awal, tgl_transaksi_akhir_plus):
  return \
    'select D.REKENING_DEPOSITO '\
    '  , D.KODE_PIHAK_KETIGA '\
    '  , D.TGL_BUKA  '\
    '  , D.AKUM_NOMINAL '\
    '  , D.NISBAH      '\
    '  , T.TGL_TRANSAKSI '\
    '  , T.MUTASI_KREDIT   '\
    '  , T.KETERANGAN  '\
    'from DEPOSITOHISTORI D, TRANSAKSIHISTORIINVESTASI T '\
    'where D.REKENING_DEPOSITO = T.REKENING_DEPOSITO '\
    '  AND T.tgl_transaksi >= \'%s\' '\
    '  and T.tgl_transaksi < \'%s\' '\
    ' ORDER BY D.KODE_PIHAK_KETIGA,D.REKENING_DEPOSITO, T.TGL_TRANSAKSI ;'\
    % (config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_awal)\
       , config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_akhir_plus)\
    )
    


def ConstructReportValues(config, strSQL, oFile):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  resSQL = config.CreateSQL(strSQL).RawResult
  no_urut = 0
  nomHasilreal = 0.0
  nomHasilNonreal = 0.0
  nomBeban = 0.0
  nomHasilBersih = 0.0
  totHasilInvestasi = hasilinvestasi = 0.0

  resSQL.First()
  while not resSQL.Eof:
    no_urut += 1

    if moduleapi.IsOddNumber(no_urut):
      bgcolor = '#EFEFEF'
    else:
      bgcolor = '#FFFFFF'

    config.SendDebugMsg('MASUK')
    strSQL = strSQLPihakKetiga(config, resSQL.kode_pihak_ketiga)
    rSQL = config.CreateSQL(strSQL).RawResult
    
    config.SendDebugMsg('horerererer')
    
    #config.SendDebugMsg('horerererer')
    #tgltutup = resSQL.tgl_tutup
    
    #if resSQL.tgl_jatuh_tempo <> None:
    #   strTglTutup = config.FormatDateTime('dd/mmm/yyyy',moduleapi.DateTimeTupleToFloat(config, resSQL.tgl_tutup))
    #else:
    #   strTglTutup = ''
    
    
    strTglBuka = config.FormatDateTime('dd/mmm/yyyy',moduleapi.DateTimeTupleToFloat(config, resSQL.tgl_buka))
    config.SendDebugMsg('cek tgl buka ')
    strTglTransaksi = config.FormatDateTime('dd/mmm/yyyy',moduleapi.DateTimeTupleToFloat(config, resSQL.tgl_transaksi))
    config.SendDebugMsg('cek tgl trans ')
    
    mutasi_kredit = resSQL.mutasi_kredit or 0.0
    mutasi_debet  =  0.0
    nominal_pembukaan = resSQL.akum_nominal or 0.0
    nomHasilreal  = (mutasi_kredit - mutasi_debet)
    hasilinvestasi = nomHasilreal
    #kode_pihak = resSQL.kode_pihak_ketiga
    
    totHasilInvestasi = totHasilInvestasi + hasilinvestasi

    #if resSQL.jatuhtempo > 0:
    #   depo = 'Berjangka'
    #else:
    #   depo = 'On Call'
    
    #if rSQL.eof:
    #   nama_pihak_ketiga = resSQL.nama_bank
    #else:
    nama_pihak_ketiga = rSQL.nama_pihak_ketiga
       
       
    config.SendDebugMsg('akan ke report ')
    oFile.write('	<tr>\n')
    oFile.write('		<td width="3%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'" height="22">'+ str(no_urut) +'</td>\n')
    oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="center">'+resSQL.kode_pihak_ketiga+'</td>\n')
    config.SendDebugMsg('kode bank '+ str(resSQL.kode_pihak_ketiga))
    oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="left">'+nama_pihak_ketiga+'</td>\n')
    config.SendDebugMsg('nama bank '+ nama_pihak_ketiga)
    oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="center">'+ str(resSQL.rekening_deposito) +'</td>\n')
    config.SendDebugMsg('nomdep '+ str(resSQL.rekening_deposito))
    oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="center">'+ strTglBuka +'</td>\n')
    config.SendDebugMsg('tgl buka '+ strTglBuka)
  #  oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
  #  oFile.write('		<p align="center">'+strTglTutup+'</td>\n')
    oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, nominal_pembukaan) +'</td>\n')
    config.SendDebugMsg('nom awal '+ str(moduleapi.FormatFloatStd(config, nominal_pembukaan)))
    oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="center">'+ strTglTransaksi +'</td>\n')
    config.SendDebugMsg('tgl trans '+ strTglTransaksi)
    oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, hasilinvestasi) +'</td>\n')
    config.SendDebugMsg('hasil investasi '+ str(moduleapi.FormatFloatStd(config, hasilinvestasi)))
    oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="center">'+ str(moduleapi.FormatFloatStd(config, resSQL.nisbah)) +'</td>\n')
    config.SendDebugMsg('nisbah '+ str(moduleapi.FormatFloatStd(config, resSQL.nisbah)))
    #oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
    #oFile.write('		<p align="center">'+ resSQL.status +'</td>\n')
    oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="center">'+ resSQL.keterangan +'</td>\n')
    oFile.write('	</tr>\n')
    config.SendDebugMsg('sukseeeeeeeeees')
    resSQL.Next()

  return totHasilInvestasi
  
def ConstructReportTrailer(config, totHasilInvestasi, oFile):
    moduleapi = modman.getModule(config, 'moduleapi')

    oFile.write('	<tr>\n')
    oFile.write('		<td width="100%" colspan="8" style="border-style: solid; border-width: medium">\n')
    oFile.write('		<font color="#008000"><p align="right"><b>Total Hasil Investasi</font></td>\n')
    oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#CC6699" height="22">\n')
    oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, totHasilInvestasi) +'</td>\n')
    oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#CC6699"" height="22">\n')
    oFile.write('		<p align="center">&nbsp;</td>\n')
    oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#CC6699"" height="22">\n')
    oFile.write('		<p align="center">&nbsp;</td>\n')
    oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#CC6699"" height="22">\n')
    oFile.write('		<p align="center">&nbsp;</td>\n')
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

  strSQL = strSQLHistHslInv(config, tgl_transaksi_awal, tgl_transaksi_akhir + 1)
  config.SendDebugMsg(strSQL)

  totHasilInvestasi = ConstructReportValues(config, strSQL, oFile)

  ConstructReportTrailer(
    config, totHasilInvestasi
    , oFile
  )

def CreateReport(config, parameter, returnpacket):
  sBaseFileName = 'historihslinv.htm'
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