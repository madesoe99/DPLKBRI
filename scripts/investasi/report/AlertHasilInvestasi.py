import sys
import string
import calendar
import com.ihsan.util.modman as modman

sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi

def ConstructReportHeader(config, strTanggalAwal, strTanggalAkhir, oFile):
  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Laporan Perolehan Peserta</title>\n')
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Arial; line-height:100%; margin-top:0; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td colspan="8" height="20" style="border-left:medium none #000000; border-right:medium none #000000; border-top-style:none; border-top-width:medium; border-bottom-style:none; border-bottom-width:medium">\n')
  oFile.write('		<p align="center"><font size="3" color="#008000"><b>ALERT HASIL INVESTASI</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" colspan="11" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font color="#008000"><b>PERIODE '+ string.upper(strTanggalAwal) +' HINGGA '+ string.upper(strTanggalAkhir) +'</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="3%" align="center" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>NO</b></td>\n')
  oFile.write('		<td width="7%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>KODE PIHAK III</b></td>\n')
  oFile.write('		<td width="18%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>NAMA PIHAK III</b></td>\n')
  oFile.write('		<td width="7%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>NO BILYET</b></td>\n')
  oFile.write('		<td width="7%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>REKENING DEPOSITO</b></td>\n')
  oFile.write('		<td width="9%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>TGL BUKA</b></td>\n')
  oFile.write('		<td width="9%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>TGL TUTUP</b></td>\n')
  oFile.write('		<td width="9%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>TGL JATUH TEMPO</b></td>\n')
  oFile.write('		<td width="9%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>NOMINAL PEMBUKAAN</b></td>\n')
  oFile.write('		<td width="9%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>TGL BAG HAS</b></td>\n')
  oFile.write('		<td width="9%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>HASIL INVESTASI</b></td>\n')
  oFile.write('		<td width="9%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>NISBAH</b></td>\n')
  oFile.write('		<td width="9%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>ER</b></td>\n')
  oFile.write('		<td width="9%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>INVESTASI MANUAL</b></td>\n')
  oFile.write('		<td width="9%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>JENIS DEPO</b></td>\n')
  oFile.write('	</tr>\n')

def strSQLPihakKetiga(config, kode_pihak_ketiga):
  return \
    'select nama_pihak_ketiga '\
    '  from pihakketiga '\
    '  where kode_pihak_ketiga = \'%s\' ;'\
    % (kode_pihak_ketiga)
  
#--- New
def strSQLHasilInvestasi(config, tgl_transaksi_awal, tgl_transaksi_akhir_plus):
  return \
     ' select ti.tgl_transaksi '\
     '      ,ti.clsfTransaksiInvestasi '\
     '      ,ti.mutasi_kredit '\
     '      ,ti.mutasi_debet '\
     '      ,t.kode_pihak_ketiga '\
     '      ,t.rekening_deposito '\
     '      ,t.no_bilyet '\
     '      ,t.nominal_pembukaan '\
     '      ,t.tgl_buka '\
     '      ,t.tgl_tutup '\
     '      ,t.jenisjatuhtempo '\
     '      ,t.nisbah '\
     '      ,t.equivalent_rate '\
     '      ,t.tgl_jatuh_tempo '\
     '      ,t.kode_pihak_ketiga'\
     '  from transaksiinvestasi ti, '\
     '      (select d.id_investasi '\
     '          ,d.rekening_deposito '\
     '          ,i.no_bilyet '\
     '          ,i.nominal_pembukaan '\
     '          ,i.tgl_buka '\
     '          ,i.tgl_tutup '\
     '          ,d.jenisjatuhtempo '\
     '          ,d.nisbah '\
     '          ,d.equivalent_rate '\
     '          ,d.tgl_jatuh_tempo '\
     '          ,i.kode_pihak_ketiga '\
     '         from deposito d, investasi i '\
     '         where d.id_investasi = i.id_investasi ) t '\
     ' where ti.id_investasi = t.id_investasi '\
     '   and clsfTransaksiInvestasi in (\'B\',\'C\') '\
     '   and tgl_transaksi >= \'%s\' '\
     '   and tgl_transaksi < \'%s\' '\
     ' order by t.kode_pihak_ketiga ; '\
     % ( config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_awal)\
       , config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_akhir_plus)\
    )

# End New

def ConstructReportValues(config, strSQL, tgl_transaksi_awal, tgl_transaksi_akhir_plus, oFile):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  resSQL = config.CreateSQL(strSQL).RawResult
  no_urut = 0
  nomHasilreal = 0.0
  nomHasilNonreal = 0.0
  nomBeban = 0.0
  nomHasilBersih = 0.0
  totHasilInvestasi = hasilinvestasi = 0.0

  resSQL.First()
  while not resSQL.Eof:
      no_urut += 1

      config.SendDebugMsg('masuk.....01 ')
      if moduleapi.IsOddNumber(no_urut):
          bgcolor = '#EFEFEF'
      else:
          bgcolor = '#FFFFFF'
      
      strSQL = strSQLPihakKetiga(config, resSQL.kode_pihak_ketiga)
      rSQL = config.CreateSQL(strSQL).RawResult
   
      equivalent_rate = resSQL.equivalent_rate or 0.0

      if resSQL.jenisjatuhtempo > 0:
          depo = 'Berjangka'
      else:
          depo = 'On Call'

      invManual = 0.0

      if resSQL.tgl_jatuh_tempo <> None:
         strTglJatuhTempo = config.FormatDateTime('dd mmmm yyyy',moduleapi.DateTimeTupleToFloat(config, resSQL.tgl_jatuh_tempo))

         if depo == 'Berjangka':
            #config.SendDebugMsg('No Bilyet : '+ resSQL.no_bilyet)
            #config.SendDebugMsg('Kode Pihakk Ke III : '+ resSQL.kode_pihak_ketiga)
            #config.SendDebugMsg('invManual-02A')
            y,m,d = (resSQL.tgl_jatuh_tempo)[:3]
            #config.SendDebugMsg('invManual-02A1 '+str(y) +' '+ str(m)+' '+ str(d))
            strTanggalAwal = config.ModLibUtils.DecodeDate(tgl_transaksi_awal)
            yy,mm,dd = strTanggalAwal[:3]
            #config.SendDebugMsg('invManual-02B '+str(yy) +' '+ str(mm)+' '+ str(dd))
            
            jml_tempo = calendar.monthrange(yy,mm-1)[1]
            jml_tempo = jml_tempo - d + 1
            jml_now = calendar.monthrange(yy,mm)[1]
            
            #config.SendDebugMsg('Nominal Pembukaan : '+str(resSQL.nominal_pembukaan))
            #config.SendDebugMsg('jml_tempo : '+str(jml_tempo))
            #config.SendDebugMsg('ER : '+str(equivalent_rate))
            invManual = (resSQL.nominal_pembukaan * (float(equivalent_rate)/100)) * (float(jml_tempo)/365)
            #config.SendDebugMsg('invManual-021A : '+str(invManual))
            invManual = invManual + ((resSQL.nominal_pembukaan * (float(equivalent_rate)/100)) * (float(d)/365))
            #config.SendDebugMsg('invManual-021B : '+str(invManual))
            #config.SendDebugMsg('No Bilyet : '+ resSQL.no_bilyet)

         else:
             strTglJatuhTempo = ''

      if resSQL.tgl_buka <> None:
         strTglBuka = config.FormatDateTime('dd/mmm/yyyy',moduleapi.DateTimeTupleToFloat(config, resSQL.tgl_buka))
      else:
         strTglBuka = ''

      if resSQL.tgl_tutup <> None:
         if resSQL.tgl_jatuh_tempo > tgl_transaksi_akhir_plus:
            strTglJatuhTempo = ''
            strTglTutup = config.FormatDateTime('dd/mmm/yyyy',moduleapi.DateTimeTupleToFloat(config, resSQL.tgl_tutup))
         else:
            strTglTutup = config.FormatDateTime('dd/mmm/yyyy',moduleapi.DateTimeTupleToFloat(config, resSQL.tgl_tutup))
      else:
         strTglTutup = ''

      strTglTransaksi = config.FormatDateTime('dd/mmm/yyyy',moduleapi.DateTimeTupleToFloat(config, resSQL.tgl_transaksi))
    
      #config.FormatDateTime('d-mmm-yy', moduleapi.DateTimeTupleToFloat(config, resDep.tgl_jatuh_tempo))

      if resSQL.clsfTransaksiInvestasi == 'B':
         # Piutang pendapatan
         #config.SendDebugMsg('masukkkkk.......A1')
         mutasi_kredit = resSQL.mutasi_kredit or 0.0
         mutasi_debet  = resSQL.mutasi_debet or 0.0
         nomHasilNonreal  = (mutasi_debet - mutasi_kredit)
         hasilinvestasi = nomHasilNonreal

      elif resSQL.clsfTransaksiInvestasi == 'C':
           # Pendapatan
           # nomHasilreal += resSQL.mutasi_kredit
           # beban
           # nomBeban += resSQL.mutasi_debet
           #config.SendDebugMsg('masukkkkk.......A2')
           mutasi_kredit = resSQL.mutasi_kredit or 0.0
           mutasi_debet  = resSQL.mutasi_debet or 0.0
           nomHasilreal  = (mutasi_kredit - mutasi_debet)
           hasilinvestasi = nomHasilreal

      totHasilInvestasi = totHasilInvestasi + hasilinvestasi
     
      equivalent_rate = resSQL.equivalent_rate or 0.0
      config.SendDebugMsg('ER : '+str(equivalent_rate))

      oFile.write('	<tr>\n')
      oFile.write('		<td width="3%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'" height="22">'+ str(no_urut) +'</td>\n')
      oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
      oFile.write('		<p align="center">'+ resSQL.kode_pihak_ketiga +'</td>\n')
      oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
      oFile.write('		<p align="left">'+ rSQL.nama_pihak_ketiga+'</td>\n')
      oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
      oFile.write('		<p align="center">'+ str(resSQL.no_bilyet) +'</td>\n')
      oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
      oFile.write('		<p align="center">'+ str(resSQL.rekening_deposito) +'</td>\n')
      oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
      oFile.write('		<p align="center">'+ strTglBuka +'</td>\n')
      oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
      oFile.write('		<p align="center">'+strTglTutup +'</td>\n')
      oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
      oFile.write('		<p align="center">'+strTglJatuhTempo+'</td>\n')
      oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
      oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, resSQL.nominal_pembukaan) +'</td>\n')
      oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
      oFile.write('		<p align="center">'+ strTglTransaksi +'</td>\n')
      oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
      oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, hasilinvestasi) +'</td>\n')
      oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
      oFile.write('		<p align="center">'+ moduleapi.FormatFloatStd(config, resSQL.nisbah) +'</td>\n')
      oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
      oFile.write('		<p align="center">'+ str(equivalent_rate) +'</td>\n')
      oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
      oFile.write('		<p align="center">'+ moduleapi.FormatFloatStd(config, invManual) +'</td>\n')
      oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
      oFile.write('		<p align="center">'+ depo +'</td>\n')
      oFile.write('	</tr>\n')

      resSQL.Next()

  return totHasilInvestasi
  
def ConstructReportTrailer(config, totHasilInvestasi, oFile):
    moduleapi = modman.getModule(config, 'moduleapi')
    
    oFile.write('	<tr>\n')
    oFile.write('		<td width="100%" colspan="10" style="border-style: solid; border-width: medium">\n')
    oFile.write('		<font color="#008000"><p align="right"><b>Total Hasil Investasi</font></td>\n')
    oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#CC6699" height="22">\n')
    oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, totHasilInvestasi) +'</td>\n')
    oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#CC6699"" height="22">\n')
    oFile.write('		<p align="center">&nbsp;</td>\n')
    oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#CC6699"" height="22">\n')
    oFile.write('		<p align="center">&nbsp;</td>\n')
    oFile.write('		<td width="9%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#CC6699"" height="22">\n')
    oFile.write('		<p align="center">&nbsp;</td>\n')
    oFile.write('	</tr>\n')
     
def WriteToFile(config, parameter, oFile):
    tgl_transaksi_awal = parameter.FirstRecord.tanggal_awal
    tgl_transaksi_akhir = parameter.FirstRecord.tanggal_akhir

    strTanggalAwal = config.FormatDateTime('dd mmmm yyyy',tgl_transaksi_awal)
    strTanggalAkhir = config.FormatDateTime('dd mmmm yyyy',tgl_transaksi_akhir)
    ConstructReportHeader(config, strTanggalAwal, strTanggalAkhir, oFile)
 
    strSQL = strSQLHasilInvestasi(config, tgl_transaksi_awal, tgl_transaksi_akhir + 1)
    totHasilInvestasi = ConstructReportValues(config, strSQL, tgl_transaksi_awal, tgl_transaksi_akhir + 1, oFile)

    ConstructReportTrailer(
       config
     , totHasilInvestasi
     , oFile
    )

    oFile.write('</table>\n')
    oFile.write('<p>&nbsp;</p>\n')
    oFile.write('<table border="2" width="100%" id="table4" style="border-width: 0px; border-collapse:collapse" bordercolorlight="#000000" bordercolordark="#000000">\n')
    oFile.write('	<tr>\n')
    oFile.write('		<td align="right" style="border-left-style: none; border-left-width: medium; border-right-style: none; border-right-width: medium; border-top-style: none; border-top-width: medium; border-bottom-style: solid; border-bottom-width: 1px">\n')
    oFile.write('		Dicetak tanggal '+ config.FormatDateTime('d mmmm yyyy', config.Now()) +'</td>\n')
    oFile.write('	</tr>\n')
    oFile.write('	<tr>\n')
    oFile.write('		<td style="border-left-style: none; border-left-width: medium; border-right-style: none; border-right-width: medium; border-top-style: solid; border-top-width: 1px; border-bottom-style: none; border-bottom-width: medium"></td>\n')
    oFile.write('	</tr>\n')
    oFile.write('</table>\n')
    oFile.write('\n')
    oFile.write('\n')
    oFile.write('</body>\n')
    oFile.write('\n')
    oFile.write('</html>\n')

def CreateReport(config, parameter, returnpacket):
    sBaseFileName = 'alerthslinv.htm'
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

