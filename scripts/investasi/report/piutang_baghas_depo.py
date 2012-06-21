import sys, string
import com.ihsan.util.modman as modman

#moduleapi = modman.getModule(config, 'moduleapi')

NOCOL = 30
NILAICOL = 150
TABLEWIDTH = NOCOL + NILAICOL * 4
NBOFCOLUMNS = 5


def ConstructReportHeader(config, monthBaghas, yearBaghas, monthPiutang, yearPiutang, oFile):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Piutang Investasi Per %s %s </title>\n' % (moduleapi.MONTHS_ID[monthPiutang-1], yearPiutang))
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Arial; line-height:100%; margin-top:0; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="'+ str(TABLEWIDTH) +'" id="table1" cellpadding="2">\n')
  
  oFile.write('	<tr>\n')
  oFile.write('		<td align="center" colspan="'+ str(NBOFCOLUMNS) +'" height="20" style="border-left:medium none #000000; border-right:medium none #000000; border-top-style:none; border-top-width:medium; border-bottom-style:none; border-bottom-width:medium">\n')
  oFile.write('		<font size="3" color="#008000"><b>Dana Pensiun Lembaga Keuangan PT. Bank Rakyat Indonesia, Tbk</b></font><br/>\n')
  oFile.write('		<font size="3" color="#008000"><b>Laporan Piutang Bagi Hasil Investasi</b></font><br/>\n')
  oFile.write('	</tr>\n')

  oFile.write('	<tr>\n')
  oFile.write('		<td align="center" width="'+ str(TABLEWIDTH) +'" colspan="'+ str(NBOFCOLUMNS) +'" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2" color="#008000"><b>Periode %s %s </b><br/><br/></font></td>\n' % (moduleapi.MONTHS_ID[monthPiutang-1], yearPiutang))
  oFile.write('	</tr>\n')

  oFile.write('	<tr>\n')
  # nomor urut
  oFile.write('		<td width="'+ str(NOCOL) +'" align="center" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b><font size="2">No.</font></b></td>\n')

  # nomor rekening
  oFile.write('		<td width="'+ str(NILAICOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Nomor Deposito</b></font></td>\n')

  # tanggal bagi hasil / buka
  oFile.write('		<td width="'+ str(NILAICOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Tgl Baghas/Buka</b></font></td>\n')

  # nominal baghas
  oFile.write('		<td width="'+ str(NILAICOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Nominal Baghas</b></font></td>\n')

  # nominal piutang
  oFile.write('		<td width="'+ str(NILAICOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Piutang Investasi</b></font></td>\n')
  
  oFile.write('	</tr>\n')
    
  oFile.write('\n')
  oFile.write('\n')

def resSQLBaghas(config, strDateAwBaghasSQL, strDateAkhBaghasSQL):
  strSQL = \
    "select rekening_deposito, tgl_buka, \
    sum(mutasi_kredit) - sum(mutasi_debet) as baghas \
    from TransaksiInvestasi t, Deposito d, investasi i \
    where clsfTransaksiInvestasi = 'C' \
    and t.id_investasi = d.id_investasi \
    and d.id_investasi = i.id_investasi \
    and isCommitted = 'T' \
    and tgl_transaksi >= '%s' \
    and tgl_transaksi < '%s' \
    group by rekening_deposito, tgl_buka"\
    % (strDateAwBaghasSQL, strDateAkhBaghasSQL)
  config.SendDebugMsg(strSQL)

  return config.CreateSQL(strSQL).RawResult

def ConstructReportHasil(config, monthBaghas, yearBaghas, monthPiutang, yearPiutang, oFile):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  strDateAwBaghasSQL = '%d-%d-1' % (yearBaghas, monthBaghas)
  lastday_baghas = moduleapi.GetLastDayOfMonth(monthBaghas, yearBaghas)
  dateBaghasTmrwDT = config.ModDateTime.EncodeDate(yearBaghas, monthBaghas, lastday_baghas) + 1
  strDateAkhBaghasSQL = config.FormatDateTime('yyyy-mm-dd', dateBaghasTmrwDT)

  strDateAwPiutangSQL = '%d-%d-1' % (yearPiutang, monthPiutang)
  lastday_piutang = moduleapi.GetLastDayOfMonth(monthPiutang, yearPiutang) 
  datePiutangTmrwDT = config.ModDateTime.EncodeDate(yearPiutang, monthPiutang, lastday_piutang) + 1
  strDateAkhPiutangSQL = config.FormatDateTime('yyyy-mm-dd', datePiutangTmrwDT)

  resSQL = resSQLBaghas(config, strDateAwBaghasSQL, strDateAkhBaghasSQL)
    
  resSQL.First(); i = 1
  while not resSQL.Eof:
    WriteContentRow(config, oFile, resSQL, i, lastday_piutang)
    i += 1   
    resSQL.Next()
    
  oFile.write('\n')
  oFile.write('\n')

def WriteContentRow(config, oFile, resSQL, i, lastday_piutang):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  baghas = resSQL.baghas or 0.0
  strBaghas = moduleapi.FormatFloatStd(config, baghas)
  tgl_buka = resSQL.tgl_buka[2]
  strTglBuka = str(tgl_buka)
  piutang = (lastday_piutang - tgl_buka + 1) * baghas / lastday_piutang
  strPiutang = moduleapi.FormatFloatStd(config, piutang) 
    
  oFile.write('	<tr>\n')
  # nomor urut
  oFile.write('		<td width="'+ str(NOCOL) +'" align="left" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#FFFFFF">\n')
  oFile.write('		%s</td>\n' % str(i))

  # nomor rekening
  oFile.write('		<td width="'+ str(NILAICOL) +'" align="left" style="border-style: solid; border-width: 1px; " bgcolor="#FFFFFF">\n')
  oFile.write('		%s</td>\n' % resSQL.rekening_deposito)

  # tanggal bagi hasil / buka
  oFile.write('		<td width="'+ str(NILAICOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#FFFFFF">\n')
  oFile.write('		%s</td>\n' % strTglBuka)

  # nominal baghas
  oFile.write('		<td width="'+ str(NILAICOL) +'" align="right" style="border-style: solid; border-width: 1px; " bgcolor="#FFFFFF">\n')
  oFile.write('		%s</td>\n' % strBaghas)

  # nominal piutang
  oFile.write('		<td width="'+ str(NILAICOL) +'" align="right" style="border-style: solid; border-width: 1px; " bgcolor="#FFFFFF">\n')
  oFile.write('		%s</td>\n' % strPiutang)
  
  oFile.write('	</tr>\n')
  
def ConstructReportTrailer(config, oFile):

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

  sBaseFileName = 'piutang_baghas_depo.htm'
  sFileName = config.UserHomeDirectory + sBaseFileName
  oFile = open(sFileName, 'w')

  ConstructReportHeader(
    config
    , parameter.FirstRecord.monthBaghas
    , parameter.FirstRecord.yearBaghas
    , parameter.FirstRecord.monthPiutang
    , parameter.FirstRecord.yearPiutang
    , oFile
  )

  ConstructReportHasil(
    config
    , parameter.FirstRecord.monthBaghas
    , parameter.FirstRecord.yearBaghas
    , parameter.FirstRecord.monthPiutang
    , parameter.FirstRecord.yearPiutang\
    , oFile
  )

  ConstructReportTrailer(
    config
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
