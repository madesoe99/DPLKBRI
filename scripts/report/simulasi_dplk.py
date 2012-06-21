import sys, string
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi, transaksiapi

def tabelpremi(config, usia_masuk, usia_pensiun):

  x = 45
  z = 0

  while x <= 65:
    if usia_pensiun == x:
       b = z
    z += 1
    x += 1

  #b = b - 45
  if usia_masuk == 18:
     rate=[1.35,1.35,1.35,1.40,1.40,1.45,1.45,1.50,1.50,1.55,1.65,1.70,1.75,1.80,1.85,1.90,2.05,2.10,2.20,2.25,2.35]
     ratepremi = rate[b]
  if usia_masuk == 19:
     rate=[1.35,1.35,1.35,1.40,1.40,1.45,1.45,1.50,1.50,1.55,1.65,1.70,1.75,1.80,1.85,1.90,2.05,2.10,2.20,2.25,2.35]
     ratepremi = rate[b]
  if usia_masuk == 20:
     rate=[1.35,1.35,1.35,1.40,1.40,1.45,1.45,1.50,1.55,1.55,1.65,1.70,1.75,1.80,1.90,1.95,2.05,2.15,2.20,2.30,2.45]
     ratepremi = rate[b]
  if usia_masuk == 21:
     rate=[1.35,1.35,1.40,1.40,1.40,1.45,1.45,1.50,1.55,1.65,1.70,1.75,1.80,1.85,1.90,1.95,2.10,2.20,2.25,2.35,2.50]
     ratepremi = rate[b]
  if usia_masuk == 22:
     rate=[1.35,1.35,1.40,1.40,1.40,1.45,1.50,1.50,1.55,1.65,1.70,1.75,1.80,1.85,1.95,2.05,2.15,2.20,2.30,2.45,2.55]
     ratepremi = rate[b]
  if usia_masuk == 23:
     rate=[1.35,1.35,1.40,1.40,1.45,1.45,1.50,1.55,1.55,1.65,1.70,1.75,1.85,1.90,1.95,2.10,2.15,2.25,2.35,2.50,2.60]
     ratepremi = rate[b]
  if usia_masuk == 24:
     rate=[1.35,1.35,1.40,1.40,1.45,1.45,1.50,1.55,1.65,1.70,1.75,1.80,1.85,1.90,2.05,2.15,2.20,2.30,2.45,2.55,2.65]
     ratepremi = rate[b]
  if usia_masuk == 25:
     rate=[1.35,1.35,1.40,1.40,1.45,1.45,1.50,1.55,1.65,1.70,1.75,1.80,1.90,1.95,2.10,2.15,2.25,2.35,2.50,2.60,2.70]
     ratepremi = rate[b]
  if usia_masuk == 26:
     rate=[1.35,1.35,1.40,1.40,1.45,1.50,1.50,1.55,1.65,1.70,1.80,1.85,1.90,2.05,2.10,2.20,2.30,2.45,2.55,2.65,2.75]
     ratepremi = rate[b]
  if usia_masuk == 27:
     rate=[1.35,1.35,1.40,1.40,1.45,1.50,1.55,1.65,1.70,1.75,1.80,1.90,1.95,2.10,2.15,2.25,2.35,2.50,2.60,2.70,2.90]
     ratepremi = rate[b]
  if usia_masuk == 28:
     rate=[1.35,1.35,1.40,1.40,1.45,1.50,1.55,1.65,1.70,1.80,1.85,1.90,2.05,2.15,2.20,2.30,2.45,2.55,2.70,2.85,2.95]
     ratepremi = rate[b]
  if usia_masuk == 29:
     rate=[1.35,1.40,1.40,1.45,1.50,1.55,1.65,1.70,1.75,1.85,1.90,1.95,2.10,2.20,2.30,2.45,2.55,2.65,2.75,2.95,3.05]
     ratepremi = rate[b]
  if usia_masuk == 30:
     rate=[1.40,1.40,1.45,1.50,1.55,1.65,1.70,1.75,1.80,1.90,1.95,2.10,2.15,2.25,2.35,2.50,2.60,2.75,2.90,3.05,3.15]
     ratepremi = rate[b]
  if usia_masuk == 31:
     rate=[1.45,1.45,1.50,1.55,1.65,1.70,1.75,1.80,1.90,1.95,2.10,2.15,2.25,2.35,2.50,2.60,2.70,2.90,3.00,3.15,3.35]
     ratepremi = rate[b]
  if usia_masuk == 32:
     rate=[1.50,1.50,1.55,1.65,1.70,1.75,1.80,1.90,1.95,2.10,2.15,2.25,2.35,2.50,2.60,2.70,2.85,3.00,3.15,3.30,3.45]
     ratepremi = rate[b]
  if usia_masuk == 33:
     rate=[1.55,1.55,1.65,1.70,1.75,1.85,1.90,1.95,2.10,2.15,2.25,2.35,2.50,2.60,2.70,2.85,3.00,3.10,3.30,3.45,3.65]
     ratepremi = rate[b]
  if usia_masuk == 34:
     rate=[1.65,1.70,1.75,1.80,1.85,1.90,1.95,2.10,2.15,2.25,2.35,2.50,2.60,2.70,2.85,3.00,3.10,3.30,3.45,3.65,3.80]
     ratepremi = rate[b]
  if usia_masuk == 35:
     rate=[1.75,1.75,1.80,1.90,1.95,2.05,2.10,2.20,2.25,2.35,2.50,2.60,2.70,2.85,3.00,3.10,3.30,3.45,3.65,3.80,3.95]
     ratepremi = rate[b]
  if usia_masuk == 36:
     rate=[1.85,1.90,1.95,2.05,2.10,2.15,2.20,2.30,2.45,2.50,2.60,2.70,2.90,3.00,3.10,3.30,3.45,3.65,3.80,3.95,4.20]
     ratepremi = rate[b]
  if usia_masuk == 37:
     rate=[1.95,2.05,2.10,2.15,2.20,2.30,2.35,2.45,2.55,2.65,2.75,2.90,3.05,3.15,3.35,3.45,3.65,3.80,4.05,4.20,4.45]
     ratepremi = rate[b]
  if usia_masuk == 38:
     rate=[2.15,2.20,2.25,2.30,2.20,2.45,2.55,2.60,2.70,2.85,2.95,3.05,3.25,3.35,3.50,3.70,3.85,4.05,4.20,4.45,4.65]
     ratepremi = rate[b]
  if usia_masuk == 39:
     rate=[2.35,2.35,2.45,2.50,2.35,2.60,2.70,2.75,2.90,3.00,3.10,3.30,3.40,3.55,3.75,3.90,4.10,4.25,4.50,4.65,4.90]
     ratepremi = rate[b]
  if usia_masuk == 40:
     rate=[2.60,2.60,2.60,2.65,2.55,2.90,2.90,3.00,3.05,3.15,3.35,3.45,3.65,3.75,3.90,4.15,4.30,4.50,4.70,4.95,5.15]
     ratepremi = rate[b]
  if usia_masuk == 41:
     rate=[0.00,2.85,2.85,2.90,2.70,3.00,3.05,3.15,3.30,3.40,3.50,3.70,3.80,3.95,4.15,4.35,4.55,4.75,5.00,5.25,5.45]
     ratepremi = rate[b]
  if usia_masuk == 42:
     rate=[0.00,0.00,3.10,3.10,2.95,3.15,3.30,3.35,3.45,3.65,3.75,3.90,4.05,4.25,4.45,4.60,4.85,5.00,5.25,5.50,5.75]
     ratepremi = rate[b]
  if usia_masuk == 43:
     rate=[0.00,0.00,0.00,3.35,3.10,3.40,3.59,3.55,3.70,3.85,3.95,4.15,4.30,4.50,4.65,4.90,5.10,5.35,5.55,5.80,6.10]
     ratepremi = rate[b]
  if usia_masuk == 44:
     rate=[0.00,0.00,0.00,0.00,3.40,3.70,3.75,3.85,3.95,4.10,4.25,4.35,4.60,4.75,4.95,5.15,5.40,5.65,5.85,6.15,6.45]
     ratepremi = rate[b]
  if usia_masuk == 45:
     rate=[0.00,0.00,0.00,0.00,3.65,3.95,4.05,4.15,4.25,4.35,4.55,4.70,4.90,5.05,5.30,5.50,5.75,5.95,6.25,6.50,6.75]
     ratepremi = rate[b]
  if usia_masuk == 46:
     rate=[0.00,0.00,0.00,0.00,0.00,0.00,4.45,4.50,4.55,4.70,4.90,5.05,5.25,5.40,5.65,5.85,6.10,6.35,6.65,6.95,7.25]
     ratepremi = rate[b]
  if usia_masuk == 47:
     rate=[0.00,0.00,0.00,0.00,0.00,0.00,0.00,4.90,4.95,5.10,5.25,5.40,5.65,5.80,6.05,6.25,6.55,6.75,7.05,7.35,7.70]
     ratepremi = rate[b]
  if usia_masuk == 48:
     rate=[0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,5.45,5.55,5.70,5.85,6.05,6.25,6.50,6.70,7.00,7.30,7.55,7.85,8.15]
     ratepremi = rate[b]
  if usia_masuk == 49:
     rate=[0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,6.15,6.25,6.35,6.55,6.75,7.00,7.25,7.50,7.80,8.10,8.35,8.70]
     ratepremi = rate[b]
  if usia_masuk == 50:
     rate=[0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,6.95,7.00,7.15,7.35,7.55,7.80,8.10,8.35,8.65,8.95,9.30]
     ratepremi = rate[b]
  if usia_masuk == 51:
     rate=[0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,7.75,7.85,8.05,8.20,8.45,8.65,8.95,9.30,9.55,9.90]
     ratepremi = rate[b]
  if usia_masuk == 52:
     rate=[0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,8.65,8.70,8.90,9.10,9.35,9.65,9.90,10.25,10.60]
     ratepremi = rate[b]
  if usia_masuk == 53:
     rate=[0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,9.55,9.70,9.85,10.10,10.30,10.60,10.95,11.30]
     ratepremi = rate[b]
  if usia_masuk == 54:
     rate=[0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,10.60,10.65,10.85,11.10,11.40,11.70,12.05]
     ratepremi = rate[b]
  if usia_masuk == 55:
     rate=[0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,11.70,11.75,11.95,12.20,12.55,12.90]
     ratepremi = rate[b]
  if usia_masuk == 56:
     rate=[0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,12.85,1295,13.15,13.40,13.75]
     ratepremi = rate[b]
  if usia_masuk == 57:
     rate=[0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,14.10,14.20,14.45,14.70]
     ratepremi = rate[b]
  if usia_masuk == 58:
     rate=[0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,15.45,15.55,15.80]
     ratepremi = rate[b]
  if usia_masuk == 59:
     rate=[0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,16.95,17.05]
     ratepremi = rate[b]
  if usia_masuk == 60:
     rate=[0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,18.55]
     ratepremi = rate[b]

  return ratepremi

def ConstructReportHeader(config
       , usia_masuk
       , nama_lengkap
       , iuran_bulanan
       , usia_pensiun
       , pengalihan_dana
       , paket_investasi
       , tingkat_investasi
       , biaya_administrasi
       , biaya_pengelolaan
       , kenaikan_iuran
       , oFile ):

  config.SendDebugMsg('masuk....07'+str(kenaikan_iuran))
  
  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Simulasi</title>\n')
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Arial; line-height:100%; margin-top:0; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="0" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td colspan="8" height="20" style="border-left:0; border-right:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0">\n')
  oFile.write('		<p align="left"><font size="3" color="#008000"><b>D P L K  M U A M A L A T</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('</table>\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="0" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td colspan="8" height="20" style="border-left:0; border-right:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0">\n')
  oFile.write('		<p align="left"><font size="1" color="#008000"><b>Proyeksi Dana Peserta</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('</table>\n')
  
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="7%" align="left" style="border-left:0 none; border-right-style:solid; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		Nama Peserta</td>\n')
  oFile.write('		<td width="2%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		:</td>\n')
  oFile.write('		<td width="10%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		 '+string.upper(nama_lengkap) + '</td>\n')
  oFile.write('		<td width="10%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		<b>&nbsp;</b></td>\n')
  oFile.write('		<td width="12%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		Pengalihan Dari DPPK/DPLK Lain</td>\n')
  oFile.write('		<td width="2%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		:</td>\n')
  oFile.write('		<td width="7%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		'+moduleapi.FormatFloatStd(config, pengalihan_dana, '-')+'</b></td>\n')
  oFile.write('	</tr>\n')

  oFile.write('	<tr>\n')
  oFile.write('		<td width="7%" align="left" style="border-left:0 none; border-right-style:solid; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		Usia Masuk</td>\n')
  oFile.write('		<td width="2%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		:</td>\n')
  oFile.write('		<td width="10%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		'+str(usia_masuk)+'</td>\n')
  oFile.write('		<td width="10%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		<b>&nbsp;</b></td>\n')
  oFile.write('		<td width="12%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		Biaya Adm dan Pengelolaan</td>\n')
  oFile.write('		<td width="2%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		:</td>\n')
  oFile.write('		<td width="7%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  #oFile.write('		 '+moduleapi.FormatFloatStd(config, biaya_administrasi, '-') +'</td>\n')
  oFile.write('		 '+moduleapi.FormatFloatStd(config, biaya_administrasi, '-')+' dan '+str(biaya_pengelolaan)+' %</td>\n')
  oFile.write('	</tr>\n')

  oFile.write('	<tr>\n')
  oFile.write('		<td width="7%" align="left" style="border-left:0 none; border-right-style:solid; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		Iuran/bln</td>\n')
  oFile.write('		<td width="2%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		:</td>\n')
  oFile.write('		<td width="10%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		'+moduleapi.FormatFloatStd(config, iuran_bulanan, '-')+'</b></td>\n')
  oFile.write('		<td width="10%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		<b>&nbsp;</b></td>\n')
  oFile.write('		<td width="12%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		Persentasi Kenaikan Penghasilan</td>\n')
  oFile.write('		<td width="2%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		:</td>\n')
  oFile.write('		<td width="7%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		'+str(kenaikan_iuran)+' %</td>\n')
  oFile.write('	</tr>\n')

  oFile.write('	<tr>\n')
  oFile.write('		<td width="7%" align="left" style="border-left:0 none; border-right-style:solid; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		Usia Pensiun</td>\n')
  oFile.write('		<td width="2%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		:</td>\n')
  oFile.write('		<td width="10%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		'+str(usia_pensiun)+'</td>\n')
  oFile.write('		<td width="10%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		<b>&nbsp;</b></td>\n')
  oFile.write('		<td width="12%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		Kode Paket & Asumsi Tingkat Investasi</td>\n')
  oFile.write('		<td width="2%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		:</b></td>\n')
  oFile.write('		<td width="7%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		'+string.upper(paket_investasi)+' & '+str(tingkat_investasi)+' %</td>\n')
  oFile.write('	</tr>\n')
  oFile.write('</table>\n')
  
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="3%" align="center" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		Tahun</td>\n')
  oFile.write('		<td width="10%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		Iuran / bln</td>\n')
  oFile.write('		<td width="10%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		Iuran Tahunan</td>\n')
  oFile.write('		<td width="12%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		Akum Iuran</td>\n')
  oFile.write('		<td width="10%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		Dana Akhir Thn*</td>\n')
  oFile.write('		<td width="7%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		Dana pst Akhir Thn**</td>\n')
  oFile.write('	</tr>\n')


def ConstructReportValues(
      config
      , blnLhr
      , blnReg
      , usia_masuk
      , usia_pensiun
      , iuran_bulanan
      , kenaikan_iuran
      , paket_investasi
      , tingkat_investasi
      , pengalihan_dana
      , biaya_administrasi
      , biaya_pengelolaan
      , oFile):
      
  tglNow = config.ModDateTime.DecodeDate(config.Now()) #time.localtime()[:3]
  #dtNowDate = config.ModDateTime.EncodeDate(y,m,d)
  
  thn_ini   = int(tglNow[0])
  usia_reg  = usia_masuk
  bln_reg   = blnReg
  bln_lahir = blnLhr
  iuran_manfaat_penurunan   = iuran_bulanan
  biaya_pengelolaan_menurun = biaya_pengelolaan
  
  fee_bln = 0.0
  akumulasi_sebelum_biaya = 0.0
  akumulasi_setelah_biaya = 0.0
  coverDPLK = 0.0
  vPengalihan_dana  = pengalihan_dana
  vKenaikan_iuran   = kenaikan_iuran
  vIuran_bulanan    = iuran_bulanan
  persentase_iuran  = 100
  BiayaPengelolaan  = biaya_pengelolaan
  BiayaAdministrasi = 18000  #biaya_administrasi
  
  no_urut = 0
  yearDeath = 0
  line = 14
  # tambahan usia masuk
  usia_masuk = (usia_masuk)

  # perubahan kekurangan 1 tahun
  v_loop = (usia_pensiun-usia_masuk)+1

  dana_akhir_tahun = (iuran_bulanan + pengalihan_dana)

  akumulasi_iuran = 0
  kenaikan_iuran1 = kenaikan_iuran
  v_loop1 = 12
  loop_data = ((12-bln_reg)+1)
  i = 1
  
  yearDeath = (v_loop/2)
  yearDeath -= 1
  
  while  i <= v_loop:
  
     no_urut += 1
     bgcolor = '#FFFFFF'

     # Kondisi berdasarkan bulan registrasi
     if i == 1:
        b = bln_reg
        v_loop1 = loop_data
     else:
        b = 1
        v_loop1 = 12

     # Kondisi akhir periode berdasarkan bulan kelahiran
     if i == v_loop:
        v_loop1 = bln_lahir
        loop_data = bln_lahir
        
     iuran_tahunan    = (iuran_bulanan * v_loop1)
     akumulasi_iuran  = iuran_tahunan + akumulasi_iuran
     vIuran_tahunan   = iuran_tahunan
     vAkumulasi_iuran = akumulasi_iuran
     vIuran_bulanan   = iuran_bulanan
     fee_bln = 0
     
     if i == 1:
          oFile.write('	<tr>\n')
          oFile.write('		<td width="3%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'" height="22"> ***'+ str(i) +'</td>\n')
          oFile.write('		<td width="10%" align="right" style="border-style: solid; border-width: 1px; " bgcolor="#FFFFFF">\n')
          oFile.write('		'+moduleapi.FormatFloatStd(config, vIuran_bulanan, '-')+'</td>\n')

     elif i == v_loop:
         oFile.write('	<tr>\n')
         oFile.write('		<td width="3%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'" height="22"> ****'+ str(v_loop) +'</td>\n')
         oFile.write('		<td width="10%" align="right" style="border-style: solid; border-width: 1px; " bgcolor="#FFFFFF">\n')
         oFile.write('		'+moduleapi.FormatFloatStd(config, vIuran_bulanan, '-')+'</td>\n')
         
     else:
         oFile.write('	<tr>\n')
         oFile.write('		<td width="3%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'" height="22">'+ str(i) +'</td>\n')
         oFile.write('		<td width="10%" align="right" style="border-style: solid; border-width: 1px; " bgcolor="#FFFFFF">\n')
         oFile.write('		'+moduleapi.FormatFloatStd(config, vIuran_bulanan, '-')+'</td>\n')

     if i == 1:
        v_loop1 = 12
        
     if i == v_loop:
        v_loop1 = bln_lahir
        
     c = b
     while c <= v_loop1:            # ------------------------ Looping ------------
     #for c in  (v_loop1):
         config.SendDebugMsg('mulai :'+str(c))
         fee_bln = ((float(tingkat_investasi)/100)/12)*dana_akhir_tahun
         akumulasi = (fee_bln+dana_akhir_tahun)
         #config.SendDebugMsg('akumulasi :'+str(akumulasi))
         
         if i == 1:
            if c <> 12:
               dana_akhir_tahun = (akumulasi+iuran_bulanan)
            else:
               if akumulasi < 100000001:
                  biaya_pengelolaan = 1.25
               else:
                  biaya_pengelolaan = 1

               biaya_adm = (BiayaAdministrasi/12)*loop_data
               biaya_pengelolaan = ((float(BiayaPengelolaan)/100)/12)*loop_data
               dana_akhir_tahun = ((akumulasi-(akumulasi*biaya_pengelolaan))-biaya_adm)
               akumulasi_sebelum_biaya = akumulasi
               akumulasi_setelah_biaya = ((akumulasi-(akumulasi*biaya_pengelolaan))-biaya_adm)

         else:
            if v_loop1 == 12:   # --------------------- 12 -------------------
                if c <> 12:
                      dana_akhir_tahun =(akumulasi+iuran_bulanan)
                else:
                      if akumulasi < 100000001:
                         biaya_pengelolaan = 1.25
                      else:
                         biaya_pengelolaan = 1

                      dana_akhir_tahun = ((akumulasi-(akumulasi*(float(BiayaPengelolaan)/100)))-BiayaAdministrasi)
                      akumulasi_sebelum_biaya = akumulasi
                      akumulasi_setelah_biaya = ((akumulasi - (akumulasi*(float(BiayaPengelolaan)/100)))-BiayaAdministrasi)

            else:
                # Kondisi sesuai dengan bulan kelahiran peserta
                if c <> v_loop1:
                      dana_akhir_tahun = (akumulasi+iuran_bulanan)
                else:
                      if akumulasi < 100000001:
                         biaya_pengelolaan = 1.25
                      else:
                         biaya_pengelolaan = 1

                      biaya_adm = ((BiayaAdministrasi/12)*v_loop1)
                      biaya_pengelolaan=(((float(BiayaPengelolaan)/100)/12)*loop_data)
                      dana_akhir_tahun = ((akumulasi-(akumulasi*biaya_pengelolaan))-biaya_adm)
                      akumulasi_sebelum_biaya = akumulasi
                      akumulasi_setelah_biaya = ((akumulasi - (akumulasi*biaya_pengelolaan))-biaya_adm)

             # ---------------------- END 12 ------------
         c += 1
         # ---------------------------------- end looping -----------------------
                      
     vAkumulasi_sebelum_biaya = akumulasi_sebelum_biaya
     vAkumulasi_setelah_biaya = akumulasi_setelah_biaya
     
     # Kenaikan Iuran
     config.SendDebugMsg('masuk....08'+str(kenaikan_iuran))
     
     if kenaikan_iuran >= 1:
          config.SendDebugMsg('masuk....09'+str(kenaikan_iuran))
          
          kenaikan_iuran = (iuran_bulanan*(float(kenaikan_iuran1)/100))
          iuran_bulanan = (iuran_bulanan+kenaikan_iuran)
          dana_akhir_tahun = (dana_akhir_tahun +iuran_bulanan)
          
     else:
          dana_akhir_tahun = dana_akhir_tahun + iuran_bulanan

     oFile.write('		<td width="10%" align="right" style="border-style: solid; border-width: 1px; " bgcolor="#FFFFFF">\n')
     oFile.write('		'+moduleapi.FormatFloatStd(config, vIuran_tahunan, '-')+'</td>\n')
     oFile.write('		<td width="10%" align="right" style="border-style: solid; border-width: 1px; " bgcolor="#FFFFFF">\n')
     oFile.write('		'+moduleapi.FormatFloatStd(config, vAkumulasi_iuran, '-')+'</td>\n')
     oFile.write('		<td width="10%" align="right" style="border-style: solid; border-width: 1px; " bgcolor="#FFFFFF">\n')
     oFile.write('		'+moduleapi.FormatFloatStd(config, vAkumulasi_sebelum_biaya, '-')+'</td>\n')
     oFile.write('		<td width="10%" align="right" style="border-style: solid; border-width: 1px; " bgcolor="#FFFFFF">\n')
     oFile.write('		'+moduleapi.FormatFloatStd(config, vAkumulasi_setelah_biaya, '-')+'</td>\n')

     if  i == yearDeath:
         config.SendDebugMsg('masuk ')
         coverDPLK = vAkumulasi_setelah_biaya
         
     i += 1
  # end looping

  return  akumulasi_setelah_biaya, v_loop, coverDPLK, yearDeath


def ConstructReportTrailer(config, danastlhbiaya, tglRegistrasi, tglLahir, vloop, tingkat_investasi, ratepremi, covDPLK, yDeath, oFile):

  Pajakpenghasilan = 0.0
  danastlhpajak = 0.0
  mMenurun = 0.0
  sMasaKepesertaan = 0.0
  
  config.SendDebugMsg('danastlhbiaya : '+str(danastlhbiaya))
  
  if danastlhbiaya <= 50000000:
     Pajakpenghasilan = 0
     #config.SendDebugMsg('Pajak = 0 : '+str(Pajakpenghasilan))
  else:
     Pajakpenghasilan = danastlhbiaya*(float(5)/100)
     #config.SendDebugMsg('Pajakpenghasilan-01 : '+str(Pajakpenghasilan))
     
  Pajakpenghasilan = transaksiapi.HitungPajakPengambilanManfaat(config,danastlhbiaya)

  #------ Manfaat menurun
  sMasaKepesertaan = (vloop - yDeath)*12
  config.SendDebugMsg('sMasaKepesertaan :'+str(sMasaKepesertaan))
  mPerjanjian = (vloop*12)
  config.SendDebugMsg('sMasaPerjanjian :'+str(mPerjanjian))
  mMenurun = (float(sMasaKepesertaan)/mPerjanjian)
  mMenurun = (danastlhbiaya * mMenurun)
  config.SendDebugMsg('danastlhbiaya :'+str(danastlhbiaya))
  #-------------------
  #config.SendDebugMsg('sMasaKepesertaan :'+str(sMasaKepesertaan))
  
  premi = ((danastlhbiaya * ratepremi)/tingkat_investasi)/1000
  danastlhpajak = (danastlhbiaya - Pajakpenghasilan)
  if danastlhpajak > 100000000:
     Manfaatsekaligus = (danastlhpajak*(float(20)/100))
     Manfaatanuitas = (danastlhpajak -Manfaatsekaligus)
     
  else:
     Manfaatsekaligus = (danastlhpajak)
     Manfaatanuitas = 0
     
  #Manfaatanuitas = (danastlhpajak -Manfaatsekaligus)
  
  # Sum Dana Peserta Akhir Kepesertaan
  
  oFile.write('	</tr>\n')
  oFile.write('</table>\n')
  
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="10%" align="right" style="border-left:0 none; border-right-style:solid; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		Total Sebelum Pajak</td>\n')
  oFile.write('		<td width="2%" align="center" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		:</td>\n')
  oFile.write('		<td width="5%" align="right" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		'+moduleapi.FormatFloatStd(config,danastlhbiaya, '-')+'</td>\n')
  oFile.write('		<td width="10%" align="right" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		<b>&nbsp;</b></td>\n')
  oFile.write('		<td width="12%" align="right" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		Manfaat Pensiun Sekaligus</td>\n')
  oFile.write('		<td width="2%" align="center" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		:</td>\n')
  oFile.write('		<td width="7%" align="right" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		'+moduleapi.FormatFloatStd(config,Manfaatsekaligus, '-')+'</td>\n')
  oFile.write('	</tr>\n')

  oFile.write('	<tr>\n')
  oFile.write('		<td width="10%" align="right" style="border-left:0 none; border-right-style:solid; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		Pajak Penghasilan Final</td>\n')
  oFile.write('		<td width="2%" align="center" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		:</td>\n')
  oFile.write('		<td width="5%" align="right" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		'+moduleapi.FormatFloatStd(config,Pajakpenghasilan, '-')+'</td>\n')
  oFile.write('		<td width="10%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		&nbsp;</b></td>\n')
  oFile.write('		<td width="12%" align="right" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		Manfaat Pensiun Anuitas</td>\n')
  oFile.write('		<td width="2%" align="center" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		:</td>\n')
  oFile.write('		<td width="7%" align="right" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		'+moduleapi.FormatFloatStd(config,Manfaatanuitas, '-')+'</td>\n')
  oFile.write('	</tr>\n')

  oFile.write('	<tr>\n')
  oFile.write('		<td width="10%" align="right" style="border-left:0 none; border-right-style:solid; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		Total Setelah Pajak</td>\n')
  oFile.write('		<td width="2%" align="center" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		:</td>\n')
  oFile.write('		<td width="5%" align="right" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		'+moduleapi.FormatFloatStd(config,danastlhpajak, '-')+'</td>\n')
  oFile.write('		<td width="10%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		<b>&nbsp;</b></td>\n')
  oFile.write('		<td width="12%" align="right" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		Premi Wasiat Ummat</td>\n')
  oFile.write('		<td width="2%" align="center" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		:</td>\n')
  oFile.write('		<td width="7%" align="right" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('			'+moduleapi.FormatFloatStd(config,premi, '-')+'</td>\n')
  oFile.write('	</tr>\n')

  oFile.write('	<tr>\n')
  oFile.write('		<td width="10%" align="left" style="border-left:0 none; border-right-style:solid; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		&nbsp; </td>\n')
  oFile.write('		<td width="2%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		&nbsp</td>\n')
  oFile.write('		<td width="5%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		&nbsp; </td>\n')
  oFile.write('		<td width="10%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		<b>&nbsp;</b></td>\n')
  oFile.write('		<td width="12%" align="right" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		Manfaat Yang Dicover</td>\n')
  oFile.write('		<td width="2%" align="center" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		:</td>\n')
  oFile.write('		<td width="7%" align="right" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		'+moduleapi.FormatFloatStd(config,danastlhbiaya, '-')+'</td>\n')
  oFile.write('	</tr>\n')
  oFile.write('</table>\n')

  # Keterangan

  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:1; border-right-width:1; border-top-width:1" bordercolor="#111111" border="1" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="7%" align="left" style="border-left:0 none; border-right-style:solid; border-right-width:1; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		   *) Dana Akhir Tahun belum dipotong Biaya Administrasi & Biaya Pengelolaan</td>\n')
  oFile.write('		<td width="7%" align="left" style="border-left:0 none; border-right-style:solid; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		    Untuk Peserta Wasiat Ummat</td>\n')
  oFile.write('	</tr>\n')

  oFile.write('	<tr>\n')
  oFile.write('		<td width="7%" align="left" style="border-left:0 none; border-right-style:solid; border-right-width:1; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		  **) Dana pst Akhir tahun setelah dipotong Biaya Administrasi & Biaya Pengelolaan</td>\n')
  oFile.write('		<td width="7%" align="left" style="border-left:0 none; border-right-style:solid; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		    Jika terjadi musibah peserta meninggal dunia pada tahun <b>'+str(yDeath)+'</b></td>\n')
  oFile.write('	</tr>\n')

  oFile.write('	<tr>\n')
  oFile.write('		<td width="7%" align="left" style="border-left:0 none; border-right-style:solid; border-right-width:1; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		 ***) Tahun <b>1</b> dimulai dari <b>'+config.FormatDateTime('dd mmmm yyyy',tglRegistrasi)+'</b> (registrasi) s/d <b>akhir tahun</b> (desember)</td>\n')
  oFile.write('		<td width="7%" align="left" style="border-left:0 none; border-right-style:solid; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		    Ahli waris akan mendapatkan dana dari DPLK Muamalat sebesar Rp. <b>'+moduleapi.FormatFloatStd(config,covDPLK, '-')+'</b></td>\n')
  oFile.write('	</tr>\n')

  oFile.write('	<tr>\n')
  oFile.write('		<td width="7%" align="left" style="border-left:0 none; border-right-style:solid; border-right-width:1; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		****) Tahun <b>'+str(vloop)+'</b> dimulai dari awal tahun (januari) s/d <b>'+config.FormatDateTime('dd mmmm yyyy',tglLahir)+' </b>(bulan kelahiran)</td>\n')
  oFile.write('		<td width="7%" align="left" style="border-left:0 none; border-right-style:solid; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		    dan dari pihak asuransi akan mendapatkan sebesar Rp. <b>'+moduleapi.FormatFloatStd(config,mMenurun, '-')+'</b></td>\n')
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

def strSQLSumValues(config, no_peserta):
  return \
    'select n.NO_PESERTA '\
    '     , n.NAMA_LENGKAP '\
    '     , r.USIA_PENSIUN '\
    '     , n.TANGGAL_LAHIR '\
    '     , r.AKUM_DANA_IURAN_PST '\
    '     , r.AKUM_DANA_IURAN_PK '\
    '     , r.AKUM_DANA_PENGEMBANGAN '\
    '     , r.AKUM_DANA_PERALIHAN '\
    'from NASABAHDPLK n'\
    '   , REKENINGDPLK r '\
    'where n.no_peserta = r.no_peserta '\
    '  and n.NO_PESERTA = \'%s\' '\
     %( no_peserta
    )


def WriteToFile(config, parameter, oFile):

  akumiuranpst = 0.0
  akumiuranpk  = 0.0
  akumpengembangan = 0.0
  akumperalihan = 0.0
  totakum = 0.0

  flagCode = parameter.FirstRecord.nama_lengkap
  flag = flagCode[0]

  if flag not in str(range(10)):
     # Simulasi Peserta Baru.................
     tgl_transaksi_lahir      = parameter.FirstRecord.tanggal_lahir
     nama_lengkap             = parameter.FirstRecord.nama_lengkap
     pengalihan_dana          = parameter.FirstRecord.pengalihan_dana
     usia_pensiun             = parameter.FirstRecord.usia_pensiun
     
  else:
     # Simulasi peserta lama...................
     no_peserta = parameter.FirstRecord.nama_lengkap
     strSQL = strSQLSumValues(config, no_peserta)
     rSQL = config.CreateSQL(strSQL).RawResult
     #config.SendDebugMsg(resSQL)

     nama_lengkap        = rSQL.nama_lengkap
     y, m, d             = rSQL.tanggal_lahir[:3]
     tgl_transaksi_lahir = config.ModDateTime.EncodeDate(y, m, d)
     usia_pensiun        = rSQL.usia_pensiun
     akumiuranpst        = rSQL.akum_dana_iuran_pst or 0.0
     akumiuranpk         = rSQL.akum_dana_iuran_pk or 0.0
     akumpengembangan    = rSQL.akum_dana_pengembangan or 0.0
     akumperalihan       = rSQL.akum_dana_peralihan or 0.0
     totakum             = (akumiuranpst + akumiuranpk + akumpengembangan + akumperalihan )
     pengalihan_dana     = totakum

  config.SendDebugMsg('masuk....01')
  oParameter = config.CreatePObjImplProxy('Parameter')
  oParameter.Key = 'JUMLAH_HARI_SETAHUN'
  JumlahHariSetahun = oParameter.Numeric_Value

  config.SendDebugMsg('masuk....02')
  oParameter = config.CreatePObjImplProxy('Parameter')
  oParameter.Key = 'BIAYA_ADM_TAHUNAN'
  biaya_administrasi = oParameter.Numeric_value
  biaya_administrasi = (biaya_administrasi * 2)
  
  config.SendDebugMsg('masuk....03')
  oParameter = config.CreatePObjImplProxy('Parameter')
  oParameter.Key = 'PERSEN_BIAYA_PENGELOLAAN'
  biaya_pengelolaan = oParameter.Numeric_value
  
  iuran_bulanan            = parameter.FirstRecord.iuran_bulanan
  tgl_transaksi_registrasi = parameter.FirstRecord.tanggal_registrasi
  kenaikan_iuran           = parameter.FirstRecord.kenaikan_iuran
  paket_investasi          = parameter.FirstRecord.paket_investasi
  
  if paket_investasi in ('a','A'):
     kode_investasi = 'INVESTASI_PAKET_A'

  if paket_investasi in ('b','B'):
     kode_investasi = 'INVESTASI_PAKET_B'

  if paket_investasi in ('c','C'):
     kode_investasi = 'INVESTASI_PAKET_C'

  config.SendDebugMsg('masuk....04')
  oParameter = config.CreatePObjImplProxy('Parameter')
  oParameter.Key = kode_investasi
  tingkat_investasi = oParameter.Numeric_value

  config.SendDebugMsg('masuk....05')
  danasblmbiaya = 0.0
  danastlhbiaya = 0.0
  ratepremi = 0.0
  vLoop = 0


  #tgl_transaksi_lahir = config.FormatDateTime('dd mmmm yyyy',strTanggalLahir)
  #strTanggalRegistrasi = config.FormatDateTime('dd mmmm yyyy',tgl_transaksi_registrasi)

  tglRegistrasi = config.ModDateTime.DecodeDate(tgl_transaksi_registrasi)
  tglLahir = config.ModDateTime.DecodeDate(tgl_transaksi_lahir)
  usia_masuk = int((tgl_transaksi_registrasi - tgl_transaksi_lahir)/JumlahHariSetahun)

  blnReg = int(tglRegistrasi[1])
  blnLhr = int(tglLahir[1])
  #usia_masuk = (int(tglRegistrasi[0])-int(tglLahir[0]))
  
  config.SendDebugMsg('masuk....06'+str(kenaikan_iuran))
  
  ConstructReportHeader(
     config
     , usia_masuk
     , nama_lengkap
     , iuran_bulanan
     , usia_pensiun
     , pengalihan_dana
     , paket_investasi
     , tingkat_investasi
     , biaya_administrasi
     , biaya_pengelolaan
     , kenaikan_iuran
     , oFile)

  #nama_lengkap


  danastlhbiaya, vloop, covDPLK, yDeath =  ConstructReportValues(config, blnLhr, blnReg, usia_masuk, usia_pensiun, iuran_bulanan, kenaikan_iuran, paket_investasi, tingkat_investasi, pengalihan_dana, biaya_administrasi, biaya_pengelolaan, oFile)
  if usia_masuk <= 60:
     ratepremi = tabelpremi(config,usia_masuk,usia_pensiun)
  else:
     retepremi = 0.0;

  ConstructReportTrailer(
    config
    , danastlhbiaya
    , tgl_transaksi_registrasi
    , tgl_transaksi_lahir
    , vloop
    , tingkat_investasi
    , ratepremi
    , covDPLK
    , yDeath
    , oFile
  )

def CreateReport(config, parameter, returnpacket):
  sBaseFileName = 'proyeksi_dana.htm'
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

