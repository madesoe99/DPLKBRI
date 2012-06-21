import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi
import string

def ConstructReportHeader(config, strTanggalAwal, strTanggalAkhir, oFile):
  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Laporan Pengambilan Manfaat</title>\n')
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Arial; line-height:100%; margin-top:0; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td colspan="11" height="20" style="border-left:medium none #000000; border-right:medium none #000000; border-top-style:none; border-top-width:medium; border-bottom-style:none; border-bottom-width:medium">\n')
  oFile.write('		<p align="center"><font size="3" color="#008000"><b>PENGAMBILAN MANFAAT</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" colspan="11" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font color="#008000"><b>PERIODE '+ string.upper(strTanggalAwal) +' HINGGA '+ string.upper(strTanggalAkhir) +'</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="3%" align="center" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>NO</b></td>\n')
  oFile.write('		<td width="18%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>NAMA LENGKAP</b></td>\n')
  oFile.write('		<td width="7%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>NO. PESERTA</b></td>\n')
  oFile.write('		<td width="9%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<p style="margin-top: 0; margin-bottom: 0"><b>TGL. TRANSAKSI</b></p>\n')
  oFile.write('		<p style="margin-top: 0; margin-bottom: 0"><b>(DD/MM/YY)</b></td>\n')
  oFile.write('		<td width="9%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>NOMINAL AWAL</b></td>\n')
  oFile.write('		<td width="9%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>PENGELOLAAN</b></td>\n')
  oFile.write('		<td width="9%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>ADM. TAHUNAN</b></td>\n')
  oFile.write('		<td width="9%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')

  #siapkan objek Parameter Biaya default
  oP = config.CreatePObjImplProxy('Parameter')
  oP.Key = 'PSN_CM_ALIH_<1TH'
  persenCairAlih1Th = oP.Numeric_Value

  oFile.write('		<b>'+ str(persenCairAlih1Th) +' % ADM</b>.</td>\n')
  oFile.write('		<td width="9%" align="center" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>PAJAK</b></td>\n')
  oFile.write('		<td width="9%" align="center" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>NOMINAL</b></td>\n')
  oFile.write('		<td width="9%" align="center" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>JENIS<br>\n')
  oFile.write('		PENARIKAN</b></td>\n')
  oFile.write('		<td width="21%" align="center" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>KETERANGAN</b></td>\n')
  oFile.write('		<td width="9%" align="center" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>N P W P</b></td>\n')
  oFile.write('		<td width="9%" align="center" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>Alamat NPWP</b></td>\n')
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
    '  and kode_jenis_transaksi = \'J\' '\
    'order by tgl_transaksi; '\
    % (config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_awal)\
       , config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_akhir_plus)\
    )

def ConstructReportValues(config, strSQL, oFile):
  resSQL = config.CreateSQL(strSQL).RawResult

  no_urut = 0

  totSaldo_jml_dana = 0.0
  totBiaya_pengelolaan = 0.0
  totBiaya_administrasi = 0.0
  totBiaya_pencairan = 0.0
  totPajak = 0.0
  totManfaat_tunai = 0.0

  resSQL.First()
  while not resSQL.Eof:

    oNasabah = config.CreatePObjImplProxy('NasabahDPLK')
    oNasabah.Key = resSQL.no_peserta
    npwp = oNasabah.npwp
    alamatnpwp = oNasabah.keterangan

    no_urut += 1

    if moduleapi.IsOddNumber(no_urut):
      bgcolor = '#EFEFEF'
    else:
      bgcolor = '#FFFFFF'

    if resSQL.tgl_transaksi <> '':
      strTglTransaksi = config.FormatDateTime('dd/mm/yyyy',moduleapi.DateTimeTupleToFloat(config, resSQL.tgl_transaksi))
    else:
      strTglTransaksi = ''

    oPengambilanManfaat = config.CreatePObjImplProxy('PengambilanManfaat')
    oPengambilanManfaat.Key = resSQL.ID_Transaksi

    saldo_jml_dana = oPengambilanManfaat.saldo_jml_dana or 0.0
    biaya_pengelolaan = oPengambilanManfaat.biaya_pengelolaan or 0.0
    biaya_administrasi = oPengambilanManfaat.biaya_administrasi or 0.0
    biaya_pencairan = oPengambilanManfaat.biaya_pencairan or 0.0
    pajak = oPengambilanManfaat.pajak or 0.0
    #manfaat_tunai = oPengambilanManfaat.manfaat_tunai or 0.0
    nominalBersih = saldo_jml_dana - biaya_pengelolaan - biaya_administrasi - biaya_pencairan - pajak

    jenisManfaat = '&nbsp;'
    kode_jns_manfaat = oPengambilanManfaat.kode_jns_manfaat
    if kode_jns_manfaat:
      oJenisPenerimaanManfaat = config.CreatePObjImplProxy('JenisPenerimaanManfaat')
      oJenisPenerimaanManfaat.Key = kode_jns_manfaat
      if not oJenisPenerimaanManfaat.IsNull:
        jenisManfaat = oJenisPenerimaanManfaat.nama_jns_manfaat or '&nbsp;'

    oFile.write('	<tr>\n')
    oFile.write('		<td width="3%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'" height="22">'+ str(no_urut) +'</td>\n')
    oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">'+ oPengambilanManfaat.LRekeningDPLK.LNasabahDPLK.nama_lengkap +'</td>\n')
    oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="center">'+ oPengambilanManfaat.no_peserta +'</td>\n')
    oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="center">'+ strTglTransaksi +'</td>\n')
    oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, saldo_jml_dana, '-') +'</td>\n')
    oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, biaya_pengelolaan, '-') +'</td>\n')
    oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, biaya_administrasi, '-') +'</td>\n')
    oFile.write('		<td width="9%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, biaya_pencairan, '-') +'</td>\n')
    oFile.write('		<td width="9%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		'+ moduleapi.FormatFloatStd(config, pajak, '-') +'</td>\n')
    oFile.write('		<td width="9%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		'+ moduleapi.FormatFloatStd(config, nominalBersih, '-') +'</td>\n')
    oFile.write('		<td width="9%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="center">'+ jenisManfaat +'</td>\n')
    oFile.write('		<td width="9%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="center">'+ resSQL.keterangan +'</td>\n')
    oFile.write('		<td width="9%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="center">'+ npwp +'</td>\n')
    oFile.write('		<td width="9%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'" height="22">\n')
    oFile.write('		<p align="center">'+ alamatnpwp +'</td>\n')
    oFile.write('	</tr>\n')

    totSaldo_jml_dana += saldo_jml_dana
    totBiaya_pengelolaan += biaya_pengelolaan
    totBiaya_administrasi += biaya_administrasi
    totBiaya_pencairan += biaya_pencairan
    totPajak += pajak
    totManfaat_tunai += nominalBersih #manfaat_tunai

    resSQL.Next()

  return totSaldo_jml_dana, totBiaya_pengelolaan, totBiaya_administrasi, totBiaya_pencairan, totPajak, totManfaat_tunai

def ConstructReportTrailer(config, totSaldo_jml_dana, totBiaya_pengelolaan, totBiaya_administrasi, totBiaya_pencairan, totPajak, totManfaat_tunai, oFile):
  oFile.write('	<tr>\n')
  oFile.write('		<td width="29%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" colspan="4" bgcolor="#CC6699">\n')
  oFile.write('		<b>TOTAL</b></td>\n')
  oFile.write('		<td width="9%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totSaldo_jml_dana) +'</b></td>\n')
  oFile.write('		<td width="9%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totBiaya_pengelolaan) +'</b></td>\n')
  oFile.write('		<td width="9%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totBiaya_administrasi) +'</b></td>\n')
  oFile.write('		<td width="9%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totBiaya_pencairan) +'</b></td>\n')
  oFile.write('		<td width="9%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totPajak) +'</b></td>\n')
  oFile.write('		<td width="9%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totManfaat_tunai) +'</b></td>\n')
  oFile.write('		<td width="9%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
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

  totSaldo_jml_dana \
  , totBiaya_pengelolaan \
  , totBiaya_administrasi \
  , totBiaya_pencairan \
  , totPajak \
  , totManfaat_tunai = ConstructReportValues(config, strSQL, oFile)

  ConstructReportTrailer(
    config
    , totSaldo_jml_dana
    , totBiaya_pengelolaan
    , totBiaya_administrasi
    , totBiaya_pencairan
    , totPajak
    , totManfaat_tunai
    , oFile
  )

def CreateReport(config, parameter, returnpacket):
  sBaseFileName = 'pengambilan_manfaat.htm'
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

