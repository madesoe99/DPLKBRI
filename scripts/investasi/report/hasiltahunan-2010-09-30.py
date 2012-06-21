import sys
import com.ihsan.util.modman as modman

NOCOL = 30
JENISCOL = 400
NILAICOL = 150
TABLEWIDTH = NOCOL + JENISCOL + NILAICOL * 6
NBOFCOLUMNS = 10

noUrut = 1
sumHasilReal = 0.0
sumHasilNonreal = 0.0
sumBeban = 0.0
sumHasilBersih = 0.0
sumLRPelepasan = 0.0

enumJenisRow = [0,'Surat Berharga Negara','Tabungan',3,4,'Sertifikat Deposito',
  'Sertifikat Bank Indonesia','Saham','Obligasi',9,10,'Reksa Dana Terproteksi, Reksa Dana dengan penjaminan dan Reksa Dana indeks',
  'Reksa Dana berbentuk KIK Penyertaan Terbatas','Reksa Dana yang UP-nya diperdagangkan di bursa','Efek Beragun Aset dari KIK EBA',
  'Unit Penyertaan Dana Investasi Real Estate berbentuk KIK','Kontrak Opsi Saham','Penempatan langsung pada saham',
  'Tanah','Bangunan','Tanah dan Bangunan','Surat Pengakuan Utang']

def ConstructReportHeader(config, startDate, endDate, oFile):
  strStartDate = config.FormatDateTime('d mmmm yyyy', startDate)
  strEndDate = config.FormatDateTime('d mmmm yyyy', endDate)

  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Laporan Hasil Investasi Tahunan</title>\n')
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Arial; line-height:100%; margin-top:0; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')

  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="'+ str(TABLEWIDTH) +'" id="table1" cellpadding="2">\n')

  oFile.write('	<tr>\n')
  oFile.write('		<td align="center" colspan="'+ str(NBOFCOLUMNS) +'" height="20" style="border-left:medium none #000000; border-right:medium none #000000; border-top-style:none; border-top-width:medium; border-bottom-style:none; border-bottom-width:medium">\n')
  oFile.write('		<font size="3" color="#008000"><b>Dana Pensiun Lembaga Keuangan PT. Bank Rakyat Indonesia, Tbk</b></font><br/>\n')
  oFile.write('		<font size="3" color="#008000"><b>Laporan Hasil Investasi Tahunan</b></font><br/></td>\n')
  oFile.write('	</tr>\n')

  oFile.write('	<tr>\n')
  oFile.write('		<td align="center" width="'+ str(TABLEWIDTH) +'" colspan="'+ str(NBOFCOLUMNS) +'" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2" color="#008000"><b>Periode '+ strStartDate +' s.d. '+ strEndDate +'</b><br/><br/></font>\n')
  oFile.write('	</tr>\n')

  oFile.write('	<tr>\n')
  oFile.write('		<td align="right" width="'+ str(TABLEWIDTH) +'" colspan="'+ str(NBOFCOLUMNS) +'" style="border-style: none; border-width: medium">\n')
  oFile.write('		<align="right" font size="2" color="#008000"><b>dalam rupiah</b></font></td>\n')
  oFile.write('	</tr>\n')


  oFile.write('	<tr>\n')
  # nomor urut
  oFile.write('		<td rowspan="2" width="'+ str(NOCOL) +'" align="center" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b><font size="2">No.</font></b></td>\n')

  # jenis investasi
  oFile.write('		<td rowspan="2" width="'+ str(JENISCOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Jenis Investasi</b></font></td>\n')

  # hasil yg terealisasi
  oFile.write('		<td colspan="5" width="'+ str(NILAICOL*3) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Hasil Investasi yang Terealisasi</b></font></td>\n')

  # hasil yg belum terealisasi
  oFile.write('		<td rowspan="2" width="'+ str(NILAICOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Hasil Investasi<br/>yang Belum Terealisasi</b></font></td>\n')

  # beban investasi
  oFile.write('		<td rowspan="2" width="'+ str(NILAICOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Beban Investasi</b></font></td>\n')

  # hasil bersih
  oFile.write('		<td rowspan="2" width="'+ str(NILAICOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Hasil Investasi<br/>Bersih</b></font></td>\n')
  oFile.write('	</tr>\n')

  # hasil terealisasi
  oFile.write('		<tr><td width="'+ str(NILAICOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699"><font size="2"><b>Bagi Hasil</b></font></td>\n')
  oFile.write('		<td width="'+ str(NILAICOL/2) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699"><font size="2"><b>Deviden</b></font></td>\n')
  oFile.write('		<td width="'+ str(NILAICOL/2) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699"><font size="2"><b>Sewa</b></font></td>\n')
  oFile.write('		<td width="'+ str(NILAICOL/2) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699"><font size="2"><b>Laba/Rugi<br/>Pelepasan</b></font></td>\n')
  oFile.write('		<td width="'+ str(NILAICOL/2) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699"><font size="2"><b>Lainnya</b></font></td>\n')
  oFile.write('   </tr>\n')

def resSQLDepOnCall(config, strSQLStartDate, strSQLEndDate):
  strSQL = '\
    select \
    	clsfTransaksiInvestasi \
    	, mutasi_kredit \
    	, mutasi_debet \
    from TransaksiInvestasi t, Deposito d \
    where isCommitted = \'T\' \
    	and clsfTransaksiInvestasi in (\'B\',\'C\') \
    	and t.id_investasi = d.id_investasi \
    	and jenisJatuhTempo = 0 \
    	and tgl_transaksi >= %s \
    	and tgl_transaksi < %s'\
    % (strSQLStartDate, strSQLEndDate)
  return config.CreateSQL(strSQL).RawResult

def resSQLDepBjangka(config, strSQLStartDate, strSQLEndDate):
  strSQL = '\
    select \
    	clsfTransaksiInvestasi \
    	, mutasi_kredit \
    	, mutasi_debet \
    from TransaksiInvestasi t, Deposito d \
    where isCommitted = \'T\' \
    	and clsfTransaksiInvestasi in (\'B\',\'C\') \
    	and t.id_investasi = d.id_investasi \
    	and jenisJatuhTempo > 0 \
    	and tgl_transaksi >= %s \
    	and tgl_transaksi < %s'\
    % (strSQLStartDate, strSQLEndDate)
  return config.CreateSQL(strSQL).RawResult

def resSQLSukuk(config, strSQLStartDate, strSQLEndDate):
  strSQL = '\
    select \
    	clsfTransaksiInvestasi \
    	, mutasi_kredit \
    	, mutasi_debet \
    from TransaksiInvestasi t, Obligasi o \
    where isCommitted = \'T\' \
    	and clsfTransaksiInvestasi in (\'B\',\'C\',\'D\') \
    	and t.id_investasi = o.id_investasi \
    	and tgl_transaksi >= %s \
    	and tgl_transaksi < %s'\
    % (strSQLStartDate, strSQLEndDate)
  return config.CreateSQL(strSQL).RawResult

def resSQLReksadana(config, kode_jns_reksadana, strSQLStartDate, strSQLEndDate):
  strSQL = '\
    select \
    	clsfTransaksiInvestasi \
    	, mutasi_kredit \
    	, mutasi_debet \
    from TransaksiInvestasi t, Reksadana r \
    where isCommitted = \'T\' \
    	and clsfTransaksiInvestasi <> \'A\' \
    	and t.id_investasi = r.id_investasi \
    	and kode_jns_reksadana = \'%s\' \
    	and tgl_transaksi >= %s \
    	and tgl_transaksi < %s'\
    % (kode_jns_reksadana, strSQLStartDate, strSQLEndDate)

  strSQL = '\
    select \
    	clsfTransaksiInvestasi \
    	, mutasi_kredit \
    	, mutasi_debet \
    	, t.id_investasi \
    from TransaksiInvestasi t, Reksadana r \
    where isCommitted = \'T\' \
    	and clsfTransaksiInvestasi = \'C\' \
    	and t.id_investasi = r.id_investasi \
    	and kode_jns_reksadana in (\'RDPT\',\'RDS\',\'RDC\') \
    	and tgl_transaksi >= %s \
    	and tgl_transaksi < %s'\
    % (strSQLStartDate, strSQLEndDate)

  return config.CreateSQL(strSQL).RawResult

def getNomHasilReksadana(config,jenisReturn, strSQLStartDate, strSQLEndDate) :
  strSQL = '\
    select \
    	sum(mutasi_kredit-mutasi_debet) nom \
    from TransaksiInvestasi t, TransLRInvestasi l, reksadana r \
    where isCommitted = \'T\' \
    	and clsfTransaksiInvestasi = \'C\' \
    	and t.id_transaksiinvestasi = l.id_transaksiinvestasi \
    	and t.id_investasi = r.id_investasi \
    	and jenis = \'%s\' \
    	and tgl_transaksi >= %s \
    	and tgl_transaksi < %s '\
    % (jenisReturn,strSQLStartDate, strSQLEndDate)
    
  rSQL = config.CreateSQL(strSQL).RawResult
  return (rSQL.nom or 0.0)

def getSelisihNilaiWajarSukuk(config,strSQLStartDate, strSQLEndDate) :
  strSQL = '\
    select \
    	sum(mutasi_debet-mutasi_kredit) nom \
    from TransaksiInvestasi t, obligasi o \
    where isCommitted = \'T\' \
    	and clsfTransaksiInvestasi = \'D\' \
    	and t.id_investasi = o.id_investasi \
    	and tgl_transaksi >= %s \
    	and tgl_transaksi < %s '\
    % (strSQLStartDate, strSQLEndDate)

  rSQL = config.CreateSQL(strSQL).RawResult
  return (rSQL.nom or 0.0)
  
def resSQLNone(config) :
  strSQL = '\
    select \
    	mutasi_debet \
      , mutasi_kredit \
    from TransaksiInvestasi \
    where Id_transaksiinvestasi < 0 ' \

  return config.CreateSQL(strSQL).RawResult

def WriteContentRow(config, strJenis, strSQLStartDate, strSQLEndDate, oFile, lsJnsReks = None):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  global noUrut
  global sumHasilReal
  global sumHasilNonreal
  global sumBeban
  global sumHasilBersih
  global sumLRPelepasan
  global enumJenisRow

  nomHasilReal = 0.0
  nomHasilNonreal = 0.0
  nomBeban = 0.0
  nomHasilBersih = 0.0
  nomLRPelepasan = 0.0

  if strJenis == 'Deposito on Call':
    res = resSQLDepOnCall(config, strSQLStartDate, strSQLEndDate)
  elif strJenis == 'Deposito Berjangka':
    res = resSQLDepBjangka(config, strSQLStartDate, strSQLEndDate)
  elif strJenis == 'Sukuk':
    res = resSQLSukuk(config, strSQLStartDate, strSQLEndDate)
  elif strJenis == 'Reksadana':
    #strJenis = lsJnsReks[1]
    res = resSQLReksadana(config, lsJnsReks[0], strSQLStartDate, strSQLEndDate)
  elif strJenis == 'KOSONG' :
    strJenis = enumJenisRow[noUrut]
    res = resSQLNone(config)
  else:
    raise 'Laporan Error', 'Jenis investasi "%s" tidak dikenali' % (str(strJenis))

  while not res.Eof:
    if res.clsfTransaksiInvestasi == 'B':
      # piutang pendapatan
      nomHasilNonreal += res.mutasi_debet - res.mutasi_kredit

    elif res.clsfTransaksiInvestasi == 'C':
      # pendapatan
      #nomHasilReal += res.mutasi_kredit
      # beban
      #nomBeban += res.mutasi_debet
      nomHasilReal += (res.mutasi_kredit - res.mutasi_debet)
      
    elif res.clsfTransaksiInvestasi == 'D':
      nomHasilReal += (res.mutasi_debet - res.mutasi_kredit)
    res.Next()

  nomHasilBersih = nomHasilReal + nomHasilNonreal - nomBeban

  #deposito dan sukuk
  if strJenis in ('Deposito on Call','Deposito Berjangka','Sukuk'):
    nomHasilReal += nomHasilNonreal
    nomHasilNonreal = 0.0

  #reksadana
  if strJenis == 'Reksadana' :
    strJenis = 'Reksa Dana Pasar Uang, Reksa Dana Pendapatan Tetap, Reksa Dana saham dan Reksa Dana Campuran'
    nomHasilNonreal = 0.0
    nomHasilReal = 0.0
    nomBeban = 0.0
    nomLRPelepasan = getNomHasilReksadana(config,'U', strSQLStartDate, strSQLEndDate)
    nomHasilNonreal = getNomHasilReksadana(config,'K', strSQLStartDate, strSQLEndDate)

  if moduleapi.IsOddNumber(noUrut):
    bgcolor = '#EFEFEF'
  else:
    bgcolor = '#FFFFFF'

  oFile.write('	<tr>\n')
  # no urut
  oFile.write('		<td width="'+ str(NOCOL) +'" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'">\n')
  oFile.write('		<font size="2">'+ str(noUrut) +'</td>\n')

  # jenis investasi
  oFile.write('		<td width="'+ str(JENISCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'">\n')
  oFile.write('		<font size="2">'+ strJenis +'</font></td>\n')

  # hasil real
  oFile.write('		<td width="'+ str(NILAICOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'">\n')
  oFile.write('		<p align="right"><font size="2">'+ moduleapi.FormatFloatStd(config, nomHasilReal, '-') +'</font></td>\n')

  # deviden, sewa, LR pelepasan, Lainnya
  oFile.write('		<td width="'+ str(NILAICOL/2) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'">\n')
  oFile.write('		<p align="right"><font size="2">-</font></td>\n')
  oFile.write('		<td width="'+ str(NILAICOL/2) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'">\n')
  oFile.write('		<p align="right"><font size="2">-</font></td>\n')
  oFile.write('		<td width="'+ str(NILAICOL/2) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'">\n')
  oFile.write('		<p align="right"><font size="2">'+ moduleapi.FormatFloatStd(config, nomLRPelepasan, '-') +'</font></td>\n')
  oFile.write('		<td width="'+ str(NILAICOL/2) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'">\n')
  oFile.write('		<p align="right"><font size="2">-</font></td>\n')

  # hasil nonreal
  oFile.write('		<td width="'+ str(NILAICOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'">\n')
  oFile.write('		<p align="right"><font size="2">'+ moduleapi.FormatFloatStd(config, nomHasilNonreal, '-') +'</font></td>\n')

  # beban
  oFile.write('		<td width="'+ str(NILAICOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'">\n')
  oFile.write('		<p align="right"><font size="2">'+ moduleapi.FormatFloatStd(config, nomBeban, '-') +'</font></td>\n')

  # hasil investasi bersih
  oFile.write('		<td width="'+ str(NILAICOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'">\n')
  oFile.write('		<p align="right"><font size="2">'+ moduleapi.FormatFloatStd(config, nomHasilBersih, '-') +'</font></td>\n')

  oFile.write('	</tr>\n')

  noUrut += 1
  sumHasilReal += nomHasilReal
  sumHasilNonreal += nomHasilNonreal
  sumBeban += nomBeban
  sumHasilBersih += nomHasilBersih
  sumLRPelepasan += nomLRPelepasan
  
def resSQLJenisReksadana(config):
  strSQL = '\
    select kode_jns_reksadana, jenis_reksadana \
    from JenisReksadana'
  return config.CreateSQL(strSQL).RawResult

def ConstructReportValues(config, strSQLStartDate, strSQLEndDate, oFile):
  for i in range(2) :
    WriteContentRow(config, 'KOSONG', strSQLStartDate, strSQLEndDate, oFile)
  # deposito on call
  WriteContentRow(config, 'Deposito on Call', strSQLStartDate, strSQLEndDate, oFile)

  # deposito berjangka
  WriteContentRow(config, 'Deposito Berjangka', strSQLStartDate, strSQLEndDate, oFile)

  for i in range(4) :
    WriteContentRow(config, 'KOSONG', strSQLStartDate, strSQLEndDate, oFile)
  # sukuk
  WriteContentRow(config, 'Sukuk', strSQLStartDate, strSQLEndDate, oFile)


  # reksadana (masing-masing jenis)
  res = resSQLJenisReksadana(config)
  #while not res.Eof:
  #  WriteContentRow(config, 'Reksadana', strSQLStartDate, strSQLEndDate, oFile, [res.kode_jns_reksadana, res.jenis_reksadana])

  #  res.Next()
  WriteContentRow(config, 'Reksadana', strSQLStartDate, strSQLEndDate, oFile, [res.kode_jns_reksadana, res.jenis_reksadana])

  for i in range(11) :
    WriteContentRow(config, 'KOSONG', strSQLStartDate, strSQLEndDate, oFile)
    
def resSQLInvPerTanggal(config, strSQLDate):
  strSQL = '\
    select mutasi_debet, mutasi_kredit \
    from TransaksiInvestasi t \
    where isCommitted = \'T\' \
    	and clsfTransaksiInvestasi in (\'A\',\'D\') \
    	and tgl_transaksi < %s'\
    % (strSQLDate)
  return config.CreateSQL(strSQL).RawResult

def ConstructReportTrailer(config, strSQLStartDate, strSQLEndDate, oFile):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  # BARIS TOTAL
  oFile.write('	<tr>\n')
  oFile.write('		<td width="'+ str(NOCOL) +'" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		&nbsp;</td>\n')

  oFile.write('		<td width="'+ str(JENISCOL) +'" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<p align="left"><b><font size="2">Total</font></b></td>\n')

  # total hasil real
  oFile.write('		<td width="'+ str(NILAICOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<p align="right"><font size="2">'+ moduleapi.FormatFloatStd(config, sumHasilReal, '-') +'</font></td>\n')

  # deviden, sewa, LR pelepasan, Lainnya
  oFile.write('		<td width="'+ str(NILAICOL/2) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<p align="right"><font size="2">-</font></td>\n')
  oFile.write('		<td width="'+ str(NILAICOL/2) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<p align="right"><font size="2">-</font></td>\n')
  oFile.write('		<td width="'+ str(NILAICOL/2) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<p align="right"><font size="2">'+ moduleapi.FormatFloatStd(config, sumLRPelepasan, '-') +'</font></td>\n')
  oFile.write('		<td width="'+ str(NILAICOL/2) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<p align="right"><font size="2">-</font></td>\n')

  # total hasil nonreal
  oFile.write('		<td width="'+ str(NILAICOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<p align="right"><font size="2">'+ moduleapi.FormatFloatStd(config, sumHasilNonreal, '-') +'</font></td>\n')

  # total beban
  oFile.write('		<td width="'+ str(NILAICOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<p align="right"><font size="2">'+ moduleapi.FormatFloatStd(config, sumBeban, '-') +'</font></td>\n')

  # total hasil bersih
  oFile.write('		<td width="'+ str(NILAICOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<p align="right"><font size="2">'+ moduleapi.FormatFloatStd(config, sumHasilBersih, '-') +'</font></td>\n')

  oFile.write('	</tr>\n')


  # BARIS TOTAL INVESTASI AWAL TAHUN
  oFile.write('	<tr>\n')
  oFile.write('		<td width="'+ str(NOCOL) +'" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		&nbsp;</td>\n')

  oFile.write('		<td width="'+ str(JENISCOL) +'" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<p align="left"><b><font size="2">Total Investasi Awal Tahun</font></b></td>\n')

  # total investasi awal tahun
  sumTotalAwal = 0.0
  res = resSQLInvPerTanggal(config, strSQLStartDate)
  while not res.Eof:
    sumTotalAwal += res.mutasi_debet - res.mutasi_kredit

    res.Next()

  if strSQLStartDate[1:11] == '01/01/2010' :
    sumTotalAwal = 199572166267.0
    
  oFile.write('		<td colspan="'+ str(NBOFCOLUMNS - 2) +'" width="'+ str(NILAICOL * (NBOFCOLUMNS - 2)) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<p align="right"><font size="2">'+ moduleapi.FormatFloatStd(config, sumTotalAwal, '-') +'</font></td>\n')

  oFile.write('	</tr>\n')

  # BARIS TOTAL INVESTASI AKHIR TAHUN
  oFile.write('	<tr>\n')
  oFile.write('		<td width="'+ str(NOCOL) +'" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		&nbsp;</td>\n')

  oFile.write('		<td width="'+ str(JENISCOL) +'" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<p align="left"><b><font size="2">Total Investasi Akhir Tahun</font></b></td>\n')

  # total investasi akhir tahun
  sumTotalAkhir = 0.0
  res = resSQLInvPerTanggal(config, strSQLEndDate)
  while not res.Eof:
    sumTotalAkhir += res.mutasi_debet - res.mutasi_kredit

    res.Next()

  oFile.write('		<td colspan="'+ str(NBOFCOLUMNS - 2) +'" width="'+ str(NILAICOL * (NBOFCOLUMNS - 2)) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<p align="right"><font size="2">'+ moduleapi.FormatFloatStd(config, sumTotalAkhir, '-') +'</font></td>\n')

  oFile.write('	</tr>\n')

  # BARIS RATA-RATA INVESTASI
  oFile.write('	<tr>\n')
  oFile.write('		<td width="'+ str(NOCOL) +'" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		&nbsp;</td>\n')

  oFile.write('		<td width="'+ str(JENISCOL) +'" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<p align="left"><b><font size="2">Rata-rata Investasi</font></b></td>\n')

  rataInvestasi = (sumTotalAwal + sumTotalAkhir) / 2
  oFile.write('		<td colspan="'+ str(NBOFCOLUMNS - 2) +'" width="'+ str(NILAICOL * (NBOFCOLUMNS - 2)) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<p align="right"><font size="2">'+ moduleapi.FormatFloatStd(config, rataInvestasi, '-') +'</font></td>\n')

  oFile.write('	</tr>\n')

  # BARIS ROI
  oFile.write('	<tr>\n')
  oFile.write('		<td width="'+ str(NOCOL) +'" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		&nbsp;</td>\n')

  oFile.write('		<td width="'+ str(JENISCOL) +'" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<p align="left"><b><font size="2">ROI</font></b></td>\n')

  if moduleapi.IsApproxZero(rataInvestasi):
    strROI = '-'
  else:
    strROI = config.FormatFloat('0.00', 100.0 * sumHasilBersih / rataInvestasi) + '%'
  oFile.write('		<td colspan="'+ str(NBOFCOLUMNS - 2) +'" width="'+ str(NILAICOL * (NBOFCOLUMNS - 2)) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<p align="center"><font size="2">'+ strROI +'</font></td>\n')

  oFile.write('	</tr>\n')

  oFile.write('</table>\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('</body>\n')
  oFile.write('\n')
  oFile.write('</html>\n')

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  year = parameter.FirstRecord.year
  
  startDate = config.ModDateTime.EncodeDate(year, 1, 1)
  endDate = config.ModDateTime.EncodeDate(year, 12, 31)
  nextYearDate = config.ModDateTime.EncodeDate(year + 1, 1, 1)

  strSQLStartDate = config.FormatDateTimeForQuery(startDate)
  strSQLEndDate = config.FormatDateTimeForQuery(nextYearDate)

  sBaseFileName = 'hasil_tahunan.htm'
  sFileName = config.UserHomeDirectory + sBaseFileName
  oFile = open(sFileName, 'w')

  ConstructReportHeader(
    config
    , startDate
    , endDate
    , oFile
  )
  ConstructReportValues(
    config
    , strSQLStartDate
    , strSQLEndDate
    , oFile
  )
  ConstructReportTrailer(
    config
    , strSQLStartDate
    , strSQLEndDate
    , oFile
  )

  oFile.close()

  recRes = returnpacket.CreateDataPacketStructure('filename:string')
  recRes.filename = sBaseFileName

  #tambahan 
  sw = returnpacket.AddStreamWrapper()
  sw.LoadFromFile(sFileName)
  sw.MIMEType = config.AppObject.GetMIMETypeFromExtension(sFileName)

  return 1

