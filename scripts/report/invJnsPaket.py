import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi
import string
import calendar

def ConstructReportHeader(config, monthFrom, yearFrom, monthUntil, yearUntil, oFile):

  nama_jns_investasi = 'Perjenis & Perpaket Investasi'

  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Total Investasi Akhir Bulan</title>\n')
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Arial; line-height:100%; margin-top:0; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0; border-bottom-width:0px" bordercolor="#111111" border="1" width="750" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td height="20" style="border-left:medium none #000000; border-right:medium none #000000; border-top-style:none; border-top-width:medium; border-bottom-style:none; border-bottom-width:medium">\n')
  oFile.write('		<p align="center"><font size="3" color="#008000"><b>Dana Pensiun Lembaga \n')
  oFile.write('		Keuangan Muamalat<br>\n')
  oFile.write('		Laporan '+ nama_jns_investasi +' Akhir Bulan</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="750" style="border-style: none; border-width: medium">\n')
  oFile.write('		<p align="left"><font size="2" color="#008000">&nbsp;</font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="750" style="border-style: none; border-width: medium">\n')
  oFile.write('		<p align="left"><font size="2" color="#008000"><b>'+ moduleapi.IntMonthToStr(monthFrom) +' '+ str(yearFrom) +' sampai '+ moduleapi.IntMonthToStr(monthUntil) +' '+ str(yearUntil) +'</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	</table><font size="2">\n')
  oFile.write('\n')
  oFile.write('\n')


def ConstructReportValues(config, monthFrom, yearFrom, monthUntil, yearUntil, oFile):
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0; border-bottom-width:0px" bordercolor="#111111" border="1" width="750" id="table3" cellpadding="2">\n')

  ## Looping rata-rata investasi by ade herman 2011-05-24
  totpaketInvA = totpaketInvB = totpaketInvC = 0.0
  totjenisInvA = totjenisInvB = totjenisInvC = 0.0
  paketInvA = paketInvB = paketInvC = 0.0
  totcontribusiA = totcontribusiB = totcontribusiC = 0.0
  totproporsiA = totproporsiB = totproporsiC = 0.0
  totjenisDepo = totjenisSukuk = totjenisReksadana = 0.0
  totjenisHi_depo =   totjenisHi_sukuk=   totjenisHi_reksadana = 0.0
  counter = 0

  #if monthFrom == monthUntil:

  while monthFrom <= monthUntil:
  
     # Variable
     lastday_from      = moduleapi.GetLastDayOfMonth(monthFrom, yearFrom)
     lastday_until     = moduleapi.GetLastDayOfMonth(monthUntil, yearUntil)
     #lastday_investasi = moduleapi.GetLastDayOfMonth((monthFrom - 1), yearUntil)
     
     if monthFrom == 1:
        monthfrom = 12
        yearfrom = yearFrom - 1
        lastday_investasi = moduleapi.GetLastDayOfMonth(monthfrom, yearfrom)
        strtgl_investasi = '%s-%s-%s 23:59:59.000' % (yearfrom, monthfrom , lastday_investasi)
     else:
        lastday_investasi = moduleapi.GetLastDayOfMonth((monthFrom - 1), yearFrom)
        strtgl_investasi = '%s-%s-%s 23:59:59.000' % (yearFrom, monthFrom - 1, lastday_investasi)

     strtgl_from   = '%s-%s-%s 23:59:59.000' % (yearFrom, monthFrom, lastday_from)
     strtgl_until  = '%s-%s-%s 23:59:59.000' % (yearUntil, monthUntil, lastday_until)
     #strtgl_investasi = '%s-%s-%s 23:59:59.000' % (yearFrom, monthFrom - 1, lastday_investasi)

     #config.SendDebugMsg('strtgl_from'+str(strtgl_from))
     #config.SendDebugMsg('strtgl_until'+str(strtgl_until))
     #config.SendDebugMsg('strtgl_investasi'+str(strtgl_investasi))

     paketA = paketB = paketC = 0.0

     ## Filtering Data
     #config.SendDebugMsg('Dana Perpaket Aktif .....')
     rSQLPerpaketAktif = BuildSQLDanaPaket(config, strtgl_investasi)
     while not rSQLPerpaketAktif.Eof:
           if rSQLPerpaketAktif.paket == 'A':
              paketA = paketA + rSQLPerpaketAktif.nominal
              #config.SendDebugMsg('Paket A : '+str(paketA))
           if rSQLPerpaketAktif.paket == 'B':
              paketB = paketB + rSQLPerpaketAktif.nominal
              #config.SendDebugMsg('Paket B : '+str(paketB))
           if rSQLPerpaketAktif.paket == 'C':
              paketC = paketC + rSQLPerpaketAktif.nominal
              #config.SendDebugMsg('Paket C : '+str(paketC))
              
           rSQLPerpaketAktif.Next()

     #config.SendDebugMsg('Dana Perpaket Tutup .....')
     rSQLPerpaketTutup = BuildSQLDanaTutup(config, strtgl_investasi)
     while not rSQLPerpaketTutup.Eof:
           if rSQLPerpaketTutup.paket == 'A':
              paketA = paketA + rSQLPerpaketTutup.nominal
              #config.SendDebugMsg('Paket A : '+str(paketA))
           if rSQLPerpaketTutup.paket == 'B':
              paketB = paketB + rSQLPerpaketTutup.nominal
              #config.SendDebugMsg('Paket B : '+str(paketB))
           if rSQLPerpaketTutup.paket == 'C':
              paketC = paketC + rSQLPerpaketTutup.nominal
              #config.SendDebugMsg('Paket C : '+str(paketC))

           rSQLPerpaketTutup.Next()
           
     #config.SendDebugMsg('Proporsi Perpaket .....')
     rSQLProporsiPerpaket = BuildSQLProporsiPerPaket(config, strtgl_investasi, strtgl_from)
     while not rSQLProporsiPerpaket.Eof:
           if rSQLProporsiPerpaket.paket == 'A':
              proporsiA = rSQLProporsiPerpaket.nominal or 0.00
              #config.SendDebugMsg('proporsiA : '+str(proporsiA))
           if rSQLProporsiPerpaket.paket == 'B':
              proporsiB = rSQLProporsiPerpaket.nominal or 0.00
              #config.SendDebugMsg('proporsiB : '+str(proporsiB))
           if rSQLProporsiPerpaket.paket == 'C':
              proporsiC =  rSQLProporsiPerpaket.nominal or 0.00
              #config.SendDebugMsg('proporsiC : '+str(proporsiC))

           rSQLProporsiPerpaket.Next()

     ## Dana Perpaket
     inv_deposito      = GetNominalInv(config, "'A'", 'Deposito', strtgl_investasi)
     #config.SendDebugMsg('inv_deposito .....'+str(inv_deposito))
     inv_sukuk         = GetNominalInv(config, "'A','D'", 'Obligasi', strtgl_investasi)
     #config.SendDebugMsg('inv_sukuk .....'+str(inv_sukuk))
     inv_reksadana     = GetNominalInv(config, "'A','D'", 'Reksadana', strtgl_investasi)
     #config.SendDebugMsg('inv_reksadana .....'+str(inv_reksadana))

     # total Dana Idle
     idleDana          = (paketA + (paketB - inv_sukuk) + (paketC - inv_reksadana))
     #config.SendDebugMsg('idleDana : '+str(idleDana))

     # hasil investasi perpaket
     hi_deposito       = GetHasilInv(config, 'D', strtgl_investasi, strtgl_from)
     #config.SendDebugMsg('hi_deposito : '+str(hi_deposito))
     hi_sukuk          = GetHasilInv(config, 'O', strtgl_investasi, strtgl_from)
     #config.SendDebugMsg('hi_sukuk : '+str(hi_sukuk))
     hi_reksadana      = GetHasilInv(config, 'R', strtgl_investasi, strtgl_from)
     #config.SendDebugMsg('hi_reksadana : '+str(hi_reksadana))

     ## Kontribusi pembentukan deposito
     contribusiA       = ((paketA / idleDana) * inv_deposito)
     #config.SendDebugMsg('contribusiA : '+str(contribusiA))
     contribusiB       = (((paketB - inv_sukuk) / idleDana) * inv_deposito)
     #config.SendDebugMsg('contribusiB : '+str(contribusiB))
     contribusiC       = (((paketC - inv_reksadana) / idleDana)  * inv_deposito)
     config.SendDebugMsg('contribusiC : '+str(contribusiC))
     
     #strReturn = config.FormatFloat('0.##', ((proporsiA / contribusiA)*100))
     
     ## Perpaket investasi
     paketInvA = ((proporsiA / contribusiA)*100) #* 12 #(365/lastday_from)
     paketInvB = (((proporsiB + hi_sukuk) / (inv_sukuk + contribusiB))*100) #* (365/lastday_from)
     paketInvC = (((proporsiC + hi_reksadana) / (inv_reksadana + contribusiC))*100) #* (365/lastday_from)

     totpaketInvA = totpaketInvA + paketInvA
     totpaketInvB = totpaketInvB + paketInvB
     totpaketInvC = totpaketInvC + paketInvC
     
     totcontribusiA = totcontribusiA + contribusiA
     totcontribusiB = totcontribusiB + contribusiB + inv_sukuk
     totcontribusiC = totcontribusiC + contribusiC + inv_reksadana
     
     totproporsiA = totproporsiA + proporsiA
     totproporsiB = totproporsiB + proporsiB + hi_sukuk
     totproporsiC = totproporsiC + proporsiC + hi_reksadana
     
     ## Perjenis Investasi
     jenisInvA = (((proporsiA + proporsiB + proporsiC)/ inv_deposito) * 100) #* 12  #(365/lastday_from)
     jenisInvB = ((hi_sukuk / inv_sukuk) * 100) * (365/lastday_from)
     jenisInvC = ((hi_reksadana / inv_reksadana) * 100) ## * (365/lastday_from)
     
     totjenisDepo      = totjenisDepo + inv_deposito
     totjenisSukuk     = totjenisSukuk + inv_sukuk
     totjenisReksadana = totjenisReksadana + inv_reksadana
     
     totjenisHi_depo      = totjenisHi_depo + hi_deposito
     totjenisHi_sukuk     = totjenisHi_sukuk + hi_sukuk
     totjenisHi_reksadana = totjenisHi_reksadana + hi_reksadana
     
     totjenisInvA = totjenisInvA + jenisInvA
     totjenisInvB = totjenisInvB + jenisInvB
     totjenisInvC = totjenisInvC + jenisInvC
     
     counter += 1
     monthFrom += 1
     
  strPaketA = config.FormatFloat('0.##', (totpaketInvA/counter))
  strPaketB = config.FormatFloat('0.##', (totpaketInvB/counter))
  strPaketC = config.FormatFloat('0.##', (totpaketInvC/counter))
  
  strContribusiA   = moduleapi.FormatFloatStd(config, (totcontribusiA/counter))
  strContribusiB   = moduleapi.FormatFloatStd(config, (totcontribusiB/counter))
  strContribusiC   = moduleapi.FormatFloatStd(config, (totcontribusiC/counter))
  
  #moduleapi.FormatFloatStd(config, nominal)
  strProporsiA   = moduleapi.FormatFloatStd(config, (totproporsiA/counter))
  strProporsiB   = moduleapi.FormatFloatStd(config, (totproporsiB/counter))
  strProporsiC   = moduleapi.FormatFloatStd(config, (totproporsiC/counter))

  strJenisDepo = moduleapi.FormatFloatStd(config, (totjenisDepo/counter))
  strJenisSukuk = moduleapi.FormatFloatStd(config, (totjenisSukuk/counter))
  strJenisReksadana = moduleapi.FormatFloatStd(config, (totjenisReksadana/counter))

  strJenisHi_Depo = moduleapi.FormatFloatStd(config, (totjenisHi_depo/counter))
  strJenisHi_Sukuk = moduleapi.FormatFloatStd(config, (totjenisHi_sukuk/counter))
  strJenisHi_Reksadana = moduleapi.FormatFloatStd(config, (totjenisHi_reksadana/counter))

  strJenisA = config.FormatFloat('0.##', (totjenisInvA/counter))
  strJenisB = config.FormatFloat('0.##', (totjenisInvB/counter))
  strJenisC = config.FormatFloat('0.##', (totjenisInvC/counter))

  # Paket A
  oFile.write('	<tr>\n')
  oFile.write('		<td width="750" style="border-style: none; border-width: medium">\n')
  oFile.write('		<p align="left"><font size="2" color="#008000"><b>Paket A - Deposito Rupiah </b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="600" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="left"><b><font size="2">&nbsp;&nbsp;Investasi </font></b></td>\n')
  oFile.write('		<td width="150" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="right"><b>\n')
  oFile.write('		<font size="2">'+ strContribusiA +' </font></b></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="600" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="left"><b><font size="2">&nbsp;&nbsp;Hasil Investasi </font></b></td>\n')
  oFile.write('		<td width="150" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="right"><b>\n')
  oFile.write('		<font size="2">'+ strProporsiA +' </font></b></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="600" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="left"><b><font size="2">&nbsp;&nbsp;Rata-Rata Hasil Investasi (%)</font></b></td>\n')
  oFile.write('		<td width="150" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="right"><b>\n')
  oFile.write('		<font size="2">'+ strPaketA +'% </font></b></td>\n')
  oFile.write('	</tr>\n')

  ## Paket B
  oFile.write('	<tr>\n')
  oFile.write('		<td width="750" style="border-style: none; border-width: medium">\n')
  oFile.write('		<p align="left"><font size="2" color="#008000"><b>Paket B - Deposito Rupiah + Sukuk </b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="600" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="left"><b><font size="2">&nbsp;&nbsp;Investasi </font></b></td>\n')
  oFile.write('		<td width="150" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="right"><b>\n')
  oFile.write('		<font size="2">'+ strContribusiB +' </font></b></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="600" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="left"><b><font size="2">&nbsp;&nbsp;Hasil Investasi </font></b></td>\n')
  oFile.write('		<td width="150" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="right"><b>\n')
  oFile.write('		<font size="2">'+ strProporsiB +' </font></b></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="600" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="left"><b><font size="2">&nbsp;&nbsp;Rata-Rata Hasil Investasi (%)</font></b></td>\n')
  oFile.write('		<td width="150" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="right"><b>\n')
  oFile.write('		<font size="2">'+ strPaketB +'% </font></b></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="600" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="left"><i><font size="1">&nbsp;&nbsp;( Hasil investasi sukuk ada bulanan dan triwulanan )</font></i></td>\n')
  oFile.write('		<td width="150" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="right"><b>\n')
  oFile.write('		<font size="2">&nbsp;</font></b></td>\n')
  oFile.write('	</tr>\n')

  ## Paket C
  oFile.write('	<tr>\n')
  oFile.write('		<td width="750" style="border-style: none; border-width: medium">\n')
  oFile.write('		<p align="left"><font size="2" color="#008000"><b>Paket C - Deposito Rupiah + Reksadana </b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="600" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="left"><b><font size="2">&nbsp;&nbsp;Investasi </font></b></td>\n')
  oFile.write('		<td width="150" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="right"><b>\n')
  oFile.write('		<font size="2">'+ strContribusiC +' </font></b></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="600" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="left"><b><font size="2">&nbsp;&nbsp;Hasil Investasi </font></b></td>\n')
  oFile.write('		<td width="150" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="right"><b>\n')
  oFile.write('		<font size="2">'+ strProporsiC +' </font></b></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="600" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="left"><b><font size="2">&nbsp;&nbsp;Rata-Rata Hasil Investasi (%)</font></b></td>\n')
  oFile.write('		<td width="150" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="right"><b>\n')
  oFile.write('		<font size="2">'+ strPaketC +'% </font></b></td>\n')
  oFile.write('	</tr>\n')

  ## Jenis Investasi
  oFile.write('	<tr>\n')
  oFile.write('		<td width="750" style="border-style: none; border-width: medium">\n')
  oFile.write('		<p align="left"><font size="2" color="#008000">&nbsp;</font></td>\n')
  oFile.write('	</tr>\n')

  ## Deposito
  oFile.write('	<tr>\n')
  oFile.write('		<td width="750" style="border-style: none; border-width: medium">\n')
  oFile.write('		<p align="left"><font size="2" color="#008000"><b>Jenis Investasi Deposito Rupiah </b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="600" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="left"><b><font size="2">&nbsp;&nbsp;Investasi </font></b></td>\n')
  oFile.write('		<td width="150" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="right"><b>\n')
  oFile.write('		<font size="2">'+ strJenisDepo +' </font></b></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="600" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="left"><b><font size="2">&nbsp;&nbsp;Hasil Investasi </font></b></td>\n')
  oFile.write('		<td width="150" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="right"><b>\n')
  oFile.write('		<font size="2">'+ strJenisHi_Depo +' </font></b></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="600" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="left"><b><font size="2">&nbsp;&nbsp;Rata-Rata Hasil Investasi (%)</font></b></td>\n')
  oFile.write('		<td width="150" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="right"><b>\n')
  oFile.write('		<font size="2">'+ strJenisA +'% </font></b></td>\n')
  oFile.write('	</tr>\n')

  ## Jenis Invetasi Sukuk
  oFile.write('	<tr>\n')
  oFile.write('		<td width="750" style="border-style: none; border-width: medium">\n')
  oFile.write('		<p align="left"><font size="2" color="#008000"><b>Jenis Investasi Sukuk </b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="600" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="left"><b><font size="2">&nbsp;&nbsp;Investasi </font></b></td>\n')
  oFile.write('		<td width="150" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="right"><b>\n')
  oFile.write('		<font size="2">'+ strJenisSukuk +' </font></b></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="600" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="left"><b><font size="2">&nbsp;&nbsp;Hasil Investasi </font></b></td>\n')
  oFile.write('		<td width="150" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="right"><b>\n')
  oFile.write('		<font size="2">'+ strJenisHi_Sukuk +' </font></b></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="600" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="left"><b><font size="2">&nbsp;&nbsp;Rata-Rata Hasil Investasi (%)</font></b></td>\n')
  oFile.write('		<td width="150" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="right"><b>\n')
  oFile.write('		<font size="2">'+ strJenisB +'% </font></b></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="600" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="left"><i><font size="1">&nbsp;&nbsp;( Hasil investasi sukuk ada bulanan dan triwulanan )</font></i></td>\n')
  oFile.write('		<td width="150" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="right"><b>\n')
  oFile.write('		<font size="2">&nbsp;</font></b></td>\n')
  oFile.write('	</tr>\n')


  ## Jenis Invetasi Reksadana
  oFile.write('	<tr>\n')
  oFile.write('		<td width="750" style="border-style: none; border-width: medium">\n')
  oFile.write('		<p align="left"><font size="2" color="#008000"><b>Jenis Investasi Reksadana </b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="600" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="left"><b><font size="2">&nbsp;&nbsp;Investasi </font></b></td>\n')
  oFile.write('		<td width="150" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="right"><b>\n')
  oFile.write('		<font size="2">'+ strJenisReksadana +' </font></b></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="600" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="left"><b><font size="2">&nbsp;&nbsp;Hasil Investasi </font></b></td>\n')
  oFile.write('		<td width="150" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="right"><b>\n')
  oFile.write('		<font size="2">'+ strJenisHi_Reksadana +' </font></b></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="600" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="left"><b><font size="2">&nbsp;&nbsp;Rata-Rata Hasil Investasi (%)</font></b></td>\n')
  oFile.write('		<td width="150" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="right"><b>\n')
  oFile.write('		<font size="2">'+ strJenisC +'% </font></b></td>\n')
  oFile.write('	</tr>\n')

  ###  --------------------end -------------

  oFile.write('</table>\n')
  
### Tambahan by Ade Herman  - 2011-05-24'
def BuildSQLDanaPaket(config, tgl_investasi):
  sSQL = "SELECT r.kode_paket_investasi as paket,\
          sum(mutasi_iuran_pst) + sum(mutasi_iuran_pk) +\
          sum(mutasi_pengembangan) + sum(mutasi_peralihan) as nominal\
          FROM transaksidplk t, rekeningdplk r \
          WHERE \
          t.no_peserta = r.no_peserta\
          and status_dplk ='A'\
          and isCommitted = 'T'\
          and tgl_transaksi <= '%s'\
          GROUP BY r.kode_paket_investasi\
          ORDER BY r.kode_paket_investasi"  % (tgl_investasi)
  #config.SendDebugMsg(sSQL)
  rSQL = config.CreateSQL(sSQL).RawResult
  	
  return rSQL

def BuildSQLDanaTutup(config, strtgl_investasi):
  sSQL = "select r.kode_paket_investasi as paket ,\
          sum(mutasi_iuran_pk) + sum(mutasi_iuran_pst) +\
          sum(mutasi_pengembangan) + sum(mutasi_peralihan) as nominal\
          from transaksidplk t, rekeningdplk r\
          where \
          t.no_peserta = r.no_peserta\
          and t.iscommitted = 'T'\
          and t.tgl_transaksi < '%s'\
          and r.no_peserta in\
          (\
          	select t.no_peserta\
          	from transaksidplk t, nasabahdplk n\
          	where \
          	t.no_peserta = n.no_peserta\
          	and tgl_registrasi <= '%s'\
          	and kode_jenis_transaksi = 'J'\
          	and t.iscommitted = 'T'\
          	and tgl_transaksi > '%s'\
          )\
          group by r.kode_paket_investasi\
          order by r.kode_paket_investasi"  % (strtgl_investasi, strtgl_investasi, strtgl_investasi)
  #config.SendDebugMsg(sSQL)
  rSQL = config.CreateSQL(sSQL).RawResult
  	
  return rSQL

   
def GetNominalInv(config, cls, jenisinv, strSQLEndDate):
  strSQL = "\
        select \
    	       sum(mutasi_debet) - sum(mutasi_kredit) as nominal_investasi \
             from TransaksiInvestasi t, %s d \
             where isCommitted = 'T' \
    	       and clsfTransaksiInvestasi in (%s) \
    	       and t.id_investasi = d.id_investasi \
    	       and tgl_transaksi <= '%s'"\
             % (jenisinv, cls, strSQLEndDate)
  #config.SendDebugMsg(strSQL)
  res = config.CreateSQL(strSQL).RawResult

  return res.nominal_investasi or 0.0
  
def GetHasilInv(config, jenisinv, strtgl_investasi, strtgl_from):
  strSQL = "\
    select sum(mutasi_kredit) - sum(mutasi_debet) as hasil_investasi \
        from TransaksiInvestasi ti, Investasi i \
        where clsfTransaksiInvestasi = 'C' \
        and isCommitted = 'T' \
        and tgl_transaksi > '%s' \
        and tgl_transaksi <= '%s' \
        and i.id_investasi = ti.id_investasi \
        and i.kode_jns_investasi = '%s'"\
        % (strtgl_investasi, strtgl_from, jenisinv)

  #config.SendDebugMsg(strSQL)
  res = config.CreateSQL(strSQL).RawResult

  return res.hasil_investasi or 0.0
  
  
def BuildSQLProporsiPerPaket(config,strtgl_investasi,strtgl_from):

   strSQL = \
          "select r.kode_paket_investasi as paket, (sum(t.prosenKredit)-sum(t.prosenDebet)) as nominal \
            from rincianinvestasi r, ( \
              select r.kode_paket_investasi as kode_paket_investasi, \
                     r.id_investasi as id_investasi, \
                     (r.proporsi * t.mutasi_kredit) as prosenKredit, \
                     (r.proporsi * t.mutasi_debet) as prosenDebet \
                from rincianinvestasi r, transaksiinvestasi t \
               where r.id_investasi = t.id_investasi \
                 and t.tgl_transaksi >= '%s' \
                 and t.tgl_transaksi < '%s'  \
                 and t.kode_jenis_trinvestasi IN ('E','I') \
               ) t \
          where r.kode_paket_investasi = t.kode_paket_investasi \
            and r.id_investasi = t.id_investasi \
          group by r.kode_paket_investasi ; "\
          % (strtgl_investasi, strtgl_from)

   rSQL = config.CreateSQL(strSQL).RawResult
   return rSQL

###  End 2011-05-24 By Ade herman' ------------


def ConstructReportTrailer(config, oFile):
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('</body>\n')
  oFile.write('\n')
  oFile.write('</html>\n')

def DAFScriptMain(config, parameter, returnpacket):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)

  sBaseFileName = 'investasi_akhir_bulan.htm'
  sFileName = config.UserHomeDirectory + sBaseFileName
  oFile = open(sFileName, 'w')

  ConstructReportHeader(
    config
    , parameter.FirstRecord.monthFrom
    , parameter.FirstRecord.yearFrom
    , parameter.FirstRecord.monthUntil
    , parameter.FirstRecord.yearUntil
    , oFile
  )

  strDateFromSQL = '%d-%d-1' % (parameter.FirstRecord.yearFrom, parameter.FirstRecord.monthFrom)

  dateUntilTmrwDT = config.ModDateTime.EncodeDate(
    parameter.FirstRecord.yearUntil
    , parameter.FirstRecord.monthUntil
    , moduleapi.GetLastDayOfMonth(parameter.FirstRecord.monthUntil, parameter.FirstRecord.yearUntil)
  ) + 1
  strDateUntilTmrwSQL = config.FormatDateTime('yyyy-mm-dd', dateUntilTmrwDT)

  #hasil =ConstructReportHasil( config, parameter.FirstRecord.kode_jns_investasi, strDateFromSQL, strDateUntilTmrwSQL, oFile)

  ConstructReportValues(
    config
    , parameter.FirstRecord.monthFrom
    , parameter.FirstRecord.yearFrom
    , parameter.FirstRecord.monthUntil
    , parameter.FirstRecord.yearUntil
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
