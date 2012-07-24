import sys, string
import com.ihsan.util.modman as modman
import com.ihsan.foundation.appserver as appserver

modman.loadStdModules(globals(),
  [
    "moduleapi",
    "transaksiapi"
  ]
)

def Terbilang(x):

  Hasil = ''
  satuan=["","Satu","Dua","Tiga","Empat","Lima","Enam","Tujuh",\
          "Delapan","Sembilan","Sepuluh","Sebelas"]

  n = int(x)

  if n >= 0 and n <= 11:
    Hasil = " " + satuan[n]
  elif n >= 12 and n <= 19:
    Hasil = Terbilang(n % 10) + " Belas"
  elif n >= 20 and n <= 99:
    Hasil = Terbilang(n / 10) + " Puluh" + Terbilang(n % 10)
  elif n >= 100 and n <= 199:
    Hasil = " Seratus" + Terbilang(n - 100)
  elif n >= 200 and n <= 999:
    Hasil = Terbilang(n / 100) + " Ratus" + Terbilang(n % 100)
  elif n >= 1000 and n <= 2000:
    Hasil = " Seribu" + Terbilang(n - 1000)
  elif n >= 2000 and n <= 1000000:
	 	Hasil = Terbilang(n / 1000) + " Ribu" + Terbilang(n % 1000)
  elif n >= 1000000 and n < 1000000000:
	 	Hasil = Terbilang(n / 1000000) + " Ribu" + Terbilang(n % 1000000)


  return Hasil
	

def ConstructReportHeader(config
       , strSQL
       , oFile ):
       
  dictBulan = {'01':'Januari','02':'Februari','03':'Maret',\
               '04':'April','05':'Mei','06':'Juni',\
               '07':'Juli','08':'Agustus','09':'September',\
               '10':'Oktober','11':'November','12':'Desember'}

  dictBulanRomawi = {'01':'I','02':'II','03':'III','04':'IV',\
                     '05':'V','06':'VI','07':'VII','08':'VIII',
                     '09':'IX','10':'X','11':'XI','12':'XII'}

  resSQL = config.CreateSQL(strSQL).RawResult
  resSQL.First()

  strSQL = strSQLTunggakanPremi(config, resSQL.NO_PESERTA)
  rSQL = config.CreateSQL(strSQL).RawResult


  y, m, d = resSQL.tgl_akseptasi[:3]
      # tanggal dengan format dd/mm/yyyy

  tglPremi = config.FormatDateTime('dd',\
    config.ModLibUtils.EncodeDate(y,m,d))

  blnPremi = config.FormatDateTime('mm',\
    config.ModLibUtils.EncodeDate(y,m,d))

  thnPremi = config.FormatDateTime('yyyy',\
    config.ModLibUtils.EncodeDate(y,m,d))

  tglNow = config.FormatDateTime('dd', config.Now())
  blnNow = config.FormatDateTime('mm', config.Now())
  thnNow = config.FormatDateTime('yyyy', config.Now())
  
  nama_bulan = '%s' % (dictBulan[blnPremi])
  tglAkseptasi = tglPremi+' '+nama_bulan+' '+thnPremi

  nama_bulan = '%s' % (dictBulan[blnNow])
  tglCetak = tglNow+' '+nama_bulan+' '+thnNow
  
  bulan_romawi = '%s' % (dictBulanRomawi[blnPremi])
  #no_surat = str(resSQL.rekeningwasiatummat_id)+'/BMI/DPLK-PREMI/'+ bulan_romawi+'/'+thnPremi
  no_surat = rSQL.no_surat
  
  premi    = resSQL.besar_premi or 0.0

  #manfaat_pensiun = resSQL.manfaat_asuransi or 0.0
  #terbilangManfaat = Terbilang(manfaat_pensiun)
  
  jmlBulanTunggak = resSQL.bln_tunggakan_wasiat_ummat or 0.0
  blnTerbilang = Terbilang(jmlBulanTunggak)
  nomTunggakan = resSQL.kewajiban_wasiat_ummat or 0.0
  terbilanNomTunggakan = Terbilang(nomTunggakan)
  
  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Simulasi</title>\n')
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Times New Roman; FONT-SIZE: 12 ; line-height:100%; margin-top:5; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('<table style=" border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="0" width="100%" id="table1" cellpadding="1">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="50%" align="left" style="border-left:0 none; border-right-style:none; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		No : '+no_surat+'</b></td>\n')
  oFile.write('		<td width="50%" align="right" style="border-left:0 none; border-right-style:none; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		Jakarta, '+tglCetak+'</td>\n')
  oFile.write('	</tr>\n')
  oFile.write('</table>\n')

  oFile.write('<table style=" border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="0" width="100%" id="table1" cellpadding="1">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="90%" align="center" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		&nbsp;</b></td>\n')
  oFile.write('	</tr>\n')

  oFile.write('<table style="border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="0" width="100%" id="table1" cellpadding="1">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" align="left" style="border-left:0 none; border-right-style:none; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		Kepada Yth.</td>')
  oFile.write('	</tr>\n')

  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" align="left" style="border-left:0 none; border-right-style:none ; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		Bapak/Ibuk '+resSQL.nama_lengkap+' ('+resSQL.no_peserta+')</td>')
  oFile.write('		<td width="100%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff"></td>\n')
  oFile.write('	</tr>\n')

  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" align="left" style="border-left:0 none; border-right-style: none; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		Perihal : <u>Tunggakan Pembayaran Premi </u></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" align="left" style="border-left:0 none; border-right-style:none; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('	&nbsp; </td>\n')
  oFile.write('	</tr>\n')

  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" align="left" style="border-left:0 none; border-right-style:none; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write("		<b><i>Assalamu'alaikum Warahmatullahi Wabarakatuh</b></i></td>\n")
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" align="left" style="border-left:0 none; border-right-style:none; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('	&nbsp; </td>\n')
  oFile.write('	</tr>\n')

  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" align="left" style="border-left:0 none; border-right-style:none; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write("		Semoga Allah Subhanahu Wata'ala senantiasa memberikan Taufik dan Hidayah-Nya kepada kita ")
  oFile.write('		 semua dalam menjalankan aktifitas sehari-hari. </td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" align="left" style="border-left:0 none; border-right-style:none; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('	&nbsp; </td>\n')
  oFile.write('	</tr>\n')

  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" align="left" style="border-left:0 none; border-right-style:none; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		Bersama ini kami sampaikan bahwa Bapak/Ibu sudah '+str(jmlBulanTunggak) +' ('+blnTerbilang+') bulan tidak melakukan pembayaran premi. Jika sampai 1 (satu) bulan ke depan ')
  oFile.write('		Bapak/Ibu tidak melakukan pembayaran premi tersebut, maka status kepesertaan Wasiat Ummatnya dinyatakan gugur.</td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" align="left" style="border-left:0 none; border-right-style:none; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('	&nbsp; </td>\n')
  oFile.write('	</tr>\n')

  oFile.write('<table style=" border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="0" width="100%" id="table1" cellpadding="1">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="90%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		Pembayaran dapat dilakukan secara tunai di seluruh cabang Bank Muamalat, melalui')
  oFile.write('		transfer dari bank lain atau menggunakan fasilitas Auto Debet. Pembayaran Premi')
  oFile.write('		DPLK ditujukan ke : </td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="2%" align="top" style="border-left:0 none; border-right-style:none; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		&nbsp;</td>\n')
  oFile.write('	</tr>\n')

  oFile.write('<table style=" border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="0" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="90%" align="center" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		<b>Rekening No. 301.00443.15 untuk Iuran Premi Wasiat Ummat </b> </td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="2%" align="top" style="border-left:0 none; border-right-style:none; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		&nbsp;</td>\n')
  oFile.write('	</tr>\n')

  oFile.write('<table style=" border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="0" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="2%" align="top" style="border-left:0 none; border-right-style:none; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		Demikian hal ini disampaikan. Atas perhatiannya kami ucapkan terima kasih.</td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="2%" align="top" style="border-left:0 none; border-right-style:none; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		&nbsp;</td>\n')
  oFile.write('	</tr>\n')
  oFile.write('</table>\n')

  oFile.write('<table style=" border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="0" width="100%" id="table1" cellpadding="1">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" align="left" style="border-left:0 none; border-right-style:none; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write("		<b><i>Wabillahi Taufik Wal Hidayah</b></i></td>\n")
  oFile.write('	</tr>\n')

  oFile.write('<table style=" border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="0" width="100%" id="table1" cellpadding="1">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" align="left" style="border-left:0 none; border-right-style:none; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write("		<b><i>Wassalaamu'alaikum Warahmatullaahi Wabarakatuh</b></i></td>\n")
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" align="left" style="border-left:0 none; border-right-style:none; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('	&nbsp; </td>\n')
  oFile.write('	</tr>\n')

  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" align="center" style="border-left:0 none; border-right-style:none; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('	<b>DPLK Muamalat</b> </td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" align="left" style="border-left:0 none; border-right-style:none; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('	&nbsp; </td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" align="left" style="border-left:0 none; border-right-style:none; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('	&nbsp; </td>\n')
  oFile.write('	</tr>\n')

  oFile.write('<table style=" border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="0" width="100%" id="table1" cellpadding="1">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="50%" align="center" style="border-left:0 none; border-right-style:none; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		<b><u>Nur Alfa Agustina</u></b></td>\n')
  oFile.write('		<td width="50%" align="center" style="border-left:0 none; border-right-style:none; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		<b><u>Yuniar Mustofa</u></b></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="50%" align="center" style="border-left:0 none; border-right-style:none; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		Pelaksana Tugas Pengurus</td>\n')
  oFile.write('		<td width="50%" align="center" style="border-left:0 none; border-right-style:none; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		Team Leader Operasional/Adm</td>\n')
  oFile.write('	</tr>\n')
  oFile.write('</table>\n')


def ConstructReportTrailer(config, oFile):

  # Keterangan
  oFile.write('<table style=" border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="0" width="100%" id="table1" cellpadding="1">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" align="left" style="border-left:0 none; border-right-style:none; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('	&nbsp; </td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="%" align="left" style=""FONT-FAMILY: Times New Roman; FONT-SIZE: 8; border-left:0 none; border-right-style:none; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:0 none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		<font size=1><b><i>Note: </b></i> &nbsp;Premi Wasiat Ummat bukan bersifat tabungan oleh karenanya Premi tersebut tidak termasuk komponen DPLK Muamalat.</td>\n')
  oFile.write('	</tr>\n')
  oFile.write('</table>\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('</body>\n')
  oFile.write('\n')
  oFile.write('</html>\n')

def strSQLDataWu(config, no_peserta):
  return \
    'select n.NO_PESERTA '\
    '     , n.NAMA_LENGKAP '\
    '     , r.BLN_TUNGGAKAN_WASIAT_UMMAT '\
    '     , r.KEWAJIBAN_WASIAT_UMMAT '\
    '     , wu.BESAR_PREMI '\
    '     , wu.MANFAAT_ASURANSI '\
    '     , wu.TGL_AKSEPTASI '\
    '     , wu.REKENINGWASIATUMMAT_ID '\
    'from NASABAHDPLK n'\
    '   , REKINVDPLK r '\
    '   , REKASURANSI wu '\
    '   , TUNGGAKANPREMI tp '\
    'where n.no_peserta = r.no_peserta '\
    '  and r.no_peserta = wu.no_peserta '\
    '  AND r.status_wasiat_ummat = \'T\' '\
    '  and r.status_dplk = \'A\' '\
    '  and n.NO_PESERTA = \'%s\' '\
    '  and r.BLN_TUNGGAKAN_WASIAT_UMMAT >= 1'\
     %( no_peserta )


def strSQLTunggakanPremi(config, no_peserta):
  return \
    'select ID_TUNGGAKANPREMI, NO_SURAT '\
    'from TUNGGAKANPREMI '\
    'where NO_PESERTA = \'%s\' '\
    'ORDER BY ID_TUNGGAKANPREMI DESC '\
     %( no_peserta )

def WriteToFile(config, parameter, oFile):

  no_rekening = parameter.FirstRecord.no_rekening
  strSQL = strSQLDataWu(config, no_rekening)

  ConstructReportHeader(
     config
     , strSQL
     , oFile)

  ConstructReportTrailer(
    config
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
