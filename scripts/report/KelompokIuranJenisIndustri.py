import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi
import string

def ConstructReportHeader(config, strTanggalAwal, strTanggalAkhir, oFile):
  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Laporan Kelompok Iuran Menurut Jenis Usaha</title>\n')
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Arial; line-height:100%; margin-top:0; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td colspan="4" height="20" style="border-left:medium none #000000; border-right:medium none #000000; border-top-style:none; border-top-width:medium; border-bottom-style:none; border-bottom-width:medium">\n')
  oFile.write('		<p align="center"><font size="3" color="#008000"><b>Laporan Kelompok Iuran Menurut Jenis Usaha</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" colspan="4" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font color="#008000"><b>PERIODE '+ string.upper(strTanggalAwal) +' HINGGA '+ string.upper(strTanggalAkhir) +'</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="7%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>JENIS PEKERJAAN</b></td>\n')
  oFile.write('		<td width="18%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b> < Rp 50.000</b></td>\n')
  oFile.write('		<td width="18%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>Rp 50.001 sd 300.000</b></td>\n')
  oFile.write('		<td width="18%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>Rp 300.001 sd 500.000</b></td>\n')
  oFile.write('		<td width="18%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>Rp 500.001 sd 1.000.000</b></td>\n')
  oFile.write('		<td width="18%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b> > Rp 1.000.000</b></td>\n')
  oFile.write('	</tr>\n')


def strSQLDaftarPeserta(config, tgl_transaksi_awal, tgl_transaksi_akhir_plus):
  return \
    'select n.NO_PESERTA, c.kode_jenis_usaha  '\
    'from NasabahDPLK n '\
    '  , RekeningDPLK r '\
    '  , nasabahdplkcorporate c '\
    'where n.no_peserta = r.no_peserta '\
    '  and n.kode_nasabah_corporate = c.kode_nasabah_corporate '\
    '  and n.tgl_registrasi >= \'%s\' '\
    '  and n.tgl_registrasi < \'%s\' '\
    '  and r.STATUS_DPLK = \'A\' '\
    '  and c.kode_nasabah_corporate in \
            (\'ISAT1\',\'ISAT2\',\'ISAT3\',\'ISAT4\',\'ISAT5\',\'ISAT6\',\'BMI\', \
             \'ISAT7\',\'ISAT8\',\'ISAT9\',\'ISAT10\',\'ISAT11\',\'ISAT12\',\'HITTS\',    \
             \'ISAT13\',\'ISAT14\',\'ISAT15\',\'ISAT16\',\'ISAT17\',\'ISAT18\',\'MUTUAL\',   \
             \'ISAT19\',\'ISAT20\',\'ISAT21\',\'ISAT22\',\'ISAT23\',\'ISAT24\',   \
             \'ISAT25\',\'ISAT26\',\'ISAT27\',\'ISAT28\',\'ISAT29\',\'ISAT30\',     \
             \'HDY\',\'PETRO\',\'BNSLH\',\'VBS\',\'MHJR\',\'ACT\',\'PROAS\',\'IM2\', \
             \'BENS\',\'LIART\',\'247\',\'MELATI\',\'FSL\',\'UMUQ\',\'YKK\',\'SBBS\',   \
             \'IHB\',\'RSAG\',\'DDR\',\'MEDEK\',\'SDA\',\'TIPTOP\',\'SAMSUNG\',\'GLM\') '\
    % (config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_awal)\
       , config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_akhir_plus)\
    )


def strSQLRataRataIuran(config, tgl_transaksi_awal, tgl_transaksi_akhir_plus, no_peserta):
  return \
    'select NO_PESERTA '\
    ' , sum(isnull(mutasi_iuran_pst, 0.0)) iuran_pst '\
    ' , sum(isnull(mutasi_iuran_pk, 0.0)) iuran_pk '\
    'from TransaksiDPLK '\
    'where no_peserta = \'%s\' '\
    '  and kode_jenis_transaksi = \'K\' '\
    '  and tgl_transaksi >= \'%s\' '\
    '  and tgl_transaksi < \'%s\' '\
    'group by no_peserta ;'\
    % (no_peserta
       ,config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_awal)\
       , config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_akhir_plus)\
    )
    
    
def ConstructReportValues(config, strSQL, tgl_transaksi_awal, tgl_transaksi_akhir_plus, oFile):
  resSQL = config.CreateSQL(strSQL).RawResult

  iuran = 0.0
  p11 = p12 = p13 = p14 = p15 = 0
  p21 = p22 = p23 = p24 = p25 = 0
  p31 = p32 = p33 = p34 = p35 = 0
  p41 = p42 = p43 = p44 = p45 = 0
  p51 = p52 = p53 = p54 = p55 = 0
  p61 = p62 = p63 = p64 = p65 = 0
  p71 = p72 = p73 = p74 = p75 = 0
  totPeserta = 0.0

  thn = 12
  config.SendDebugMsg('Mulai ')
  resSQL.First()
  while not resSQL.Eof:

    config.SendDebugMsg('Masuk ')

    strSQL = strSQLRataRataIuran(config, tgl_transaksi_awal, tgl_transaksi_akhir_plus, resSQL.no_peserta)
    rSQL = config.CreateSQL(strSQL).RawResult
    
    iuran = (rSQL.iuran_pk or 0.0)/thn
    

    if resSQL.kode_jenis_usaha == '01':
       config.SendDebugMsg('01')
       if iuran < 50000:
          p11 += 1
          
       if iuran >= 50000:
          if iuran <= 300000:
             p12 += 1

       if iuran > 300000:
          if iuran <= 500000:
             p13 += 1

       if iuran > 500000:
          if iuran <= 1000000:
             p14 += 1

       if iuran > 1000000:
          p15 += 1
          
    if resSQL.kode_jenis_usaha == '02':
       config.SendDebugMsg('02')
       if iuran < 50000:
          p21 += 1
       if iuran >= 50000:
          if iuran <= 300000:
             p22 += 1
       if iuran > 300000:
          if iuran <= 500000:
             p23 += 1
       if iuran > 500000:
          if iuran <= 1000000:
             p24 += 1
       if iuran > 1000000:
          p25 += 1

    if resSQL.kode_jenis_usaha == '04':
       config.SendDebugMsg('04')
       if iuran < 50000:
          p31 += 1
       if iuran >= 50000:
          if iuran <= 300000:
             p32 += 1
       if iuran > 300000:
          if iuran <= 500000:
             p33 += 1
       if iuran > 500000:
          if iuran <= 1000000:
             p34 += 1
       if iuran > 1000000:
          p35 += 1
          
    if resSQL.kode_jenis_usaha == '06':
       config.SendDebugMsg('06')
       if iuran < 50000:
          p41 += 1
       if iuran >= 50000:
          if iuran <= 300000:
             p42 += 1
       if iuran > 300000:
          if iuran <= 500000:
             p43 += 1
       if iuran > 500000:
          if iuran <= 1000000:
             p44 += 1
       if iuran > 1000000:
          p45 += 1

    if resSQL.kode_jenis_usaha == '12':
       config.SendDebugMsg('12')
       if iuran < 50000:
          p51 += 1
       if iuran >= 50000:
          if iuran <= 300000:
             p52 += 1
       if iuran > 300000:
          if iuran <= 500000:
             p53 += 1
       if iuran > 500000:
          if iuran <= 1000000:
             p54 += 1
       if iuran > 1000000:
          p55 += 1

    if resSQL.kode_jenis_usaha == '45':
       config.SendDebugMsg('45')
       if iuran < 50000:
          p61 += 1
       if iuran >= 50000:
          if iuran <= 300000:
             p62 += 1
       if iuran > 300000:
          if iuran <= 500000:
             p63 += 1
       if iuran > 500000:
          if iuran <= 1000000:
             p64 += 1
       if iuran > 1000000:
          p65 += 1

    if resSQL.kode_jenis_usaha == '56':
       config.SendDebugMsg('56')
       if iuran < 50000:
          p71 += 1
       if iuran >= 50000:
          if iuran <= 300000:
             p72 += 1
       if iuran > 300000:
          if iuran <= 500000:
             p73 += 1
       if iuran > 500000:
          if iuran <= 1000000:
             p74 += 1
       if iuran > 1000000:
          p75 += 1

    totPeserta += 1
    
    resSQL.Next()

  bgcolor1 = '#EFEFEF'
  bgcolor2 = '#FFFFFF'

  oFile.write('	<tr>\n')
  oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="center">PENDIDIKAN & YAYASAN</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p11) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p12) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p13) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p14) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p15) +'</td>\n')
  oFile.write('	</tr>\n')
  oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor2 +'" height="22">\n')
  oFile.write('		<p align="center">JASA</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor2 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p21) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p22) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p23) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p24) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p25) +'</td>\n')
  oFile.write('	</tr>\n')
  oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="center">PERBANKAN</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p31) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p32) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p33) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p34) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p35) +'</td>\n')
  oFile.write('	</tr>\n')
  oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor2 +'" height="22">\n')
  oFile.write('		<p align="center">KONSULTAN</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor2 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p41) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p42) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p43) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p44) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p45) +'</td>\n')

  oFile.write('	</tr>\n')
  oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="center">LAIN-LAIN</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p51) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p52) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p53) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p54) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p55) +'</td>\n')
  oFile.write('	</tr>\n')
  oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor2 +'" height="22">\n')
  oFile.write('		<p align="center">TELEKOMUNIKASI</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor2 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p61) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p62) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p63) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p64) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p65) +'</td>\n')
  oFile.write('	</tr>\n')
  oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor2 +'" height="22">\n')
  oFile.write('		<p align="center">ADVERTISING, PRINTING & MEDIA</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor2 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p71) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p72) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p73) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p74) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p75) +'</td>\n')
  oFile.write('	</tr>\n')


  return totPeserta

def ConstructReportTrailer(config, totPeserta, oFile):
  oFile.write('	<tr>\n')
  oFile.write('		<td width="44%" colspan="3" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" colspan="6" bgcolor="#CC6699">\n')
  oFile.write('		<b>TOTAL PESERTA</b></td>\n')
  oFile.write('		<td width="9%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totPeserta) +'</b></td>\n')
  oFile.write('	</tr>\n')
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

def WriteToFile(config, parameter, oFile):

  tgl_transaksi_awal = parameter.FirstRecord.tanggal_awal
  tgl_transaksi_akhir = parameter.FirstRecord.tanggal_akhir

  strTanggalAwal = config.FormatDateTime('dd mmmm yyyy',tgl_transaksi_awal)
  strTanggalAkhir = config.FormatDateTime('dd mmmm yyyy',tgl_transaksi_akhir)
  ConstructReportHeader(config, strTanggalAwal, strTanggalAkhir, oFile)

  strSQL = strSQLDaftarPeserta(config, tgl_transaksi_awal, tgl_transaksi_akhir + 1)
  config.SendDebugMsg(strSQL)

  totPeserta = ConstructReportValues(config, strSQL, tgl_transaksi_awal, tgl_transaksi_akhir, oFile)

  ConstructReportTrailer(
    config, totPeserta
    , oFile
  )

def CreateReport(config, parameter, returnpacket):
  sBaseFileName = 'perolehan_cabang.htm'
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
