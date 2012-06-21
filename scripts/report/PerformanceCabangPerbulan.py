import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi
import string

def ConstructReportHeader(config, strTanggalAwal, strTanggalAkhir, nama_bulan, oFile):
  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Laporan Periode Performance Cabang</title>\n')
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Arial; line-height:100%; margin-top:0; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td colspan="6" height="20" style="border-left:medium none #000000; border-right:medium none #000000; border-top-style:none; border-top-width:medium; border-bottom-style:none; border-bottom-width:medium">\n')
  oFile.write('		<p align="center"><font size="3" color="#008000"><b>LAPORAN PERFORMANCE CABANG PERBULAN </b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" colspan="4" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font color="#008000"><b>'+string.upper(strTanggalAwal)+' HINGGA '+ string.upper(strTanggalAkhir)+'</b></font></td>\n')
  oFile.write('		<td width="100%" colspan="3" style="border-style: none; border-width: medium">\n')
  oFile.write('		<font color="#008000"></font></td>\n')
  oFile.write('		<td width="100%" colspan="2" style="border-style: none; border-width: medium">\n')
  oFile.write('		<p align="center">Sign <font color="#FF0000" size ="3" ><b>&#8226 </font><font color="#FF0000"> = < 80%</b></font></td>\n')
  oFile.write('		<td width="100%" colspan="2" style="border-style: none; border-width: medium">\n')
  oFile.write('		<p align="center"><font color="#0000FF"  size ="3"><b> &#8226 </font><font color="#0000FF"> = 81 s.d. 99%</b></font></td>\n')
  oFile.write('		<td width="100%" colspan="2" style="border-style: none; border-width: medium">\n')
  oFile.write('		<p align="center"><font color="#01DF01" size ="3"><b>&#8226 </font><font color="#01DF01"> = > 100%</b></font></td>\n')

  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="3%" rowspan = "3" align="center" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>NO</b></td>\n')
  oFile.write('		<td width="7%" rowspan = "3" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>KODE CABANG</b></td>\n')
  oFile.write('		<td width="18%" rowspan = "3" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>NAMA CABANG</b></td>\n')
  oFile.write('		<td width="7%" rowspan = "2" colspan = "2" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>TARGET 2011</b></td>\n')
  oFile.write('		<td width="7%" colspan = "8" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>Target & Realisasi Peserta Baru (Branch Based)</b></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="7%" colspan = "2" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b> Target/Bulan</b></td>\n')
  oFile.write('		<td width="18%" colspan = "6" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b> Realisasi '+ nama_bulan + ' (terhadap target s.d. '+ nama_bulan+' ) </b></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="7%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>Account</b></td>\n')
  oFile.write('		<td width="7%"  align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>Rupiah</b></td>\n')
  oFile.write('		<td width="7%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>Account</b></td>\n')
  oFile.write('		<td width="7%"  align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>Rupiah</b></td>\n')
  oFile.write('		<td width="7%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>Account</b></td>\n')
  oFile.write('		<td width="3%"  align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b> % </b></td>\n')  
  oFile.write('		<td width="3%"  align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b> Sign </b></td>\n')  
  oFile.write('		<td width="7%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b>Rupiah</b></td>\n')
  oFile.write('		<td width="3%"  align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b> % </b></td>\n')  
  oFile.write('		<td width="3%"  align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699">\n')
  oFile.write('		<b> Sign </b></td>\n')  
  oFile.write('	</tr>\n')

def strSQLDana(config, kode_cabang, tgl_transaksi_awal, tgl_transaksi_akhir_plus):
  return \
    'select  '\
    '    isnull(sum(t.MUTASI_IURAN_PK),0.0)  as MUTASI_PK '\
    '  , isnull(sum(t.MUTASI_IURAN_PST),0.0) as MUTASI_PESERTA '\
    '  , isnull(sum(t.MUTASI_PERALIHAN),0.0) as MUTASI_PERALIHAN '\
    '  , isnull(sum(t.MUTASI_PENGEMBANGAN),0.0) as MUTASI_PENGEMBANGAN '\
    'from TRANSAKSIDPLK t, REKENINGDPLK r '\
    'where t.no_peserta = r.no_peserta '\
    '  and t.TGL_TRANSAKSI >= \'%s\' '\
    '  and t.TGL_TRANSAKSI < \'%s\' '\
    '  and r.kode_cab_daftar = \'%s\' '\
    '  and t.kode_jenis_transaksi in ( \'K\',\'M\') '\
    '  and t.ISCOMMITTED = \'T\' ;'\
    %( config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_awal)\
       ,config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_akhir_plus)\
       , kode_cabang)

def strSQLPeserta(config, kode_cabang, tgl_transaksi_awal, tgl_transaksi_akhir_plus):
  return \
    'select  '\
    '   count(R.NO_PESERTA) as jmlPeserta '\
    'from NASABAHDPLK n, REKENINGDPLK r '\
    'where n.no_peserta = r.no_peserta '\
    '  and n.TGL_REGISTRASI >= \'%s\' '\
    '  and n.TGL_REGISTRASI < \'%s\' '\
    '  and r.kode_cab_daftar = \'%s\' ;'\
    %( config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_awal)\
       ,config.FormatDateTime('yyyy-mm-dd',tgl_transaksi_akhir_plus)\
       , kode_cabang
    )

def strSQLCabang(config):
  return \
    'select AREA,BRANCH_CODE,BRANCHNAME,BRANCHSTATUS,TGL_BUKA '\
    'from BRANCHLOCATION '\
    'WHERE BRANCHSTATUS IN ( \'B\',\'S\') '\
    'ORDER BY AREA,BRANCH_CODE';

def ConstructReportValues(config, strSQL, tgl_transaksi_awal, tgl_transaksi_plus, blnAwl, blnAkh, oFile):

  ## query Cabang
  resSQL = config.CreateSQL(strSQL).RawResult


  strThnAwl = config.FormatDateTime('yyyy',tgl_transaksi_awal)
  strThnAkh = config.FormatDateTime('yyyy',tgl_transaksi_plus)
  
  if (strThnAwl == strThnAkh):
     blnProses = (blnAkh - blnAwl) + 1
  else:
     blnAwl = (12 - blnAwl) + 1
     blnProses = blnAkh + blnAwl

  no_urut = 0
  totPeserta = 0.0
  totDana = 0.0
  totDPLK = 0.0
  totCabangAll = 0.0
  totDPLKAll = totAllAccount = totAllRupiah = 0.0
  totAllAccountBln = totAllRupiahBln = 0.0
  TotSubPeserta = TotSubDana = TotSubCabang = 0.0
  TotSubDPLK = TotTargetAccount = TotTargetRupiah = 0.0
  TotTargetAccountBln = TotTargetRupiahBln = 0.0
  
  area = '0000'
  config.SendDebugMsg('masuk......01A')

  dictKodeCabang = {'A001':'AREA SUMBAGUT',\
                    'A002':'AREA SUMBAGSEL',\
                    'A003':'AREA KALIMANTAN',\
                    'A004':'AREA JAWA BARAT',\
                    'A005':'AREA JAWA TENGAH & DIY',\
                    'A006':'AREA JAWA TIMUR',\
                    'A007':'AREA K T I',\
                    'A008':'AREA TIER ONE 1',\
                    'A009':'AREA TIER ONE 2',\
                    'A010':'AREA TIER ONE 3',\
                    'A011':'KPO',\
                    'A999':'OTHERS'}
  dictStatus = {'S':120,'B':240}

  resSQL.First()
  while not resSQL.Eof:
    config.SendDebugMsg('masuk......02'+ str(resSQL.BRANCH_CODE))
    strSQL = strSQLDana(config, resSQL.BRANCH_CODE, tgl_transaksi_awal, tgl_transaksi_plus)
    rSQLDana = config.CreateSQL(strSQL).RawResult
    
    strSQL = strSQLPeserta(config, resSQL.BRANCH_CODE, tgl_transaksi_awal, tgl_transaksi_plus)
    rSQLPeserta = config.CreateSQL(strSQL).RawResult
    config.SendDebugMsg('masuk......032')
    no_urut += 1

    akum_iuran_pst    = rSQLDana.mutasi_peserta or 0.0
    akum_iuran_pk     = rSQLDana.mutasi_pk or 0.0
    akum_pengembangan = rSQLDana.mutasi_pengembangan or 0.0
    akum_peralihan    = rSQLDana.mutasi_peralihan or 0.0
    total_dana        = (akum_iuran_pst + akum_iuran_pk + akum_pengembangan + akum_peralihan)
    totCabang         = total_dana * (float(20)/100)
    totDPLK           = total_dana * (float(80)/100)

    config.SendDebugMsg('masuk......04')

    if moduleapi.IsOddNumber(no_urut):
      bgcolor = '#EFEFEF'
    else:
      bgcolor = '#FFFFFF'

    config.SendDebugMsg('masuk......04a')
    if resSQL.area == 'A000':
       config.SendDebugMsg('masuk......05')
       resSQL.Next()
    else:
       config.SendDebugMsg('masuk......04b')
       nama_area = '%s' % (dictKodeCabang[resSQL.area])

       y,m,d               = resSQL.tgl_buka[:3]
       thnBuka = y
       blnBuka = m

       if resSQL.branchstatus == 'B':
          if thnBuka < 2011:
             targetAccount = 240
             bln1 = 12
             targetRupiah = 1182572614.11
          else:
             targetAccount = ((12-blnBuka)) * 20
             bln1 = ((12-blnBuka)+1)
             targetRupiah = (1182572614.11/12)*bln1

          #targetRupiah = 1182572614.11
          targetAccountBln = 20
          targetRupiahBln = (1182572614.11/12)

       if resSQL.branchstatus == 'S':
          if thnBuka < 2011:
             targetAccount = 120
             bln1 = 12
             targetRupiah =  (591286307.051)
          else:
             targetAccount = ((12-blnBuka)) * 10
             bln1 = ((12-blnBuka)+1)
             targetRupiah = (591286307.051/12)*bln1

          #targetRupiah = 591286307.051
          targetAccountBln = 10
          targetRupiahBln = (591286307.051/12)

       if resSQL.branchstatus == 'K':
          if thnBuka < 2011:
             targetAccount = 60
             bln1 = 12
             targetRupiah =  (295643153.53)
          else:
             targetAccount = ((12-blnBuka)) * 5
             bln1 = ((12-blnBuka)+1)
             targetRupiah = (295643153.53/12)*bln1

          targetAccountBln = 5
          targetRupiahBln = (295643153.53/12)


          
       config.SendDebugMsg('masuk......04b1')
       config.SendDebugMsg('peserta : '+ str(rSQLPeserta.jmlPeserta))
       config.SendDebugMsg('targetbulan : '+ str(targetAccountBln))
       config.SendDebugMsg('bulan : '+ str(blnProses))

       AccountPersen = (float(rSQLPeserta.jmlPeserta)/(targetAccountBln * blnProses))* 100
       config.SendDebugMsg('masuk......04b2')
       RupiahPersen = (float(total_dana)/(targetRupiahBln * blnProses))* 100

       config.SendDebugMsg('masuk......04c')
       config.SendDebugMsg('AP.......'+str(AccountPersen))
       config.SendDebugMsg('AP.......'+str(RupiahPersen))
       
       if AccountPersen < 81:
          bgAccount = '#FF0000' # Merah
       if AccountPersen >= 81:
          if AccountPersen < 100:
             bgAccount = '#0000FF' # Kuning
       if AccountPersen >= 100:
          bgAccount = '#01DF01' # Hijau
       
       if RupiahPersen < 81:
          config.SendDebugMsg('masuk......04c1')
          bgRupiah = '#FF0000' # Merah
       if RupiahPersen >= 81:
          if RupiahPersen < 100:
             config.SendDebugMsg('masuk......04c2')
             bgRupiah = '#0000FF' # Kuning
       if RupiahPersen >= 100:
          config.SendDebugMsg('masuk......04c3')
          bgRupiah = '#01DF01' # Hijau
       
       config.SendDebugMsg('masuk......04d')
       
       if area <> resSQL.area:
          if no_urut == 1:
             oFile.write('	<tr>\n')
             oFile.write('		<td width="7%" colspan="13" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#CC6699" height="22">\n')
             oFile.write('		<p align="center"> <b>'+ nama_area +'</b></td>\n')
             oFile.write('	</tr>\n')
          else:
             totAccountPersen = (float(TotSubPeserta)/(TotTargetAccountBln* blnProses)) * 100
             totRupiahPersen = (float(TotSubDana)/(TotTargetRupiahBln * blnProses)) * 100
              
             if totAccountPersen < 81:
                bgtotAccount = '#FF0000' # Merah
             if totAccountPersen >= 81:
                if totAccountPersen < 100:
                   bgtotAccount = '#0000FF' # Kuning
             if totAccountPersen >= 100:
                bgtotAccount = '#01DF01' # Hijau

             if totRupiahPersen < 81:
                bgtotRupiah = '#FF0000' # Merah
             if totRupiahPersen >= 81:
                if totRupiahPersen < 100:
                   bgtotRupiah = '#0000FF' # Kuning
             if totRupiahPersen >= 100:
                bgtotRupiah = '#01DF01' # Hijau
             
             config.SendDebugMsg('masuk......04e')
             oFile.write('	<tr>\n')
             oFile.write('		<td width="18%" colspan="3" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
             oFile.write('		<p align="right"><b>Sub Total Area</b></td>\n')

             oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
             oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, TotTargetAccount) +'</td>\n')
             oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
             oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, TotTargetRupiah) +'</td>\n')
             oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
             oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, TotTargetAccountBln) +'</td>\n')
             oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
             oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, TotTargetRupiahBln) +'</td>\n')

             oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
             oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, TotSubPeserta) +'</td>\n')
             oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
             oFile.write('		<p align="right"> '+ moduleapi.FormatFloatStd(config, totAccountPersen)+'%</td>\n')
             oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
             oFile.write('		<p align="center"><font size="5" color="'+ bgtotAccount +'"> <B>&#8226</B></td>\n')

             oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
             oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, TotSubDana) +'</td>\n')
             oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
             oFile.write('		<p align="right"> '+ moduleapi.FormatFloatStd(config, totRupiahPersen)+'%</td>\n')
             oFile.write('		<td width="10%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
             oFile.write('		<p align="center"><font size="5" color="'+ bgtotRupiah +'"> <B>&#8226</B></td>\n')
             oFile.write('	</tr>\n')

             oFile.write('	<tr>\n')
             oFile.write('		<td width="7%" colspan="13" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#CC6699" height="22">\n')
             oFile.write('		<p align="center"> <b>'+ nama_area +'</b></td>\n')
             oFile.write('	</tr>\n')
             
             TotSubPeserta = TotSubDana = TotSubCabang = TotSubDPLK = TotTargetAccount = TotTargetRupiah = 0.0
             TotTargetAccountBln = TotTargetRupiahBln = 0.0 
             totAccountPersen = totRupiahPersen = 0.0

       if  resSQL.branch_code == '000':
           branchName = 'OTHERS'
       else:
           branchName = resSQL.branchname

       config.SendDebugMsg('masuk......04f')
       oFile.write('	<tr>\n')
       oFile.write('		<td width="3%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'" height="22">'+ str(no_urut) +'</td>\n')
       oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
       oFile.write('		<p align="center">'+ resSQL.branch_code +'</td>\n')
       oFile.write('		<td width="18%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
       oFile.write('		<p align="left">'+ branchName +'</td>\n')
       oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
       oFile.write('		<p align="right">'+ str(targetAccount) +'</td>\n')
       oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
       oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, targetRupiah) +'</td>\n')

       oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
       oFile.write('		<p align="right">'+ str(targetAccountBln) +'</td>\n')
       oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
       oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, (targetRupiahBln)) +'</td>\n')

       oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
       oFile.write('		<p align="right">'+ str(rSQLPeserta.jmlPeserta) +'</td>\n')
       oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
       oFile.write('		<p align="right">'+ str(AccountPersen)+'% </td>\n')
       oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
       oFile.write('		<p align="center"><font size="5" color="'+ bgAccount +'"> <B>&#8226</B></td>\n')

       oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
       oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, total_dana) +'</td>\n')
       oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
       oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config,RupiahPersen)+'%</td>\n')
       oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
       oFile.write('		<p align="center"><font size="5" color="'+ bgRupiah +'"> <B>&#8226</B></td>\n')

       oFile.write('	</tr>\n')

       TotSubPeserta += rSQLPeserta.jmlPeserta
       TotSubDana += total_dana
       TotSubDPLK += totDPLK
       
       TotTargetAccount += targetAccount
       TotTargetRupiah  += targetRupiah
       TotTargetAccountBln += targetAccountBln
       TotTargetRupiahBln  += targetRupiahBln

       area = resSQL.area
       totPeserta += rSQLPeserta.jmlPeserta
       totDana  += total_dana
       totDPLKAll += totDPLK
       totAllAccount += targetAccount
       totAllRupiah += targetRupiah
       totAllAccountBln += targetAccountBln
       totAllRupiahBln += targetRupiahBln

       # jIKA CABANG OOO
       if  resSQL.branch_code == '000':

             totAccountPersen = (float(TotSubPeserta)/(TotTargetAccountBln* blnProses)) * 100
             totRupiahPersen = (float(TotSubDana)/(TotTargetRupiahBln * blnProses)) * 100

             if totAccountPersen < 81:
                bgtotAccount = '#FF0000' # Merah
             if totAccountPersen >= 81:
                if totAccountPersen < 100:
                   bgtotAccount = '#0000FF' # Kuning
             if totAccountPersen >= 100:
                bgtotAccount = '#01DF01' # Hijau

             if totRupiahPersen < 81:
                bgtotRupiah = '#FF0000' # Merah
             if totRupiahPersen >= 81:
                if totRupiahPersen < 100:
                   bgtotRupiah = '#0000FF' # Kuning
             if totRupiahPersen >= 100:
                bgtotRupiah = '#01DF01' # Hijau

             oFile.write('	<tr>\n')
             oFile.write('		<td width="18%" colspan="3" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
             oFile.write('		<p align="right"><b>Sub Total Area</b></td>\n')

             oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
             oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, TotTargetAccount) +'</td>\n')
             oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
             oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, TotTargetRupiah) +'</td>\n')
             oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
             oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, TotTargetAccountBln) +'</td>\n')
             oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
             oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, TotTargetRupiahBln) +'</td>\n')

             oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
             oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, TotSubPeserta) +'</td>\n')
             oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
             oFile.write('		<p align="right"> '+ moduleapi.FormatFloatStd(config, totAccountPersen)+'%</td>\n')
             oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
             oFile.write('		<p align="center"><font size="5" color="'+ bgtotAccount +'"> <B>&#8226</B></td>\n')

             oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
             oFile.write('		<p align="right">'+ moduleapi.FormatFloatStd(config, TotSubDana) +'</td>\n')
             oFile.write('		<td width="7%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
             oFile.write('		<p align="right"> '+ moduleapi.FormatFloatStd(config, totRupiahPersen)+'%</td>\n')
             oFile.write('		<td width="10%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" height="22">\n')
             oFile.write('		<p align="center"><font size="5" color="'+ bgtotRupiah +'"> <B>&#8226</B></td>\n')
             oFile.write('	</tr>\n')

       resSQL.Next()

  return totPeserta, totDana, totCabangAll, totDPLKAll, totAllAccount, totAllRupiah, totAllAccountBln, totAllRupiahBln, blnProses
  

def ConstructReportTrailer(config, totPeserta, totDana, totCabangAll, totDPLKAll, totAccount, totRupiah, totAccountBln, totRupiahBln, blnProses, oFile):

  totAccountPersen = (float(totPeserta)/(totAccountBln* blnProses)) * 100
  totRupiahPersen = (float(totDana)/(totRupiahBln * blnProses)) * 100

  if totAccountPersen < 81:
     bgtotAccount = '#FF0000' # Merah
  if totAccountPersen >= 81:
     if totAccountPersen < 100:
        bgtotAccount = '#0000FF' # Kuning
  if totAccountPersen >= 100:
     bgtotAccount = '#01DF01' # Hijau

  if totRupiahPersen < 81:
     bgtotRupiah = '#FF0000' # Merah
  if totRupiahPersen >= 81:
     if totRupiahPersen < 100:
        bgtotRupiah = '#0000FF' # Kuning
  if totRupiahPersen >= 100:
     bgtotRupiah = '#01DF01' # Hijau

  oFile.write('	<tr>\n')
  oFile.write('		<td width="44%" colspan="3" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" colspan="6" bgcolor="#CC6699">\n')
  oFile.write('		<b>TOTAL PESERTA</b></td>\n')
  oFile.write('		<td width="9%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totAccount) +'</b></td>\n')
  oFile.write('		<td width="9%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totRupiah) +'</b></td>\n')

  oFile.write('		<td width="9%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totAccountBln) +'</b></td>\n')
  oFile.write('		<td width="9%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totRupiahBln) +'</b></td>\n')

  oFile.write('		<td width="9%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totPeserta) +'</b></td>\n')
  oFile.write('		<td width="9%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>' + moduleapi.FormatFloatStd(config, totAccountPersen) +' </b></td>\n')
  oFile.write('		<td width="9%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<p align="center"><font size="5" color="'+ bgtotAccount +'"> <B>&#8226</B></td>\n')
  oFile.write('		<td width="9%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ moduleapi.FormatFloatStd(config, totDana) +'</b></td>\n')
  oFile.write('		<td width="9%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>' + moduleapi.FormatFloatStd(config, totRupiahPersen) +'</b></td>\n')
  oFile.write('		<td width="9%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<p align="center"><font size="5" color="'+ bgtotRupiah +'"> <B>&#8226</B></td>\n')

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
  
  y,m,d = config.ModLibUtils.DecodeDate(parameter.FirstRecord.tanggal_awal)
  blnAwl = m
  y,m,d = config.ModLibUtils.DecodeDate(parameter.FirstRecord.tanggal_akhir)
  blnAkh = m
  #tglHitung = [y,m,d]
  
  #config.SendDebugMsg('masuk......02')
  strTanggalAwal = config.FormatDateTime('dd mmmm yyyy',tgl_transaksi_awal)
  strTanggalAkhir = config.FormatDateTime('dd mmmm yyyy',tgl_transaksi_akhir)
   
  dictNamaBulan = {1: 'Januari',2:'Februari',3:'Maret',4:'April',5:'Mei',6:'Juni',\
                   7: 'Juli',8:'Agustus',9:'September',10:'Oktober',11:'November',12:'Desember'}
                   
  nama_bulan = '%s' % (dictNamaBulan[blnAkh])

  ConstructReportHeader(config, strTanggalAwal, strTanggalAkhir, nama_bulan, oFile)

  strSQL = strSQLCabang(config)
  config.SendDebugMsg(strSQL)

  totPeserta, totReferensi, totDanaCabang, totDanaDPLK, totAccount, totRupiah, totAccountBln, totRupiahBln, blnProses = ConstructReportValues(config, strSQL, tgl_transaksi_awal, tgl_transaksi_akhir + 1, blnAwl, blnAkh ,oFile)

  ConstructReportTrailer(
    config, totPeserta
    , totReferensi
    , totDanaCabang
    , totDanaDPLK
    , totAccount
    , totRupiah
    , totAccountBln
    , totRupiahBln
    , blnProses
    , oFile
  )

def CreateReport(config, parameter, returnpacket):
  sBaseFileName = 'Laporan_Performance_Cabang_Rev.htm'
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

