import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi
import string

def ConstructReportHeader(config, strTanggalAwal, strTanggalAkhir, oFile):
  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>DATA PREMI KE ASURANSI</title>\n')
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Arial; line-height:100%; margin-top:0; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td colspan="8" height="20" style="border-left:medium none #000000; border-right:medium none #000000; border-top-style:none; border-top-width:medium; border-bottom-style:none; border-bottom-width:medium">\n')
  oFile.write('		<p align="center"><font size="3" color="#008000"><b>DATA CETAK KARTU</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" colspan="11" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font color="#008000"><b>PERIODE '+ string.upper(strTanggalAwal) +' HINGGA '+ string.upper(strTanggalAkhir) +'</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="3%" align="center" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>NO</b></td>\n')
  oFile.write('		<td width="18%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>NO PESERTA</b></td>\n')
  oFile.write('		<td width="18%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>NAMA PESERTA</b></td>\n')
  oFile.write('		<td width="7%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>TGL LAHIR</b></td>\n')
  oFile.write('		<td width="7%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>IURAN</b></td>\n')
  oFile.write('		<td width="9%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>USIA PENSIUN</b></td>\n')
  oFile.write('		<td width="9%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>SALDO</b></td>\n')
  oFile.write('		<td width="9%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>MANFAAT</b></td>\n')
  oFile.write('		<td width="9%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>PREMI</b></td>\n')

  oFile.write('	</tr>\n')


def strSQLPesertaAlkhairat(config, tgl_transaksi_awal, tgl_transaksi_plus):
  return \
    'select n.no_peserta '\
    '  , n.nama_lengkap '\
    '  , n.tanggal_lahir '\
    '  , m.iuran_perbulan '\
    '  , r.usia_pensiun '\
    '  , m.saldo_awal '\
    '  , m.manfaat_asuransi '\
    '  , m.premi_perbulan '\
    'from NasabahDPLK n '\
    '  , MonitoringAlkhairat m '\
    '  , rekeningDPLK r   '\
    'where n.no_peserta = m.no_peserta '\
    '  and n.no_peserta = r.no_peserta '\
    '  and m.flag = \'F\' '\
    'order by n.no_peserta; '\

def ConstructReportValues(config, strSQL, oFile):
  resSQL = config.CreateSQL(strSQL).RawResult

  no_urut = 0
  
  resSQL.First()
  config.BeginTransaction()
  try:

     while not resSQL.Eof:
     
        oMonitoring = config.CreatePObjImplProxy('MonitoringAlkhairat')
        oMonitoring.key = resSQL.no_peserta
        oMonitoring.flag = 'T'
        oMonitoring.tgl_kirim = config.Now()

        config.Commit()
        
        no_urut += 1

        if moduleapi.IsOddNumber(no_urut):
           bgcolor = '#EFEFEF'
        else:
           bgcolor = '#FFFFFF'
      
        strTglLahir = config.FormatDateTime('dd/mm/yyyy',moduleapi.DateTimeTupleToFloat(config, resSQL.tanggal_lahir))

        oFile.write('	<tr>\n')
        oFile.write('		<td width="3%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'" height="22">'+ str(no_urut) +'</td>\n')
        oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
        oFile.write('		<p align="left">'+ resSQL.no_peserta +'</td>\n')
        oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
        oFile.write('		<p align="left">'+ resSQL.nama_lengkap +'</td>\n')
        oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
        oFile.write('		<p align="center">'+ strTglLahir +'</td>\n')
        oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
        oFile.write('		<p align="center">'+ moduleapi.FormatFloatStd(config,resSQL.iuran_perbulan, '-') +'</td>\n')
        oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
        oFile.write('		<p align="center">'+''+ str(resSQL.usia_pensiun) +'</td>\n')
        oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
        oFile.write('		<p align="center">'+ moduleapi.FormatFloatStd(config,resSQL.saldo_awal, '-') +'</td>\n')
        oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
        oFile.write('		<p align="center">'+ moduleapi.FormatFloatStd(config,resSQL.manfaat_asuransi, '-') +'</td>\n')
        oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
        oFile.write('		<p align="center">'+ moduleapi.FormatFloatStd(config,resSQL.premi_perbulan, '-') +'</td>\n')

        oFile.write('	</tr>\n')
        resSQL.Next()
        
  except:
     raise
  

def ConstructReportTrailer(config, strSQLNot, oFile):
  rSQL = config.CreateSQL(strSQLNot).RawResult
  
  if rSQL.jmlPeserta == 0:
     oFile.write('</table>\n')
  else:
     oFile.write('	<tr>\n')
     oFile.write('		<td width="100%" colspan="8" style="border-style: solid; border-width: medium">\n')
     oFile.write('		<font color="#008000"><b>ADA '+ str(rSQL.jmlPeserta) +' PESERTA YANG BELUM DI OTORISASI </b></font></td>\n')
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

  strSQL = strSQLPesertaAlkhairat(config, tgl_transaksi_awal, tgl_transaksi_akhir + 1)
  config.SendDebugMsg(strSQL)

  ConstructReportValues(config, strSQL, oFile)

  #ConstructReportTrailer(
  #  config, strSQLNot
  #  , oFile
  #)

def CreateReport(config, parameter, returnpacket):
  sBaseFileName = 'Data Cetak Kartu.htm'
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

