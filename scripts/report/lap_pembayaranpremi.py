import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi, string, daftar_transaksi

def ConstructReportHeader(config, strTanggalAwal, strTanggalAkhir, oFile):
  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Laporan Pembayaran Premi</title>\n')
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Arial; line-height:100%; margin-top:0; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td colspan="7" height="20" style="border-left:medium none #000000; border-right:medium none #000000; border-top-style:none; border-top-width:medium; border-bottom-style:none; border-bottom-width:medium">\n')
  oFile.write('		<p align="center"><font size="3" color="#008000"><b>LAPORAN PEMBAYARAN PREMI</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" colspan="7" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font color="#008000"><b>PERIODE '+ string.upper(strTanggalAwal) +' HINGGA '+ string.upper(strTanggalAkhir) +'</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="5%" align="center" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>NO</b></td>\n')
  oFile.write('		<td width="10%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>NO. PESERTA</b></td>\n')
  oFile.write('		<td width="30%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>NAMA LENGKAP</b></td>\n')
  oFile.write('		<td width="10%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<p style="margin-top: 0; margin-bottom: 0"><b>TGL. AKSEPTASI</b></p>\n')
  oFile.write('		<p style="margin-top: 0; margin-bottom: 0"><b>(MM/DD/YYYY)</b></td>\n')
  oFile.write('		<td width="10%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<p style="margin-top: 0; margin-bottom: 0"><b>TGL. TRANSAKSI</b></p>\n')
  oFile.write('		<p style="margin-top: 0; margin-bottom: 0"><b>(MM/DD/YYYY)</b></td>\n')
  oFile.write('		<td width="15%" align="center" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>NOMINAL</b></td>\n')
  oFile.write('		<td width="15%" align="center" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>STATUS PREMI</b></td>\n')

  oFile.write('	</tr>\n')


def strSQLDaftarTransaksi(config, tgl_transaksi_awal, tgl_transaksi_akhir_plus):
  return \
    'select isnull(tgl_transaksi,\'\') tgl_transaksi '\
    '  , isnull(tgl_akseptasi,\'\') tgl_akseptasi '\
    '  , n.no_peserta '\
    '  , isnull(nama_lengkap,\'\') nama_lengkap '\
    '  , isnull(mutasi_premi, 0.0) mutasi '\
    'from TransaksiPremi t '\
    '  , NasabahDPLK n '\
    '  , RekeningWasiatUmmat w '\
    'where t.isCommitted = \'T\' '\
    '  and tgl_transaksi >= \'%s\' '\
    '  and tgl_transaksi < \'%s\' '\
    '  and t.no_peserta = n.no_peserta '\
    '  and n.no_peserta = w.no_peserta '\
    'order by tgl_transaksi '\
    % (config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_awal)\
       , config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_akhir_plus)\
    )

def strSQLHistTrans(config, no_peserta):
  return \
    'select count(no_peserta) jmlTrans '\
    'from TransaksiPremi  '\
    'where no_peserta = \'%s\' ;'\
    % (no_peserta)

def ConstructReportValues(config, strSQL, oFile):
  resSQL = config.CreateSQL(strSQL).RawResult

  no_urut = 0
  sumPrev = 0
  sumCurr = 0
  totJmlMutasi = 0
  resSQL.First()
  
  while not resSQL.Eof:
    no_urut += 1

    rSQLHistTrans = strSQLHistTrans(config, resSQL.no_peserta)
    rSQL = config.CreateSQL(rSQLHistTrans).RawResult

    if rSQL.jmlTrans >= 2:
       ket = 'Lanjutan'
    else:
       ket = 'Pertama'
       
    if moduleapi.IsOddNumber(no_urut):
      bgcolor = '#EFEFEF'
    else:
      bgcolor = '#FFFFFF'

    if resSQL.tgl_transaksi <> '':
      strTglTransaksi = config.FormatDateTime('mm/dd/yyyy',moduleapi.DateTimeTupleToFloat(config, resSQL.tgl_transaksi))
    else:
      strTglTransaksi = ''

    if resSQL.tgl_akseptasi <> '':
       strTglAkseptasi = config.FormatDateTime('mm/dd/yyyy',moduleapi.DateTimeTupleToFloat(config, resSQL.tgl_akseptasi))
    else:
       strTglAkseptasi = ''

    oFile.write('	<tr>\n')
    oFile.write('		<td width="5%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'">'+ str(no_urut) +'</td>\n')
    oFile.write('		<td width="10%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" >\n')
    oFile.write('		<p align="center">'+ resSQL.no_peserta +'</td>\n')
    oFile.write('		<td width="30%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" >'+ resSQL.nama_lengkap +'</td>\n')
    oFile.write('		<td width="10%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" >\n')
    oFile.write('		<p align="center">'+ strTglAkseptasi +'</td>\n')
    oFile.write('		<td width="10%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" >\n')
    oFile.write('		<p align="center">'+ strTglTransaksi +'</td>\n')
    oFile.write('		<td width="15%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'" >\n')
    oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, resSQL.mutasi) +'</td>\n')
    oFile.write('		<td width="10%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" >\n')
    oFile.write('		<p align="center">'+ ket +'</td>\n')
    oFile.write('	</tr>\n')

    totJmlMutasi += resSQL.mutasi

    resSQL.Next()

  return totJmlMutasi

def ConstructReportTrailer(config, totJmlMutasi, oFile):
  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" colspan="5" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" colspan="6" bgcolor="#CC6699">\n')
  oFile.write('		<b>TOTAL</b></td>\n')
  oFile.write('		<td width="9%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totJmlMutasi) +'</b></td>\n')
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
  config.SendDebugMsg('masuk.....01-WU')
  totJmlMutasi = ConstructReportValues(config, strSQL, oFile)

  ConstructReportTrailer(
    config, totJmlMutasi
    , oFile
  )

  #daftar_transaksi.ConstructReportTrailer(config, totJmlMutasi, oFile)

def CreateReport(config, parameter, returnpacket):
  config.SendDebugMsg('masuk.....WU')
  sBaseFileName = 'daftar_pembayaran_premi.htm'
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

