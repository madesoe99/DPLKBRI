import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi

def FormSetDataEx(buffers, params):
  if params.DatasetCount == 0:
    return

  config = buffers.config
  no_peserta = params.FirstRecord.no_peserta
  oNasabah = config.CreatePObjImplProxy("NasabahDPLK")
  oNasabah.Key = no_peserta
  
  ds = buffers.uipNoData.Dataset
  rec = ds.AddRecord()
  rec.SetFieldByName("LNasabahDPLK.no_peserta", no_peserta)
  rec.SetFieldByName("LNasabahDPLK.nama_lengkap", oNasabah.nama_lengkap)
  
def ConstructReportHeader(config, no_peserta, dari_tanggal, hingga_tanggal, saldo_awal, oFile):
  oNasabahDPLK = config.CreatePObjImplProxy('NasabahDPLK')
  oNasabahDPLK.Key = no_peserta

  alamat = '%s %s RTRW: %s %s ' % (oNasabahDPLK.alamat_surat_jalan, oNasabahDPLK.alamat_jalan2,\
    oNasabahDPLK.alamat_rtrw, oNasabahDPLK.alamat_surat_kelurahan, )
  kota_kodepos = '%s %s %s' % (oNasabahDPLK.alamat_surat_kecamatan, oNasabahDPLK.alamat_surat_kota,\
    oNasabahDPLK.alamat_surat_kode_pos)
  paket_investasi = '(%s) %s' % (oNasabahDPLK.LRekeningDPLK.LPaketInvestasi.kode_paket_investasi, oNasabahDPLK.LRekeningDPLK.LPaketInvestasi.nama_paket_investasi)

  y,m,d = oNasabahDPLK.LRekeningDPLK.tgl_pensiun[:3]
  tglPensiun = config.FormatDateTime('d mmmm yyyy',\
    config.ModLibUtils.EncodeDate(y,m,d))

  pensiun = '%d [%s]' % (oNasabahDPLK.LRekeningDPLK.usia_pensiun, tglPensiun)
  periode = '%s - %s' % (config.FormatDateTime('d mmmm yyyy',dari_tanggal), config.FormatDateTime('d mmmm yyyy',hingga_tanggal))

  oFile.write('<html>\n')
  oFile.write('\n')
  oFile.write('<head>\n')
  oFile.write('<title>Statemen Individual</title>\n')
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
  oFile.write('		<b>STATEMEN INDIVIDUAL</b></td>\n')
  oFile.write('	</tr>&nbsp;\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="15%" style="border-style: none; border-width: medium"><b>No. \n')
  oFile.write('		Peserta</b></td>\n')
  oFile.write('		<td width="2%" style="border-style: none; border-width: medium">:</td>\n')
  oFile.write('		<td width="46%" style="border-style: none; border-width: medium">'+ no_peserta +'</td>\n')
  oFile.write('		<td width="15%" style="border-style: none; border-width: medium"><b>Usia Pensiun</b></td>\n')
  oFile.write('		<td width="2%" style="border-style: none; border-width: medium">:</td>\n')
  oFile.write('		<td width="20%" style="border-style: none; border-width: medium">'+ pensiun +'</td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="15%" style="border-style: none; border-width: medium"><b>Nama</b></td>\n')
  oFile.write('		<td width="2%" style="border-style: none; border-width: medium">:</td>\n')
  oFile.write('		<td width="46%" style="border-style: none; border-width: medium">'+ oNasabahDPLK.nama_lengkap +'</td>\n')
  oFile.write('		<td width="15%" style="border-style: none; border-width: medium"><b>Paket \n')
  oFile.write('		Investasi</b></td>\n')
  oFile.write('		<td width="2%" style="border-style: none; border-width: medium">:</td>\n')
  oFile.write('		<td width="20%" style="border-style: none; border-width: medium">'+ paket_investasi +'</td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="15%" valign="center" style="border-style: none; border-width: medium"><b>Alamat</b></td>\n')
  oFile.write('		<td width="2%" valign="center" style="border-style: none; border-width: medium">:</td>\n')
  oFile.write('		<td width="46%" valign="center" style="border-style: none; border-width: medium">'+ alamat +'</td>\n')
  oFile.write('		<td width="15%" valign="center" style="border-style: none; border-width: medium"></td>\n')
  oFile.write('		<td width="2%" valign="center" style="border-style: none; border-width: medium"></td>\n')
  oFile.write('		<td width="20%" valign="center" style="border-style: none; border-width: medium"></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="15%" style="border-style: none; border-width: medium">&nbsp;</td>\n')
  oFile.write('		<td width="2%" style="border-style: none; border-width: medium">&nbsp;</td>\n')
  oFile.write('		<td width="46%" style="border-style: none; border-width: medium">'+ kota_kodepos +'</td>\n')
  oFile.write('		<td width="15%" style="border-style: none; border-width: medium"></td>\n')
  oFile.write('		<td width="2%" style="border-style: none; border-width: medium"></td>\n')
  oFile.write('		<td width="20%" style="border-style: none; border-width: medium"></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="15%" style="border-style: none; border-width: medium"><b>Periode</b></td>\n')
  oFile.write('		<td width="2%" style="border-style: none; border-width: medium">:</td>\n')
  oFile.write('		<td width="46%" style="border-style: none; border-width: medium">'+ periode +'</td>\n')
  oFile.write('		<td width="15%" style="border-style: none; border-width: medium"></td>\n')
  oFile.write('		<td width="2%" style="border-style: none; border-width: medium"></td>\n')
  oFile.write('		<td width="20%" style="border-style: none; border-width: medium"></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('</table>\n')

def ContructSumValues(config, no_peserta, str_dari_tanggal, str_hingga_tanggal_plus, \
  saldo_awal, oFile, dari_tanggal, hingga_tanggal):

  sSQL = 'select t.KODE_JENIS_TRANSAKSI,\
                 isnull(t.KODE_TRANSAKSI_MANUAL,\'M\') as kode_transaksi_manual,\
                 isnull(sum(t.MUTASI_IURAN_PK),0.0) as sumIuranPK,\
                 isnull(sum(t.MUTASI_IURAN_PST),0.0) as sumIuranPeserta,\
                 isnull(sum(t.MUTASI_PENGEMBANGAN),0.0) as sumPengembangan,\
                 isnull(sum(t.MUTASI_PERALIHAN),0.0) as sumPeralihan\
          from TRANSAKSIDPLK t\
          where t.TGL_TRANSAKSI >= \'%s\' and\
                t.TGL_TRANSAKSI < \'%s\' and\
                t.NO_PESERTA = \'%s\' and\
                t.KODE_JENIS_TRANSAKSI not in (\'A\',\'B\') and\
                t.ISCOMMITTED = \'T\'\
          group by t.KODE_JENIS_TRANSAKSI, kode_transaksi_manual'\
          % (str_dari_tanggal,str_hingga_tanggal_plus,no_peserta)
  config.SendDebugMsg(sSQL)
  rSQL = config.CreateSQL(sSQL).RawResult

  #inisialisasi dictionary kode jenis transaksi dan sum dana untuk kode tersebut
  dictJenisTransaksi = {'C':0.0,'D':0.0,'F':0.0,'G':0.0,'H':0.0,'I':0.0,'J':0.0,\
    'K':0.0,'M':0.0,'O':0.0,'P':0.0,'V':0.0,'W':0.0,'X':0.0,'E':0.0}

  #tentukan jenis transaksi
  sumDanaTotal = 0.0
  rSQL.First()
  while not rSQL.Eof:
    sumDana = (rSQL.sumIuranPK or 0.0) + (rSQL.sumIuranPeserta or 0.0) + (rSQL.sumPengembangan or 0.0) + \
      (rSQL.sumPeralihan or 0.0)
    if rSQL.KODE_JENIS_TRANSAKSI != 'M':
      # bukan transaksi manual
      dictJenisTransaksi[rSQL.KODE_JENIS_TRANSAKSI] += sumDana
    else:
      # transaksi manual, disesuaikan dengan kode_transaksi_manual
      dictJenisTransaksi[rSQL.kode_transaksi_manual] += sumDana
    sumDanaTotal += sumDana
    rSQL.Next()

  #write to file
  oFile.write('<table border="2" width="100%" id="table2" style="border-width: 0px">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="20%" align="left"   style="border-style: none; border-width: medium"></td>\n')
  oFile.write('		<td width="30%" align="left"   style="border-style: none; border-width: medium"><font size="2">Saldo Akhir per '+ config.FormatDateTime('d mmmm yyyy',dari_tanggal-1) +'</font></td>\n')
  oFile.write('		<td width="2%"  align="center" style="border-style: none; border-width: medium"><font size="2">:</font></td>\n')
  oFile.write('		<td width="20%" align="right"  style="border-style: none; border-width: medium"><font size="2">'+ moduleapi.FormatFloatStd(config, saldo_awal) +'</font></td>\n')
  oFile.write('		<td width="28%" align="left"  style="border-style: none; border-width: medium"><font size="2"></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="20%" align="left"   style="border-style: none; border-width: medium"></td>\n')
  oFile.write('		<td width="30%" align="left"   style="border-style: none; border-width: medium"><font size="2">Akumulasi Iuran</font></td>\n')
  oFile.write('		<td width="2%"  align="center" style="border-style: none; border-width: medium"><font size="2">:</font></td>\n')
  oFile.write('		<td width="20%" align="right"  style="border-style: none; border-width: medium"><font size="2">'+ moduleapi.FormatFloatStd(config, dictJenisTransaksi['K']) +'</font></td>\n')
  oFile.write('		<td width="28%" align="left"  style="border-style: none; border-width: medium"><font size="2"></font></td>\n')
  oFile.write('	</tr>\n')
  akumPenarikanTotal = abs((dictJenisTransaksi['V'] or 0.0) + (dictJenisTransaksi['W'] or 0.0) + (dictJenisTransaksi['E'] or 0.0))
  oFile.write('	<tr>\n')
  oFile.write('		<td width="20%" align="left"   style="border-style: none; border-width: medium"></td>\n')
  oFile.write('		<td width="30%" align="left"   style="border-style: none; border-width: medium"><font size="2">Akumulasi Penarikan</font></td>\n')
  oFile.write('		<td width="2%"  align="center" style="border-style: none; border-width: medium"><font size="2">:</font></td>\n')
  oFile.write('		<td width="20%" align="right"  style="border-style: none; border-width: medium"><font size="2">'+ moduleapi.FormatFloatStd(config, akumPenarikanTotal) +'</font></td>\n')
  oFile.write('		<td width="28%" align="left"  style="border-style: none; border-width: medium"><font size="2"></font></td>\n')
  oFile.write('	</tr>\n')
#   oFile.write('	<tr>\n')
#   oFile.write('		<td width="20%" align="left"   style="border-style: none; border-width: medium"></td>\n')
#   oFile.write('		<td width="30%" align="left"   style="border-style: none; border-width: medium"><font size="2">Akumulasi Penarikan Sebagian</font></td>\n')
#   oFile.write('		<td width="2%"  align="center" style="border-style: none; border-width: medium"><font size="2">:</font></td>\n')
#   oFile.write('		<td width="20%" align="right"  style="border-style: none; border-width: medium"><font size="2">'+ moduleapi.FormatFloatStd(config, abs(dictJenisTransaksi['V'] or 0.0)) +'</font></td>\n')
#   oFile.write('		<td width="28%" align="left"  style="border-style: none; border-width: medium"><font size="2"></font></td>\n')
#   oFile.write('	</tr>\n')
#   oFile.write('	<tr>\n')
#   oFile.write('		<td width="20%" align="left"   style="border-style: none; border-width: medium"></td>\n')
#   oFile.write('		<td width="30%" align="left"   style="border-style: none; border-width: medium"><font size="2">Akumulasi Penarikan PHK</font></td>\n')
#   oFile.write('		<td width="2%"  align="center" style="border-style: none; border-width: medium"><font size="2">:</font></td>\n')
#   oFile.write('		<td width="20%" align="right"  style="border-style: none; border-width: medium"><font size="2">'+ moduleapi.FormatFloatStd(config, abs(dictJenisTransaksi['W'] or 0.0)) +'</font></td>\n')
#   oFile.write('		<td width="28%" align="left"  style="border-style: none; border-width: medium"><font size="2"></font></td>\n')
#   oFile.write('	</tr>\n')
#   oFile.write('	<tr>\n')
#   oFile.write('		<td width="20%" align="left"   style="border-style: none; border-width: medium"></td>\n')
#   oFile.write('		<td width="30%" align="left"   style="border-style: none; border-width: medium"><font size="2">Akumulasi Penarikan Dana</font></td>\n')
#   oFile.write('		<td width="2%"  align="center" style="border-style: none; border-width: medium"><font size="2">:</font></td>\n')
#   oFile.write('		<td width="20%" align="right"  style="border-style: none; border-width: medium"><font size="2">'+ moduleapi.FormatFloatStd(config, abs(dictJenisTransaksi['E'] or 0.0)) +'</font></td>\n')
#   oFile.write('		<td width="28%" align="left"  style="border-style: none; border-width: medium"><font size="2"></font></td>\n')
#   oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="20%" align="left"   style="border-style: none; border-width: medium"></td>\n')
  oFile.write('		<td width="30%" align="left"   style="border-style: none; border-width: medium"><font size="2">Hasil Pengembangan</font></td>\n')
  oFile.write('		<td width="2%"  align="center" style="border-style: none; border-width: medium"><font size="2">:</font></td>\n')
  oFile.write('		<td width="20%" align="right"  style="border-style: none; border-width: medium"><font size="2">'+ moduleapi.FormatFloatStd(config, dictJenisTransaksi['G']) +'</font></td>\n')
  oFile.write('		<td width="28%" align="left"  style="border-style: none; border-width: medium"><font size="2"></font></td>\n')
  oFile.write('	</tr>\n')
  akumBiayaTotal = abs((dictJenisTransaksi['D'] or 0.0) + (dictJenisTransaksi['C'] or 0.0)+ (dictJenisTransaksi['X'] or 0.0))
  oFile.write('	<tr>\n')
  oFile.write('		<td width="20%" align="left"   style="border-style: none; border-width: medium"></td>\n')
  oFile.write('		<td width="30%" align="left"   style="border-style: none; border-width: medium"><font size="2">Biaya Adm. dan Pengelolaan Dana</font></td>\n')
  oFile.write('		<td width="2%"  align="center" style="border-style: none; border-width: medium"><font size="2">:</font></td>\n')
  oFile.write('		<td width="20%" align="right"  style="border-style: none; border-width: medium"><font size="2">'+ moduleapi.FormatFloatStd(config, akumBiayaTotal) +'</font></td>\n')
  oFile.write('		<td width="28%" align="left"  style="border-style: none; border-width: medium"><font size="2"></font></td>\n')
  oFile.write('	</tr>\n')
#   oFile.write('	<tr>\n')
#   oFile.write('		<td width="20%" align="left"   style="border-style: none; border-width: medium"></td>\n')
#   oFile.write('		<td width="30%" align="left"   style="border-style: none; border-width: medium"><font size="2">Biaya Administrasi</font></td>\n')
#   oFile.write('		<td width="2%"  align="center" style="border-style: none; border-width: medium"><font size="2">:</font></td>\n')
#   oFile.write('		<td width="20%" align="right"  style="border-style: none; border-width: medium"><font size="2">'+ moduleapi.FormatFloatStd(config, abs(dictJenisTransaksi['D'] or 0.0)) +'</font></td>\n')
#   oFile.write('		<td width="28%" align="left"  style="border-style: none; border-width: medium"><font size="2"></font></td>\n')
#   oFile.write('	</tr>\n')
#   oFile.write('	<tr>\n')
#   oFile.write('		<td width="20%" align="left"   style="border-style: none; border-width: medium"></td>\n')
#   oFile.write('		<td width="30%" align="left"   style="border-style: none; border-width: medium"><font size="2">Biaya Pengelolaan Dana</font></td>\n')
#   oFile.write('		<td width="2%"  align="center" style="border-style: none; border-width: medium"><font size="2">:</font></td>\n')
#   oFile.write('		<td width="20%" align="right"  style="border-style: none; border-width: medium"><font size="2">'+ moduleapi.FormatFloatStd(config, abs(dictJenisTransaksi['C'] or 0.0)) +'</font></td>\n')
#   oFile.write('		<td width="28%" align="left"  style="border-style: none; border-width: medium"><font size="2"></font></td>\n')
#   oFile.write('	</tr>\n')
  akumPengalihanTotal = abs((dictJenisTransaksi['I'] or 0.0) + (dictJenisTransaksi['O'] or 0.0) + (dictJenisTransaksi['P'] or 0.0))
  oFile.write('	<tr>\n')
  oFile.write('		<td width="20%" align="left"   style="border-style: none; border-width: medium"></td>\n')
  oFile.write('		<td width="30%" align="left"   style="border-style: none; border-width: medium"><font size="2">Pengalihan Dari DPLK/DPPK/DPK Lain</font></td>\n')
  oFile.write('		<td width="2%"  align="center" style="border-style: none; border-width: medium"><font size="2">:</font></td>\n')
  oFile.write('		<td width="20%" align="right"  style="border-style: none; border-width: medium"><font size="2">'+ moduleapi.FormatFloatStd(config, akumPengalihanTotal) +'</font></td>\n')
  oFile.write('		<td width="28%" align="left"  style="border-style: none; border-width: medium"><font size="2"></font></td>\n')
  oFile.write('	</tr>\n')
#   oFile.write('	<tr>\n')
#   oFile.write('		<td width="20%" align="left"   style="border-style: none; border-width: medium"></td>\n')
#   oFile.write('		<td width="30%" align="left"   style="border-style: none; border-width: medium"><font size="2">Pengalihan Dari DPLK Lain</font></td>\n')
#   oFile.write('		<td width="2%"  align="center" style="border-style: none; border-width: medium"><font size="2">:</font></td>\n')
#   oFile.write('		<td width="20%" align="right"  style="border-style: none; border-width: medium"><font size="2">'+ moduleapi.FormatFloatStd(config, abs(dictJenisTransaksi['I'] or 0.0)) +'</font></td>\n')
#   oFile.write('		<td width="28%" align="left"  style="border-style: none; border-width: medium"><font size="2"></font></td>\n')
#   oFile.write('	</tr>\n')
#   oFile.write('	<tr>\n')
#   oFile.write('		<td width="20%" align="left"   style="border-style: none; border-width: medium"></td>\n')
#   oFile.write('		<td width="30%" align="left"   style="border-style: none; border-width: medium"><font size="2">Pengalihan Dari DPPK Lain</font></td>\n')
#   oFile.write('		<td width="2%"  align="center" style="border-style: none; border-width: medium"><font size="2">:</font></td>\n')
#   oFile.write('		<td width="20%" align="right"  style="border-style: none; border-width: medium"><font size="2">'+ moduleapi.FormatFloatStd(config, abs(dictJenisTransaksi['O'] or 0.0)) +'</font></td>\n')
#   oFile.write('		<td width="28%" align="left"  style="border-style: none; border-width: medium"><font size="2"></font></td>\n')
#   oFile.write('	</tr>\n')
#   oFile.write('	<tr>\n')
#   oFile.write('		<td width="20%" align="left"   style="border-style: none; border-width: medium"></td>\n')
#   oFile.write('		<td width="30%" align="left"   style="border-style: none; border-width: medium"><font size="2">Pengalihan Dari DPK Lain</font></td>\n')
#   oFile.write('		<td width="2%"  align="center" style="border-style: none; border-width: medium"><font size="2">:</font></td>\n')
#   oFile.write('		<td width="20%" align="right"  style="border-style: none; border-width: medium"><font size="2">'+ moduleapi.FormatFloatStd(config, abs(dictJenisTransaksi['P'] or 0.0)) +'</font></td>\n')
#   oFile.write('		<td width="28%" align="left"  style="border-style: none; border-width: medium"><font size="2"></font></td>\n')
#   oFile.write('	</tr>&nbsp;\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="20%" align="left"   style="border-style: none; border-width: medium"></td>\n')
  oFile.write('		<td width="30%" align="left"   style="border-style: none; border-width: medium"><font size="2">Total Dana per '+ config.FormatDateTime('d mmmm yyyy',hingga_tanggal) +'</font></td>\n')
  oFile.write('		<td width="2%"  align="center" style="border-style: none; border-width: medium"><font size="2">:</font></td>\n')
  oFile.write('		<td width="20%" align="right"  style="border-style: none; border-width: medium"><font size="2">'+ moduleapi.FormatFloatStd(config, sumDanaTotal+saldo_awal) +'</font></td>\n')
  oFile.write('		<td width="28%" align="left"  style="border-style: none; border-width: medium"><font size="2"></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('</table>&nbsp;\n')

def resSQLCatMutasiIndv(config, no_peserta, str_dari_tanggal, str_hingga_tanggal_plus):
  strSQL = '\
    select tgl_transaksi \
      , kode_jenis_transaksi \
      , isnull(kode_transaksi_manual,\'M\') as kode_transaksi_manual \
      , isnull(mutasi_peralihan,0.0) + isnull(mutasi_pengembangan,0.0) + isnull(mutasi_iuran_pst,0.0) + isnull(mutasi_iuran_pk,0.0) as mutasi_total \
      , keterangan \
    from TransaksiDPLK \
    where tgl_transaksi >= \'%s\' \
      and tgl_transaksi < \'%s\' \
      and no_peserta = \'%s\' \
      and kode_jenis_transaksi not in (\'A\',\'B\') \
      and isCommitted = \'T\' \
    order by tgl_transaksi, id_transaksi' \
    % (str_dari_tanggal, str_hingga_tanggal_plus, no_peserta)
  config.SendDebugMsg(strSQL)
  return config.CreateSQL(strSQL).RawResult

def ConstructReportValues(config, no_peserta, str_dari_tanggal, str_hingga_tanggal_plus, saldo_awal, oFile):
  #inisiasi tabel report values, write to file
  oFile.write('<table border="2" width="100%" id="table3" bordercolorlight="#000000" bordercolordark="#000000" style="border-collapse: collapse" bordercolor="#000000" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="15%" align="center" style="border-style: solid; border-width: 1px"><b>TANGGAL<br>\n')
  oFile.write('		(dd/mm/yyyy)</b></td>\n')
  oFile.write('		<td width="15%" align="center" style="border-style: solid; border-width: 1px"><b>MUTASI</b></td>\n')
  oFile.write('		<td width="30%" align="center" style="border-style: solid; border-width: 1px"><b>TRANSAKSI</b></td>\n')
#  oFile.write('		<td width="40%" align="center" style="border-style: solid; border-width: 1px"><b>KETERANGAN</b></td>\n')
  oFile.write('		<td width="20%" align="center" style="border-style: solid; border-width: 1px"><b>NOMINAL</b></td>\n')
  oFile.write('		<td width="20%" align="center" style="border-style: solid; border-width: 1px"><b>SALDO</b></td>\n')
  oFile.write('	</tr>\n')

  resSQL = resSQLCatMutasiIndv(config, no_peserta, str_dari_tanggal, str_hingga_tanggal_plus)

  dictJenisTransaksiDPLK = {'A':'Pendaftaran','B':'Pembayaran Premi',\
    'C':'Biaya Pengelolaan Dana','D':'Biaya Administrasi Tahunan',\
    'F':'Pengubahan Jenis Investasi','G':'Bagi Hasil','H':'Pengalihan ke DPLK Lain',\
    'I':'Pengalihan dari DPLK Lain','J':'Pengambilan Manfaat','K':'Iuran Peserta',\
    'M':'Transaksi DPLK Manual','O':'Pengalihan dari DPPK Lain',\
    'P':'Pengalihan dari DPK Lain','V':'Penarikan Dana 30%',\
    'W':'Penarikan Dana PHK','X':'Biaya Administrasi Transaksi',\
    'E':'Pernarikan Dana'}

  saldo_curr = saldo_awal
  resSQL.First()
  while not resSQL.Eof:
    y, m, d = resSQL.tgl_transaksi[:3]
    # tanggal dengan format dd/mm/yyyy
    tanggal = '%s/%s/%s' % (moduleapi.MyZFill(str(d),2), moduleapi.MyZFill(str(m),2), str(y))
    if  resSQL.mutasi_total < 0.0 or resSQL.kode_jenis_transaksi in ['J','V','W']:
      # debet untuk mutasi negatif atau penarikan dana dan pengambilan manfaat
      mutasi = 'D'
    else:
      mutasi = 'C'

    if resSQL.kode_jenis_transaksi != 'M':
      # bukan transaksi manual
      transaksi = '(%s) <font size="2">%s</font>' % (resSQL.kode_jenis_transaksi, dictJenisTransaksiDPLK[resSQL.kode_jenis_transaksi])
    else:
      # transaksi manual, disesuaikan dengan kode_transaksi_manual
      transaksi = '(%s) <font size="2">%s</font>' % (resSQL.kode_transaksi_manual, dictJenisTransaksiDPLK[resSQL.kode_transaksi_manual])
    #keterangan = '<font size="2">%s</font>' % (resSQL.keterangan or '&nbsp;')

#    transaksi = '(%s) <font size="2">%s</font>' % (resSQL.kode_jenis_transaksi, '&nbsp;')
#    keterangan = '<font size="2">%s</font>' % (dictJenisTransaksiDPLK[resSQL.kode_jenis_transaksi] or '&nbsp;')

    saldo_curr += resSQL.mutasi_total or 0.0

    oFile.write('	<tr>\n')
    oFile.write('		<td width="15%" align="center" style="border-style: solid; border-width: 1px">'+ tanggal +'</td>\n')
    oFile.write('		<td width="15%" align="center" style="border-style: solid; border-width: 1px">'+ mutasi +'</td>\n')
    oFile.write('		<td width="30%" align="center" style="border-style: solid; border-width: 1px">'+ transaksi +'</td>\n')
#    oFile.write('		<td width="40%" align="left" style="border-style: solid; border-width: 1px">'+ keterangan +'</td>\n')
    oFile.write('		<td width="20%" align="right" style="border-style: solid; border-width: 1px">'+ moduleapi.FormatFloatStd(config, abs(resSQL.mutasi_total or 0.0)) +'</td>\n')
    oFile.write('		<td width="20%" align="right" style="border-style: solid; border-width: 1px">'+ moduleapi.FormatFloatStd(config, saldo_curr) +'</td>\n')
    oFile.write('	</tr>\n')

    resSQL.Next()

  return saldo_curr

def ConstructReportTrailer(config, saldo_akhir, oFile):
  oFile.write('	<tr>\n')
#  oFile.write('		<td width="90%" style="border-style: solid; border-width: 1px" colspan="5" align="right"><b>SALDO AKHIR</b></td>\n')
#  oFile.write('		<td width="10%" style="border-style: solid; border-width: 1px">\n')
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

  saldo_awal = moduleapi.GetSaldoAwal(config, no_peserta, str_dari_tanggal)

  ConstructReportHeader(config, no_peserta, dari_tanggal, hingga_tanggal, \
    saldo_awal, oFile)
  ContructSumValues(config, no_peserta, str_dari_tanggal, str_hingga_tanggal_plus, \
    saldo_awal, oFile, dari_tanggal, hingga_tanggal)
  saldo_akhir = ConstructReportValues(config, no_peserta, str_dari_tanggal, \
    str_hingga_tanggal_plus, saldo_awal, oFile)
  ConstructReportTrailer(config, saldo_akhir, oFile)

def CreateReport(config, parameter, returnpacket):
  sBaseFileName = 'statemen_individual.htm'
  sFileName = config.UserHomeDirectory + sBaseFileName

  oFile = open(sFileName, 'w')
  WriteToFile(config, parameter, oFile)
  oFile.close()

  # pack as stream
  sw = returnpacket.AddStreamWrapper()
  sw.LoadFromFile(sFileName)
  sw.MIMEType = config.AppObject.GetMIMETypeFromExtension(sFileName)
