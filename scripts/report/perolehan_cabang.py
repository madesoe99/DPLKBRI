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
  oFile.write('		<td colspan="4" height="20" style="border-left:medium none #000000; border-right:medium none #000000; border-top-style:none; border-top-width:medium; border-bottom-style:none; border-bottom-width:medium">\n')
  oFile.write('		<p align="center"><font size="3" color="#008000"><b>PEROLEHAN CABANG</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" colspan="4" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font color="#008000"><b>PERIODE '+ string.upper(strTanggalAwal) +' HINGGA '+ string.upper(strTanggalAkhir) +'</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="3%" align="center" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>NO</b></td>\n')
  oFile.write('		<td width="7%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>KODE CABANG</b></td>\n')
  oFile.write('		<td width="18%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>NAMA CABANG</b></td>\n')
  oFile.write('		<td width="18%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>AKTIF</b></td>\n')
  oFile.write('		<td width="18%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>SUSPEND</b></td>\n')
  oFile.write('		<td width="7%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>JUMLAH PESERTA</b></td>\n')
  oFile.write('	</tr>\n')


def strSQLDaftarPesertaAktif(config, kode_cabang, tgl_transaksi_awal, tgl_transaksi_akhir_plus):
  return \
    'select kode_cab_daftar,count(n.no_peserta) as jmlPeserta '\
    'from NasabahDPLK n '\
    '  , RekeningDPLK r '\
    'where n.no_peserta = r.no_peserta '\
    '  and n.tgl_registrasi >= \'%s\' '\
    '  and n.tgl_registrasi < \'%s\' '\
    '  and r.status_dplk = \'A \' '\
    '  and r.kode_cab_daftar = \'%s\' '\
    'group by r.kode_cab_daftar; '\
    % (config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_awal)\
       , config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_akhir_plus)\
       , kode_cabang \
    )

def strSQLDaftarPesertaSuspend(config, kode_cabang, tgl_transaksi_awal, tgl_transaksi_akhir_plus):
  return \
    'select kode_cab_daftar, count(n.no_peserta) as jmlPeserta '\
    'from NasabahDPLK n '\
    '  , RekeningDPLK r '\
    'where n.no_peserta = r.no_peserta '\
    '  and n.tgl_registrasi >= \'%s\' '\
    '  and n.tgl_registrasi < \'%s\' '\
    '  and r.kode_cab_daftar = \'%s\' '\
    '  and r.status_dplk = \'S \' '\
    'group by r.kode_cab_daftar '\
    % (config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_awal)\
       , config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_akhir_plus)\
       , kode_cabang\
    )


def strSQLCabang(config):
  return \
    'select Branch_Code,BranchName '\
    'from BRANCHLOCATION '\
    'order by Branch_Code ;'


def ConstructReportValues(config, strSQL, tgl_transaksi_awal, tgl_transaksi_akhir_plus, oFile):

  rSQLCabang = config.CreateSQL(strSQL).RawResult

  no_urut = 0
  totPeserta = totAktif = totSuspend = 0.0
  jmlPeserta = 0
  vSuspend = 0
  vAktif = 0
  
  #strCabang = strSQLCabang(config,  tgl_transaksi_awal, tgl_transaksi_akhir_plus )
  #rSQlCabang =  config.CreateSQL(strCabang).RawResult

  #resSQL.First()
  
  rSQLCabang.First()
  while not rSQLCabang.Eof:

    #BranchCode = resSQL.kode_cab_daftar

    strSQLAktif = strSQLDaftarPesertaAktif(config, rSQLCabang.Branch_Code,tgl_transaksi_awal, tgl_transaksi_akhir_plus)
    rSQLAktif =  config.CreateSQL(strSQLAktif).RawResult

    strSuspend  = strSQLDaftarPesertaSuspend(config, rSQLCabang.Branch_Code,tgl_transaksi_awal, tgl_transaksi_akhir_plus)
    rSQLSuspend = config.CreateSQL(strSuspend).RawResult

    if rSQLSuspend.eof:
        vSuspend = 0
    else:
        vSuspend = rSQLSuspend.jmlPeserta

    if rSQLAktif.eof:
        vAktif = 0
    else:
        vAktif = rSQLAktif.jmlPeserta

    no_urut += 1
    


    if moduleapi.IsOddNumber(no_urut):
      bgcolor = '#EFEFEF'
    else:
      bgcolor = '#FFFFFF'

    jmlPeserta = (vAktif + vSuspend)

    oFile.write('	<tr>\n')
    oFile.write('		<td width="3%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'" height="22">'+ str(no_urut) +'</td>\n')
    oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="center">'+ rSQLCabang.Branch_Code +'</td>\n')
    oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="left">'+ rSQLCabang.branchname +'</td>\n')
    oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="right">'+ str(vAktif) +'</td>\n')
    oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="right">'+ str(vSuspend) +'</td>\n')
    oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="right">'+ str(jmlPeserta) +'</td>\n')
    oFile.write('	</tr>\n')


    totPeserta += jmlPeserta
    totAktif += vAktif
    totSuspend +=vSuspend
    vAktif = vSuspend = 0
    rSQLCabang.Next()

  return totPeserta, totAktif, totSuspend

def ConstructReportTrailer(config, totPeserta, totAktif, totSuspend, oFile):
  oFile.write('	<tr>\n')
  oFile.write('		<td width="44%" colspan="3" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" colspan="6" bgcolor="#CC6699">\n')
  oFile.write('		<b>TOTAL PESERTA</b></td>\n')
  oFile.write('		<td width="9%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totAktif) +'</b></td>\n')
  oFile.write('		<td width="9%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totSuspend) +'</b></td>\n')
  oFile.write('		<td width="9%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totPeserta) +'</b></td>\n')
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

  strSQL = strSQLCabang(config)
  config.SendDebugMsg(strSQL)

  totPeserta, totAktif, totSuspend = ConstructReportValues(config, strSQL, tgl_transaksi_awal, tgl_transaksi_akhir + 1, oFile)

  ConstructReportTrailer(
    config, totPeserta
    , totAktif
    , totSuspend
    , oFile
  )

def CreateReport(config, parameter, returnpacket):
  sBaseFileName = 'perolehan_cabang.htm'
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

