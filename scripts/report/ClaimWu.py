import sys, string
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi, transaksiapi

def ConstructReportHeader(config
     , no_peserta
     , nama_lengkap
     , tanggal_registrasi
     , tanggal_akseptasi
     , tanggal_pensiun
     , besar_premi
     , manfaat_pensiun
     , lama_kepesertaan
     , sisa_kepesertaan
     , masa_dijalani
     , manfaat_diterima
     , oFile ):

  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Simulasi</title>\n')
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Arial; line-height:60%; margin-top:0; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="0" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td colspan="8" height="20" style="border-left:0; border-right:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0">\n')
  oFile.write('		<p align="left"><font size="3" color="#008000"><b>Perhitungan Pengcoveran Asuransi</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('</table>\n')

  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="0" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td colspan="8" height="20" style="border-left:0; border-right:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0">\n')
  oFile.write('		<p align="left"><font size="3" color="#008000"></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('</table>\n')

  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="7%" align="left" style="border-left:0 none; border-right-style:solid; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		Nomor Peserta</td>\n')
  oFile.write('		<td width="2%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		:</td>\n')
  oFile.write('		<td width="10%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		 '+string.upper(no_peserta) + '</td>\n')
  oFile.write('	</tr>\n')

  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="7%" align="left" style="border-left:0 none; border-right-style:solid; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		Nama Peserta</td>\n')
  oFile.write('		<td width="2%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		:</td>\n')
  oFile.write('		<td width="10%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		 '+string.upper(nama_lengkap) + '</td>\n')
  oFile.write('	</tr>\n')

  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="7%" align="left" style="border-left:0 none; border-right-style:solid; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		Premi</td>\n')
  oFile.write('		<td width="2%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		:</td>\n')
  oFile.write('		<td width="10%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		 '+moduleapi.FormatFloatStd(config, besar_premi, '-') + '</td>\n')
  oFile.write('	</tr>\n')

  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="7%" align="left" style="border-left:0 none; border-right-style:solid; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		Manfaat Asuransi Yg Dicover</td>\n')
  oFile.write('		<td width="2%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		:</td>\n')
  oFile.write('		<td width="10%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		 '+moduleapi.FormatFloatStd(config, manfaat_pensiun, '-') + '</td>\n')
  oFile.write('	</tr>\n')

  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="7%" align="left" style="border-left:0 none; border-right-style:solid; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		Tanggal AkseptasiPremi</td>\n')
  oFile.write('		<td width="2%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		:</td>\n')
  oFile.write('		<td width="10%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		 '+config.FormatDateTime('dd mmmm yyyy',tanggal_akseptasi)+ '</td>\n')
  oFile.write('	</tr>\n')

  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="7%" align="left" style="border-left:0 none; border-right-style:solid; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		Jatuh Tempo</td>\n')
  oFile.write('		<td width="2%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		:</td>\n')
  oFile.write('		<td width="10%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		 '+config.FormatDateTime('dd mmmm yyyy',tanggal_pensiun)+ '</td>\n')
  oFile.write('	</tr>\n')
  
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="7%" align="left" style="border-left:0 none; border-right-style:solid; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		Meninggal Dunia</td>\n')
  oFile.write('		<td width="2%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		:</td>\n')
  oFile.write('		<td width="10%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		 '+config.FormatDateTime('dd mmmm yyyy',tanggal_registrasi)+ '</td>\n')
  oFile.write('	</tr>\n')

  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="7%" align="left" style="border-left:0 none; border-right-style:solid; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		Lama Kepesertaan</td>\n')
  oFile.write('		<td width="2%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		:</td>\n')
  oFile.write('		<td width="10%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		 '+str(lama_kepesertaan)+ ' (bln)</td>\n')
  oFile.write('	</tr>\n')

  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="7%" align="left" style="border-left:0 none; border-right-style:solid; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		Sisa Kepesertaan</td>\n')
  oFile.write('		<td width="2%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		:</td>\n')
  oFile.write('		<td width="10%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		 '+str(sisa_kepesertaan)+ ' (bln)</td>\n')
  oFile.write('	</tr>\n')

  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="7%" align="left" style="border-left:0 none; border-right-style:solid; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		Kepesertaan Yg Sudah Dijalani</td>\n')
  oFile.write('		<td width="2%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		:</td>\n')
  oFile.write('		<td width="10%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		 '+str(masa_dijalani)+ ' (bln)</td>\n')
  oFile.write('	</tr>\n')

  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="7%" align="left" style="border-left:0 none; border-right-style:solid; border-right-width:0; border-top-style:none; border-top-width:0; border-bottom-style:none; border-bottom-width:0" bgcolor="#ffffff">\n')
  oFile.write('		Manfaat yang diterima</td>\n')
  oFile.write('		<td width="2%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		:</td>\n')
  oFile.write('		<td width="10%" align="left" style="border-style: none; border-width: 0; " bgcolor="#ffffff">\n')
  oFile.write('		 '+moduleapi.FormatFloatStd(config, manfaat_diterima, '-')+ '</td>\n')
  oFile.write('	</tr>\n')


def ConstructReportTrailer(config, oFile):

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

def strSQLDetail(config, no_peserta):
  return \
    'select n.NO_PESERTA '\
    '     , n.NAMA_LENGKAP '\
    '     , u.TGL_AKSEPTASI '\
    '     , r.TGL_PENSIUN '\
    '     , u.BESAR_PREMI '\
    '     , u.MANFAAT_ASURANSI '\
    'from NASABAHDPLK n'\
    '   , REKENINGDPLK r '\
    '   , REKENINGWASIATUMMAT U '\
    'where n.no_peserta = r.no_peserta '\
    '  and r.no_peserta = u.no_peserta '\
    '  and n.NO_PESERTA = \'%s\' '\
     %( no_peserta
    )


def WriteToFile(config, parameter, oFile):

  no_peserta = parameter.FirstRecord.nama_lengkap
  strSQL = strSQLDetail(config, no_peserta)
  rSQL = config.CreateSQL(strSQL).RawResult
  #config.SendDebugMsg(resSQL)

  if (rSQL.nama_lengkap == None or rSQL.nama_lengkap == ''):
     raise Exception, 'Error' + '\nBukan Peserta Wasiat Ummat.....!'
  else:
     nama_lengkap        = rSQL.nama_lengkap
     y, m, d             = rSQL.tgl_akseptasi[:3]
     tanggal_akseptasi   = config.ModDateTime.EncodeDate(y, m, d)
     y, m, d             = rSQL.tgl_pensiun[:3]
     tanggal_pensiun     = config.ModDateTime.EncodeDate(y, m, d)
     besar_premi         = rSQL.besar_premi or 0.0
     manfaat_pensiun     = rSQL.manfaat_asuransi or 0.0
     manfaat_diterima    = 0.0

     tgl_registrasi      = parameter.FirstRecord.tanggal_registrasi

     tglMeninggal        = config.ModDateTime.DecodeDate(tgl_registrasi)
     y_Meninggal         = int(tglMeninggal[0])
     m_Meninggal         = int(tglMeninggal[1])

     tglAkseptasi        = config.ModDateTime.DecodeDate(tanggal_akseptasi)
     y_Akseptasi         = int(tglAkseptasi[0])
     m_Akseptasi         = int(tglAkseptasi[1])

     tglPensiun          = config.ModDateTime.DecodeDate(tanggal_pensiun)
     y_Pensiun           = int(tglPensiun[0])
     m_Pensiun           = int(tglPensiun[1])
  
     lama_kepesertaan    = (m_Pensiun + (12 - m_Akseptasi + 1)) + (((y_Pensiun - 1) - (y_Akseptasi + 1))+1)*12
     sisa_kepesertaan    = (m_Pensiun + (12 - m_Meninggal)) + (((y_Pensiun - 1) - (y_Meninggal + 1))+1)*12
     masa_dijalani       = (lama_kepesertaan - sisa_kepesertaan )
     manfaat_diterima    = manfaat_pensiun * (float(sisa_kepesertaan)/float(lama_kepesertaan))

  ConstructReportHeader(
     config
     , no_peserta
     , nama_lengkap
     , tgl_registrasi
     , tanggal_akseptasi
     , tanggal_pensiun
     , besar_premi
     , manfaat_pensiun
     , lama_kepesertaan
     , sisa_kepesertaan
     , masa_dijalani
     , manfaat_diterima
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

