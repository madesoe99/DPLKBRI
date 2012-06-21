import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi
import string

def ConstructReportHeader(config, strTanggalAwal, strTanggalAkhir, nik, oFile):
  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Laporan SIP NIK</title>\n')
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Arial; line-height:100%; margin-top:0; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td colspan="4" height="20" style="border-left:medium none #000000; border-right:medium none #000000; border-top-style:none; border-top-width:medium; border-bottom-style:none; border-bottom-width:medium">\n')
  oFile.write('		<p align="center"><font size="3" color="#008000"><b>LAPORAN SIP '+string.upper(nik)+' </b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" colspan="4" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font color="#008000"><b>PERIODE '+ string.upper(strTanggalAwal) +' HINGGA '+ string.upper(strTanggalAkhir) +'</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="3%" align="center" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>NO</b></td>\n')
  oFile.write('		<td width="7%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>NO PESERTA</b></td>\n')
  oFile.write('		<td width="7%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>NAMA LENGKAP</b></td>\n')
  oFile.write('		<td width="7%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>TGL REGISTRASI</b></td>\n')
  oFile.write('		<td width="7%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>KODE NASABAH</b></td>\n')

  oFile.write('	</tr>\n')


def strSQLDaftarPeserta(config, tgl_transaksi_awal, tgl_transaksi_akhir_plus, nik):
  return \
    'select n.NO_PESERTA, NAMA_LENGKAP, TGL_REGISTRASI, n.KODE_NASABAH_CORPORATE '\
    'from NasabahDPLK n '\
    '  , RekeningDPLK r '\
    'where n.no_peserta = r.no_peserta '\
    '  and n.tgl_registrasi >= \'%s\' '\
    '  and n.tgl_registrasi < \'%s\' '\
    '  and n.no_referensi = \'%s\' '\
    'order by n.no_peserta; '\
    % (config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_awal)\
       , config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_akhir_plus)\
       , nik \
    )

def ConstructReportValues(config, strSQL, tgl_transaksi_awal, tgl_transaksi_akhir_plus, oFile):
  resSQL = config.CreateSQL(strSQL).RawResult

  no_urut = 0
  totPeserta = 0.0
  config.SendDebugMsg('masuk......01')
  
  resSQL.First()
  while not resSQL.Eof:

    y, m, d = resSQL.tgl_registrasi[:3]
    # tanggal dengan format dd/mm/yyyy
    tanggal = '%s/%s/%s' % (moduleapi.MyZFill(str(d),2), moduleapi.MyZFill(str(m),2), str(y))

    config.SendDebugMsg('masuk......02')
    no_urut += 1

    if moduleapi.IsOddNumber(no_urut):
      bgcolor = '#EFEFEF'
    else:
      bgcolor = '#FFFFFF'

    kode_nasabah_corporate = resSQL.kode_nasabah_corporate or ''
    #config.SendDebugMsg('masuk......03')
    oFile.write('	<tr>\n')
    oFile.write('		<td width="3%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'" height="22">'+ str(no_urut) +'</td>\n')
    oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="center">'+ resSQL.no_peserta +'</td>\n')
    #config.SendDebugMsg('nomor :'+str(resSQL.no_peserta))
    oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="center">'+ resSQL.nama_lengkap +'</td>\n')
    oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="center"> '+ tanggal +' </td>\n')
    #config.SendDebugMsg('nomor :'+str(resSQL.nama_lengkap))
    oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="center">'+ kode_nasabah_corporate +'</td>\n')
    #config.SendDebugMsg('nomor :'+str(kode_nasabah_corporate))
    oFile.write('	</tr>\n')
    
    config.SendDebugMsg('masuk......04')
    #totPeserta += resSQL.jmlPeserta
    resSQL.Next()

  return totPeserta

def ConstructReportTrailer(config, totPeserta, oFile):
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

  #BranchCode = parameter.FirstRecord.kode_cabang
  no_referensi = parameter.FirstRecord.no_referensi
  tgl_transaksi_awal = parameter.FirstRecord.tanggal_awal
  tgl_transaksi_akhir = parameter.FirstRecord.tanggal_akhir
  
  #config.SendDebugMsg('masuk......02')
  nik = no_referensi
  config.SendDebugMsg('NIK :'+ nik)
  strTanggalAwal = config.FormatDateTime('dd mmmm yyyy',tgl_transaksi_awal)
  strTanggalAkhir = config.FormatDateTime('dd mmmm yyyy',tgl_transaksi_akhir)
  ConstructReportHeader(config, strTanggalAwal, strTanggalAkhir, nik, oFile)

  strSQL = strSQLDaftarPeserta(config, tgl_transaksi_awal, tgl_transaksi_akhir + 1, nik)
  config.SendDebugMsg(strSQL)

  totPeserta = ConstructReportValues(config, strSQL, tgl_transaksi_awal, tgl_transaksi_akhir + 1, oFile)

  ConstructReportTrailer(
    config, totPeserta
    , oFile
  )

def CreateReport(config, parameter, returnpacket):
  sBaseFileName = 'perolehan_cabang.htm'
  sFileName = config.UserHomeDirectory + sBaseFileName
  #config.SendDebugMsg('masuk......')
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

