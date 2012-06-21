import sys
import com.ihsan.util.modman as modman

#moduleapi = modman.getModule(config, 'moduleapi')

NOCOL = 30
NAMACOL = 250
TGLCOL = 100
NILAICOL = 150
RATINGCOL = 70
NISBAHCOL = 70
TABLEWIDTH = NOCOL + NAMACOL + NILAICOL + TGLCOL + NILAICOL + NILAICOL + TGLCOL + RATINGCOL + RATINGCOL + NISBAHCOL

NBOFCOLUMNS = 10

def ConstructReportHeader(config, dtDate, oFile):
  strDate = config.FormatDateTime('d mmmm yyyy', dtDate)

  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Laporan Portofolio Investasi Sukuk</title>\n')
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Arial; line-height:100%; margin-top:0; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')

  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="'+ str(TABLEWIDTH) +'" id="table1" cellpadding="2">\n')

  oFile.write('	<tr>\n')
  oFile.write('		<td align="center" colspan="'+ str(NBOFCOLUMNS) +'" height="20" style="border-left:medium none #000000; border-right:medium none #000000; border-top-style:none; border-top-width:medium; border-bottom-style:none; border-bottom-width:medium">\n')
  oFile.write('		<font size="3" color="#008000"><b>Dana Pensiun Lembaga Keuangan PT. Bank Rakyat Indonesia, Tbk</b></font><br/>\n')
  oFile.write('		<font size="3" color="#008000"><b>Laporan Portofolio Investasi<br/>SUKUK</b></font><br/></td>\n')
  oFile.write('	</tr>\n')

  oFile.write('	<tr>\n')
  oFile.write('		<td align="center" width="'+ str(TABLEWIDTH) +'" colspan="'+ str(NBOFCOLUMNS) +'" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2" color="#008000"><b>Per '+ strDate +'</b><br/><br/></font></td>\n')
  oFile.write('	</tr>\n')

  oFile.write('	<tr>\n')

  # no urut
  oFile.write('		<td width="'+ str(NOCOL) +'" align="center" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b><font size="2">No.</font></b></td>\n')

  # nama sukuk
  oFile.write('		<td width="'+ str(NAMACOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Nama Sukuk</b></font></td>\n')

  # nominal
  oFile.write('		<td width="'+ str(NILAICOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Nilai Nominal</b></font></td>\n')

  # tgl perolehan
  oFile.write('		<td width="'+ str(TGLCOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Tanggal<br/>Perolehan</b></font></td>\n')

  # nilai perolehan
  oFile.write('		<td width="'+ str(NILAICOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Nilai Perolehan</b></font></td>\n')

  # nilai wajar
  oFile.write('		<td width="'+ str(NILAICOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Nilai Wajar</b></font></td>\n')

  # tgl jatuh tempo
  oFile.write('		<td width="'+ str(TGLCOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Tanggal<br/>Jatuh Tempo</b></font></td>\n')

  # rating pembelian
  oFile.write('		<td width="'+ str(RATINGCOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Rating saat<br/>Pembelian</b></font></td>\n')

  # rating laporan
  oFile.write('		<td width="'+ str(RATINGCOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Rating saat<br/>Laporan</b></font></td>\n')

  # nisbah
  oFile.write('		<td width="'+ str(NISBAHCOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Nisbah</b></font></td>\n')

  oFile.write('	</tr>\n')

def resSQLObligasi(config, strNextDateSQL):
  strSQL = '\
    select \
    	nama_obligasi \
    	, nominal_pembukaan \
    	, tgl_buka \
    	, harga_pari \
    	, akum_nominal \
    	, tgl_jatuh_tempo \
    	, i.id_investasi \
    	, ER \
    	, RateBeli \
    	, RateSekarang \
    from Obligasi o, Investasi i \
    where status = \'T\' \
    	and o.id_investasi = i.id_investasi \
    	and tgl_buka < %s'\
    % (strNextDateSQL)
  return config.CreateSQL(strSQL).RawResult

##Tambahan By Ade Herman 2011-04-07
def resSQLObligasiTutup(config, strNextDateSQL):
  strSQL = '\
    select \
    	nama_obligasi \
    	, nominal_pembukaan \
    	, tgl_buka \
    	, harga_pari \
    	, akum_nominal \
    	, tgl_jatuh_tempo \
    	, i.id_investasi \
    	, ER \
    	, RateBeli \
    	, RateSekarang \
    from Obligasi o, Investasi i \
    where status = \'F\' \
    	and o.id_investasi = i.id_investasi \
    	and tgl_buka < %s \
    	and tgl_tutup > %s '\
    % (strNextDateSQL,strNextDateSQL)
  return config.CreateSQL(strSQL).RawResult
  
##End Tambahan By Ade Herman 2011-04-07

def nominalNilaiWajarObligasi(config, id_investasi, strNextDateSQL):
  strSQL = '\
    select \
    	sum(mutasi_debet-mutasi_kredit) NomNilaiWajar \
    from  Investasi i,transaksiinvestasi t \
    where isCommitted = \'T\' \
    	and clsfTransaksiInvestasi in (\'A\',\'D\') \
      and i.id_investasi = %s \
      and t.id_investasi = i.id_investasi \
    	and tgl_transaksi < %s '\
    % (id_investasi, strNextDateSQL)
  resSQL = config.CreateSQL(strSQL).RawResult
  return resSQL.NomNilaiWajar or 0.0

def ConstructReportValues(config, dtDate, oFile):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  strNextDateSQL = config.FormatDateTimeForQuery(dtDate + 1)

  noUrut = 1
  sumNominal = 0.0
  sumPerolehan = 0.0
  sumWajar = 0.0

  res = resSQLObligasi(config, strNextDateSQL)
  while not res.Eof:
    nominal = res.harga_pari or 0.0
    perolehan = res.nominal_pembukaan or 0.0
    #wajar = res.akum_nominal or 0.0
    wajar = nominalNilaiWajarObligasi(config, res.id_investasi, strNextDateSQL )

    oFile.write('	<tr>\n')
    # no urut
    oFile.write('		<td width="'+ str(NOCOL) +'" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#FFFFFF">\n')
    oFile.write('		<font size="2">'+ str(noUrut) +'</td>\n')

    # nama sukuk
    oFile.write('		<td width="'+ str(NAMACOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
    oFile.write('		<font size="2">'+ (res.nama_obligasi or '&nbsp;') +'</font></td>\n')

    # nilai perolehan
    oFile.write('		<td align="right" width="'+ str(NILAICOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
    oFile.write('		<font size="2">'+ moduleapi.FormatFloatStd(config, nominal) +'</font></td>\n')

    # tgl perolehan
    oFile.write('		<td align="center" width="'+ str(TGLCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
    oFile.write('		<font size="2">'+ config.FormatDateTime('d-mmm-yy', moduleapi.DateTimeTupleToFloat(config, res.tgl_buka)) +'</font></td>\n')

    # nilai perolehan
    oFile.write('		<td align="right" width="'+ str(NILAICOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
    oFile.write('		<font size="2">'+ moduleapi.FormatFloatStd(config, perolehan) +'</font></td>\n')

    # nilai wajar
    oFile.write('		<td align="right" width="'+ str(NILAICOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
    oFile.write('		<font size="2">'+ moduleapi.FormatFloatStd(config, wajar) +'</font></td>\n')

    # tgl jatuh tempo
    oFile.write('		<td align="center" width="'+ str(TGLCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
    oFile.write('		<font size="2">'+ config.FormatDateTime('d-mmm-yy', moduleapi.DateTimeTupleToFloat(config, res.tgl_jatuh_tempo)) +'</font></td>\n')

    # rating pembelian
    oFile.write('		<td align="center" width="'+ str(RATINGCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
    oFile.write('		<font size="2">'+(res.RateBeli or '&nbsp;')+'</font></td>\n')

    # rating laporan
    oFile.write('		<td align="center" width="'+ str(RATINGCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
    oFile.write('		<font size="2">'+(res.RateSekarang or '&nbsp;')+'</font></td>\n')

    # nisbah (%)
    oFile.write('		<td align="right" width="'+ str(NISBAHCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
    oFile.write('		<font size="2">'+moduleapi.FormatFloatStd(config, res.ER)+'%</font></td>\n')

    oFile.write('	</tr>\n')

    noUrut += 1
    sumNominal += nominal
    sumPerolehan += perolehan
    sumWajar += wajar

    res.Next()

  ## Tambahan By Ade Herman 2011-04-07
  res = resSQLObligasiTutup(config, strNextDateSQL)
  while not res.Eof:
    nominal = res.harga_pari or 0.0
    perolehan = res.nominal_pembukaan or 0.0
    #wajar = res.akum_nominal or 0.0
    wajar = nominalNilaiWajarObligasi(config, res.id_investasi, strNextDateSQL )

    oFile.write('	<tr>\n')
    # no urut
    oFile.write('		<td width="'+ str(NOCOL) +'" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#FFFFFF">\n')
    oFile.write('		<font size="2">'+ str(noUrut) +'</td>\n')

    # nama sukuk
    oFile.write('		<td width="'+ str(NAMACOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
    oFile.write('		<font size="2">'+ (res.nama_obligasi or '&nbsp;') +'</font></td>\n')

    # nilai perolehan
    oFile.write('		<td align="right" width="'+ str(NILAICOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
    oFile.write('		<font size="2">'+ moduleapi.FormatFloatStd(config, nominal) +'</font></td>\n')

    # tgl perolehan
    oFile.write('		<td align="center" width="'+ str(TGLCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
    oFile.write('		<font size="2">'+ config.FormatDateTime('d-mmm-yy', moduleapi.DateTimeTupleToFloat(config, res.tgl_buka)) +'</font></td>\n')

    # nilai perolehan
    oFile.write('		<td align="right" width="'+ str(NILAICOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
    oFile.write('		<font size="2">'+ moduleapi.FormatFloatStd(config, perolehan) +'</font></td>\n')

    # nilai wajar
    oFile.write('		<td align="right" width="'+ str(NILAICOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
    oFile.write('		<font size="2">'+ moduleapi.FormatFloatStd(config, wajar) +'</font></td>\n')

    # tgl jatuh tempo
    oFile.write('		<td align="center" width="'+ str(TGLCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
    oFile.write('		<font size="2">'+ config.FormatDateTime('d-mmm-yy', moduleapi.DateTimeTupleToFloat(config, res.tgl_jatuh_tempo)) +'</font></td>\n')

    # rating pembelian
    oFile.write('		<td align="center" width="'+ str(RATINGCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
    oFile.write('		<font size="2">'+(res.RateBeli or '&nbsp;')+'</font></td>\n')

    # rating laporan
    oFile.write('		<td align="center" width="'+ str(RATINGCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
    oFile.write('		<font size="2">'+(res.RateSekarang or '&nbsp;')+'</font></td>\n')

    # nisbah (%)
    oFile.write('		<td align="right" width="'+ str(NISBAHCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
    oFile.write('		<font size="2">'+moduleapi.FormatFloatStd(config, res.ER)+'%</font></td>\n')

    oFile.write('	</tr>\n')

    noUrut += 1
    sumNominal += nominal
    sumPerolehan += perolehan
    sumWajar += wajar

    res.Next()
    ## End Tambahan By Ade Herman 2011-04-07
    
  return sumNominal, sumPerolehan, sumWajar

def ConstructReportTrailer(config, sumNominal, sumPerolehan, sumWajar, oFile):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  oFile.write('	<tr>\n')
  # no urut
  oFile.write('		<td width="'+ str(NOCOL) +'" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#FFFFFF">\n')
  oFile.write('		<font size="2">&nbsp;</td>\n')

  # nama sukuk
  oFile.write('		<td width="'+ str(NAMACOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
  oFile.write('		<font size="2">TOTAL SUKUK</font></td>\n')

  # nilai perolehan
  oFile.write('		<td align="right" width="'+ str(NILAICOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
  oFile.write('		<font size="2">'+ moduleapi.FormatFloatStd(config, sumNominal) +'</font></td>\n')

  # tgl perolehan
  oFile.write('		<td align="center" width="'+ str(TGLCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
  oFile.write('		<font size="2">&nbsp;</td>\n')

  # nilai perolehan
  oFile.write('		<td align="right" width="'+ str(NILAICOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
  oFile.write('		<font size="2">'+ moduleapi.FormatFloatStd(config, sumPerolehan) +'</font></td>\n')

  # nilai wajar
  oFile.write('		<td align="right" width="'+ str(NILAICOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
  oFile.write('		<font size="2">'+ moduleapi.FormatFloatStd(config, sumWajar) +'</font></td>\n')

  # tgl jatuh tempo
  oFile.write('		<td align="center" width="'+ str(TGLCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
  oFile.write('		<font size="2">&nbsp;</td>\n')

  # rating pembelian
  oFile.write('		<td align="center" width="'+ str(RATINGCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
  oFile.write('		<font size="2">&nbsp;</font></td>\n')

  # rating laporan
  oFile.write('		<td align="center" width="'+ str(RATINGCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
  oFile.write('		<font size="2">&nbsp;</font></td>\n')

  # nisbah (%)
  oFile.write('		<td align="right" width="'+ str(NISBAHCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
  oFile.write('		<font size="2">&nbsp;</font></td>\n')

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

  dtDate = parameter.FirstRecord.dateUntil

  sBaseFileName = 'portofolio_obligasi.htm'
  sFileName = config.UserHomeDirectory + sBaseFileName
  oFile = open(sFileName, 'w')

  ConstructReportHeader(config, dtDate, oFile)
  sumNominal, sumPerolehan, sumWajar = ConstructReportValues(config, dtDate, oFile)
  ConstructReportTrailer(config, sumNominal, sumPerolehan, sumWajar, oFile)

  oFile.close()

  recRes = returnpacket.CreateDataPacketStructure('filename:string')
  recRes.filename = sBaseFileName
  
  #tambahan 
  sw = returnpacket.AddStreamWrapper()
  sw.LoadFromFile(sFileName)
  sw.MIMEType = config.AppObject.GetMIMETypeFromExtension(sFileName)

  return 1

