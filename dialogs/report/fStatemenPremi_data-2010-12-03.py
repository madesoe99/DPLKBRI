import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi

def ConstructReportHeader(config, no_peserta, dari_tanggal, hingga_tanggal, oFile):
  oNasabahDPLK = config.CreatePObjImplProxy('NasabahDPLK')
  oNasabahDPLK.Key = no_peserta

  #kamus kolektibilitas premi
  dictKolektibilitasPremi = {'T':'Lancar','F':'Tidak Lancar'}

  #cek apakah peserta ikutan wasiat ummat
  if oNasabahDPLK.LRekeningDPLK.status_wasiat_ummat == 'F':
    #bukan peserta wasiat ummat
    raise '\n\nPERINGATAN','Peserta tidak ikut kepesertaan Wasiat Ummat!'

  #ambil data peserta
  alamat = '%s %s RTRW: %s' % (oNasabahDPLK.alamat_jalan, oNasabahDPLK.alamat_jalan2,\
    oNasabahDPLK.alamat_rtrw)
  kota_kodepos = '%s %s' % (oNasabahDPLK.alamat_kota, oNasabahDPLK.alamat_kode_pos)
  periode = '%s - %s' % (config.FormatDateTime('d mmmm yyyy',dari_tanggal), config.FormatDateTime('d mmmm yyyy',hingga_tanggal))

  #ambil data wasiat ummat
  oNasabahDPLK.LRekeningDPLK.Ls_RekeningWasiatUmmat.First()
  oRWU = oNasabahDPLK.LRekeningDPLK.Ls_RekeningWasiatUmmat.CurrentElement

  if oRWU.tgl_akseptasi not in [None,[]]:
    y,m,d = oRWU.tgl_akseptasi[:3]
    tglAkseptasi = config.FormatDateTime('d mmmm yyyy',\
      config.ModLibUtils.EncodeDate(y,m,d))
  else:
    tglAkseptasi = ''

  if oRWU.tgl_berakhir not in [None,[]]:
    y,m,d = oRWU.tgl_berakhir[:3]
    tglBerakhir = config.FormatDateTime('d mmmm yyyy',\
      config.ModLibUtils.EncodeDate(y,m,d))
  else:
    tglBerakhir = ''

  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Statemen Premi</title>\n')
  oFile.write('</head>\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('<b>DANA PENSIUN LEMBAGA KEUANGAN</b>\n')
  oFile.write('<br><b>PT. Bank Rakyat Indonesia, Tbk.</b>\n')
  oFile.write('\n')
  oFile.write('\n')
  oFile.write('<table border="2" width="100%" id="table1" style="border-width: 0px">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td colspan="6" align="center" style="border-style: none; border-width: medium">\n')
  oFile.write('		<b>STATEMEN PREMI</b></td>\n')
  oFile.write('	</tr>&nbsp;\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="20%" style="border-style: none; border-width: medium"><b>No. \n')
  oFile.write('		Peserta</b></td>\n')
  oFile.write('		<td width="2%" style="border-style: none; border-width: medium">:</td>\n')
  oFile.write('		<td width="46%" style="border-style: none; border-width: medium">'+ no_peserta +'</td>\n')
  oFile.write('		<td width="20%" style="border-style: none; border-width: medium"></td>\n')
  oFile.write('		<td width="2%" style="border-style: none; border-width: medium"></td>\n')
  oFile.write('		<td width="10%" style="border-style: none; border-width: medium"></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="20%" style="border-style: none; border-width: medium"><b>Nama</b></td>\n')
  oFile.write('		<td width="2%" style="border-style: none; border-width: medium">:</td>\n')
  oFile.write('		<td width="46%" style="border-style: none; border-width: medium">'+ oNasabahDPLK.nama_lengkap +'</td>\n')
  oFile.write('		<td width="20%" style="border-style: none; border-width: medium"></td>\n')
  oFile.write('		<td width="2%" style="border-style: none; border-width: medium"></td>\n')
  oFile.write('		<td width="10%" style="border-style: none; border-width: medium"></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="20%" style="border-style: none; border-width: medium"><b>Alamat</b></td>\n')
  oFile.write('		<td width="2%" style="border-style: none; border-width: medium">:</td>\n')
  oFile.write('		<td width="46%" style="border-style: none; border-width: medium">'+ alamat +'</td>\n')
  oFile.write('		<td width="20%" style="border-style: none; border-width: medium"></td>\n')
  oFile.write('		<td width="2%" style="border-style: none; border-width: medium"></td>\n')
  oFile.write('		<td width="10%" style="border-style: none; border-width: medium"></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="20%" style="border-style: none; border-width: medium">&nbsp;</td>\n')
  oFile.write('		<td width="2%" style="border-style: none; border-width: medium">&nbsp;</td>\n')
  oFile.write('		<td width="46%" style="border-style: none; border-width: medium">'+ kota_kodepos +'</td>\n')
  oFile.write('		<td width="20%" style="border-style: none; border-width: medium"></td>\n')
  oFile.write('		<td width="2%" style="border-style: none; border-width: medium"></td>\n')
  oFile.write('		<td width="10%" style="border-style: none; border-width: medium"></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="20%" style="border-style: none; border-width: medium"><b>Tanggal Akseptasi</b></td>\n')
  oFile.write('		<td width="2%" style="border-style: none; border-width: medium">:</td>\n')
  oFile.write('		<td width="46%" style="border-style: none; border-width: medium">'+ tglAkseptasi +'</td>\n')
  oFile.write('		<td width="20%" style="border-style: none; border-width: medium"><b>Besar Premi</b></td>\n')
  oFile.write('		<td width="2%" style="border-style: none; border-width: medium">:</td>\n')
  oFile.write('		<td width="10%" style="border-style: none; border-width: medium">'+ moduleapi.FormatFloatStd(config, oRWU.besar_premi) +'</td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="20%" style="border-style: none; border-width: medium"><b>Tanggal Berakhir</b></td>\n')
  oFile.write('		<td width="2%" style="border-style: none; border-width: medium">:</td>\n')
  oFile.write('		<td width="46%" style="border-style: none; border-width: medium">'+ tglBerakhir +'</td>\n')
  oFile.write('		<td width="20%" style="border-style: none; border-width: medium"><b>Kolektibilitas Premi</b></td>\n')
  oFile.write('		<td width="2%" style="border-style: none; border-width: medium">:</td>\n')
  oFile.write('		<td width="10%" style="border-style: none; border-width: medium">'+ str(dictKolektibilitasPremi[oNasabahDPLK.LRekeningDPLK.collectivity_wasiat_ummat]) +'</td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="20%" style="border-style: none; border-width: medium"><b>Manfaat Asuransi</b></td>\n')
  oFile.write('		<td width="2%" style="border-style: none; border-width: medium">:</td>\n')
  oFile.write('		<td width="46%" style="border-style: none; border-width: medium">'+ moduleapi.FormatFloatStd(config, oRWU.manfaat_asuransi) +'</td>\n')
  oFile.write('		<td width="20%" style="border-style: none; border-width: medium"><b>Tunggakan Premi</b></td>\n')
  oFile.write('		<td width="2%" style="border-style: none; border-width: medium">:</td>\n')
  oFile.write('		<td width="10%" style="border-style: none; border-width: medium">'+ moduleapi.FormatFloatStd(config, oNasabahDPLK.LRekeningDPLK.kewajiban_wasiat_ummat) +'</td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="20%" style="border-style: none; border-width: medium"><b>Periode</b></td>\n')
  oFile.write('		<td width="2%" style="border-style: none; border-width: medium">:</td>\n')
  oFile.write('		<td width="46%" style="border-style: none; border-width: medium">'+ periode +'</td>\n')
  oFile.write('		<td width="20%" style="border-style: none; border-width: medium"></td>\n')
  oFile.write('		<td width="2%" style="border-style: none; border-width: medium"></td>\n')
  oFile.write('		<td width="10%" style="border-style: none; border-width: medium"></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('</table>\n')

def ContructSumValues(config, no_peserta, str_dari_tanggal, str_hingga_tanggal_plus, \
  oFile, dari_tanggal, hingga_tanggal):

  sSQLBefore = 'select isnull(sum(t.MUTASI_PREMI),0.0) as sumPremiBefore\
                from TRANSAKSIPREMI t\
                where t.TGL_TRANSAKSI < \'%s\' and\
                      t.NO_PESERTA = \'%s\' and\
                      t.ISCOMMITTED = \'T\''\
                % (str_dari_tanggal,no_peserta)
  rSQLBefore = config.CreateSQL(sSQLBefore).RawResult

  sSQL = 'select isnull(sum(t.MUTASI_PREMI),0.0) as sumPremi\
          from TRANSAKSIPREMI t\
          where t.TGL_TRANSAKSI >= \'%s\' and\
                t.TGL_TRANSAKSI < \'%s\' and\
                t.NO_PESERTA = \'%s\' and\
                t.ISCOMMITTED = \'T\''\
          % (str_dari_tanggal,str_hingga_tanggal_plus,no_peserta)
  rSQL = config.CreateSQL(sSQL).RawResult

  rSQL.First()
  rSQLBefore.First()
  TotalPremi = 0.0
  if not (rSQL.Eof or rSQLBefore.Eof):
    TotalPremi = rSQLBefore.sumPremiBefore + rSQL.sumPremi

  #write to file
  oFile.write('<table border="2" width="100%" id="table2" style="border-width: 0px">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="20%" align="left"   style="border-style: none; border-width: medium"></td>\n')
  oFile.write('		<td width="30%" align="left"   style="border-style: none; border-width: medium"><font size="2">Saldo Akhir Premi per '+ config.FormatDateTime('d mmmm yyyy',dari_tanggal-1) +'</font></td>\n')
  oFile.write('		<td width="2%"  align="center" style="border-style: none; border-width: medium"><font size="2">:</font></td>\n')
  oFile.write('		<td width="20%" align="right"  style="border-style: none; border-width: medium"><font size="2">'+ moduleapi.FormatFloatStd(config, rSQLBefore.sumPremiBefore) +'</font></td>\n')
  oFile.write('		<td width="28%" align="left"  style="border-style: none; border-width: medium"><font size="2"></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="20%" align="left"   style="border-style: none; border-width: medium"></td>\n')
  oFile.write('		<td width="30%" align="left"   style="border-style: none; border-width: medium"><font size="2">Akumulasi Premi</font></td>\n')
  oFile.write('		<td width="2%"  align="center" style="border-style: none; border-width: medium"><font size="2">:</font></td>\n')
  oFile.write('		<td width="20%" align="right"  style="border-style: none; border-width: medium"><font size="2">'+ moduleapi.FormatFloatStd(config, rSQL.sumPremi) +'</font></td>\n')
  oFile.write('		<td width="28%" align="left"  style="border-style: none; border-width: medium"><font size="2"></font></td>\n')
  oFile.write('	</tr>&nbsp;\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="20%" align="left"   style="border-style: none; border-width: medium"></td>\n')
  oFile.write('		<td width="30%" align="left"   style="border-style: none; border-width: medium"><font size="2">Total Premi per '+ config.FormatDateTime('d mmmm yyyy',hingga_tanggal) +'</font></td>\n')
  oFile.write('		<td width="2%"  align="center" style="border-style: none; border-width: medium"><font size="2">:</font></td>\n')
  oFile.write('		<td width="20%" align="right"  style="border-style: none; border-width: medium"><font size="2">'+ moduleapi.FormatFloatStd(config, TotalPremi) +'</font></td>\n')
  oFile.write('		<td width="28%" align="left"  style="border-style: none; border-width: medium"><font size="2"></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('</table>&nbsp;\n')

  return rSQLBefore.sumPremiBefore

def resSQLCatMutasiIndv(config, no_peserta, str_dari_tanggal, str_hingga_tanggal_plus):
  strSQL = 'select t.TGL_TRANSAKSI,\
                   t.JENIS_TRANSAKSI,\
                   e.enum_description,\
                   t.ISDEBET,\
                   isnull(t.MUTASI_PREMI,0.0) as Premi\
            from TRANSAKSIPREMI t, ENUM_VARCHAR e\
            where t.TGL_TRANSAKSI >= \'%s\' and\
                  t.TGL_TRANSAKSI < \'%s\' and\
                  t.NO_PESERTA = \'%s\' and\
                  t.ISCOMMITTED = \'T\' and\
                  t.JENIS_TRANSAKSI = e.enum_value and\
                  e.enum_name = \'eJenisTransaksiPremi\'\
            order by t.TGL_TRANSAKSI'\
            % (str_dari_tanggal, str_hingga_tanggal_plus, no_peserta)
  return config.CreateSQL(strSQL).RawResult

def ConstructReportValues(config, no_peserta, str_dari_tanggal, str_hingga_tanggal_plus, saldo_awal, oFile):
  #inisiasi tabel report values, write to file
  oFile.write('<table border="2" width="100%" id="table3" bordercolorlight="#000000" bordercolordark="#000000" style="border-collapse: collapse" bordercolor="#000000" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="15%" align="center" style="border-style: solid; border-width: 1px"><b>TANGGAL (dd/mm/yyyy)</b></td>\n')
  oFile.write('		<td width="15%" align="center" style="border-style: solid; border-width: 1px"><b>MUTASI</b></td>\n')
  oFile.write('		<td width="30%" align="center" style="border-style: solid; border-width: 1px"><b>TRANSAKSI</b></td>\n')
  oFile.write('		<td width="20%" align="center" style="border-style: solid; border-width: 1px"><b>NOMINAL</b></td>\n')
  oFile.write('		<td width="20%" align="center" style="border-style: solid; border-width: 1px"><b>SALDO</b></td>\n')
  oFile.write('	</tr>\n')

  resSQL = resSQLCatMutasiIndv(config, no_peserta, str_dari_tanggal, str_hingga_tanggal_plus)

  saldo_curr = saldo_awal
  resSQL.First()
  while not resSQL.Eof:
    # tanggal dengan format dd/mm/yyyy
    y, m, d = resSQL.TGL_TRANSAKSI[:3]
    tanggal = '%s/%s/%s' % (moduleapi.MyZFill(str(d),2), moduleapi.MyZFill(str(m),2), str(y))

    if  resSQL.ISDEBET == 'T':
      mutasi = 'D'
    else:
      mutasi = 'C'

    transaksi = '(%s) <font size="2">%s</font>' % (resSQL.JENIS_TRANSAKSI, resSQL.enum_description)

    saldo_curr += resSQL.Premi

    oFile.write('	<tr>\n')
    oFile.write('		<td width="15%" align="center" style="border-style: solid; border-width: 1px">'+ tanggal +'</td>\n')
    oFile.write('		<td width="15%" align="center" style="border-style: solid; border-width: 1px">'+ mutasi +'</td>\n')
    oFile.write('		<td width="30%" align="left" style="border-style: solid; border-width: 1px">'+ transaksi +'</td>\n')
    oFile.write('		<td width="20%" align="right" style="border-style: solid; border-width: 1px">'+ moduleapi.FormatFloatStd(config, abs(resSQL.Premi)) +'</td>\n')
    oFile.write('		<td width="20%" align="right" style="border-style: solid; border-width: 1px">'+ moduleapi.FormatFloatStd(config, saldo_curr) +'</td>\n')
    oFile.write('	</tr>\n')

    resSQL.Next()

  return saldo_curr

def ConstructReportTrailer(config, saldo_akhir, oFile):
  oFile.write('	<tr>\n')
  oFile.write('		<td width="80%" style="border-style: solid; border-width: 1px" colspan="4" align="right"><b>SALDO AKHIR</b></td>\n')
  oFile.write('		<td width="20%" style="border-style: solid; border-width: 1px">\n')
  oFile.write('		<p align="right"><b>'+ moduleapi.FormatFloatStd(config, saldo_akhir) +'</b></td>\n')
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
  oFile.write('</body>\n')
  oFile.write('\n')
  oFile.write('</html>\n')

def WriteToFile(config, parameter, oFile):
  no_peserta = parameter.FirstRecord.no_peserta
  dari_tanggal = parameter.FirstRecord.dari_tanggal
  hingga_tanggal = parameter.FirstRecord.hingga_tanggal

  str_dari_tanggal = config.FormatDateTime('yyyy-mm-dd', dari_tanggal)
  str_hingga_tanggal_plus = config.FormatDateTime('yyyy-mm-dd', hingga_tanggal + 1)

  #saldo_awal = moduleapi.GetSaldoAwal(config, no_peserta, str_dari_tanggal)

  ConstructReportHeader(config, no_peserta, dari_tanggal, hingga_tanggal, oFile)
  saldo_awal = ContructSumValues(config, no_peserta, str_dari_tanggal, \
    str_hingga_tanggal_plus, oFile, dari_tanggal, hingga_tanggal)
  saldo_akhir = ConstructReportValues(config, no_peserta, str_dari_tanggal, \
    str_hingga_tanggal_plus, saldo_awal, oFile)
  ConstructReportTrailer(config, saldo_akhir, oFile)

def CreateReport(config, parameter, returnpacket):
  sBaseFileName = 'statemen_premi.htm'
  sFileName = config.UserHomeDirectory + sBaseFileName

  oFile = open(sFileName, 'w')
  WriteToFile(config, parameter, oFile)
  oFile.close()

  returnpacket.CreateValues(['filename',sBaseFileName])

  # pack as stream
  sw = returnpacket.AddStreamWrapper()
  sw.LoadFromFile(sFileName)
  sw.MIMEType = config.AppObject.GetMIMETypeFromExtension(sFileName)
