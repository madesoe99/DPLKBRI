import sys
import string
import calendar
import com.ihsan.util.modman as modman

def ConstructReportHeader(config, kode_jns_investasi, monthFrom, yearFrom, monthUntil, yearUntil, oFile):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  if kode_jns_investasi:
    oJenisInvestasi = config.CreatePObjImplProxy('JenisInvestasi')
    oJenisInvestasi.Key = kode_jns_investasi
    nama_jns_investasi = string.capwords(oJenisInvestasi.nama_jns_investasi)
  else:
    nama_jns_investasi = 'Investasi'

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
  oFile.write('		<p align="left"><font size="2" color="#008000"><b>'+ moduleapi.IntMonthToStr(monthFrom) +' '+ str(yearFrom) +' sampai '+ moduleapi.IntMonthToStr(monthUntil) +' '+ str(yearUntil) +'</b></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	</table><font size="2">\n')
  oFile.write('\n')
  oFile.write('\n')

def resSQLHasilInv(config, kode_jns_investasi, strDateFromSQL, strDateUntilTmrwSQL):
  strFilterJnsInv = ''
  if kode_jns_investasi:
    strFilterJnsInv = 'and kode_jns_investasi = \'%s\'' % (kode_jns_investasi)

  strSQL = \
    'select sum(mutasi_kredit - mutasi_debet) as hasil '\
    'from TransaksiInvestasi '\
    'where clsfTransaksiInvestasi = \'C\' '\
    '  and isCommitted = \'T\' '\
    '  %s '\
    '  and tgl_transaksi >= \'%s\' '\
    '  and tgl_transaksi < \'%s\' '\
    % (strFilterJnsInv
      , strDateFromSQL
      , strDateUntilTmrwSQL
    )
  config.SendDebugMsg(strSQL)

  return config.CreateSQL(strSQL).RawResult
  
def resSQLHasilSukuk(config, strDateFromSQL, strDateUntilTmrwSQL):

  strSQL = \
    'select sum(mutasi_kredit + mutasi_debet) as hasil  '\
    'from TransaksiInvestasi t, Obligasi o '\
    'where isCommitted = \'T\' '\
    '	and clsfTransaksiInvestasi in (\'B\',\'C\',\'D\') '\
    '	and t.id_investasi = o.id_investasi '\
    '	and tgl_transaksi >= \'%s\' '\
    '	and tgl_transaksi < \'%s\' '\
    % (strDateFromSQL
      , strDateUntilTmrwSQL
    )
  config.SendDebugMsg(strSQL)

  return config.CreateSQL(strSQL).RawResult

def ConstructReportHasil(config, kode_jns_investasi, strDateFromSQL, strDateUntilTmrwSQL, oFile):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  if kode_jns_investasi == 'O':
     config.SendDebugMsg('sukukkkkkkkkkkk.....')
     resSQLHI = resSQLHasilSukuk(config, strDateFromSQL, strDateUntilTmrwSQL)
     
  else:
     resSQLHI = resSQLHasilInv(config, kode_jns_investasi, strDateFromSQL, strDateUntilTmrwSQL)
  hasil = 0.0
  if not resSQLHI.Eof:
    hasil = resSQLHI.hasil or 0.0
  strHasil = moduleapi.FormatFloatStd(config, hasil)

  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0; border-bottom-width:0px" bordercolor="#111111" border="1" width="750" id="table2" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="600" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="left"><b><font size="2">Hasil Investasi</font></b></td>\n')
  oFile.write('		<td width="150" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="right"><b>\n')
  oFile.write('		<font size="2">'+ strHasil +'</font></b></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('</table>\n')
  oFile.write('\n')
  oFile.write('\n')
  
  return hasil

def resSQLTotalInv(config, kode_jns_investasi, strDateUntilTmrwSQL):
  strFilterJnsInv = ''
  if kode_jns_investasi:
    strFilterJnsInv = 'and kode_jns_investasi = \'%s\'' % (kode_jns_investasi)

  strSQL = \
    'select sum(mutasi_debet - mutasi_kredit) as nominal '\
    'from TransaksiInvestasi '\
    'where clsfTransaksiInvestasi = \'A\' '\
    '  and isCommitted = \'T\' '\
    '  %s '\
    '  and tgl_transaksi < \'%s\' '\
    % (strFilterJnsInv
      , strDateUntilTmrwSQL
    )
  config.SendDebugMsg(strSQL)

  return config.CreateSQL(strSQL).RawResult

def ConstructReportValues(config, kode_jns_investasi, monthFrom, yearFrom, monthUntil, yearUntil, hasil, oFile):
  moduleapi = modman.getModule(config, 'moduleapi')
  
  oFile.write('<table style="FONT-SIZE: 11; border-collapse: collapse; border-left-width:0; border-right-width:0; border-top-width:0; border-bottom-width:0px" bordercolor="#111111" border="1" width="750" id="table3" cellpadding="2">\n')

  lsEOM = moduleapi.CreateLsEndOfMonth(monthFrom, yearFrom, monthUntil, yearUntil)

  totalNominal = 0.0
  for eom in lsEOM:
    y, m, d = eom
    config.ModDateTime.EncodeDate(y, m, d)
    strTanggal = '%d %s %d' % (d, moduleapi.IntMonthToStr(m), y)
    tanggalDT = config.ModDateTime.EncodeDate(y, m, d)
    tanggalDTTmrw = tanggalDT + 1
    strDateUntilTmrwSQL = config.FormatDateTime('yyyy-mm-dd', tanggalDTTmrw)


    resSQLTI = resSQLTotalInv(config, kode_jns_investasi, strDateUntilTmrwSQL)
    nominal = 0.0
    if not resSQLTI.Eof:
      nominal = resSQLTI.nominal or 0.0
    totalNominal += nominal

    oFile.write('	<tr>\n')
    oFile.write('		<td width="600" align="center" style="border-style: none; border-width: medium; " bgcolor="#FFFFFF">\n')
    oFile.write('		<p align="left"><b><font size="2">Total Investasi '+ strTanggal +'</font></b></td>\n')
    oFile.write('		<td width="150" align="center" style="border-style: none; border-width: medium; " bgcolor="#FFFFFF">\n')
    oFile.write('		<p align="right"><b>\n')
    oFile.write('		<font size="2">'+ moduleapi.FormatFloatStd(config, nominal) +'</font></b></td>\n')
    oFile.write('	</tr>\n')


  rataNominal = totalNominal / len(lsEOM)

  oFile.write('	<tr>\n')
  oFile.write('		<td width="600" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="left"><b><font size="2">Rata-rata Investasi</font></b></td>\n')
  oFile.write('		<td width="150" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="right"><b>\n')
  oFile.write('		<font size="2">'+ moduleapi.FormatFloatStd(config, rataNominal) +'</font></b></td>\n')
  oFile.write('	</tr>\n')

  strROI = config.FormatFloat('0.##', hasil * 100.0/rataNominal)
  
  oFile.write('	<tr>\n')
  oFile.write('		<td width="600" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="left"><b><font size="2">ROI (%)</font></b></td>\n')
  oFile.write('		<td width="150" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="right"><b>\n')
  oFile.write('		<font size="2">'+ strROI +'% </font></b></td>\n')
  oFile.write('	</tr>\n')


  ## Looping rata-rata investasi by ade herman 2011-05-24
  rateRoi = 0.0
  counter = 0

  #if monthFrom == monthUntil:

  while monthFrom <= monthUntil:

     # Variable
     lastday_from      = moduleapi.GetLastDayOfMonth(monthFrom, yearFrom)
     lastday_until     = moduleapi.GetLastDayOfMonth(monthUntil, yearUntil)
     lastday_investasi = moduleapi.GetLastDayOfMonth((monthFrom - 1), yearUntil)

     strtgl_from   = '%s-%s-%s 23:59:59.000' % (yearFrom, monthFrom, lastday_from)
     strtgl_until  = '%s-%s-%s 23:59:59.000' % (yearUntil, monthUntil, lastday_until)
     strtgl_investasi = '%s-%s-%s 23:59:59.000' % (yearFrom, monthFrom - 1, lastday_investasi)

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
     #config.SendDebugMsg('contribusiC : '+str(contribusiC))
     
     if kode_jns_investasi == 'D':
        totRate = ((proporsiA / contribusiA)*100)
        #strReturn = config.FormatFloat('0.##', ((proporsiA / contribusiA)*100))
     if kode_jns_investasi == 'O':
        totRate = (((proporsiB + hi_sukuk) / (inv_sukuk + contribusiB))*100)
        #strReturn = config.FormatFloat('0.##', (((proporsiB + hi_sukuk) / (inv_sukuk + contribusiB))*100))
     if kode_jns_investasi == 'R':
        totRate = (((proporsiC + hi_reksadana) / (inv_reksadana + contribusiC))*100)
        #strReturn = config.FormatFloat('0.##', (((proporsiC + hi_reksadana) / (inv_reksadana + contribusiC))*100))

     rateRoi = rateRoi + totRate
     counter += 1
     monthFrom += 1
     
  strReturn = config.FormatFloat('0.##', (rateRoi/counter))
  
  oFile.write('	<tr>\n')
  oFile.write('		<td width="600" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="left"><b><font size="2">Rata-Rata Hasil Investasi (%)</font></b></td>\n')
  oFile.write('		<td width="150" align="center" style="border-style: none; border-width: medium; " bgcolor="#EFEFEF">\n')
  oFile.write('		<p align="right"><b>\n')
  oFile.write('		<font size="2">'+ strReturn +'% </font></b></td>\n')
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
    , parameter.FirstRecord.kode_jns_investasi
    , parameter.FirstRecord.monthFrom
    , parameter.FirstRecord.yearFrom
    , parameter.FirstRecord.monthUntil
    , parameter.FirstRecord.yearUntil
    , oFile
  )

  strDateFromSQL = '%d-%d-1' % (parameter.FirstRecord.yearFrom, parameter.FirstRecord.monthFrom)

  moduleapi = modman.getModule(config, 'moduleapi')
  dateUntilTmrwDT = config.ModDateTime.EncodeDate(
    parameter.FirstRecord.yearUntil
    , parameter.FirstRecord.monthUntil
    , moduleapi.GetLastDayOfMonth(parameter.FirstRecord.monthUntil, parameter.FirstRecord.yearUntil)
  ) + 1
  strDateUntilTmrwSQL = config.FormatDateTime('yyyy-mm-dd', dateUntilTmrwDT)

  hasil =ConstructReportHasil( config, parameter.FirstRecord.kode_jns_investasi, strDateFromSQL, strDateUntilTmrwSQL, oFile)

  ConstructReportValues(
    config
    , parameter.FirstRecord.kode_jns_investasi
    , parameter.FirstRecord.monthFrom
    , parameter.FirstRecord.yearFrom
    , parameter.FirstRecord.monthUntil
    , parameter.FirstRecord.yearUntil
    , hasil
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
