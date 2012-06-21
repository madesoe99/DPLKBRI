import sys, string
import com.ihsan.util.modman as modman

#moduleapi = modman.getModule(config, 'moduleapi')

NOCOL = 30
NILAICOL = 150
TABLEWIDTH = NOCOL + NILAICOL * 4
NBOFCOLUMNS = 5
DAY_IN_MONTH = 30

def ConstructReportHeader(config, monthBaghas, yearBaghas, monthPiutang, yearPiutang, oFile):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Piutang Yield Sukuk Per %s %s </title>\n' % (moduleapi.MONTHS_ID[monthPiutang-1], yearPiutang))
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Arial; line-height:100%; margin-top:0; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="'+ str(TABLEWIDTH) +'" id="table1" cellpadding="2">\n')
  
  oFile.write('	<tr>\n')
  oFile.write('		<td align="center" colspan="'+ str(NBOFCOLUMNS) +'" height="20" style="border-left:medium none #000000; border-right:medium none #000000; border-top-style:none; border-top-width:medium; border-bottom-style:none; border-bottom-width:medium">\n')
  oFile.write('		<font size="3" color="#008000"><b>Dana Pensiun Lembaga Keuangan PT. Bank Rakyat Indonesia, Tbk</b></font><br/>\n')
  oFile.write('		<font size="3" color="#008000"><b>Laporan Piutang Yield Sukuk</b></font><br/>\n')
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
  oFile.write('		<font size="2"><b>Nama Obligasi</b></font></td>\n')

  # tanggal bagi hasil / buka
  oFile.write('		<td width="'+ str(NILAICOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Tgl Realisasi</br>Kupon Sebelumnya</b></font></td>\n')

  # nominal baghas
  oFile.write('		<td width="'+ str(NILAICOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Realisasi Kupon</br>%s %s</b></font></td>\n' % (moduleapi.MONTHS_ID[monthBaghas-1], yearBaghas))

  # nominal piutang
  oFile.write('		<td width="'+ str(NILAICOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Piutang Yield</br>%s %s</b></font></td>\n' % (moduleapi.MONTHS_ID[monthPiutang-1], yearPiutang))
  
  oFile.write('	</tr>\n')
    
  oFile.write('\n')
  oFile.write('\n')

def GetTglBaghasPrev(config, strDateAwBaghasSQL, id_investasi):
  strSQL = \
    "select tgl_transaksi \
    from TransaksiInvestasi t \
    where clsfTransaksiInvestasi = 'C' \
    and id_investasi = %s \
    and isCommitted = 'T' \
    and (mutasi_debet <> 0 or mutasi_kredit <> 0)\
    and tgl_transaksi < '%s'\
    order by tgl_transaksi desc" % (id_investasi, strDateAwBaghasSQL)
  config.SendDebugMsg(strSQL)
  resSQL = config.CreateSQL(strSQL).RawResult
  
  return resSQL.tgl_transaksi or '' 

def resSQLBaghas(config, strDateAwBaghasSQL, strDateAkhBaghasSQL):
  strSQL = \
    "select i.id_investasi, nama_obligasi, jeniskupon, tgl_transaksi,\
    (mutasi_kredit - mutasi_debet) as baghas \
    from TransaksiInvestasi t, Obligasi o, investasi i \
    where clsfTransaksiInvestasi = 'C' \
    and t.id_investasi = o.id_investasi \
    and o.id_investasi = i.id_investasi \
    and isCommitted = 'T' \
    and (mutasi_debet <> 0 or mutasi_kredit <> 0)\
    and tgl_transaksi >= '%s' \
    and tgl_transaksi < '%s' \
    order by tgl_transaksi desc"\
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
    WriteContentRow(config, oFile, resSQL, i, yearBaghas, monthBaghas, yearPiutang, monthPiutang)
    i += 1   
    resSQL.Next()
    
  oFile.write('\n')
  oFile.write('\n')

def IsValidPrev(tgl_baghas_prev, jeniskupon, yBaghas, mBaghas):
  m_baghas_prev = tgl_baghas_prev[1]
  y_baghas_prev = tgl_baghas_prev[0]  
  
  return (mBaghas-m_baghas_prev == jeniskupon and yBaghas-y_baghas_prev == 0) or (mBaghas-m_baghas_prev == jeniskupon - 12 and yBaghas-y_baghas_prev == 1)

def WriteContentRow(config, oFile, resSQL, i, yBaghas, mBaghas, yPiutang, mPiutang):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  strDateAwBaghasSQL = '%d-%d-1' % (yBaghas, mBaghas)

  baghas = resSQL.baghas or 0.0
  strBaghas = moduleapi.FormatFloatStd(config, baghas)
  
  hr_pembagi = resSQL.jeniskupon * DAY_IN_MONTH
      
  tgl_baghas_prev = GetTglBaghasPrev(config, strDateAwBaghasSQL, resSQL.id_investasi)
  d_baghas_prev = 0; m_baghas_prev = 0; y_baghas_prev = 0 
   
  if tgl_baghas_prev <> '' and IsValidPrev(tgl_baghas_prev, resSQL.jeniskupon, yBaghas, mBaghas): #sudah pernah realisasi kupon sebelumnya    
    d_baghas_prev = tgl_baghas_prev[2]
    m_baghas_prev = tgl_baghas_prev[1]
    y_baghas_prev = tgl_baghas_prev[0]
  else: #realisasi kupon pertama
    d_baghas_prev = resSQL.tgl_transaksi[2]
    m_baghas_prev = resSQL.tgl_transaksi[1]
    y_baghas_prev = resSQL.tgl_transaksi[0]
  
  strTglBaghasPrev = '%s/%s/%s' % (d_baghas_prev, m_baghas_prev, y_baghas_prev)
    
  num_day_prev = moduleapi.GetLastDayOfMonth(yPiutang, mPiutang) - d_baghas_prev + 1
  config.SendDebugMsg('id='+str(resSQL.id_investasi))
  config.SendDebugMsg('a='+str(num_day_prev))
  j = 1
  for j in range(resSQL.jeniskupon-1):  
    if mPiutang == 1: mPiutang = 12; yPiutang = yPiutang - 1
    else: mPiutang -= 1
      
    num_day_prev = num_day_prev + moduleapi.GetLastDayOfMonth(yPiutang, mPiutang)
    config.SendDebugMsg('b='+str(num_day_prev))

  piutang = num_day_prev * baghas / hr_pembagi  
  config.SendDebugMsg('c='+str(num_day_prev)) 
  config.SendDebugMsg('hr_pembagi='+str(hr_pembagi))
  config.SendDebugMsg('baghas='+str(baghas))
  config.SendDebugMsg('piutang='+str(piutang))
  strPiutang = moduleapi.FormatFloatStd(config, piutang) 
    
  oFile.write('	<tr>\n')
  # nomor urut 
  oFile.write('		<td width="'+ str(NOCOL) +'" align="left" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#FFFFFF">\n')
  oFile.write('		%s</td>\n' % str(i))

  # nomor rekening
  oFile.write('		<td width="'+ str(NILAICOL) +'" align="left" style="border-style: solid; border-width: 1px; " bgcolor="#FFFFFF">\n')
  oFile.write('		%s</td>\n' % resSQL.nama_obligasi)

  # tanggal bagi hasil / buka
  oFile.write('		<td width="'+ str(NILAICOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#FFFFFF">\n')
  oFile.write('		%s</td>\n' % strTglBaghasPrev)

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
