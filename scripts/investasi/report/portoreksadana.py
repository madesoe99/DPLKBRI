import sys
import com.ihsan.util.modman as modman

NOCOL = 30
NAMACOL = 250
PENERBITCOL = 200
NABCOL = 100
UNITCOL = 100
RPCOL = 150
NILAICOL = NABCOL + UNITCOL + RPCOL
TABLEWIDTH = NOCOL + NAMACOL + PENERBITCOL + NILAICOL + NILAICOL

NBOFCOLUMNS = 1 + 1 + 1 + 3 + 3

def ConstructReportHeader(config, dtDate, oFile):
  strDate = config.FormatDateTime('d mmmm yyyy', dtDate)

  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Laporan Portofolio Investasi Reksadana</title>\n')
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Arial; line-height:100%; margin-top:0; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')

  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="'+ str(TABLEWIDTH) +'" id="table1" cellpadding="2">\n')

  oFile.write('	<tr>\n')
  oFile.write('		<td align="center" colspan="'+ str(NBOFCOLUMNS) +'" height="20" style="border-left:medium none #000000; border-right:medium none #000000; border-top-style:none; border-top-width:medium; border-bottom-style:none; border-bottom-width:medium">\n')
  oFile.write('		<font size="3" color="#008000"><b>Dana Pensiun Lembaga Keuangan PT. Bank Rakyat Indonesia, Tbk</b></font><br/>\n')
  oFile.write('		<font size="3" color="#008000"><b>Laporan Portofolio Investasi</b></font><br/>\n')
  oFile.write('		<font size="3" color="#008000"><b>UNIT PENYERTAAN REKSA DANA & UNIT PENYERTAAN DANA INVESTASI REAL ESTATE BERBENTUK KIK</b></font><br/>\n')
  oFile.write('	</tr>\n')

  oFile.write('	<tr>\n')
  oFile.write('		<td align="center" width="'+ str(TABLEWIDTH) +'" colspan="'+ str(NBOFCOLUMNS) +'" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2" color="#008000"><b>Per '+ strDate +'</b><br/><br/></font></td>\n')
  oFile.write('	</tr>\n')

  oFile.write('	<tr>\n')

  # no urut
  oFile.write('		<td rowspan="2" width="'+ str(NOCOL) +'" align="center" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b><font size="2">No.</font></b></td>\n')

  # nama produk
  oFile.write('		<td rowspan="2" width="'+ str(NAMACOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Nama Produk</b></font></td>\n')

  # nama penerbit
  oFile.write('		<td rowspan="2" width="'+ str(PENERBITCOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Nama Penerbit</b></font></td>\n')

  # nilai perolehan
  oFile.write('		<td colspan="3" width="'+ str(NILAICOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Nilai Perolehan</b></font></td>\n')

  # nilai wajar
  oFile.write('		<td colspan="3" width="'+ str(NILAICOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Nilai Wajar</b></font></td>\n')

  oFile.write('	</tr>\n')

  oFile.write('	<tr>\n')

  # NAB
  oFile.write('		<td width="'+ str(NABCOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>NAB</b></font></td>\n')

  # unit
  oFile.write('		<td width="'+ str(UNITCOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Unit</b></font></td>\n')

  # total rp
  oFile.write('		<td width="'+ str(RPCOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Total (Rp)</b></font></td>\n')

  # NAB
  oFile.write('		<td width="'+ str(NABCOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>NAB</b></font></td>\n')

  # unit
  oFile.write('		<td width="'+ str(UNITCOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Unit</b></font></td>\n')

  # total rp
  oFile.write('		<td width="'+ str(RPCOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Total (Rp)</b></font></td>\n')

  oFile.write('	</tr>\n')

def resSQLJenisReks(config):
  strSQL = '\
    select kode_jns_reksadana, jenis_reksadana \
    from JenisReksadana \
    order by kode_jns_reksadana'
  strSQL = 'select kode_jns_reksadana, jenis_reksadana \
    from JenisReksadana where kode_jns_reksadana = \'RDC\''
  return config.CreateSQL(strSQL).RawResult

def resSQLReksadana(config, kode_jns_reksadana, strNextDateSQL):
  strSQL = '\
    select \
    	nama_reksadana \
    	, NAB_Transaksi \
    	, unit_penyertaan \
    	, NAB \
    from Reksadana r, Investasi i \
    where status = \'T\' \
    	and r.id_investasi = i.id_investasi \
    	and kode_jns_reksadana = \'%s\' \
    	and tgl_buka < %s'\
    % (kode_jns_reksadana, strNextDateSQL)
    
  strSQL = '\
    select \
    	nama_reksadana \
    	, NAB_Transaksi \
    	, unit_penyertaan \
    	, NAB \
    	, nama_pihak_ketiga \
    	, i.id_investasi \
    from Reksadana r, Investasi i,pihakketiga p \
    where status = \'T\' \
      and i.kode_pihak_ketiga = p.kode_pihak_ketiga \
    	and r.id_investasi = i.id_investasi \
    	and kode_jns_reksadana in (\'RDPT\',\'RDS\',\'RDC\') \
    	and tgl_buka < %s'\
    % (strNextDateSQL)
  return config.CreateSQL(strSQL).RawResult

#Tambahan By Ade Herman 2011-04-07
def resSQLReksadanaTutup(config, kode_jns_reksadana, strNextDateSQL):
  strSQL = '\
    select \
    	nama_reksadana \
    	, NAB_Transaksi \
    	, unit_penyertaan \
    	, NAB \
    from Reksadana r, Investasi i \
    where status = \'F\' \
    	and r.id_investasi = i.id_investasi \
    	and kode_jns_reksadana = \'%s\' \
    	and tgl_buka < %s'\
    % (kode_jns_reksadana, strNextDateSQL)

  strSQL = '\
    select \
    	nama_reksadana \
    	, NAB_Transaksi \
    	, unit_penyertaan \
    	, NAB \
    	, nama_pihak_ketiga \
    	, i.id_investasi \
    from Reksadana r, Investasi i,pihakketiga p \
    where status = \'F\' \
      and i.kode_pihak_ketiga = p.kode_pihak_ketiga \
    	and r.id_investasi = i.id_investasi \
    	and kode_jns_reksadana in (\'RDPT\',\'RDS\',\'RDC\') \
    	and tgl_buka < %s'\
    % (strNextDateSQL)
  return config.CreateSQL(strSQL).RawResult

#End Tambahan By Ade Herman 2011-04-07

def akumDataPembelian(config,id_investasi, strNextDateSQL) :
  strSQL = '\
    select \
    	sum(unit_penyertaan) up \
    	, sum(mutasi_debet-mutasi_kredit) nilai \
    from SubscribeReksadana s, TransaksiInvestasi i \
    where isCommitted in (\'T\') \
    	and s.id_transaksiinvestasi = i.id_transaksiinvestasi \
    	and i.id_investasi = %s \
    	and tgl_transaksi < %s'\
    % (id_investasi,strNextDateSQL)
  resS = config.CreateSQL(strSQL).RawResult

  strSQL = '\
    select \
    	sum(unit_penyertaan) up \
    	, sum(nominal_jual-profit) nilai \
    from RedemptReksadana r, TransaksiInvestasi i \
    where isCommitted in (\'T\') \
    	and r.id_transaksiinvestasi = i.id_transaksiinvestasi \
    	and i.id_investasi = %s \
    	and tgl_transaksi < %s'\
    % (id_investasi,strNextDateSQL)
  resR = config.CreateSQL(strSQL).RawResult

  return [(resS.up or 0.0)-(resR.up or 0.0),(resS.nilai or 0.0)-(resR.nilai or 0.0)]

def NABSekarang(config, id_investasi, strNextDateSQL) :
  strSQL = '\
    select \
    	HistNABReksadanaID, NAB \
    from HistNABReksadana h \
    where h.id_investasi = %s \
      and terminaloto <> \'1\' \
    	and tgl_penetapan < %s \
    order by HistNABReksadanaID desc '\
    % (id_investasi,strNextDateSQL)
  return config.CreateSQL(strSQL).RawResult


def WriteTotalJenis(config, jenis_reksadana, sumUnit, sumTotalrpPer, sumTotalrpWjr, oFile):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  oFile.write('	<tr>\n')

  # no urut
  oFile.write('		<td width="'+ str(NOCOL) +'" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#FFFFFF">\n')
  oFile.write('		<font size="2">&nbsp;</td>\n')

  # nama produk
  oFile.write('		<td width="'+ str(NAMACOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
  oFile.write('		<font size="2">Total '+ (jenis_reksadana or '&nbsp;') +'</font></td>\n')

  # nama penerbit
  oFile.write('		<td width="'+ str(PENERBITCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
  oFile.write('		<font size="2">&nbsp;</font></td>\n')

  # NAB (perolehan)
  oFile.write('		<td align="right" width="'+ str(NABCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
  oFile.write('		<font size="2">&nbsp;</font></td>\n')

  # unit (perolehan)
  oFile.write('		<td align="right" width="'+ str(UNITCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
  oFile.write('		<font size="2">'+ moduleapi.FormatFloatStd(config, sumUnit) +'</font></td>\n')

  # total rp (perolehan)
  oFile.write('		<td align="right" width="'+ str(RPCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
  oFile.write('		<font size="2">'+ moduleapi.FormatFloatStd(config, sumTotalrpPer) +'</font></td>\n')

  # NAB (wajar)
  oFile.write('		<td align="right" width="'+ str(NABCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
  oFile.write('		<font size="2">&nbsp;</font></td>\n')

  # unit (wajar)
  oFile.write('		<td align="right" width="'+ str(UNITCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
  oFile.write('		<font size="2">'+ moduleapi.FormatFloatStd(config, sumUnit) +'</font></td>\n')

  # total rp (wajar)
  oFile.write('		<td align="right" width="'+ str(RPCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
  oFile.write('		<font size="2">'+ moduleapi.FormatFloatStd(config, sumTotalrpWjr) +'</font></td>\n')

  oFile.write('	</tr>\n')

def ConstructReportValues(config, dtDate, oFile):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  strNextDateSQL = config.FormatDateTimeForQuery(dtDate + 1)
  strNextNAB = config.FormatDateTimeForQuery(dtDate)

  noUrut = 1

  resJR = resSQLJenisReks(config) 
  while not resJR.Eof:

    sumUnit = 0.0

    sumTotalrpPer = 0.0
    sumTotalrpWjr = 0.0

    res = resSQLReksadana(config, resJR.kode_jns_reksadana, strNextDateSQL)
    
    if not res.Eof:
      jenis_reksadana = 'Reksa Dana Pasar Uang, Reksa Dana Pendapatan Tetap, Reksadana Saham dan Reksa Dana Campuran'
      # catat jenis reksadana
      oFile.write('	<tr>\n')
      # no urut
      #oFile.write('		<td width="'+ str(NOCOL) +'" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#EFEFEF">\n')
      oFile.write('		<td width="'+ str(NOCOL) +'" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#FFFFFF">\n')
      oFile.write('		<font size="2">'+ str(noUrut) +'</td>\n')

      # nama produk
      #oFile.write('		<td colspan="'+ str(NBOFCOLUMNS - 1) +'" width="'+ str(TABLEWIDTH - NOCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#EFEFEF">\n')
      oFile.write('		<td width="'+ str(NAMACOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
      #oFile.write('		<font size="2">'+ (resJR.jenis_reksadana or '&nbsp;') +'</font></td>\n')
      oFile.write('		<font size="2">'+ (jenis_reksadana or '&nbsp;') +'</font></td>\n')
      #oFile.write('	</tr>\n')

      #tambahan Haris
      # nama penerbit
      oFile.write('		<td width="'+ str(PENERBITCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
      oFile.write('		<font size="2">&nbsp;</font></td>\n')

      # NAB (perolehan)
      oFile.write('		<td align="right" width="'+ str(NABCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
      oFile.write('		<font size="2">&nbsp;</font></td>\n')

      # unit (perolehan)
      oFile.write('		<td align="right" width="'+ str(UNITCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
      oFile.write('		<font size="2">&nbsp;</font></td>\n')

      # total rp (perolehan)
      oFile.write('		<td align="right" width="'+ str(RPCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
      oFile.write('		<font size="2">&nbsp;</font></td>\n')

      # NAB (wajar)
      oFile.write('		<td align="right" width="'+ str(NABCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
      oFile.write('		<font size="2">&nbsp;</font></td>\n')

      # unit (wajar)
      oFile.write('		<td align="right" width="'+ str(UNITCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
      oFile.write('		<font size="2">&nbsp;</font></td>\n')

      # total rp (wajar)
      oFile.write('		<td align="right" width="'+ str(RPCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
      oFile.write('		<font size="2">&nbsp;</font></td>\n')

      oFile.write('	</tr>\n')
      #end tambahan

      while not res.Eof:
        #unit = res.unit_penyertaan or 0.0
        
        #NAB_awal = res.NAB_transaksi or 0.0
        #totalrpper = NAB_awal * unit
        #unit,totalrpper  = akumDataPembelian(config, res.id_investasi, strNextDateSQL)
        unit,totalrpper  = akumDataPembelian(config, res.id_investasi, strNextNAB)
        NAB_awal = totalrpper/unit
        
        #NAB_trans = res.NAB or 0.0
        #NAB_trans = NABSekarang(config, res.id_investasi, strNextDateSQL).NAB
        NAB_trans = NABSekarang(config, res.id_investasi, strNextNAB).NAB
        totalrpwjr = NAB_trans * unit

        oFile.write('	<tr>\n')
        # no urut
        noUrut += 1
        oFile.write('		<td width="'+ str(NOCOL) +'" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#FFFFFF">\n')
        oFile.write('		<font size="2">'+str(noUrut)+'</td>\n')

        # nama produk
        oFile.write('		<td width="'+ str(NAMACOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
        oFile.write('		<font size="2">'+ (res.nama_reksadana or '&nbsp;') +'</font></td>\n')

        # nama penerbit
        oFile.write('		<td width="'+ str(PENERBITCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
        oFile.write('		<font size="2">'+(res.nama_pihak_ketiga or '&nbsp;')+'</font></td>\n')

        # NAB (perolehan)
        oFile.write('		<td align="right" width="'+ str(NABCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
        oFile.write('		<font size="2">'+ moduleapi.FormatFloatExtStd(config, NAB_awal) +'</font></td>\n')

        # unit (perolehan)
        oFile.write('		<td align="right" width="'+ str(UNITCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
        oFile.write('		<font size="2">'+ moduleapi.FormatFloatStd(config, unit) +'</font></td>\n')

        # total rp (perolehan)
        oFile.write('		<td align="right" width="'+ str(RPCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
        oFile.write('		<font size="2">'+ moduleapi.FormatFloatStd(config, totalrpper) +'</font></td>\n')

        # NAB (wajar)
        oFile.write('		<td align="right" width="'+ str(NABCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
        oFile.write('		<font size="2">'+ moduleapi.FormatFloatExtStd(config, NAB_trans) +'</font></td>\n')

        # unit (wajar)
        oFile.write('		<td align="right" width="'+ str(UNITCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
        oFile.write('		<font size="2">'+ moduleapi.FormatFloatExtStd(config, unit) +'</font></td>\n')

        # total rp (wajar)
        oFile.write('		<td align="right" width="'+ str(RPCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
        oFile.write('		<font size="2">'+ moduleapi.FormatFloatExtStd(config, totalrpwjr) +'</font></td>\n')

        oFile.write('	</tr>\n')

        sumUnit += unit

        sumTotalrpPer += totalrpper
        sumTotalrpWjr += totalrpwjr

        res.Next()
        

    #Tambahan By Ade Herman 2011-04-07
    #res = resSQLReksadanaTutup(config, resJR.kode_jns_reksadana, strNextDateSQL)
    

        #End Tambahan By Ade Herman 2011-04-07
        
      # end while not res.Eof

      #WriteTotalJenis(config, resJR.jenis_reksadana, sumUnit, sumTotalrpPer, sumTotalrpWjr, oFile)
      WriteTotalJenis(config, jenis_reksadana, sumUnit, sumTotalrpPer, sumTotalrpWjr, oFile)

    # end if not res.Eof

    resJR.Next()
    
  # end while not resJR.Eof

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

  sBaseFileName = 'portofolio_reksadana.htm'
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

