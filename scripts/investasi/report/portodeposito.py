import sys
import com.ihsan.util.modman as modman

NOCOL = 30
SUBCOL = 30
PIHAKCOL = 340
NOMDEP = 100
NOMBIL = 100
TGLCOL = 100
NILAICOL = 150
WAKTUCOL = 70
NISBAHCOL = 70
TABLEWIDTH = NOCOL + SUBCOL + PIHAKCOL + NOMDEP + NOMBIL + TGLCOL + NILAICOL + NILAICOL + TGLCOL + WAKTUCOL + NISBAHCOL + NISBAHCOL

NBOFCOLUMNS = 12

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

  oFile.write('		<td width="'+ str(SUBCOL) +'" align="center" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b><font size="2">Sub No.</font></b></td>\n')

  oFile.write('		<td width="'+ str(PIHAKCOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Nama Bank</b></font></td>\n')

  oFile.write('		<td width="'+ str(NOMDEP) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Nomor Deposito</b></font></td>\n')

  oFile.write('		<td width="'+ str(NOMBIL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Nomor Bilyet</b></font></td>\n')

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
  
  oFile.write('		<td width="'+ str(NISBAHCOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Ekv Rate</b></font></td>\n')
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
      d.rekening_deposito \
      , i.no_bilyet \
    	, i.id_investasi \
    	, tgl_buka \
    	, tgl_jatuh_tempo \
    	, jmlHariOnCall as jangkaWaktu \
    	, nisbah \
    	, equivalent_rate \
    from Deposito d, Investasi i \
    where status = \'T\' \
      and d.id_investasi = i.id_investasi \
    	and jenisJatuhTempo = 0 \
    	and kode_pihak_ketiga = \'%s\' \
    	and tgl_buka < %s '\
    % (kode_pihak_ketiga, strNextDateSQL)
    
  config.SendDebugMsg('resSQLDepOnCall='+strSQL)
  return config.CreateSQL(strSQL).RawResult
  #status = \'T\' \

## Tambahan By Ade Herman 2011-04-06
def resSQLDepOnCallTutup(config, kode_pihak_ketiga, strNextDateSQL):
  strSQL = '\
    select \
        d.rekening_deposito \
      , i.no_bilyet \
    	, i.id_investasi \
    	, tgl_buka \
    	, tgl_jatuh_tempo \
    	, jmlHariOnCall as jangkaWaktu \
    	, nisbah \
    	, equivalent_rate \
    from Deposito d, Investasi i \
    where status = \'F\' \
      and d.id_investasi = i.id_investasi \
    	and jenisJatuhTempo = 0 \
    	and kode_pihak_ketiga = \'%s\' \
    	and (tgl_buka < %s \
   	  and  tgl_tutup > %s )' \
    % (kode_pihak_ketiga, strNextDateSQL, strNextDateSQL)

  config.SendDebugMsg('resSQLDepOnCall='+strSQL)
  return config.CreateSQL(strSQL).RawResult
## End Tambahan By Ade Herman 2011-04-06

def resSQLDepBjangka(config, kode_pihak_ketiga, strNextDateSQL):
  strSQL = '\
    select \
        d.rekening_deposito \
      , i.no_bilyet \
    	, i.id_investasi \
    	, tgl_buka \
    	, tgl_jatuh_tempo \
    	, jenisJatuhTempo as jangkaWaktu \
    	, nisbah \
    	, equivalent_rate \
    from Deposito d, Investasi i \
    where status = \'T\' \
     and d.id_investasi = i.id_investasi \
     and jenisJatuhTempo > 0 \
    	and kode_pihak_ketiga = \'%s\' \
    	and tgl_buka < %s ;'\
    % (kode_pihak_ketiga, strNextDateSQL)
    
  config.SendDebugMsg('resSQLDepBjangka='+strSQL)
  return config.CreateSQL(strSQL).RawResult


## Tambahan By Ade Herman 2011-04-06
def resSQLDepBjangkaTutup(config, kode_pihak_ketiga, strNextDateSQL):
  strSQL = '\
    select \
        d.rekening_deposito \
      , i.no_bilyet \
    	, i.id_investasi \
    	, tgl_buka \
    	, tgl_jatuh_tempo \
    	, jenisJatuhTempo as jangkaWaktu \
    	, nisbah \
    	, equivalent_rate \
    from Deposito d, Investasi i \
    where status = \'F\' \
     and d.id_investasi = i.id_investasi \
     and jenisJatuhTempo > 0 \
    	and kode_pihak_ketiga = \'%s\' \
    	and (tgl_buka < %s \
    	and tgl_tutup > %s );'\
    % (kode_pihak_ketiga, strNextDateSQL, strNextDateSQL)

  config.SendDebugMsg('resSQLDepBjangka='+strSQL)
  return config.CreateSQL(strSQL).RawResult
## End Tambahan By Ade Herman 2011-04-06

def resSQLDeposito(config, isBerjangka, kode_pihak_ketiga, strNextDateSQL):
  config.SendDebugMsg('masuk..........A')
  if isBerjangka:
    return resSQLDepBjangka(config, kode_pihak_ketiga, strNextDateSQL)
  else:
    # on call
    return resSQLDepOnCall(config, kode_pihak_ketiga, strNextDateSQL)

## Tambahan By Ade Herman 2011-04-06
def resSQLDepositoTutup(config, isBerjangka, kode_pihak_ketiga, strNextDateSQL):
  config.SendDebugMsg('masuk..........A')
  if isBerjangka:
    return resSQLDepBjangkaTutup(config, kode_pihak_ketiga, strNextDateSQL)
  else:
    # on call
    return resSQLDepOnCallTutup(config, kode_pihak_ketiga, strNextDateSQL)
## End Tambahan By Ade Herman 2011-04-06

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
  config.SendDebugMsg('resSQLMutasi='+strSQL)
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
  oFile.write('		<td colspan="2" width="'+ str(PIHAKCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
  oFile.write('		<font size="2"><b>Total '+ jenisDep +'</b></font></td>\n')

  # nOMOR DEPOSITO
  oFile.write('		<td width="'+ str(NOMDEP) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
  oFile.write('		<font size="2">&nbsp;</font></td>\n')

  # nOMOR bILYET
  oFile.write('		<td width="'+ str(NOMBIL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
  oFile.write('		<font size="2">&nbsp;</font></td>\n')

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

  # equivalent rate
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
  
    ## Rincian deposito Aktif
    config.SendDebugMsg('Rincian deposito Aktif..........')
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
      #oFile.write('		<td width="'+ str(PIHAKCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
      #oFile.write('		<font size="2">'+ str(noUrut) +'. '+ (resPK.nama_pihak_ketiga or '&nbsp;') +'</font></td>\n')

      oFile.write('		<td width="'+ str(SUBCOL) +'" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#FFFFFF">\n')
      oFile.write('		<font size="2">'+ str(noUrut) +'</font></td>\n')

      oFile.write('		<td width="'+ str(PIHAKCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
      oFile.write('		<font size="2">'+ (resPK.nama_pihak_ketiga or '&nbsp;') +'</font></td>\n')

      # nOMOR DEPOSITO
      oFile.write('		<td width="'+ str(NOMDEP) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
      oFile.write('		<font size="2">'+ str(resDep.rekening_deposito or '&nbsp;') +'</font></td>\n')

      # nOMOR bILYET
      oFile.write('		<td width="'+ str(NOMBIL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
      oFile.write('		<font size="2">'+ str(resDep.no_bilyet or '&nbsp;') +'</font></td>\n')

      # tgl penempatan
      oFile.write('		<td align="center" width="'+ str(TGLCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
      oFile.write('		<font size="2">'+ config.FormatDateTime('d-mmm-yy', moduleapi.DateTimeTupleToFloat(config, resDep.tgl_buka)) +'</font></td>\n')

      # nominal
      oFile.write('		<td align="right" width="'+ str(NILAICOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
      oFile.write('		<font size="2">'+ moduleapi.FormatFloatStd(config, nominal) +'</font></td>\n')

      config.SendDebugMsg('masuk..........05='+str(resDep.tgl_jatuh_tempo))
      # nominal dlm mata uang asing
      oFile.write('		<td align="right" width="'+ str(NILAICOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
      oFile.write('		<font size="2">-</font></td>\n')

      # tgl jatuh tempo
      if resDep.tgl_jatuh_tempo <> None:
        tgljt = config.FormatDateTime('d-mmm-yy', moduleapi.DateTimeTupleToFloat(config, resDep.tgl_jatuh_tempo)) 
      else:
        tgljt = ''
      oFile.write('		<td align="center" width="'+ str(TGLCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
      oFile.write('		<font size="2">'+ tgljt +'</font></td>\n')

      config.SendDebugMsg('masuk..........06')
      # jangka waktu
      oFile.write('		<td align="center" width="'+ str(WAKTUCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
      oFile.write('		<font size="2">'+ str(resDep.jangkaWaktu) +' '+ waktu +'</font></td>\n')

      config.SendDebugMsg('masuk..........07')
      # nisbah (%)
      oFile.write('		<td align="right" width="'+ str(NISBAHCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
      oFile.write('		<font size="2">'+ config.FormatFloat('0.00', resDep.nisbah) +'%</font></td>\n')

      # equivalent rate
      oFile.write('		<td align="right" width="'+ str(NISBAHCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
      oFile.write('		<font size="2">'+ config.FormatFloat('0.00', resDep.equivalent_rate or 0.0) +'</font></td>\n')

      oFile.write('	</tr>\n')
      config.SendDebugMsg('masuk..........08')
      ##

      noUrut += 1
      

      resDep.Next()

    # end while not resDep.Eof
    
    ## Tambahan By Ade Herman 2011-04-06
    ## Rincian deposito Tutup
    config.SendDebugMsg('Rincian Deposito Tutup.........')
    resDep = resSQLDepositoTutup(config, isBerjangka, resPK.kode_pihak_ketiga, strNextDateSQL)
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

      # nOMOR DEPOSITO
      oFile.write('		<td width="'+ str(NOMDEP) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
      oFile.write('		<font size="2">'+ (resDep.rekening_deposito or '&nbsp;') +'</font></td>\n')

      # nOMOR bILYET
      oFile.write('		<td width="'+ str(NOMBIL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
      oFile.write('		<font size="2">'+ (resDep.no_bilyet or '&nbsp;') +'</font></td>\n')

      # tgl penempatan
      oFile.write('		<td align="center" width="'+ str(TGLCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
      oFile.write('		<font size="2">'+ config.FormatDateTime('d-mmm-yy', moduleapi.DateTimeTupleToFloat(config, resDep.tgl_buka)) +'</font></td>\n')

      # nominal
      oFile.write('		<td align="right" width="'+ str(NILAICOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
      oFile.write('		<font size="2">'+ moduleapi.FormatFloatStd(config, nominal) +'</font></td>\n')

      config.SendDebugMsg('masuk..........05='+str(resDep.tgl_jatuh_tempo))
      # nominal dlm mata uang asing
      oFile.write('		<td align="right" width="'+ str(NILAICOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
      oFile.write('		<font size="2">-</font></td>\n')

      # tgl jatuh tempo
      if resDep.tgl_jatuh_tempo <> None:
        tgljt = config.FormatDateTime('d-mmm-yy', moduleapi.DateTimeTupleToFloat(config, resDep.tgl_jatuh_tempo))
      else:
        tgljt = ''
      oFile.write('		<td align="center" width="'+ str(TGLCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
      oFile.write('		<font size="2">'+ tgljt +'</font></td>\n')

      config.SendDebugMsg('masuk..........06')
      # jangka waktu
      oFile.write('		<td align="center" width="'+ str(WAKTUCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
      oFile.write('		<font size="2">'+ str(resDep.jangkaWaktu) +' '+ waktu +'</font></td>\n')

      config.SendDebugMsg('masuk..........07')
      # nisbah (%)
      oFile.write('		<td align="right" width="'+ str(NISBAHCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
      oFile.write('		<font size="2">'+ config.FormatFloat('0.00', resDep.nisbah) +'%</font></td>\n')

      # equivalent rate
      oFile.write('		<td align="right" width="'+ str(NISBAHCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
      oFile.write('		<font size="2">'+ config.FormatFloat('0.00', resDep.equivalent_rate or 0.0) +'</font></td>\n')

      oFile.write('	</tr>\n')
      config.SendDebugMsg('masuk..........08')
      ##

      noUrut += 1
      resDep.Next()
      ## End Tambahan By Ade Herman 2011-04-06

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
