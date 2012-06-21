import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi
import string

def ConstructReportHeader(config,  oFile):
  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Laporan Posisi Performance Cabang</title>\n')
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Arial; line-height:100%; margin-top:0; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td colspan="6" height="20" style="border-left:medium none #000000; border-right:medium none #000000; border-top-style:none; border-top-width:medium; border-bottom-style:none; border-bottom-width:medium">\n')
  oFile.write('		<p align="center"><font size="3" color="#008000"><b>LAPORAN POSISI PERFORMANCE CABANG</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" colspan="4" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font color="#008000"><b>POSISI '+ config.FormatDateTime('d mmmm yyyy', config.Now()) +'</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="3%" align="center" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>NO</b></td>\n')
  oFile.write('		<td width="7%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>KODE CABANG</b></td>\n')
  oFile.write('		<td width="18%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>NAMA CABANG</b></td>\n')
  oFile.write('		<td width="18%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>JUMLAH PESERTA</b></td>\n')
  oFile.write('		<td width="7%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>TOTAL DANA</b></td>\n')
  oFile.write('		<td width="7%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>CABANG (20%)</b></td>\n')
  oFile.write('		<td width="7%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>DPLK (80%)</b></td>\n')

  oFile.write('	</tr>\n')


def strSQLPeserta(config, kode_cabang):
  return \
    'SELECT  '\
    '   count(R.NO_PESERTA) as jmlPeserta, '\
    '   SUM(ISNULL(R.AKUM_DANA_IURAN_PST,0.0))    MUTASI_PESERTA,'\
    '   SUM(ISNULL(R.AKUM_DANA_IURAN_PK,0.0))     MUTASI_PK,'\
    '   SUM(ISNULL(R.AKUM_DANA_PENGEMBANGAN,0.0)) MUTASI_PENGEMBANGAN,'\
    '   SUM(ISNULL(R.AKUM_DANA_PERALIHAN,0.0))    MUTASI_PERALIHAN '\
    'FROM   REKENINGDPLK R, nasabahdplk N '\
    'WHERE N.NO_PESERTA = R.NO_PESERTA '\
    '  AND R.STATUS_DPLK = \'A\' '\
    '  AND R.KODE_CAB_DAFTAR = \'%s\' ;'\
     %(kode_cabang)


def strSQLCabang(config):
  return \
    'select AREA,BRANCH_CODE,BRANCHNAME,TGL_BUKA '\
    'from BRANCHLOCATION '\
    'WHERE BRANCHSTATUS IN ( \'B\',\'S\') '\
     'ORDER BY AREA,BRANCH_CODE';

def ConstructReportValues(config, strSQL, oFile):

  ## query Cabang
  resSQL = config.CreateSQL(strSQL).RawResult

  no_urut = 0
  totPeserta = 0.0
  totDana = 0.0
  totCabang = 0.0
  totDPLK = 0.0
  totCabangAll = 0.0
  totDPLKAll = 0.0
  TotSubPeserta = TotSubDana = TotSubCabang = TotSubDPLK = 0.0
  area = '0000'
  config.SendDebugMsg('masuk......01A')

  dictKodeCabang = {'A001':'AREA SUMBAGUT',\
                    'A002':'AREA SUMBAGSEL',\
                    'A003':'AREA KALIMANTAN',\
                    'A004':'AREA JAWA BARAT',\
                    'A005':'AREA JAWA TENGAH & DIY',\
                    'A006':'AREA JAWA TIMUR',\
                    'A007':'AREA KTI',\
                    'A008':'AREA TIER ONE 1',\
                    'A009':'AREA TIER ONE 2',\
                    'A010':'AREA TIER ONE 3',\
                    'A011':'KPO',\
                    'A999':'OTHERS'}

  resSQL.First()
  while not resSQL.Eof:

    #BranchCode = resSQL.kode_cab_daftar
    config.SendDebugMsg('masuk......02'+ str(resSQL.BRANCH_CODE))
    strSQL = strSQLPeserta(config, resSQL.BRANCH_CODE)
    rSQL = config.CreateSQL(strSQL).RawResult
    config.SendDebugMsg('masuk......032')
    no_urut += 1

    #target = dictJenisTransaksiDPLK[resSQL.kode_cab_daftar])

    akum_iuran_pst    = rSQL.mutasi_peserta or 0.0
    akum_iuran_pk     = rSQL.mutasi_pk or 0.0
    akum_pengembangan = rSQL.mutasi_pengembangan or 0.0
    akum_peralihan    = rSQL.mutasi_peralihan or 0.0
    total_dana = (akum_iuran_pst + akum_iuran_pk + akum_pengembangan + akum_peralihan)
    totCabang = total_dana * (float(20)/100)
    totDPLK   = total_dana * (float(80)/100)

    config.SendDebugMsg('masuk......04')
   # config.SendDebugMsg('area ' + str(float(20/100)))

    if moduleapi.IsOddNumber(no_urut):
      bgcolor = '#EFEFEF'
    else:
      bgcolor = '#FFFFFF'


    if resSQL.area == 'A000':
       config.SendDebugMsg('masuk......05')
       resSQL.Next()
    else:
       nama_area = '%s' % (dictKodeCabang[resSQL.area])
       if area <> resSQL.area:
          if no_urut == 1:
             oFile.write('	<tr>\n')
             oFile.write('		<td width="7%" colspan="7" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#CC6699" height="22">\n')
             oFile.write('		<p align="center"> <b>'+ nama_area +'</b></td>\n')
             oFile.write('	</tr>\n')
          else:
             oFile.write('	<tr>\n')
             oFile.write('		<td width="18%" colspan="3" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
             oFile.write('		<p align="right"><b>Sub Total Area</b></td>\n')
             oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
             oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, TotSubPeserta) +'</td>\n')
             oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
             oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, TotSubDana) +'</td>\n')
             oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
             oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, TotSubCabang) +'</td>\n')
             oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
             oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, TotSubDPLK) +'</td>\n')
             oFile.write('	</tr>\n')
             oFile.write('	<tr>\n')
             oFile.write('		<td width="7%" colspan="7" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#CC6699" height="22">\n')
             oFile.write('		<p align="center"> <b>'+ nama_area +'</b></td>\n')
             oFile.write('	</tr>\n')
             TotSubPeserta = TotSubDana = TotSubCabang = TotSubDPLK = 0.0

       oFile.write('	<tr>\n')
       oFile.write('		<td width="3%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'" height="22">'+ str(no_urut) +'</td>\n')
       oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
       oFile.write('		<p align="center">'+ resSQL.branch_code +'</td>\n')
       oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
       oFile.write('		<p align="left">'+ resSQL.branchname +'</td>\n')
       oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
       oFile.write('		<p align="right">'+ str(rSQL.jmlPeserta) +'</td>\n')
       oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
       oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, total_dana) +'</td>\n')
       oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
       oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, totCabang) +'</td>\n')
       oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
       oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, totDPLK) +'</td>\n')

       oFile.write('	</tr>\n')

       TotSubPeserta += rSQL.jmlPeserta
       TotSubDana += total_dana
       TotSubCabang += totCabang
       TotSubDPLK += totDPLK
       
       area = resSQL.area
       totPeserta += rSQL.jmlPeserta
       totDana  += total_dana
       totCabangAll += totCabang
       totDPLKAll += totDPLK
       resSQL.Next()

  return totPeserta, totDana, totCabangAll, totDPLKAll

def ConstructReportTrailer(config, totPeserta, totDana, totCabangAll, totDPLKAll,oFile):
  oFile.write('	<tr>\n')
  oFile.write('		<td width="44%" colspan="3" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" colspan="6" bgcolor="#CC6699">\n')
  oFile.write('		<b>TOTAL PESERTA</b></td>\n')
  oFile.write('		<td width="9%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totPeserta) +'</b></td>\n')
  oFile.write('		<td width="9%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totDana) +'</b></td>\n')
  oFile.write('		<td width="9%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totCabangAll) +'</b></td>\n')
  oFile.write('		<td width="9%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totDPLKAll) +'</b></td>\n')

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

  #BranchCode = parameter.FirstRecord.kode_cabang

  #tgl_transaksi_awal = parameter.FirstRecord.tanggal_awal
  #tgl_transaksi_akhir = parameter.FirstRecord.tanggal_akhir
  
  #config.SendDebugMsg('masuk......02')
  #strTanggalAwal = config.FormatDateTime('dd mmmm yyyy',tgl_transaksi_awal)
  #strTanggalAkhir = config.FormatDateTime('dd mmmm yyyy',tgl_transaksi_akhir)
  ConstructReportHeader(config, oFile)

  strSQL = strSQLCabang(config)
  config.SendDebugMsg(strSQL)

  totPeserta, totReferensi, totDanaCabang, totDanaDPLK = ConstructReportValues(config, strSQL, oFile)

  ConstructReportTrailer(
    config, totPeserta
    , totReferensi
    , totDanaCabang
    , totDanaDPLK
    , oFile
  )

def CreateReport(config, parameter, returnpacket):
  sBaseFileName = 'Laporan_Sip_Branch.htm'
  sFileName = config.UserHomeDirectory + sBaseFileName
  #config.SendDebugMsg('masuk......')
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

