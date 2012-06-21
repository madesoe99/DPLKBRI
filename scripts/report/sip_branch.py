import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi
import string

def ConstructReportHeader(config, strTanggalAwal, strTanggalAkhir, oFile):
  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Laporan SIP Branch</title>\n')
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Arial; line-height:100%; margin-top:0; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td colspan="4" height="20" style="border-left:medium none #000000; border-right:medium none #000000; border-top-style:none; border-top-width:medium; border-bottom-style:none; border-bottom-width:medium">\n')
  oFile.write('		<p align="center"><font size="3" color="#008000"><b>LAPORAN SIP BRANCH</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" colspan="4" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font color="#008000"><b>PERIODE '+ string.upper(strTanggalAwal) +' HINGGA '+ string.upper(strTanggalAkhir) +'</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="3%" align="center" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>NO</b></td>\n')
  oFile.write('		<td width="7%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>KODE CABANG</b></td>\n')
  oFile.write('		<td width="18%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>NAMA CABANG</b></td>\n')
  oFile.write('		<td width="18%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>TARGET</b></td>\n')
  oFile.write('		<td width="7%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>PEROLEHAN</b></td>\n')
  oFile.write('		<td width="7%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>JUMLAH REFERRAL</b></td>\n')

  oFile.write('	</tr>\n')


def strSQLPeserta(config, kode_cabang,tgl_transaksi_awal, tgl_transaksi_akhir_plus):
  return \
    'select  count(n.no_peserta) as jmlPeserta '\
    '       ,count(distinct(n.no_referensi)) as jmlReferensi '\
    'from NasabahDPLK n '\
    '  , RekeningDPLK r '\
    'where n.no_peserta = r.no_peserta '\
    '  and n.tgl_registrasi >= \'%s\' '\
    '  and n.tgl_registrasi < \'%s\' '\
    '  and r.kode_cab_daftar = \'%s\' ;'\
    % (config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_awal)\
       , config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_akhir_plus)\
       , kode_cabang \
    )

#def strSQLSumValues(config, kode_cabang):
#  return \
#    'select Branch_Code,BranchName '\
#    'from BRANCHLOCATION '\
#    'where Branch_Code = \'%s\' '\
#     %( kode_cabang
#    )

def strSQLCabang(config):
  return \
    'select AREA,BRANCH_CODE,BRANCHNAME,BRANCHSTATUS '\
    'from BRANCHLOCATION '\
    'ORDER BY AREA,BRANCH_CODE';


def ConstructReportValues(config, strSQL, tgl_transaksi_awal, tgl_transaksi_akhir_plus, oFile):
  resSQL = config.CreateSQL(strSQL).RawResult

  no_urut = 0
  totPeserta = 0.0
  totReferensi = 0.0
  area = '0000'
  totSubPeserta = totSubReferral =  0.0
  config.SendDebugMsg('masuk......01')
  
  dictKodeCabang = {
      '101':240,'102':120,'103':120,'104':120,'105':120,'106':120,'121':240,\
      '131':240,'132':120,'141':240,'151':240,'161':240,'211':240,\
      '212':120,'213':120,'221':240,'231':240,'232':120,\
      '241':240,'242':120,'251':240,'261':240,'262':120,'301':240,'298':120,\
      '302':120,'303':240,'304':240,'305':240,'306':120,\
      '307':120,'308':240,'309':240,'310':240,'311':120,\
      '312':240,'313':240,'314':240,'315':120,'316':240,'317':240,\
      '318':240,'319':240,'320':240,'321':240,'322':240,\
      '323':240,'324':240,'325':240,'326':240,'327':240,\
      '328':240,'329':240,'330':240,'331':120,'332':120,'333':240,\
      '334':120,'335':120,'336':120,'337':120,'338':120,'339':120,\
      '340':120,'351':240,'352':120,'353':120,'354':120,\
      '355':120,'361':240,'371':240,'372':120,'373':120,\
      '411':240,'421':240,'422':120,'423':120,'424':120,\
      '431':240,'432':120,'441':240,'451':240,'501':240,\
      '502':120,'503':120,'504':120,'505':120,'506':120,\
      '507':120,'508':120,'509':120,'510':120,'511':240,\
      '512':120,'513':120,'514':120,'515':120,'521':240,'522':120,'523':120,'524':120,\
      '525':120,'526':120,'527':120,'531':240,'541':240,'542':120,'601':240,\
      '602':240,'603':120,'604':120,'605':120,'606':120,'607':120,\
      '611':240,'621':240,'622':120,'631':240,'632':120,'701':240,\
      '702':120,'703':120,'704':120,'705':120,'711':240,'712':120,'713':120,'714':120,\
      '721':240,'722':120,'723':0.0,'731':240,'732':120,\
      '733':120,'741':240,'742':120,'743':120,'744':120,'745':120,'746':120,'747':120,\
      '751':240,'752':120,'753':120,'761':240,'771':240,'772':120,\
      '801':240,'802':120,'803':120,'804':120,'811':240,\
      '821':240,'822':120,'823':120,'824':120,'831':240,'832':120,'852':120,\
      '841':240,'842':120,'851':240,'861':240,'862':120,\
      '871':240,'881':240,'882':120,'883':120,'891':240,'341':120}

  dictArea = {
              'A001':'AREA SUMBAGUT',\
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
              'A999':'KPNO'}

  
  resSQL.First()
  while not resSQL.Eof:

    #BranchCode = resSQL.kode_cab_daftar
    config.SendDebugMsg('masuk......01')
    strSQL = strSQLPeserta(config, resSQL.BRANCH_CODE,tgl_transaksi_awal, tgl_transaksi_akhir_plus)
    rSQL = config.CreateSQL(strSQL).RawResult
    
    no_urut += 1

    #target = dictJenisTransaksiDPLK[resSQL.kode_cab_daftar])
    #config.SendDebugMsg('tes....'+resSQL.BRANCH_CODE +' : '+str(target))

    if moduleapi.IsOddNumber(no_urut):
      bgcolor = '#EFEFEF'
    else:
      bgcolor = '#FFFFFF'


    if resSQL.area == 'A000':
       config.SendDebugMsg('masuk......05')
       resSQL.Next()
    else:
       if resSQL.BRANCHSTATUS =='B':
          target = 240
       if resSQL.BRANCHSTATUS =='S':
          target = 120

       nama_area = '%s' % (dictArea[resSQL.area])
       #target = '%s' % (dictKodeCabang[resSQL.BRANCH_CODE])
       
       if area <> resSQL.area:
          if no_urut == 1:
             oFile.write('	<tr>\n')
             oFile.write('		<td width="7%" colspan="6" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#CC6699" height="22">\n')
             oFile.write('		<p align="center"> <b>'+ nama_area +'</b></td>\n')
             oFile.write('	</tr>\n')
          else:
             oFile.write('	<tr>\n')
             oFile.write('		<td width="18%" colspan="4" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
             oFile.write('		<p align="right"><b>Sub Total Area</b></td>\n')
             oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
             oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, totSubPeserta) +'</td>\n')
             oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
             oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, totSubReferral) +'</td>\n')
             oFile.write('	</tr>\n')
             oFile.write('	<tr>\n')
             oFile.write('		<td width="7%" colspan="6" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#CC6699" height="22">\n')
             oFile.write('		<p align="center"> <b>'+ nama_area +'</b></td>\n')
             oFile.write('	</tr>\n')
             
             totSubPeserta = totSubReferral =  0.0


       oFile.write('	<tr>\n')
       oFile.write('		<td width="3%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'" height="22">'+ str(no_urut) +'</td>\n')
       oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
       oFile.write('		<p align="center">'+ resSQL.branch_code +'</td>\n')
       oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
       oFile.write('		<p align="left">'+ resSQL.branchname +'</td>\n')
       oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
       oFile.write('		<p align="right">'+ str(target) +'</td>\n')
       oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
       oFile.write('		<p align="right">'+ str(rSQL.jmlPeserta) +'</td>\n')
       oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
       oFile.write('		<p align="right">'+ str(rSQL.jmlReferensi) +'</td>\n')
       oFile.write('	</tr>\n')

       area = resSQL.area
       totPeserta += rSQL.jmlPeserta
       totReferensi += rSQL.jmlReferensi
       totSubPeserta += rSQL.jmlPeserta
       totSubReferral += rSQL.jmlReferensi
       resSQL.Next()

  return totPeserta, totReferensi

def ConstructReportTrailer(config, totPeserta, totReferensi, oFile):
  oFile.write('	<tr>\n')
  oFile.write('		<td width="44%" colspan="4" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" colspan="6" bgcolor="#CC6699">\n')
  oFile.write('		<b>TOTAL PESERTA</b></td>\n')
  oFile.write('		<td width="9%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totPeserta) +'</b></td>\n')
  oFile.write('		<td width="9%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totReferensi) +'</b></td>\n')
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

  tgl_transaksi_awal = parameter.FirstRecord.tanggal_awal
  tgl_transaksi_akhir = parameter.FirstRecord.tanggal_akhir
  
  #config.SendDebugMsg('masuk......02')
  strTanggalAwal = config.FormatDateTime('dd mmmm yyyy',tgl_transaksi_awal)
  strTanggalAkhir = config.FormatDateTime('dd mmmm yyyy',tgl_transaksi_akhir)
  ConstructReportHeader(config, strTanggalAwal, strTanggalAkhir, oFile)

  strSQL = strSQLCabang(config)
  config.SendDebugMsg(strSQL)

  totPeserta, totReferensi = ConstructReportValues(config, strSQL, tgl_transaksi_awal, tgl_transaksi_akhir + 1, oFile)

  ConstructReportTrailer(
    config, totPeserta
    , totReferensi
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

