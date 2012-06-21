import sys
import com.ihsan.util.modman as modman

#moduleapi = modman.getModule(config, 'moduleapi')

NOCOL = 30
PIHAKCOL = 300
TGLCOL = 100
NILAICOL = 150
WAKTUCOL = 70
NISBAHCOL = 70
TABLEWIDTH = NOCOL + PIHAKCOL + TGLCOL + NILAICOL + NILAICOL + TGLCOL + WAKTUCOL + NISBAHCOL

NBOFCOLUMNS = 8

def ConstructReportHeader(config, dtDate, oFile):
  strDate = config.FormatDateTime('d mmmm yyyy', dtDate)

  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Laporan Portofolio Investasi Deposito</title>\n')
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Arial; line-height:100%; margin-top:0; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')

  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="'+ str(TABLEWIDTH) +'" id="table1" cellpadding="2">\n')

  oFile.write('	<tr>\n')
  oFile.write('		<td align="center" colspan="'+ str(NBOFCOLUMNS) +'" height="20" style="border-left:medium none #000000; border-right:medium none #000000; border-top-style:none; border-top-width:medium; border-bottom-style:none; border-bottom-width:medium">\n')
  oFile.write('		<font size="3" color="#008000"><b>Dana Pensiun Lembaga Keuangan PT. Bank Rakyat Indonesia, Tbk</b></font><br/>\n')
  oFile.write('		<font size="3" color="#008000"><b>Laporan Portofolio Investasi</b></font><br/>\n')
  oFile.write('		<font size="3" color="#008000"><b>Deposito on Call dan Deposito Berjangka</b></font><br/></td>\n')
  oFile.write('	</tr>\n')

  oFile.write('	<tr>\n')
  oFile.write('		<td align="center" width="'+ str(TABLEWIDTH) +'" colspan="'+ str(NBOFCOLUMNS) +'" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2" color="#008000"><b>Per '+ strDate +'</b><br/><br/></font></td>\n')
  oFile.write('	</tr>\n')

  oFile.write('	<tr>\n')
  oFile.write('		<td width="'+ str(NOCOL) +'" align="center" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b><font size="2">No.</font></b></td>\n')

  oFile.write('		<td width="'+ str(PIHAKCOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Nama Bank</b></font></td>\n')

  oFile.write('		<td width="'+ str(TGLCOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Tgl<br/>Penempatan</b></font></td>\n')

  oFile.write('		<td width="'+ str(NILAICOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Nilai Nominal<br/>(Rp)</b></font></td>\n')

  oFile.write('		<td width="'+ str(NILAICOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Nilai Nominal dlm<br/>mata Uang Asing</b></font></td>\n')

  oFile.write('		<td width="'+ str(TGLCOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Tgl<br/>Jatuh Tempo</b></font></td>\n')

  oFile.write('		<td width="'+ str(WAKTUCOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Jangka<br/>Waktu</b></font></td>\n')

  oFile.write('		<td width="'+ str(NISBAHCOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Nisbah</b></font></td>\n')
  oFile.write('	</tr>\n')

def resPihakKetiga(config):
  strSQL = '\
    select kode_pihak_ketiga, nama_pihak_ketiga \
    from PihakKetiga \
    order by kode_pihak_ketiga'
  return config.CreateSQL(strSQL).RawResult

def resSQLDepOnCall(config, kode_pihak_ketiga, strNextDateSQL):
  strSQL = '\
    select \
    	i.id_investasi \
    	, tgl_buka \
    	, tgl_jatuh_tempo \
    	, jmlHariOnCall as jangkaWaktu \
    	, nisbah \
    from Deposito d, Investasi i \
    where d.id_investasi = i.id_investasi \
    	and jenisJatuhTempo = 0 \
    	and kode_pihak_ketiga = %s \
    	and (tgl_buka < %s \
    	 or tgl_tutup < %s )' \
    % (kode_pihak_ketiga, strNextDateSQL, strNextDateSQL)
  return config.CreateSQL(strSQL).RawResult
  #status = \'T\' \
  
def resSQLDepBjangka(config, kode_pihak_ketiga, strNextDateSQL):
  strSQL = '\
    select \
    	i.id_investasi \
    	, tgl_buka \
    	, tgl_jatuh_tempo \
    	, jenisJatuhTempo as jangkaWaktu \
    	, nisbah \
    from Deposito d, Investasi i \
    where d.id_investasi = i.id_investasi \
      and jenisJatuhTempo > 0 \
    	and kode_pihak_ketiga = %s\
    	and tgl_buka < %s ' \
    % (kode_pihak_ketiga, strNextDateSQL)
    
  config.SendDebugMsg(strSQL)
  return config.CreateSQL(strSQL).RawResult

def resSQLDeposito(config, isBerjangka, kode_pihak_ketiga, strNextDateSQL):
  if isBerjangka == 0:
    return resSQLDepBjangka(config, kode_pihak_ketiga, strNextDateSQL)
  else:
    # on call
    return resSQLDepOnCall(config, kode_pihak_ketiga, strNextDateSQL)

def resSQLMutasi(config, id_investasi, strNextDateSQL):
  strSQL = '\
    select \
    	mutasi_debet \
    	, mutasi_kredit \
    from TransaksiInvestasi \
    where isCommitted = \'T\' \
    	and clsfTransaksiInvestasi = \'A\' \
    	and id_investasi = %d \
    	and tgl_transaksi < %s'\
    % (id_investasi, strNextDateSQL)
  return config.CreateSQL(strSQL).RawResult

def getNilaiDeposito(config, id_investasi, strNextDateSQL):
  nominal = 0.0
  res = resSQLMutasi(config, id_investasi, strNextDateSQL)
  while not res.Eof:
    nominal += (res.mutasi_debet or 0.0) - (res.mutasi_kredit or 0.0)

    res.Next()

  return nominal

def WriteTotalDeposito(config, jenisDep, sumTotal, oFile):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  ## TOTAL DEPOSITO
  oFile.write('	<tr>\n')
  oFile.write('		<td width="'+ str(NOCOL) +'" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#FFFFFF">\n')
  oFile.write('		<font size="2">&nbsp;</td>\n')

  # jenis deposito
  oFile.write('		<td width="'+ str(PIHAKCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
  oFile.write('		<font size="2"><b>Total '+ jenisDep +'</b></font></td>\n')

  # tgl penempatan
  oFile.write('		<td width="'+ str(TGLCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
  oFile.write('		<font size="2">&nbsp;</font></td>\n')

  # nominal
  oFile.write('		<td align="right" width="'+ str(NILAICOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
  oFile.write('		<font size="2"><b>'+ moduleapi.FormatFloatStd(config, sumTotal) +'</b></font></td>\n')

  # nominal dlm mata uang asing
  oFile.write('		<td width="'+ str(NILAICOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
  oFile.write('		<font size="2">&nbsp;</font></td>\n')

  # tgl jatuh tempo
  oFile.write('		<td width="'+ str(TGLCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
  oFile.write('		<font size="2">&nbsp;</font></td>\n')

  # jangka waktu
  oFile.write('		<td width="'+ str(WAKTUCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
  oFile.write('		<font size="2">&nbsp;</font></td>\n')

  # nisbah (%)
  oFile.write('		<td width="'+ str(NISBAHCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
  oFile.write('		<font size="2">&nbsp;</font></td>\n')

  oFile.write('	</tr>\n')
  ##

def WriteDeposito(config, isBerjangka, noUrutDep, resPK, strNextDateSQL, oFile):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  if isBerjangka:
    jenisDep = 'Deposito Berjangka'
    waktu = 'bulan'
  else:
    jenisDep = 'Deposito On Call'
    waktu = 'hari'

  config.SendDebugMsg('masuk..........01')
  ## HEADER DEPOSITO
  oFile.write('	<tr>\n')
  # no urut deposito
  oFile.write('		<td width="'+ str(NOCOL) +'" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#EFEFEF">\n')
  oFile.write('		<font size="2">'+ str(noUrutDep) +'</td>\n')
  # jenis deposito
  oFile.write('		<td colspan="'+ str(NBOFCOLUMNS - 1) +'" width="'+ str(TABLEWIDTH - NOCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#EFEFEF">\n')
  oFile.write('		<font size="2"><b>'+ jenisDep +'</b></font></td>\n')
  oFile.write('	</tr>\n')
  ##

  noUrut = 1
  sumTotal = 0.0

  config.SendDebugMsg('masuk..........02')
  resPK.First()
  while not resPK.Eof:
  
    config.SendDebugMsg('masuk..........02a')
    config.SendDebugMsg('isBerjangka' + str(isBerjangka))
    config.SendDebugMsg('resPK.kode_pihak_ketiga'+str(resPK.kode_pihak_ketiga))
    config.SendDebugMsg('strNextDateSQL'+ str(strNextDateSQL))
    resDep = resSQLDeposito(config, isBerjangka, resPK.kode_pihak_ketiga, strNextDateSQL)
    config.SendDebugMsg('masuk..........03')

    while not resDep.Eof:
      # ambil nilai nominal
      config.SendDebugMsg('masuk..........04')
      nominal = getNilaiDeposito(config, resDep.id_investasi, strNextDateSQL)
      sumTotal += nominal

      ## RINCIAN DEPOSITO ON CALL
      oFile.write('	<tr>\n')
      oFile.write('		<td width="'+ str(NOCOL) +'" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#FFFFFF">\n')
      oFile.write('		<font size="2">&nbsp;</td>\n')

      # pihak ketiga
      oFile.write('		<td width="'+ str(PIHAKCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
      oFile.write('		<font size="2">'+ str(noUrut) +'. '+ (resPK.nama_pihak_ketiga or '&nbsp;') +'</font></td>\n')

      # tgl penempatan
      oFile.write('		<td align="center" width="'+ str(TGLCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
      oFile.write('		<font size="2">'+ config.FormatDateTime('d-mmm-yy', moduleapi.DateTimeTupleToFloat(config, resDep.tgl_buka)) +'</font></td>\n')

      # nominal
      oFile.write('		<td align="right" width="'+ str(NILAICOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
      oFile.write('		<font size="2">'+ moduleapi.FormatFloatStd(config, nominal) +'</font></td>\n')

      # nominal dlm mata uang asing
      oFile.write('		<td align="right" width="'+ str(NILAICOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
      oFile.write('		<font size="2">-</font></td>\n')

      # tgl jatuh tempo
      oFile.write('		<td align="center" width="'+ str(TGLCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
      oFile.write('		<font size="2">'+ config.FormatDateTime('d-mmm-yy', moduleapi.DateTimeTupleToFloat(config, resDep.tgl_jatuh_tempo)) +'</font></td>\n')

      # jangka waktu
      oFile.write('		<td align="center" width="'+ str(WAKTUCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
      oFile.write('		<font size="2">'+ str(resDep.jangkaWaktu) +' '+ waktu +'</font></td>\n')

      # nisbah (%)
      oFile.write('		<td align="right" width="'+ str(NISBAHCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
      oFile.write('		<font size="2">'+ config.FormatFloat('0.00', resDep.nisbah) +'%</font></td>\n')

      oFile.write('	</tr>\n')
      ##

      noUrut += 1

      resDep.Next()

    # end while not resDep.Eof

    resPK.Next()

  # end while not resPK.Eof
  
  WriteTotalDeposito(config, jenisDep, sumTotal, oFile)

def WriteDepositoOnCall(config, noUrutDep, resPK, strNextDateSQL, oFile):
  WriteDeposito(config, 0, noUrutDep, resPK, strNextDateSQL, oFile)

def WriteDepositoBerjangka(config, noUrutDep, resPK, strNextDateSQL, oFile):
  WriteDeposito(config, 1, noUrutDep, resPK, strNextDateSQL, oFile)

def ConstructReportValues(config, dtDate, oFile):
  strNextDateSQL = config.FormatDateTimeForQuery(dtDate + 1)

  resPK = resPihakKetiga(config)
  
  WriteDepositoOnCall(config, 1, resPK, strNextDateSQL, oFile)
  WriteDepositoBerjangka(config, 2, resPK, strNextDateSQL, oFile)

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

  dtDate = parameter.FirstRecord.dateUntil

  sBaseFileName = 'portofolio_deposito.htm'
  sFileName = config.UserHomeDirectory + sBaseFileName
  oFile = open(sFileName, 'w')

  ConstructReportHeader(config, dtDate, oFile)
  ConstructReportValues(config, dtDate, oFile)
  ConstructReportTrailer(config, oFile)

  oFile.close()

  recRes = returnpacket.CreateDataPacketStructure('filename:string')
  recRes.filename = sBaseFileName
  
  #tambahan 
  sw = returnpacket.AddStreamWrapper()
  sw.LoadFromFile(sFileName)
  sw.MIMEType = config.AppObject.GetMIMETypeFromExtension(sFileName)

  return 1

