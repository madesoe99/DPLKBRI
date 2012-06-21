import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi
import string

def ConstructReportHeader(config, strTanggalAwal, strTanggalAkhir, kode_jenis_transaksi, oFile):
  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Laporan Rincian Dana Peserta Corporate</title>\n')
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Arial; line-height:100%; margin-top:0; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td colspan="11" height="20" style="border-left:medium none #000000; border-right:medium none #000000; border-top-style:none; border-top-width:medium; border-bottom-style:none; border-bottom-width:medium">\n')
  oFile.write('		<p align="center"><font size="3" color="#008000"><b>RINCIAN DANA PESERTA CORPORATE</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" colspan="11" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font color="#008000"><b>PERIODE '+ string.upper(strTanggalAwal) +' HINGGA '+ string.upper(strTanggalAkhir) +'</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="3%" align="center" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>NO</b></td>\n')
  oFile.write('		<td width="7%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>NO PESERTA</b></td>\n')
  oFile.write('		<td width="18%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>NAMA LENGKAP</b></td>\n')
  oFile.write('		<td width="7%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>TGL REGISTRASI</b></td>\n')
  oFile.write('		<td width="7%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>TGL TRANSAKSI</b></td>\n')
  oFile.write('		<td width="9%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')

  dictJenisTransaksi = {'C':'Biaya Pengelolaan','D':'Biaya Administrasi','G':'Bagi Hasil','I':'Pengalihan Masuk',\
    'K':'Iuran Peserta','M':'Iuran Manual'}

  oFile.write('		'+dictJenisTransaksi[kode_jenis_transaksi]+'</b></td>\n')
  oFile.write('	</tr>\n')


def strSQLDaftarPeserta(config, tgl_transaksi_awal, tgl_transaksi_akhir_plus, kode_nasabah_corporate):
  return \
    'select n.no_peserta '\
    '  , n.nama_lengkap '\
    '  , n.kode_nasabah_corporate '\
    '  , n.tanggal_lahir '\
    '  , n.tgl_registrasi '\
    '  , r.tgl_pensiun '\
    '  , r.kode_paket_investasi '\
    '  , r.usia_pensiun '\
    '  , r.status_dplk '\
    '  , r.akum_dana_iuran_pst '\
    '  , r.akum_dana_iuran_pk '\
    '  , r.akum_dana_pengembangan '\
    '  , r.akum_dana_peralihan '\
    'from NasabahDPLK n '\
    '  , RekeningDPLK r '\
    'where n.no_peserta = r.no_peserta '\
    '  and n.kode_nasabah_corporate = \'%s\' '\
    'order by n.no_peserta; '\
    % (kode_nasabah_corporate)

#Tambahan By Ade

def strSQLSumValues(config, tgl_transaksi_awal, tgl_transaksi_akhir_plus, no_peserta, kode_jenis_transaksi):
  return \
    'select t.NO_PESERTA '\
    '  , t.TGL_TRANSAKSI '\
    '  , isnull(t.MUTASI_IURAN_PK,0.0) as sumIuranPK '\
    '  , isnull(t.MUTASI_IURAN_PST,0.0) as sumIuranPeserta '\
    '  , isnull(t.MUTASI_PENGEMBANGAN,0.0) as sumPengembangan '\
    '  , isnull(t.MUTASI_PERALIHAN,0.0) as sumPeralihan '\
    'from TRANSAKSIDPLK t '\
    'where t.TGL_TRANSAKSI >= \'%s\' '\
    '  and t.TGL_TRANSAKSI < \'%s\' '\
    '  and t.NO_PESERTA = \'%s\' '\
    '  and t.KODE_JENIS_TRANSAKSI = \'%s\' '\
    '  and t.ISCOMMITTED = \'T\' '\
    ' order by t.tgl_transaksi; '\
    %(config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_awal)\
       , config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_akhir_plus)\
       , no_peserta\
       , kode_jenis_transaksi
    )
#


def ConstructReportValues(config, strSQL, tgl_transaksi_awal, tgl_transaksi_akhir_plus, kode_jenis_transaksi, oFile):
  resSQL = config.CreateSQL(strSQL).RawResult

  no_urut = 0
  totdana = 0.0

  resSQL.First()
  while not resSQL.Eof:
  
    no_peserta = resSQL.no_peserta
    
    strSQL = strSQLSumValues(config, tgl_transaksi_awal, tgl_transaksi_akhir_plus, no_peserta, kode_jenis_transaksi)
    rSQL = config.CreateSQL(strSQL).RawResult
    
    no_urut += 1

    if moduleapi.IsOddNumber(no_urut):
      bgcolor = '#EFEFEF'
    else:
      bgcolor = '#FFFFFF'


    while not rSQL.Eof:
      sumDana = rSQL.sumIuranPK + rSQL.sumIuranPeserta + rSQL.sumPengembangan + \
        rSQL.sumPeralihan
      strTglTransaksi = config.FormatDateTime('dd/mm/yyyy',moduleapi.DateTimeTupleToFloat(config, rSQL.tgl_transaksi))
      strTglRegistrasi = config.FormatDateTime('dd/mm/yyyy',moduleapi.DateTimeTupleToFloat(config, resSQL.tgl_registrasi))


      oFile.write('	<tr>\n')
      oFile.write('		<td width="3%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'" height="22">'+ str(no_urut) +'</td>\n')
      oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
      oFile.write('		<p align="center">'+ resSQL.no_peserta +'</td>\n')
      oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
      oFile.write('		<p align="left">'+ resSQL.nama_lengkap +'</td>\n')
      oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
      oFile.write('		<p align="center">'+ strTglRegistrasi +'</td>\n')
      oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
      oFile.write('		<p align="center">'+ strTglTransaksi +'</td>\n')
      oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
      oFile.write('		<p align="right">'+moduleapi.FormatFloatStd(config, sumDana, '-') +'</td>\n')
      oFile.write('	</tr>\n')
      
      rSQL.Next()

    resSQL.Next()


def ConstructReportTrailer(config, oFile):
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
  kode_nasabah_corporate = parameter.FirstRecord.kode_nasabah_corporate
  kode_jenis_transaksi = parameter.FirstRecord.kode_jenis_transaksi
  tgl_transaksi_awal = parameter.FirstRecord.tanggal_awal
  tgl_transaksi_akhir = parameter.FirstRecord.tanggal_akhir

  strTanggalAwal = config.FormatDateTime('dd mmmm yyyy',tgl_transaksi_awal)
  strTanggalAkhir = config.FormatDateTime('dd mmmm yyyy',tgl_transaksi_akhir)
  ConstructReportHeader(config, strTanggalAwal, strTanggalAkhir, kode_jenis_transaksi, oFile)

  strSQL = strSQLDaftarPeserta(config, tgl_transaksi_awal, tgl_transaksi_akhir + 1, kode_nasabah_corporate)
  config.SendDebugMsg(strSQL)

  ConstructReportValues(config, strSQL, tgl_transaksi_awal, tgl_transaksi_akhir + 1,kode_jenis_transaksi, oFile)

  ConstructReportTrailer(
    config
    , oFile
  )

def CreateReport(config, parameter, returnpacket):
  sBaseFileName = 'rincian dana peserta corporate.htm'
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

