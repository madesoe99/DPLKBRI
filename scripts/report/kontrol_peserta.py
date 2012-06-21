import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi
import string

def ConstructReportHeader(config, strBulan, strTahun, strBulanPrev, strTahunPrev, oFile):
  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Kontrol Jumlah Peserta</title>\n')
  oFile.write('\n')
  oFile.write('<body style="FONT-FAMILY: Arial; line-height:100%; margin-top:0; margin-bottom:0">\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0" bordercolor="#111111" border="1" width="100%" id="table1" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td colspan="7" height="20" style="border-left:medium none #000000; border-right:medium none #000000; border-top-style:none; border-top-width:medium; border-bottom-style:none; border-bottom-width:medium">\n')
  oFile.write('		<p align="center"><font size="3" color="#008000"><b>LAPORAN PERTUMBUHAN \n')
  oFile.write('		JUMLAH PESERTA</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="100%" colspan="7" style="border-style: none; border-width: medium">\n')
  oFile.write('		<b><font color="#008000">PERIODE: '+ strBulan +' '+ strTahun +'</font></b></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="5%" align="center" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699" rowspan="2">\n')
  oFile.write('		<b>NO</b></td>\n')
  oFile.write('		<td width="10%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699" rowspan="2">\n')
  oFile.write('		<b>KODE CABANG</b></td>\n')
  oFile.write('		<td width="25%" align="center" style="border-style: solid; border-width: 1px; " bgcolor="#CC6699" rowspan="2">\n')
  oFile.write('		<b>NAMA CABANG</b></td>\n')
  oFile.write('		<td width="30%" align="center" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699" colspan="2">\n')
  oFile.write('		<b>POSISI</b></td>\n')
  oFile.write('		<td width="30%" align="center" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699" colspan="2">\n')
  oFile.write('		<b>PERTUMBUHAN</b></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="15%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="center" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ strBulanPrev +' '+ strTahunPrev +'</b></td>\n')
  oFile.write('		<td width="15%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#CC6699" align="center">\n')
  oFile.write('		<b>'+ strBulan +' '+ strTahun +'</b></td>\n')
  oFile.write('		<td width="15%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#CC6699" align="center">\n')
  oFile.write('		<b>JUMLAH</b></td>\n')
  oFile.write('		<td width="15%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="#CC6699" align="center">\n')
  oFile.write('		<b>PERSENTASE (%)</b></td>\n')
  oFile.write('	</tr>\n')

def strSQLKontrolPeserta(config, intBulanPrev, intTahunPrev, intBulan, intTahun):
  return \
    'select b.branch_code kode '\
    '  , isnull(b.BranchName,\'\') nama '\
    '  , isnull(count(distinct prev.no_peserta),0) totPrev '\
    '  , isnull(count(distinct curr.no_peserta),0) totCurr '\
    'from '\
    '  (select branch_code '\
    '    , BranchName '\
    '  from BranchLocation) as b '\
    'left outer join '\
    '  (select n.no_peserta '\
    '    , kode_cab_daftar '\
    '  from RekeningDPLK r, NasabahDPLK n '\
    '  where n.no_peserta = r.no_peserta '\
    '    and ( '\
    '      ((datepart(month,tgl_registrasi) <= %d) and (datepart(year,tgl_registrasi) = %d)) '\
    '      or (datepart(year,tgl_registrasi) < %d) '\
    '    ) '\
    '  ) prev '\
    'on b.branch_code = prev.kode_cab_daftar '\
    'left outer join '\
    '  (select n.no_peserta '\
    '    , kode_cab_daftar '\
    '  from RekeningDPLK r, NasabahDPLK n '\
    '  where n.no_peserta = r.no_peserta '\
    '    and ( '\
    '      ((datepart(month,tgl_registrasi) <= %d) and (datepart(year,tgl_registrasi) = %d)) '\
    '      or (datepart(year,tgl_registrasi) < %d) '\
    '    ) '\
    '  ) curr '\
    'on b.branch_code = curr.kode_cab_daftar '\
    'group by b.branch_code, b.BranchName '\
    % (intBulanPrev, intTahunPrev, intTahunPrev, intBulan, intTahun, intTahun)

def strSQLPesertaPrev(config, intBulanPrev, intTahunPrev, kode_daftar):
  return \
    'select r.kode_cab_daftar kode '\
    '  , isnull(count(distinct n.no_peserta),0) totprev '\
    ' from rekeningdplk r, nasabahdplk n '\
    ' where r.no_peserta = n.no_peserta '\
    '   and r.kode_cab_daftar = \'%s\' '\
    '  and r.STATUS_DPLK <> \'N\' '\
    '  and ( '\
    '      ((datepart(month,n.tgl_registrasi) <= %d) and (datepart(year,n.tgl_registrasi) = %d)) '\
    '      or (datepart(year,tgl_registrasi) < %d) '\
    ' ) '\
    'group by r.kode_cab_daftar '\
    %(kode_daftar, intBulanPrev, intTahunPrev, intTahunPrev)
    

def strSQLPesertaCurr(config, intBulan, intTahun, kode_daftar):
  return \
    'select r.kode_cab_daftar kode'\
    ', isnull(count(distinct n.no_peserta),0) totcurr '\
    ' from rekeningdplk r, nasabahdplk n '\
    ' where r.no_peserta = n.no_peserta '\
    '   and r.kode_cab_daftar = \'%s\' '\
    '   and r.STATUS_DPLK <> \'N\' '\
    '   and ( '\
    '      ((datepart(month,n.tgl_registrasi) <= %d) and (datepart(year,n.tgl_registrasi) = %d)) '\
    '      or (datepart(year,tgl_registrasi) < %d) '\
    ' ) '\
    'group by r.kode_cab_daftar '\
    %(kode_daftar, intBulan, intTahun, intTahun )
    
def strSQLBranchCode(config):
  return \
    'select branch_code kode'\
    ', BranchName nama '\
    ' from BranchLocation '\
#    ' where branch_code = \'%s\' '\
 #   %(kode_daftar)


def ConstructReportValues(config, strSQL, intBulan, intTahun, intBulanPrev, intTahunPrev, oFile):
  resSQLBranch = config.CreateSQL(strSQL).RawResult

  no_urut = 0
  sumPrev = 0
  sumCurr = 0
  totJmlMutasi = 0
  resSQLBranch.First()
  while not resSQLBranch.Eof:
    no_urut += 1

    if moduleapi.IsOddNumber(no_urut):
      bgcolor = '#EFEFEF'
    else:
      bgcolor = '#FFFFFF'


    strSQLPrev = strSQLPesertaPrev(config, intBulanPrev, intTahunPrev, resSQLBranch.kode)
    resSQLPrev = config.CreateSQL(strSQLPrev).RawResult

    config.SendDebugMsg(resSQLBranch.kode)
    if resSQLPrev.eof:
       jmlPrev = 0
    else:
       jmlPrev = resSQLPrev.totPrev

    config.SendDebugMsg(resSQLBranch.kode)
    config.SendDebugMsg('prev...')
    #config.SendDebugMsg(resSQLPrev.kode)
    
    strSQLCurr = strSQLPesertaCurr(config, intBulan, intTahun, resSQLBranch.kode)
    resSQLCurr = config.CreateSQL(strSQLCurr).RawResult

    if resSQLCurr.eof:
       jmlCurr = 0
    else:
       jmlCurr = resSQLCurr.totCurr

       
    config.SendDebugMsg('Curr...')
    #config.SendDebugMsg(resSQLCurr.kode)

    #strSQLBranchName = strSQLBranchCode(config, resSQL.kode)
    #resSQLBranchName = config.CreateSQL(strSQLBranchName).RawResult


    config.SendDebugMsg(str(jmlPrev))
    config.SendDebugMsg(str(jmlCurr))
    jmlMutasi = jmlCurr - jmlPrev

    config.SendDebugMsg(str(jmlMutasi))

    
    if not moduleapi.IsApproxZero(jmlPrev):
      prsMutasi = jmlMutasi * 100.0 / jmlPrev
    else:
      # avoiding zero divide
      prsMutasi = 0.0
    strPrsMutasi = config.FormatFloat('0.0##',prsMutasi)

    config.SendDebugMsg('masuk....02')
    
    oFile.write('	<tr>\n')
    oFile.write('		<td width="5%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'">'+ str(no_urut) +'</td>\n')
    oFile.write('		<td width="10%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'">\n')
    oFile.write('		<p align="center">'+ resSQLBranch.kode +'</td>\n')
    oFile.write('		<td width="25%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'">'+resSQLBranch.nama+'</td>\n')
    oFile.write('		<td width="15%" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="'+ bgcolor +'">\n')
    oFile.write('		<p align="right">'+ str(jmlPrev) +'</td>\n')
    oFile.write('		<td width="15%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" align="right">'+ str(jmlCurr) +'</td>\n')
    oFile.write('		<td width="15%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" align="right">'+ str(jmlMutasi) +'</td>\n')
    oFile.write('		<td width="15%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px" bgcolor="'+ bgcolor +'" align="right">'+ strPrsMutasi +'</td>\n')
    oFile.write('	</tr>\n')

    config.SendDebugMsg('masuk....03')
    
    sumPrev += jmlPrev
    sumCurr += jmlCurr
    totJmlMutasi += jmlMutasi
    jmlMutasi = 0
    config.SendDebugMsg('masuk....04')
    config.SendDebugMsg(str(jmlMutasi))

    resSQLBranch.Next()

  return (sumPrev, sumCurr, totJmlMutasi)

def ConstructReportTrailer(config, sumPrev, sumCurr, totJmlMutasi, oFile):
  if not moduleapi.IsApproxZero(sumPrev):
    totPrsMutasi = totJmlMutasi * 100.0 / sumPrev
  else:
    # avoiding zero divide
    totPrsMutasi = 0.0
  strTotPrsMutasi = config.FormatFloat('0.0##',totPrsMutasi)

  oFile.write('	<tr>\n')
  oFile.write('		<td width="40%" style="border-left:1px solid #000000; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" colspan="3" bgcolor="#CC6699">\n')
  oFile.write('		<b>TOTAL</b></td>\n')
  oFile.write('		<td width="15%" style="border-left-style:solid; border-left-width:1px; border-right-style:solid; border-right-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" align="right" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ str(sumPrev) +'</b></td>\n')
  oFile.write('		<td width="15%" align="right" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ str(sumCurr) +'</b></td>\n')
  oFile.write('		<td width="15%" align="right" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ str(totJmlMutasi) +'</b></td>\n')
  oFile.write('		<td width="15%" align="right" style="border-right:1px solid #000000; border-left-style:solid; border-left-width:1px; border-top-style:solid; border-top-width:1px; border-bottom-style:solid; border-bottom-width:1px" bgcolor="#CC6699">\n')
  oFile.write('		<b>'+ strTotPrsMutasi +'</b></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('</table>\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('</body>\n')
  oFile.write('\n')
  oFile.write('</html>\n')

def WriteToFile(config, parameter, oFile):
  intBulan = parameter.FirstRecord.bulan
  intTahun = parameter.FirstRecord.tahun

  if intBulan == 1:
    intBulanPrev = 12
    intTahunPrev = intTahun - 1
  else:
    intBulanPrev = intBulan - 1
    intTahunPrev = intTahun

  strBulan = string.upper(moduleapi.IntMonthToStr(intBulan)) 
  strBulanPrev = string.upper(moduleapi.IntMonthToStr(intBulanPrev)) 
  ConstructReportHeader(config, strBulan, str(intTahun), strBulanPrev, str(intTahunPrev), oFile)
  #strSQL = strSQLKontrolPeserta(config, intBulanPrev, intTahunPrev, intBulan, intTahun)
  #strSQL = strSQLPesertaPrev(config, intBulanPrev, intTahunPrev)
  
  strSQL = strSQLBranchCode(config)
  
  sumPrev, sumCurr, totJmlMutasi = ConstructReportValues(config, strSQL, intBulan, intTahun, intBulanPrev, intTahunPrev, oFile)[:3]
  
  ConstructReportTrailer(config, sumPrev, sumCurr, totJmlMutasi,  oFile)

def CreateReport(config, parameter, returnpacket):
  sBaseFileName = 'kontrol_peserta.htm'
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
