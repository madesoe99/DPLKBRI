import sys
import com.ihsan.util.modman as modman

#moduleapi = modman.getModule(config, 'moduleapi')

NO_WIDTH = 30
JENIS_WIDTH = 400
NILAI_WIDTH = 150
NBOFCOLUMNS = 4

noUrut = 1
sumNominalCurr = 0.0
sumNominalPrev = 0.0
enumJenisRow = [0,'Surat Berharga Negara','Tabungan',3,4,'Sertifikat Deposito',
  'Sertifikat Bank Indonesia','Saham','Obligasi',9,10,'Reksa Dana Terproteksi, Reksa Dana dengan penjaminan dan Reksa Dana indeks',
  'Reksa Dana berbentuk KIK Penyertaan Terbatas','Reksa Dana yang UP-nya diperdagangkan di bursa','Efek Beragun Aset dari KIK EBA',
  'Unit Penyertaan Dana Investasi Real Estate berbentuk KIK','Kontrak Opsi Saham','Penempatan langsung pada saham',
  'Tanah','Bangunan','Tanah dan Bangunan','Surat Pengakuan Utang']


def ConstructReportHeader(config, colwidth, colspan, strDateUntil, strDateUntilPrev, oFile):
  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Laporan Portofolio Investasi</title>\n')
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Arial; line-height:100%; margin-top:0; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')

  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="'+ str(colwidth) +'" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td colspan="'+ str(colspan) +'" height="20" style="border-left:medium none #000000; border-right:medium none #000000; border-top-style:none; border-top-width:medium; border-bottom-style:none; border-bottom-width:medium">\n')
  oFile.write('		<p align="center"><font size="3" color="#008000"><b>Dana Pensiun Lembaga Keuangan PT. Bank Rakyat Indonesia, Tbk</b><br></font>\n')
  oFile.write('		<font size="3" color="#008000"><b>Laporan Portofolio Investasi</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td align="center" width="'+ str(colwidth) +'" colspan="'+ str(colspan) +'" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2" color="#008000"><b>Per '+ strDateUntil +'</b></font><br><br></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td align="right" width="'+ str(colwidth) +'" colspan="'+ str(colspan) +'" style="border-style: none; border-width: medium">\n')
  oFile.write('		<align="right" font size="2" color="#008000"><b>dalam rupiah</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="'+ str(NO_WIDTH) +'" align="center" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b><font size="2">NO</font></b></td>\n')
  oFile.write('		<td width="'+ str(JENIS_WIDTH) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>JENIS INVESTASI</b></font></td>\n')
  oFile.write('		<td width="'+ str(NILAI_WIDTH) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Per '+ strDateUntil +'</b></font></td>\n')
  oFile.write('		<td width="'+ str(NILAI_WIDTH) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Per '+ strDateUntilPrev +'</b></font></td>\n')
  oFile.write('	</tr>\n')

def resSQLDepOnCall(config, strSQLEndDate):
  strSQL = '\
    select \
    	mutasi_debet \
      , mutasi_kredit \
    from TransaksiInvestasi t, Deposito d \
    where isCommitted = \'T\' \
    	and clsfTransaksiInvestasi = \'A\' \
    	and t.id_investasi = d.id_investasi \
    	and jenisJatuhTempo = 0 \
    	and tgl_transaksi < %s'\
    % (strSQLEndDate)
  return config.CreateSQL(strSQL).RawResult

def resSQLDepBjangka(config, strSQLEndDate):
  strSQL = '\
    select \
    	mutasi_debet \
      , mutasi_kredit \
    from TransaksiInvestasi t, Deposito d \
    where isCommitted = \'T\' \
    	and clsfTransaksiInvestasi = \'A\' \
    	and t.id_investasi = d.id_investasi \
    	and jenisJatuhTempo > 0 \
    	and tgl_transaksi < %s'\
    % (strSQLEndDate)
  config.SendDebugMsg(strSQL)
  return config.CreateSQL(strSQL).RawResult

def resSQLSukuk(config, strSQLEndDate):
  strSQL = '\
    select \
    	mutasi_debet \
      , mutasi_kredit \
    from TransaksiInvestasi t, Obligasi o \
    where isCommitted = \'T\' \
    	and clsfTransaksiInvestasi in (\'A\',\'D\') \
    	and t.id_investasi = o.id_investasi \
    	and tgl_transaksi < %s'\
    % (strSQLEndDate)
  config.SendDebugMsg(strSQL)
  return config.CreateSQL(strSQL).RawResult

def resSQLJenisReksadana(config):
  strSQL = '\
    select kode_jns_reksadana, jenis_reksadana \
    from JenisReksadana'
  return config.CreateSQL(strSQL).RawResult

def resSQLReksadana(config, kode_jns_reksadana, strSQLEndDate):
#   strSQL = '\
#     select \
#     	mutasi_debet \
#       , mutasi_kredit \
#     from TransaksiInvestasi t, Reksadana r \
#     where isCommitted = \'T\' \
#     	and clsfTransaksiInvestasi in (\'A\',\'D\') \
#     	and t.id_investasi = r.id_investasi \
#     	and kode_jns_reksadana = \'%s\' \
#     	and tgl_transaksi < %s'\
#     % (kode_jns_reksadana, strSQLEndDate)

  strSQL = '\
    select \
    	mutasi_debet \
      , mutasi_kredit \
    from TransaksiInvestasi t, Reksadana r \
    where isCommitted = \'T\' \
    	and clsfTransaksiInvestasi in (\'A\',\'D\') \
    	and t.id_investasi = r.id_investasi \
    	and kode_jns_reksadana in (\'RDPT\',\'RDS\',\'RDC\') \
      and tgl_transaksi < %s \
      and t.id_investasi in ( select id_investasi from investasi \
                              where status = \'T\') '\
    % (strSQLEndDate)
  config.SendDebugMsg(strSQL)
  return config.CreateSQL(strSQL).RawResult

def resSQLNone(config) :
  strSQL = '\
    select \
    	mutasi_debet \
      , mutasi_kredit \
    from TransaksiInvestasi \
    where Id_transaksiinvestasi < 0 ' \

  return config.CreateSQL(strSQL).RawResult
  
def WriteContentRow(config, strJenis, strDateUntilTmrwSQL, strDateUntilTmrwPrevSQL, oFile, lsJnsReks = None):
  global noUrut
  global sumNominalCurr
  global sumNominalPrev
  global enumJenisRow

  moduleapi = modman.getModule(config, 'moduleapi')
  
  nominalCurr = 0.0
  nominalPrev = 0.0

  if strJenis == 'Deposito on Call':
    resCurr = resSQLDepOnCall(config, strDateUntilTmrwSQL)
    resPrev = resSQLDepOnCall(config, strDateUntilTmrwPrevSQL)
  elif strJenis == 'Deposito Berjangka':
    resCurr = resSQLDepBjangka(config, strDateUntilTmrwSQL)
    resPrev = resSQLDepBjangka(config, strDateUntilTmrwPrevSQL)
  elif strJenis == 'Sukuk':
    resCurr = resSQLSukuk(config, strDateUntilTmrwSQL)
    resPrev = resSQLSukuk(config, strDateUntilTmrwPrevSQL)
  elif strJenis == 'Reksadana':
    #strJenis = lsJnsReks[1]
    strJenis = 'Reksa Dana Pasar Uang, Reksa Dana Pendapatan Tetap, Reksa Dana saham dan Reksa Dana Campuran'
    resCurr = resSQLReksadana(config, lsJnsReks[0], strDateUntilTmrwSQL)
    resPrev = resSQLReksadana(config, lsJnsReks[0], strDateUntilTmrwPrevSQL)
  elif strJenis == 'KOSONG' :
    strJenis = enumJenisRow[noUrut]
    resCurr = resSQLNone(config)
    resPrev = resSQLNone(config)
  else:
    raise 'Laporan Error', 'Jenis investasi "%s" tidak dikenali' % (str(strJenis))
    
  resCurr.First()
  while not resCurr.Eof:
    nominalCurr += resCurr.mutasi_debet - resCurr.mutasi_kredit
#     config.SendDebugMsg('%s-%s-%s-%s' % (strJenis,str(nominalCurr),str(resCurr.mutasi_debet), str(resCurr.mutasi_kredit)))

    resCurr.Next()

  while not resPrev.Eof:
    nominalPrev += resPrev.mutasi_debet - resPrev.mutasi_kredit

    resPrev.Next()

  if strDateUntilTmrwPrevSQL[1:-1] == '2009-12-31' :
    if strJenis == 'Deposito on Call':
      nominalPrev = 1000000000.0
    elif strJenis == 'Deposito Berjangka':
      nominalPrev = 180856205284.0
    elif strJenis == 'Sukuk':
      nominalPrev = 4000000000.0
    elif strJenis == 'Reksa Dana Pasar Uang, Reksa Dana Pendapatan Tetap, Reksa Dana saham dan Reksa Dana Campuran' :
      nominalPrev = 13715960983.0
    else:
      pass

  if moduleapi.IsOddNumber(noUrut):
    bgcolor = '#EFEFEF'
  else:
    bgcolor = '#FFFFFF'

  oFile.write('	<tr>\n')

  # no urut
  oFile.write('		<td width="'+ str(NO_WIDTH) +'" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'">\n')
  oFile.write('		<font size="2">'+ str(noUrut) +'</td>\n')

  # jenis investasi
  oFile.write('		<td width="'+ str(JENIS_WIDTH) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'">\n')
  oFile.write('		<font size="2">'+ strJenis +'</font></td>\n')

  # nominal skrg
  oFile.write('		<td width="'+ str(NILAI_WIDTH) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'">\n')
  oFile.write('		<p align="right"><font size="2">'+ moduleapi.FormatFloatStd(config, nominalCurr, '-') +'</font></td>\n')

  # nominal periode lalu
  oFile.write('		<td width="'+ str(NILAI_WIDTH) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'">\n')
  oFile.write('		<p align="right"><font size="2">'+ moduleapi.FormatFloatStd(config, nominalPrev, '-') +'</font></td>\n')

  oFile.write('	</tr>\n')

  noUrut += 1
  sumNominalCurr += nominalCurr
  sumNominalPrev += nominalPrev

def ConstructReportValues(config, dtDateUntilTmrw, oFile):
#   config.SendDebugMsg(str(dtDateUntilTmrw))  
  y, m, d = config.ModDateTime.DecodeDate(dtDateUntilTmrw)
  strDateUntilTmrwSQL = '\'%d-%d-%d\'' % (y, m, d)#config.FormatDateTimeForQuery(dtDateUntilTmrw)
  
  #strDateUntilTmrwPrevSQL = '\'%d-%d-%d\'' % (y-1, m, d)
  strDateUntilTmrwPrevSQL = '\'%d-%d-%d\'' % (y-1, 12, 31)

  # write None Data
  for i in range(2) :
    WriteContentRow(config, 'KOSONG', strDateUntilTmrwSQL, strDateUntilTmrwPrevSQL, oFile)

  # deposito on call
  WriteContentRow(config, 'Deposito on Call', strDateUntilTmrwSQL, strDateUntilTmrwPrevSQL, oFile)

  # deposito berjangka
  WriteContentRow(config, 'Deposito Berjangka', strDateUntilTmrwSQL, strDateUntilTmrwPrevSQL, oFile)

  # write None Data
  for i in range(4) :
    WriteContentRow(config, 'KOSONG', strDateUntilTmrwSQL, strDateUntilTmrwPrevSQL, oFile)

  # sukuk
  WriteContentRow(config, 'Sukuk', strDateUntilTmrwSQL, strDateUntilTmrwPrevSQL, oFile)

  # reksadana (masing-masing jenis)
  res = resSQLJenisReksadana(config)
  #while not res.Eof:
    #WriteContentRow(config, 'Reksadana', strDateUntilTmrwSQL, strDateUntilTmrwPrevSQL, oFile, [res.kode_jns_reksadana, res.jenis_reksadana])

    #res.Next()
  WriteContentRow(config, 'Reksadana', strDateUntilTmrwSQL, strDateUntilTmrwPrevSQL, oFile, [res.kode_jns_reksadana, res.jenis_reksadana])
  # write None Data
  for i in range(11) :
    WriteContentRow(config, 'KOSONG', strDateUntilTmrwSQL, strDateUntilTmrwPrevSQL, oFile)

def ConstructReportTrailer(config, sumNominal, sumNominalPrev, oFile):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  oFile.write('	<tr>\n')
  oFile.write('		<td width="'+ str(NO_WIDTH) +'" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		&nbsp;</td>\n')
  oFile.write('		<td width="'+ str(JENIS_WIDTH) +'" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<p align="left"><b><font size="2">Total Investasi</font></b></td>\n')

  oFile.write('		<td width="'+ str(NILAI_WIDTH) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<p align="right"><font size="2">'+ moduleapi.FormatFloatStd(config, sumNominal, '-') +'</font></td>\n')

  oFile.write('		<td width="'+ str(NILAI_WIDTH) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<p align="right"><font size="2">'+ moduleapi.FormatFloatStd(config, sumNominalPrev, '-') +'</font></td>\n')

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

  dtDateUntil = parameter.FirstRecord.dateUntil
  dtDateUntilTmrw = dtDateUntil + 1

  sBaseFileName = 'portofolio_investasi.htm'
  sFileName = config.UserHomeDirectory + sBaseFileName
  oFile = open(sFileName, 'w')

  tableWidth = NO_WIDTH + JENIS_WIDTH + NILAI_WIDTH + NILAI_WIDTH

  strDateUntil = config.FormatDateTime('d mmmm yyyy', dtDateUntil)
  
  y, m, d = config.ModDateTime.DecodeDate(dtDateUntil)
  #dtDateUntilPrev = config.ModDateTime.EncodeDate(y-1, m, d)
  dtDateUntilPrev = config.ModDateTime.EncodeDate(y-1, 12, 31)
  strDateUntilPrev = config.FormatDateTime('d mmmm yyyy', dtDateUntilPrev)

  ConstructReportHeader(
    config
    , tableWidth
    , NBOFCOLUMNS
    , strDateUntil
    , strDateUntilPrev
    , oFile
  )
  ConstructReportValues(
    config
    , dtDateUntilTmrw
    , oFile
  )
  ConstructReportTrailer(
    config
    , sumNominalCurr
    , sumNominalPrev
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

