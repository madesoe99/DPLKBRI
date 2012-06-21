import sys
import com.ihsan.util.modman as modman

#moduleapi = modman.getModule(config, 'moduleapi')

NOCOL = 30
PAKETCOL = 400
NILAIRPCOL = 150
PERSENCOL = 30
NILAICOL = NILAIRPCOL + PERSENCOL
NILAIPESCOL = 90
TABLEWIDTH = NOCOL + PAKETCOL + NILAICOL + NILAIPESCOL + NILAIRPCOL

NBOFCOLUMNS = 6

def ConstructReportHeader(config, dtDate, oFile):
  strDate = config.FormatDateTime('d mmmm yyyy', dtDate)

  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Laporan Paket Investasi</title>\n')
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Arial; line-height:100%; margin-top:0; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')

  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="'+ str(TABLEWIDTH) +'" id="table1" cellpadding="2">\n')

  oFile.write('	<tr>\n')
  oFile.write('		<td align="center" width="'+ str(TABLEWIDTH) +'" colspan="'+ str(NBOFCOLUMNS) +'" height="20" style="border-left:medium none #000000; border-right:medium none #000000; border-top-style:none; border-top-width:medium; border-bottom-style:none; border-bottom-width:medium">\n')
  oFile.write('		<font size="3" color="#008000"><b>Dana Pensiun Lembaga Keuangan PT. Bank Rakyat Indonesia, Tbk</b></font><br/>\n')
  oFile.write('		<font size="3" color="#008000"><b>Laporan Paket Investasi</b></font><br/></td>\n')
  oFile.write('	</tr>\n')

  oFile.write('	<tr>\n')
  oFile.write('		<td align="center" width="'+ str(TABLEWIDTH) +'" colspan="'+ str(NBOFCOLUMNS) +'" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font size="2" color="#008000"><b>Per '+ strDate +'</b><br/><br/></font></td>\n')
  oFile.write('	</tr>\n')

  oFile.write('	<tr>\n')
  oFile.write('		<td rowspan="2" width="'+ str(NOCOL) +'" align="center" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b><font size="2">No.</font></b></td>\n')

  oFile.write('		<td rowspan="2" width="'+ str(PAKETCOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Jenis/Paket Investasi</b></font></td>\n')

  oFile.write('		<td colspan="2" width="'+ str(NILAICOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Jumlah</b></font></td>\n')

  oFile.write('		<td rowspan="2" width="'+ str(NILAIPESCOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Jumlah<br/>Peserta</b></font></td>\n')

  oFile.write('		<td rowspan="2" width="'+ str(NILAIRPCOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Akumulasi Dana<br/>Peserta (Rp)</b></font></td>\n')
  oFile.write('	</tr>\n')

  oFile.write('	<tr>\n')
  oFile.write('		<td width="'+ str(NILAIRPCOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>Rp</b></font></td>\n')

  oFile.write('		<td width="'+ str(PERSENCOL) +'" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<font size="2"><b>%</b></font></td>\n')
  oFile.write('	</tr>\n')

def resSQLRincianPaketInv(config):
  strSQL = '\
    select \
      p.kode_paket_investasi, \
      nama_paket_investasi, \
      j.kode_jns_investasi, \
      nama_jns_investasi \
    from RincianPaketInvestasi r, JenisInvestasi j, PaketInvestasi p \
    where r.kode_jns_investasi = j.kode_jns_investasi \
      and r.kode_paket_investasi = p.kode_paket_investasi \
    order by p.kode_paket_investasi, j.kode_jns_investasi'

  return config.CreateSQL(strSQL).RawResult

def resSQLJumlahPesertaPaketInv(config, kode_paket_investasi, strNextDateSQL) :
  strSQL = '\
    select count(n.no_peserta) as Jum_Peserta \
    from nasabahdplk n, rekeningdplk r \
    where \
      n.no_peserta = r.no_peserta \
      and r.status_dplk = \'A\' \
    	and r.kode_paket_investasi = \'%s\' \
      and n.tgl_registrasi < %s ' \
    % (kode_paket_investasi, strNextDateSQL)
  return config.CreateSQL(strSQL).RawResult

def resSQLDanaPaketInv(config, kode_paket_investasi, strNextDateSQL) :
  strSQL = '\
    SELECT (SUM(ISNULL(T.MUTASI_IURAN_PST,0.0))+ \
         SUM(ISNULL(T.MUTASI_IURAN_PK,0.0))+ \
         SUM(ISNULL(T.MUTASI_PENGEMBANGAN,0.0)) + \
         SUM(ISNULL(T.MUTASI_PERALIHAN,0.0)) ) Jum_Dana \
    FROM TRANSAKSIDPLK T, REKENINGDPLK R \
    WHERE T.NO_PESERTA  = R.NO_PESERTA \
      AND T.ISCOMMITTED = \'T\' \
      AND R.STATUS_DPLK =  \'A\' \
      AND R.KODE_PAKET_INVESTASI = \'%s\' \
      AND T.TGL_TRANSAKSI < %s ' \
  % (kode_paket_investasi, strNextDateSQL)
  return config.CreateSQL(strSQL).RawResult


def resSQLNominalPaketInv(config, kode_paket_investasi, kode_jns_investasi, strNextDateSQL):
  strSQL = '\
    select mutasi_debet*proporsi mutasi_debet, mutasi_kredit*proporsi mutasi_kredit \
    from TransaksiInvestasi t, RincianInvestasi i \
    where t.id_investasi = i.id_investasi \
    	and isCommitted = \'T\' \
    	and clsfTransaksiInvestasi in (\'A\',\'D\') \
    	and i.kode_paket_investasi = \'%s\' \
    	and i.kode_jns_investasi = \'%s\' \
    	and tgl_transaksi < %s'\
    % (kode_paket_investasi, kode_jns_investasi, strNextDateSQL)
  #config.SendDebugMsg(strSQL)
  return config.CreateSQL(strSQL).RawResult

def WriteJenisInv(config, elmt, sumPaket, oFile):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  oFile.write('	<tr>\n')
  oFile.write('		<td width="'+ str(NOCOL) +'" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#FFFFFF">\n')
  oFile.write('		<font size="2">&nbsp;</td>\n')

  # nama jenis
  oFile.write('		<td width="'+ str(PAKETCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
  oFile.write('		<font size="2">  - '+ (elmt['jenis'] or '&nbsp;') +'</font></td>\n')

  # jumlah
  oFile.write('		<td width="'+ str(NILAICOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
  oFile.write('		<p align="right"><font size="2">'+ moduleapi.FormatFloatStd(config, elmt['nominal']) +'</font></td>\n')

  # persentase
  persentase = '-'
  if not moduleapi.IsApproxZero(sumPaket):
    persentase = config.FormatFloat('0.00', elmt['nominal'] * 100.0 / sumPaket) + '%'
    
  oFile.write('		<td width="'+ str(PERSENCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
  oFile.write('		<p align="right"><font size="2">'+ persentase +'</font></td>\n')

  # jumlah peserta
  oFile.write('		<td width="'+ str(NILAIPESCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
  oFile.write('		<p align="right"><font size="2">&nbsp;</font></td>\n')

  # akum dana peserta
  oFile.write('		<td width="'+ str(NILAICOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#FFFFFF">\n')
  oFile.write('		<p align="right"><font size="2">&nbsp;</font></td>\n')
  oFile.write('	</tr>\n')

def ConstructReportValues(config, dtDate, oFile):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  strNextDateSQL = config.FormatDateTimeForQuery(dtDate + 1)

  prevPaket = ''
  no_urut = 1
  sumPaket = 0.0
  sumTotPaket = 0.0

  sumJumPeserta = 0.0
  sumAkumDana = 0.0
  sumDanaPaket = 0.0
  
  lsPaketInv = []

  resSQLRPI = resSQLRincianPaketInv(config)
  resSQLRPI.First()
  while not resSQLRPI.Eof:

    if prevPaket != resSQLRPI.kode_paket_investasi:
      prevPaket = resSQLRPI.kode_paket_investasi

      #ambil data paket di liability
      rSQLJPPI = resSQLJumlahPesertaPaketInv(config, prevPaket,strNextDateSQL)
      sumJumPeserta += (rSQLJPPI.jum_peserta or 0)
      rSQLDPI = resSQLDanaPaketInv(config, prevPaket,strNextDateSQL)
      sumAkumDana += (rSQLDPI.Jum_dana or 0.0)
      # tambahkan penjumlahan paket sebelumnya ke total paket
      sumTotPaket += sumPaket

      # tulis nilai2 paket sebelumnya (jika ada)
      for elmt in lsPaketInv:
        #WriteJenisInv(config, elmt, sumPaket, oFile)
        WriteJenisInv(config, elmt, sumDanaPaket, oFile)
        
      # masukan ke list nilai2 paket ini
      nominal = 0.0
      resSQLNPI = resSQLNominalPaketInv(config, resSQLRPI.kode_paket_investasi, resSQLRPI.kode_jns_investasi, strNextDateSQL)
      while not resSQLNPI.Eof:
        nominal += (resSQLNPI.mutasi_debet or 0.0) - (resSQLNPI.mutasi_kredit or 0.0)

        resSQLNPI.Next()

      lsPaketInv = []
      lsPaketInv.append({
        'jenis': resSQLRPI.nama_jns_investasi
        , 'nominal': nominal
      })
      sumPaket = nominal
      # tulis paket yang ini
      oFile.write('	<tr>\n')
      oFile.write('		<td width="'+ str(NOCOL) +'" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#EFEFEF">\n')
      oFile.write('		<font size="2">'+ str(no_urut) +'</td>\n')
      oFile.write('		<td width="'+ str(PAKETCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#EFEFEF">\n')
      oFile.write('		<font size="2">'+ (resSQLRPI.nama_paket_investasi or '&nbsp;') +'</font></td>\n')
      oFile.write('		<td width="'+ str(NILAICOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#EFEFEF">\n')
      oFile.write('		<p align="right"><font size="2">&nbsp;</font></td>\n')
      oFile.write('		<td width="'+ str(PERSENCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#EFEFEF">\n')
      oFile.write('		<p align="right"><font size="2">&nbsp;</font></td>\n')
      oFile.write('		<td width="'+ str(NILAIPESCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#EFEFEF">\n')
      oFile.write('		<p align="right"><font size="2">'+ config.FormatFloat('#,##0',float(rSQLJPPI.jum_peserta or 0.0)) +'</font></td>\n')
      oFile.write('		<td width="'+ str(NILAICOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#EFEFEF">\n')
      oFile.write('		<p align="right"><font size="2">'+ moduleapi.FormatFloatStd(config, (rSQLDPI.Jum_dana or 0.0)) +'</font></td>\n')
      oFile.write('	</tr>\n')
      
      sumDanaPaket = (rSQLDPI.Jum_dana or 0.0)
      no_urut += 1

    else:
      # paket masih sama dengan sebelumnya
      # tambahkan jenis investasi dan nilainya ke list

      nominal = 0.0
      resSQLNPI = resSQLNominalPaketInv(config, resSQLRPI.kode_paket_investasi, resSQLRPI.kode_jns_investasi, strNextDateSQL)
      while not resSQLNPI.Eof:
        nominal += (resSQLNPI.mutasi_debet or 0.0) - (resSQLNPI.mutasi_kredit or 0.0)

        resSQLNPI.Next()

      lsPaketInv.append({
        'jenis': resSQLRPI.nama_jns_investasi
        , 'nominal': nominal
      })

      sumPaket += nominal
      prevPaket = resSQLRPI.kode_paket_investasi

    # end if prevPaket != resSQLRPI.kode_paket_investasi

    resSQLRPI.Next()
  # end while resSQLRPI.Eof

  # EOF, catat paket yang terakhir

  # tambahkan penjumlahan paket sebelumnya ke total paket
  sumTotPaket += sumPaket

  # tulis nilai2 paket sebelumnya (jika ada)
  for elmt in lsPaketInv:
    #WriteJenisInv(config, elmt, sumPaket, oFile)
    WriteJenisInv(config, elmt, sumDanaPaket, oFile)

  return sumTotPaket,sumJumPeserta,sumAkumDana

def ConstructReportTrailer(config, sumTotPaket, sumJumPeserta, sumAkumDana, oFile):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  oFile.write('	<tr>\n')
  oFile.write('		<td width="'+ str(NOCOL) +'" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		&nbsp;</td>\n')
  oFile.write('		<td width="'+ str(PAKETCOL) +'" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<p align="left"><b><font size="2">Total</font></b></td>\n')

  oFile.write('		<td width="'+ str(NILAICOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<p align="right"><font size="2">'+ moduleapi.FormatFloatStd(config, sumTotPaket) +'</font></td>\n')

  oFile.write('		<td width="'+ str(PERSENCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<p align="right"><font size="2">&nbsp;</font></td>\n')

  oFile.write('		<td width="'+ str(NILAIPESCOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<p align="right"><font size="2">'+config.FormatFloat('#,##0',sumJumPeserta)+'</font></td>\n')

  oFile.write('		<td width="'+ str(NILAICOL) +'" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<p align="right"><font size="2">'+moduleapi.FormatFloatStd(config, (sumAkumDana or 0.0))+'</font></td>\n')

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

  sBaseFileName = 'paket_investasi.htm'
  sFileName = config.UserHomeDirectory + sBaseFileName
  oFile = open(sFileName, 'w')

  ConstructReportHeader(config, dtDate, oFile)
  sumTotPaket, sumJumPeserta, sumAkumDana = ConstructReportValues(config, dtDate, oFile)
  ConstructReportTrailer(config, sumTotPaket, sumJumPeserta, sumAkumDana, oFile)

  oFile.close()

  recRes = returnpacket.CreateDataPacketStructure('filename:string')
  recRes.filename = sBaseFileName
  
  #tambahan 
  sw = returnpacket.AddStreamWrapper()
  sw.LoadFromFile(sFileName)
  sw.MIMEType = config.AppObject.GetMIMETypeFromExtension(sFileName)

  return 1

