import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi
import string

def ConstructReportHeader(config, strTanggalAwal, strTanggalAkhir, oFile):
  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Laporan Akumulasi Peserta Tutup</title>\n')
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Arial; line-height:100%; margin-top:0; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td colspan="7" height="20" style="border-left:medium none #000000; border-right:medium none #000000; border-top-style:none; border-top-width:medium; border-bottom-style:none; border-bottom-width:medium">\n')
  oFile.write('		<p align="center"><font size="3" color="#008000"><b>AKUMULASI DANA PERPAKET (TUTUP)</b></font></td>\n')
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
  oFile.write('		<b>TOTAL DANA PAKET</b></td>\n')
  oFile.write('	</tr>\n')


def strSQLSumValues(config, tgl_transaksi_akhir_plus, no_peserta):
  return \
    'select no_peserta '\
    '  , isnull(sum(MUTASI_IURAN_PK),0.0) as sumIuranPK '\
    '  , isnull(sum(MUTASI_IURAN_PST),0.0) as sumIuranPeserta '\
    '  , isnull(sum(MUTASI_PENGEMBANGAN),0.0) as sumPengembangan '\
    '  , isnull(sum(MUTASI_PERALIHAN),0.0) as sumPeralihan '\
    'from TRANSAKSIDPLK  '\
    'where NO_PESERTA = \'%s\' '\
    '  and TGL_TRANSAKSI < \'%s\' '\
    '  and ISCOMMITTED = \'T\' '\
    ' group by no_peserta '\
    %(no_peserta \
      , config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_akhir_plus)\
    )


def strSQLPeserta(config, tgl_transaksi_akhir_plus):
  return \
    'select t.no_peserta '\
    'from TRANSAKSIDPLK T, NASABAHDPLK N '\
    'where T.no_peserta = n.no_peserta '\
    '  and t.TGL_TRANSAKSI > \'%s\' '\
    '  and n.tgl_registrasi < \'%s\' '\
    '  and t.kode_jenis_transaksi = \'J\' '\
    '  and t.ISCOMMITTED = \'T\' '\
    %(config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_akhir_plus)\
     ,config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_akhir_plus)
    )


def ConstructReportValues(config, tgl_transaksi_plus, strSQL, oFile):
  resSQL = config.CreateSQL(strSQL).RawResult

  config.SendDebugMsg('Proses......')
  no_urut = 1
  sumDana = sumDanaTotal = totdana = totA = totB = totC = 0.0
  
  #inisialisasi dictionary kode jenis transaksi dan sum dana untuk kode tersebut
  dictJenisTransaksi = {'A':0.0,'B':0.0,'C':0.0}

  resSQL.First()
  while not resSQL.Eof:

    # Sum dana peserta
    config.SendDebugMsg('Masuk......')
    strSQL = strSQLSumValues(config, tgl_transaksi_plus+1, resSQL.no_peserta)
    rSQL = config.CreateSQL(strSQL).RawResult

    config.SendDebugMsg('SumDana......')
    sumDana = rSQL.sumIuranPK or 0.0 + rSQL.sumIuranPeserta or 0.0 + rSQL.sumPengembangan or 0.0 + \
    rSQL.sumPeralihan or 0.0
    

    oKodePaket = config.CreatePObjImplProxy('RekeningDPLK')
    oKodePaket.Key = resSQL.no_peserta
    config.SendDebugMsg('Hitung......')
    
    if oKodePaket.KODE_PAKET_INVESTASI == 'A':
       totA = totA + sumDana
    if oKodePaket.KODE_PAKET_INVESTASI == 'B':
       totB = totB + sumDana
    if oKodePaket.KODE_PAKET_INVESTASI == 'C':
       totC = totC + sumDana

    #dictJenisTransaksi[oKodePaket.KODE_PAKET_INVESTASI] = sumDana
    

    no_urut += 1
    resSQL.Next()

  sumDanaTotal = totA + totB + totC
  
  config.SendDebugMsg('Selesai....')

  oFile.write('	<tr>\n')
  oFile.write('		<td width="3%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" height="22">1</td>\n')
  oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" height="22">\n')
  oFile.write('		<p align="center">A</td>\n')
  oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" height="22">\n')
  #oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, dictJenisTransaksi['A']) +'</td>\n')
  oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, totA) +'</td>\n')

  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="3%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" height="22">2</td>\n')
  oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" height="22">\n')
  oFile.write('		<p align="center">B</td>\n')
  oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" height="22">\n')
  oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, totB) +'</td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="3%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" height="22">3</td>\n')
  oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" height="22">\n')
  oFile.write('		<p align="center">C</td>\n')
  oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" height="22">\n')
  oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, totC) +'</td>\n')
  oFile.write('	</tr>\n')
    
  return sumDanaTotal
    

def ConstructReportTrailer(config, totdana, oFile):
  oFile.write('	<tr>\n')
  oFile.write('		<td width="44%" colspan="2" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="center" colspan="6" bgcolor="#CC6699">\n')
  oFile.write('		<b>TOTAL DANA</b></td>\n')
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

  #strSQL = strSQLSumValues(config, tgl_transaksi_awal, tgl_transaksi_akhir + 1)
  #config.SendDebugMsg(strSQL)

  strSQL = strSQLPeserta(config, tgl_transaksi_akhir)
  
  totdana = ConstructReportValues(config, tgl_transaksi_akhir, strSQL, oFile)

  ConstructReportTrailer(
    config, totdana
    , oFile
  )

def CreateReport(config, parameter, returnpacket):
  sBaseFileName = 'AkumuPesertaTutup.htm'
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

