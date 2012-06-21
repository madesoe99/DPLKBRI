import sys
import string
import com.ihsan.util.modman as modman

#modulapi = modman.getModule(config, 'moduleapi')


def ConstructReportHeader(config, oFile):
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
  oFile.write('		<p align="center"><font size="3" color="#008000"><b>INFORMASI DANA IDLE</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td colspan="8" height="20" style="border-left:medium none #000000; border-right:medium none #000000; border-top-style:none; border-top-width:medium; border-bottom-style:none; border-bottom-width:medium">\n')
  oFile.write('		<p align="center"><font size="3" color="#008000"><b>PERPAKET INVESTASI</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" colspan="11" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font color="#008000"><b>&nbsp; </b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="3%" align="center" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>NO</b></td>\n')
  oFile.write('		<td width="7%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>PAKET</b></td>\n')
  oFile.write('		<td width="7%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>MAKS. PROPORSI</b></td>\n')
  oFile.write('		<td width="10%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>NOMINAL PAKET</b></td>\n')
  oFile.write('		<td width="10%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>PROPORSI MAKSIMUM</b></td>\n')
  oFile.write('		<td width="10%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>DEPOSITO EXISTING</b></td>\n')
  oFile.write('		<td width="10%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>REKSADANA/SUKUK EXISTING</b></td>\n')
  oFile.write('		<td width="10%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')

  oFile.write('		<b>DANA IDLE</b></td>\n')
  oFile.write('	</tr>\n')

def strSQLPaketInvestasi(config):
  return \
    'select kode_paket_investasi '\
    '  from paketinvestasi '\
    ' where kode_paket_investasi in (\'A\',\'B\',\'C\') '\

def ConstructReportValues(config, oFile):
  #DAF4.0
  paketinvinfoIdle = modman.getModule(config, 'scripts#investasi.transaksi.moduleapi')
  
  no_urut = 0
  nomHasilreal = 0.0
  nomHasilNonreal = 0.0
  nomBeban = 0.0
  nomHasilBersih = 0.0
  totHasilInvestasi = hasilinvestasi = 0.0
 
  strSQL = strSQLPaketInvestasi(config)
  resSQL = config.CreateSQL(strSQL).RawResult

  resSQL.First()
  totdpkTersedia = 0.0
  while not resSQL.Eof:
      no_urut += 1

      if moduleapi.IsOddNumber(no_urut):
          bgcolor = '#EFEFEF'
      else:
          bgcolor = '#FFFFFF'
      
      KodeJnsInv = 'D'      
      dpkPaket = dpkInvExisting = dpkTersedia = nilaiMaksProporsi = nominalGiro = 0.0  
      dpkPaket, dpkInvExisting, dpkTersedia, nilaiMaksProporsi, nominalGiro, dpkDiinvestasikan = paketinvinfoIdle.getPaketInfo(config, resSQL.kode_paket_investasi, KodeJnsInv)
      
      oFile.write('	<tr>\n')
      oFile.write('		<td width="3%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'" height="22">'+ str(no_urut) +'</td>\n')
      oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
      oFile.write('		<p align="center">'+ resSQL.kode_paket_investasi +'</td>\n')
      oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
      oFile.write('		<p align="center"> 100</td>\n')
      oFile.write('		<td width="10%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
      oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config,dpkPaket) +'</td>\n')
      oFile.write('		<td width="10%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
      oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config,nilaiMaksProporsi) +'</td>\n')
      oFile.write('		<td width="10%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
      oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config,dpkInvExisting)+'</td>\n')
      
      if resSQL.kode_paket_investasi == 'B':
            KodeJnsInv = 'O'
            dpkPaket, dpkInvExisting, dpkTersedia, nilaiMaksProporsi, nominalGiro, dpkDiinvestasikan = paketinvinfoIdle.getPaketInfo(config, resSQL.kode_paket_investasi, KodeJnsInv)
            oFile.write('		<td width="10%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
            oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config,dpkInvExisting)+'</td>\n')
      elif resSQL.kode_paket_investasi == 'C':
            KodeJnsInv = 'R'
            dpkPaket, dpkInvExisting, dpkTersedia, nilaiMaksProporsi, nominalGiro, dpkDiinvestasikan = paketinvinfoIdle.getPaketInfo(config, resSQL.kode_paket_investasi, KodeJnsInv)
            oFile.write('		<td width="10%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
            oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config,dpkInvExisting)+'</td>\n')
      else:
            oFile.write('		<td width="10%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
            oFile.write('		<p align="right">0</td>\n')

      oFile.write('		<td width="10%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
      oFile.write('		<p align="right">'+moduleapi.FormatFloatStd(config,dpkTersedia) +'</td>\n')
      oFile.write('	</tr>\n')
    
      totdpkTersedia += dpkTersedia
      resSQL.Next()

  return totdpkTersedia
  
def ConstructReportTrailer(config, totdpkTersedia, oFile):

    oFile.write('	<tr>\n')
    oFile.write('		<td width="100%" colspan="7" style="border-style: solid; border-width: medium">\n')
    oFile.write('		<font color="#008000"><p align="right"><b>Total Dana Idle </font></td>\n')
    oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#CC6699" height="22">\n')
    oFile.write('		<p align="right"><b>'+ moduleapi.FormatFloatStd(config, totdpkTersedia) +'</b></td>\n')
    oFile.write('	</tr>\n')
     
def WriteToFile(config, parameter, oFile):
    #tgl_transaksi_awal = parameter.FirstRecord.tanggal_awal
    #tgl_transaksi_akhir = parameter.FirstRecord.tanggal_akhir

    #strTanggalAwal = config.FormatDateTime('dd mmmm yyyy',tgl_transaksi_awal)
    #strTanggalAkhir = config.FormatDateTime('dd mmmm yyyy',tgl_transaksi_akhir)
    #ConstructReportHeader(config, strTanggalAwal, strTanggalAkhir, oFile)
    ConstructReportHeader(config, oFile)
 
    totdpkTersedia = ConstructReportValues(config, oFile)

    ConstructReportTrailer(
       config
     , totdpkTersedia
     , oFile
    )

    oFile.write('</table>\n')
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

def CreateReport(config, parameter, returnpacket):
    sBaseFileName = 'infodanaidle.htm'
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

