import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi
import string

def ConstructReportHeader(config, strTanggalAwal, strTanggalAkhir, oFile):
  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Laporan Akumulasi Peserta Corporate</title>\n')
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Arial; line-height:100%; margin-top:0; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td colspan="4" height="20" style="border-left:medium none #000000; border-right:medium none #000000; border-top-style:none; border-top-width:medium; border-bottom-style:none; border-bottom-width:medium">\n')
  oFile.write('		<p align="center"><font size="3" color="#008000"><b>LAPORAN BERDASARKAN KELOMPOK UMUR </b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" colspan="4" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font color="#008000"><b>PERIODE '+ string.upper(strTanggalAwal) +' HINGGA '+ string.upper(strTanggalAkhir) +'</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="7%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>KELOMPOK UMUR</b></td>\n')
  oFile.write('		<td width="18%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>P R I A</b></td>\n')
  oFile.write('		<td width="18%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>WANITA</b></td>\n')
  oFile.write('		<td width="18%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>PRIA/WANITA</b></td>\n')
  oFile.write('		<td width="18%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>T O T A L</b></td>\n')

  oFile.write('	</tr>\n')


def strSQLDaftarPeserta(config, tgl_transaksi_awal, tgl_transaksi_akhir_plus):
  return \
    'select n.NO_PESERTA,n.TANGGAL_LAHIR,n.JENIS_KELAMIN  '\
    'from NasabahDPLK n '\
    '  , RekeningDPLK r '\
    'where n.no_peserta = r.no_peserta '\
    '  and n.tgl_registrasi >= \'%s\' '\
    '  and n.tgl_registrasi < \'%s\' '\
    '  and r.STATUS_DPLK IN (\'A\',\'S\'); '\
    % (config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_awal)\
       , config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_akhir_plus)\
    )


def ConstructReportValues(config, strSQL, tgl_transaksi_awal, tgl_transaksi_akhir_plus, oFile):
  resSQL = config.CreateSQL(strSQL).RawResult

  no_urut =  0
  p20 = p21 = p31 = p41 = p46 = p55 = 0
  w20 = w21 = w31 = w41 = w46 = w55 = 0
  o20 = o21 = o31 = o41 = o46 = o55 = 0
  totPeserta = 0.0
  
  oParameter = config.CreatePObjImplProxy('Parameter')
  oParameter.Key = 'JUMLAH_HARI_SETAHUN'
  JumlahHariSetahun = oParameter.Numeric_Value


  config.SendDebugMsg('Mulai ')
  resSQL.First()
  while not resSQL.Eof:

    config.SendDebugMsg('Masuk ')
    y, m, d             = resSQL.tanggal_lahir[:3]
    tgl_lahir = config.ModDateTime.EncodeDate(y, m, d)

    umur = int((tgl_transaksi_akhir_plus - tgl_lahir)/JumlahHariSetahun)
    
    
    if resSQL.jenis_kelamin == 'P':
       config.SendDebugMsg('P')
       if umur < 21:
          p20 += 1
       if umur > 20:
          if umur < 31:
             p21 += 1

       if umur > 30:
          if umur < 41:
             p31 += 1

       if umur > 40:
          if umur < 46:
             p41 += 1

       if umur > 45:
          if umur < 56:
             p46 += 1
       if umur > 55:
          p55 += 1

    elif  resSQL.jenis_kelamin == 'L':
       config.SendDebugMsg('L')
       if umur < 21:
          p20 += 1
       if umur > 20:
          if umur < 31:
             p21 += 1

       if umur > 30:
          if umur < 41:
             p31 += 1

       if umur > 40:
          if umur < 46:
             p41 += 1

       if umur > 45:
          if umur < 56:
             p46 += 1
       if umur > 55:
          p55 += 1

    elif resSQL.jenis_kelamin == 'W':
       config.SendDebugMsg('W')
       if umur < 21:
          w20 += 1
       if umur > 20:
          if umur < 31:
             w21 += 1

       if umur > 30:
          if umur < 41:
             w31 += 1

       if umur > 40:
          if umur < 46:
             w41 += 1

       if umur > 45:
          if umur < 56:
             w46 += 1
       if umur > 55:
          w55 += 1

    else:
       config.SendDebugMsg('O')
       if umur < 21:
          o20 += 1
       if umur > 20:
          if umur < 31:
             o21 += 1

       if umur > 30:
          if umur < 41:
             o31 += 1

       if umur > 40:
          if umur < 46:
             o41 += 1

       if umur > 45:
          if umur < 56:
             o46 += 1
       if umur > 55:
          o55 += 1


    t20 = p20 + w20 + o20
    t21 = p21 + w21 + o21
    t31 = p31 + w31 + o31
    t41 = p41 + w41 + o41
    t46 = p46 + w46 + o46
    t55 = p55 + w55 + o55

    totPeserta += 1
    
    resSQL.Next()

  bgcolor1 = '#EFEFEF'
  bgcolor2 = '#FFFFFF'

  oFile.write('	<tr>\n')
  oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="center">Dibawah 20 Tahun</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p20) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(w20) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(o20) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(t20) +'</td>\n')
  oFile.write('	</tr>\n')
  oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor2 +'" height="22">\n')
  oFile.write('		<p align="center">21 s.d 30 tahun</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor2 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p21) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor2 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(w21) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor2 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(o21) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor2 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(t21) +'</td>\n')
  oFile.write('	</tr>\n')
  oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="center">31 s.d 40 tahun</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p31) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(w31) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(o31) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(t31) +'</td>\n')
  oFile.write('	</tr>\n')
  oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor2 +'" height="22">\n')
  oFile.write('		<p align="center">41 s.d 45 tahun</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor2 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p41)+'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor2 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(w41)+'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor2 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(o41)+'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor2 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(t41)+'</td>\n')
  oFile.write('	</tr>\n')
  oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="center">46 s.d 55 tahun</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p46) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(w46) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(o46) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor1 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(t46) +'</td>\n')
  oFile.write('	</tr>\n')
  oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor2 +'" height="22">\n')
  oFile.write('		<p align="center">diatas 55 tahun</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor2 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(p55) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor2 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(w55) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor2 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(o55) +'</td>\n')
  oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor2 +'" height="22">\n')
  oFile.write('		<p align="right">'+ str(t55) +'</td>\n')
  oFile.write('	</tr>\n')


  return totPeserta

def ConstructReportTrailer(config, totPeserta, oFile):
  oFile.write('	<tr>\n')
  oFile.write('		<td width="44%" colspan="4" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" colspan="6" bgcolor="#CC6699">\n')
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
  sBaseFileName = 'Kelompok_Umur.htm'
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

