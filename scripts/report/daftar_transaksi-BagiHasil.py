import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi
import string

def ConstructReportHeader(config, namaTransaksi, strTanggalAwal, strTanggalAkhir, oFile):
  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Laporan '+ namaTransaksi +'</title>\n')
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Arial; line-height:100%; margin-top:0; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td colspan="5" height="20" style="border-left:medium none #000000; border-right:medium none #000000; border-top-style:none; border-top-width:medium; border-bottom-style:none; border-bottom-width:medium">\n')
  oFile.write('		<p align="center"><font size="3" color="#008000"><b>LAPORAN '+ string.upper(namaTransaksi) +'</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" colspan="5" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font color="#008000"><b>PERIODE '+ string.upper(strTanggalAwal) +' HINGGA '+ string.upper(strTanggalAkhir) +'</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="5%" align="center" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>NO</b></td>\n')
  oFile.write('		<td width="10%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<p style="margin-top: 0; margin-bottom: 0"><b>TGL. TRANSAKSI</b></p>\n')
  oFile.write('		<p style="margin-top: 0; margin-bottom: 0"><b>(MM/DD/YYYY)</b></td>\n')
  oFile.write('		<td width="10%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>NO. PESERTA</b></td>\n')
  oFile.write('		<td width="20%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>NAMA LENGKAP</b></td>\n')
  #oFile.write('		<td width="10%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  #oFile.write('		<b>KODE CABANG</b></td>\n')
  #oFile.write('		<td width="10%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  #oFile.write('		<b>NAMA CABANG</b></td>\n')
  #oFile.write('		<td width="25%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  #oFile.write('		<b>KETERANGAN</b></td>\n')
  oFile.write('		<td width="25%" align="center" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>BAGI HASIL</b></td>\n')
  oFile.write('	</tr>\n')

#def strSQLDaftarTransaksi(config, tgl_transaksi_awal, tgl_transaksi_akhir_plus, lsJenis):
#  strJenis = '\''+ lsJenis.pop(0) + '\''
#  for jenis in lsJenis:
#    strJenis += ', \''+ jenis + '\''
#
#  return \
#    'select isnull(tgl_transaksi,\'\') tgl_transaksi '\
#    '  , n.no_peserta '\
#    '  , isnull(nama_lengkap,\'\') nama_lengkap '\
#    '  , b.branch_code '\
#    '  , isnull(BranchName,\'\') BranchName '\
#	'  , isnull(t.keterangan,\'\') keterangan '\
#    '  , isnull(mutasi_iuran_pk + mutasi_iuran_pst + mutasi_pengembangan + mutasi_peralihan,0.0) mutasi '\
#    'from TransaksiDPLK t '\
#    '  , NasabahDPLK n '\
#    '  , RekeningDPLK r '\
#    '  , BranchLocation b '\
#    'where t.isCommitted = \'T\' '\
#    '  and tgl_transaksi >= \'%s\' '\
#    '  and tgl_transaksi < \'%s\' '\
#    '  and t.no_peserta = n.no_peserta '\
#    '  and n.no_peserta = r.no_peserta '\
#    '  and r.kode_cab_daftar = b.branch_code '\
#    '  and kode_jenis_transaksi in (%s) '\
#    'order by tgl_transaksi '\
#    % (config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_awal)\
#       , config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_akhir_plus)\
#       , strJenis)

def strSQLDaftarTransaksi(config, tgl_transaksi_awal, tgl_transaksi_akhir_plus):
  return \
    'select isnull(tgl_transaksi,\'\') tgl_transaksi '\
    '  , n.no_peserta '\
    '  , isnull(nama_lengkap,\'\') nama_lengkap '\
    '  , isnull(mutasi_pengembangan, 0.0) mutasi '\
    'from Transaksidplk t '\
    '  , NasabahDPLK n '\
    'where t.isCommitted = \'T\' '\
    '  and tgl_transaksi >= \'%s\' '\
    '  and tgl_transaksi < \'%s\' '\
    '  and kode_jenis_transaksi = \'G\' '\
    '  and t.no_peserta = n.no_peserta '\
    % (config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_awal)\
       , config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_akhir_plus)\
    )



def ConstructReportValues(config, strSQL, oFile):
  resSQL = config.CreateSQL(strSQL).RawResult

  no_urut = 0
  sumPrev = 0
  sumCurr = 0
  totJmlMutasi = 0
  resSQL.First()
  while not resSQL.Eof:
    no_urut += 1

    config.SendDebugMsg(resSQL.no_peserta)
    if moduleapi.IsOddNumber(no_urut):
      bgcolor = '#EFEFEF'
    else:
      bgcolor = '#FFFFFF'

    if resSQL.tgl_transaksi <> '':
      strTglTransaksi = config.FormatDateTime('mm/DD/yyyy',moduleapi.DateTimeTupleToFloat(config, resSQL.tgl_transaksi))
    else:
      strTglTransaksi = ''

    oFile.write('	<tr>\n')
    oFile.write('		<td width="5%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'">'+ str(no_urut) +'</td>\n')
    oFile.write('		<td width="10%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" >\n')
    oFile.write('		<p align="center">'+ strTglTransaksi +'</td>\n')
    oFile.write('		<td width="10%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" >\n')
    oFile.write('		<p align="center">'+ resSQL.no_peserta +'</td>\n')
    oFile.write('		<td width="20%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" >'+ resSQL.nama_lengkap +'</td>\n')
    #oFile.write('		<td width="10%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" >\n')
    #oFile.write('		<p align="center">'+ resSQL.branch_code +'</td>\n')
    #oFile.write('		<td width="10%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" >\n')
    #oFile.write('		'+ resSQL.BranchName +'</td>\n')
    #oFile.write('		<td width="25%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" >\n')
    #oFile.write('		'+ resSQL.keterangan +'</td>\n')
    oFile.write('		<td width="25%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'" >\n')
    oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, resSQL.mutasi) +'</td>\n')
    oFile.write('	</tr>\n')

    totJmlMutasi += resSQL.mutasi

    resSQL.Next()

  return totJmlMutasi

def ConstructReportTrailer(config, totJmlMutasi, oFile):
  oFile.write('	<tr>\n')
  oFile.write('		<td width="85%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" colspan="5" bgcolor="#CC6699">\n')
  oFile.write('		<b>TOTAL</b></td>\n')
  oFile.write('		<td width="15%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
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
  
  lsJenis = parameter.FirstRecord.jenis.split(';')
  if len(lsJenis) == 1:
    getjeniskode = parameter.FirstRecord.jenis
  else:
    getjeniskode = lsJenis[0]

  kode_jenis_transaksi = parameter.FirstRecord.jenis

  oJenisTransaksiDPLK = moduleapi.GetJenisTransaksiDPLK(config, getjeniskode)
  strTanggalAwal = config.FormatDateTime('dd mmmm yyyy',tgl_transaksi_awal)
  strTanggalAkhir = config.FormatDateTime('dd mmmm yyyy',tgl_transaksi_akhir)
  ConstructReportHeader(config, oJenisTransaksiDPLK.nama_transaksi, strTanggalAwal, strTanggalAkhir, oFile)

  strSQL = strSQLDaftarTransaksi(config, tgl_transaksi_awal, tgl_transaksi_akhir + 1)
  config.SendDebugMsg(strSQL)
  totJmlMutasi = ConstructReportValues(config, strSQL, oFile)
  ConstructReportTrailer(config, totJmlMutasi, oFile)

def CreateReport(config, parameter, returnpacket):
  sBaseFileName = 'daftar_transaksi.htm'
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

