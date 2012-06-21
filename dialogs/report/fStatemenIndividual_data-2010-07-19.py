import sys, string, re
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

  #alamat = '%s %s RTRW: %s %s ' % (oNasabahDPLK.alamat_surat_jalan, oNasabahDPLK.alamat_jalan2,\
  #  oNasabahDPLK.alamat_rtrw, oNasabahDPLK.alamat_surat_kelurahan, )
  alamat = '%s' % (oNasabahDPLK.alamat_surat_jalan)
  alamat1 = '%s' % (oNasabahDPLK.alamat_surat_jalan2)
  alamat2 = 'RT/RW: %s %s ' % (oNasabahDPLK.alamat_surat_rtrw, oNasabahDPLK.alamat_surat_kelurahan)
  kota_kodepos = '%s %s %s' % (oNasabahDPLK.alamat_surat_kecamatan, oNasabahDPLK.alamat_surat_kota,\
    oNasabahDPLK.alamat_surat_kode_pos)
  paket_investasi = '%s' % (oNasabahDPLK.LRekeningDPLK.LPaketInvestasi.kode_paket_investasi)

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
  oFile.write('		STATEMEN INDIVIDUAL</td>\n')
  oFile.write('	</tr>&nbsp;\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="15%" style="border-style: none; border-width: medium"><font size="2"><b>No. \n')
  oFile.write('		Peserta</b></td>\n')
  oFile.write('		<td width="2%" style="border-style: none; border-width: medium"><font size="2"><font size="2">:</font></td>\n')
  oFile.write('		<td width="46%" style="border-style: none; border-width: medium"><font size="2">'+ no_peserta +'</font></td>\n')
  oFile.write('		<td width="15%" style="border-style: none; border-width: medium"><font size="2"><b>Usia Pensiun</b></font></td>\n')
  oFile.write('		<td width="2%" style="border-style: none; border-width: medium"><font size="2">:</font></td>\n')
  oFile.write('		<td width="20%" style="border-style: none; border-width: medium"><font size="2">'+ pensiun +'</font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="15%" style="border-style: none; border-width: medium"><font size="2"><b>Nama</b></font></td>\n')
  oFile.write('		<td width="2%" style="border-style: none; border-width: medium"><font size="2">:</font></font></td>\n')
  oFile.write('		<td width="46%" style="border-style: none; border-width: medium"><font size="2">'+ oNasabahDPLK.nama_lengkap +'</font></td>\n')
  oFile.write('		<td width="15%" style="border-style: none; border-width: medium"><font size="2"><b>Paket \n')
  oFile.write('		Investasi</b></td>\n')
  oFile.write('		<td width="2%" style="border-style: none; border-width: medium"><font size="2">:</font></td>\n')
  oFile.write('		<td width="20%" style="border-style: none; border-width: medium"><font size="2">'+ paket_investasi +'</font></td>\n')
  oFile.write('	</tr>\n')
  #Alamat
  oFile.write('	<tr>\n')
  oFile.write('		<td width="15%" valign="center" style="border-style: none; border-width: medium"><font size="2"><b>Alamat</b></font></td>\n')
  oFile.write('		<td width="2%" valign="center" style="border-style: none; border-width: medium"><font size="2">:</font></font></td>\n')
  oFile.write('		<td width="46%" valign="center" style="border-style: none; border-width: medium"><font size="2">'+ alamat +'</font></td>\n')
  oFile.write('		<td width="15%" valign="center" style="border-style: none; border-width: medium"><font size="2"></td>\n')
  oFile.write('		<td width="2%" valign="center" style="border-style: none; border-width: medium"><font size="2"></td>\n')
  oFile.write('		<td width="20%" valign="center" style="border-style: none; border-width: medium"><font size="2"></td>\n')
  oFile.write('	</tr>\n')

  if len(alamat1) > 4:
  #alamat1
     oFile.write('	<tr>\n')
     oFile.write('		<td width="15%" valign="center" style="border-style: none; border-width: medium"><font size="2"></font></td>\n')
     oFile.write('		<td width="2%" valign="center" style="border-style: none; border-width: medium"><font size="2"></td>\n')
     oFile.write('		<td width="46%" valign="center" style="border-style: none; border-width: medium"><font size="2">'+ alamat1 +'</font></td>\n')
     oFile.write('		<td width="15%" valign="center" style="border-style: none; border-width: medium"><font size="2"></td>\n')
     oFile.write('		<td width="2%" valign="center" style="border-style: none; border-width: medium"><font size="2"></td>\n')
     oFile.write('		<td width="20%" valign="center" style="border-style: none; border-width: medium"><font size="2"></td>\n')
     oFile.write('	</tr>\n')

  #alamat2
  oFile.write('	<tr>\n')
  oFile.write('		<td width="15%" valign="center" style="border-style: none; border-width: medium"><font size="2"></font></td>\n')
  oFile.write('		<td width="2%" valign="center" style="border-style: none; border-width: medium"><font size="2"></td>\n')
  oFile.write('		<td width="46%" valign="center" style="border-style: none; border-width: medium"><font size="2">'+ alamat2 +'</font></td>\n')
  oFile.write('		<td width="15%" valign="center" style="border-style: none; border-width: medium"><font size="2"></td>\n')
  oFile.write('		<td width="2%" valign="center" style="border-style: none; border-width: medium"><font size="2"></td>\n')
  oFile.write('		<td width="20%" valign="center" style="border-style: none; border-width: medium"><font size="2"></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="15%" style="border-style: none; border-width: medium">&nbsp;</td>\n')
  oFile.write('		<td width="2%" style="border-style: none; border-width: medium">&nbsp;</td>\n')
  oFile.write('		<td width="46%" style="border-style: none; border-width: medium"><font size="2">'+ kota_kodepos +'</font></td>\n')
  oFile.write('		<td width="15%" style="border-style: none; border-width: medium"></td>\n')
  oFile.write('		<td width="2%" style="border-style: none; border-width: medium"></td>\n')
  oFile.write('		<td width="20%" style="border-style: none; border-width: medium"></td>\n')
  oFile.write('	</tr>\n')

  oFile.write('	<tr>\n')
  oFile.write('		<td width="15%" style="border-style: none; border-width: medium">&nbsp;</td>\n')
  oFile.write('		<td width="2%" style="border-style: none; border-width: medium">&nbsp;</td>\n')
  oFile.write('		<td width="46%" style="border-style: none; border-width: medium">&nbsp;</td>\n')
  oFile.write('		<td width="15%" style="border-style: none; border-width: medium">&nbsp;</td>\n')
  oFile.write('		<td width="2%" style="border-style: none; border-width: medium">&nbsp;</td>\n')
  oFile.write('		<td width="20%" style="border-style: none; border-width: medium">&nbsp;</td>\n')
  oFile.write('	</tr>\n')

  oFile.write('	<tr>\n')
  oFile.write('		<td width="15%" style="border-style: none; border-width: medium"><font size="2"><b>Periode</b></font></td>\n')
  oFile.write('		<td width="2%" style="border-style: none; border-width: medium"><font size="2">:</td>\n')
  oFile.write('		<td width="46%" style="border-style: none; border-width: medium"><font size="2">'+ periode +'</font></td>\n')
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
  sumIuranPst = 0.0
  sumIuranPK = 0.0
  rSQL.First()
  while not rSQL.Eof:
    sumDana = (rSQL.sumIuranPK or 0.0) + (rSQL.sumIuranPeserta or 0.0) + (rSQL.sumPengembangan or 0.0) + \
      (rSQL.sumPeralihan or 0.0)
      
    if rSQL.KODE_JENIS_TRANSAKSI in ['K']:
       sumIuranPst += rSQL.sumIuranPeserta or 0.0
       sumIuranPK  += rSQL.sumIuranPK or 0.0
    
    if rSQL.KODE_JENIS_TRANSAKSI != 'M':
      # bukan transaksi manual
      dictJenisTransaksi[rSQL.KODE_JENIS_TRANSAKSI] += sumDana
    else:
      # transaksi manual, disesuaikan dengan kode_transaksi_manual
      dictJenisTransaksi[rSQL.kode_transaksi_manual] += sumDana
    sumDanaTotal += sumDana
    rSQL.Next()

  #write to file
  oFile.write('<table border="2" width="95%" id="table2" style="border-width: 0px">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="20%" align="left"   style="border-style: none; border-width: medium"></td>\n')
  oFile.write('		<td width="35%" align="left"   style="border-style: none; border-width: medium"><font size="2">Saldo Akhir per '+ config.FormatDateTime('d mmmm yyyy',dari_tanggal-1) +'</font></td>\n')
  oFile.write('		<td width="2%"  align="center" style="border-style: none; border-width: medium"><font size="2">:</font></td>\n')
  oFile.write('		<td width="15%" align="right"  style="border-style: none; border-width: medium"><font size="2">'+ moduleapi.FormatFloatStd(config, saldo_awal) +'</font></td>\n')
  oFile.write('		<td width="28%" align="left"  style="border-style: none; border-width: medium"><font size="2"></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="20%" align="left"   style="border-style: none; border-width: medium"></td>\n')
  oFile.write('		<td width="35%" align="left"   style="border-style: none; border-width: medium"><font size="2">Akumulasi Iuran Peserta</font></td>\n')
  oFile.write('		<td width="2%"  align="center" style="border-style: none; border-width: medium"><font size="2">:</font></td>\n')
  oFile.write('		<td width="15%" align="right"  style="border-style: none; border-width: medium"><font size="2">'+ moduleapi.FormatFloatStd(config, sumIuranPst) +'</font></td>\n')
  oFile.write('		<td width="28%" align="left"  style="border-style: none; border-width: medium"><font size="2"></font></td>\n')
  oFile.write('	</tr>\n')
  
  oFile.write('	<tr>\n')
  oFile.write('		<td width="20%" align="left"   style="border-style: none; border-width: medium"></td>\n')
  oFile.write('		<td width="35%" align="left"   style="border-style: none; border-width: medium"><font size="2">Akumulasi Iuran Pemberi Kerja</font></td>\n')
  oFile.write('		<td width="2%"  align="center" style="border-style: none; border-width: medium"><font size="2">:</font></td>\n')
  oFile.write('		<td width="15%" align="right"  style="border-style: none; border-width: medium"><font size="2">'+ moduleapi.FormatFloatStd(config, sumIuranPK) +'</font></td>\n')
  oFile.write('		<td width="28%" align="left"  style="border-style: none; border-width: medium"><font size="2"></font></td>\n')
  oFile.write('	</tr>\n')

  akumPenarikanTotal = abs((dictJenisTransaksi['V'] or 0.0) + (dictJenisTransaksi['W'] or 0.0) + (dictJenisTransaksi['E'] or 0.0))
  oFile.write('	<tr>\n')
  oFile.write('		<td width="20%" align="left"   style="border-style: none; border-width: medium"></td>\n')
  oFile.write('		<td width="35%" align="left"   style="border-style: none; border-width: medium"><font size="2">Akumulasi Penarikan</font></td>\n')
  oFile.write('		<td width="2%"  align="center" style="border-style: none; border-width: medium"><font size="2">:</font></td>\n')
  oFile.write('		<td width="15%" align="right"  style="border-style: none; border-width: medium"><font size="2">'+ moduleapi.FormatFloatStd(config, akumPenarikanTotal) +'</font></td>\n')
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
  oFile.write('		<td width="35%" align="left"   style="border-style: none; border-width: medium"><font size="2">Hasil Investasi</font></td>\n')
  oFile.write('		<td width="2%"  align="center" style="border-style: none; border-width: medium"><font size="2">:</font></td>\n')
  oFile.write('		<td width="15%" align="right"  style="border-style: none; border-width: medium"><font size="2">'+ moduleapi.FormatFloatStd(config, dictJenisTransaksi['G']) +'</font></td>\n')
  oFile.write('		<td width="28%" align="left"  style="border-style: none; border-width: medium"><font size="2"></font></td>\n')
  oFile.write('	</tr>\n')
  akumBiayaTotal = abs((dictJenisTransaksi['D'] or 0.0) + (dictJenisTransaksi['C'] or 0.0)+ (dictJenisTransaksi['X'] or 0.0))
  oFile.write('	<tr>\n')
  oFile.write('		<td width="20%" align="left"   style="border-style: none; border-width: medium"></td>\n')
  oFile.write('		<td width="35%" align="left"   style="border-style: none; border-width: medium"><font size="2">Biaya Adm. dan Pengelolaan Dana</font></td>\n')
  oFile.write('		<td width="2%"  align="center" style="border-style: none; border-width: medium"><font size="2">:</font></td>\n')
  oFile.write('		<td width="15%" align="right"  style="border-style: none; border-width: medium"><font size="2">'+ moduleapi.FormatFloatStd(config, akumBiayaTotal) +'</font></td>\n')
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
  oFile.write('		<td width="35%" align="left"   style="border-style: none; border-width: medium"><font size="2">Pengalihan Dari Dana Pensiun Lain</font></td>\n')
  oFile.write('		<td width="2%"  align="center" style="border-style: none; border-width: medium"><font size="2">:</font></td>\n')
  oFile.write('		<td width="15%" align="right"  style="border-style: none; border-width: medium"><font size="2">'+ moduleapi.FormatFloatStd(config, akumPengalihanTotal) +'</font></td>\n')
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
  oFile.write('</table>\n')
  oFile.write('<table border="2"  width="95%" id="table4" style="border-width: 0px; border-collapse:collapse" bordercolorlight="#000000" bordercolordark="#000000">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="20%" align="center"   style="border-style: none; border-width: medium"></td>\n')
  oFile.write('		<td width="52%" <td align="left" style="border-left-style: none; border-left-width: medium; border-right-style: none; border-right-width: medium; border-top-style: none; border-top-width: medium; border-bottom-style: solid; border-bottom-width: 1px">\n </td>\n')
  oFile.write('		<td width="28%" align="left"  style="border-style: none; border-width: medium"><font size="2"></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('</table>\n')
  oFile.write('<table border="2" width="95%" id="table2" style="border-width: 0px">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="20%" align="left"   style="border-style: none; border-width: medium"></td>\n')
  oFile.write('		<td width="35%" align="left"   style="border-style: none; border-width: medium"><font size="2">Total Dana per '+ config.FormatDateTime('d mmmm yyyy',hingga_tanggal) +'</font></td>\n')
  oFile.write('		<td width="2%"  align="center" style="border-style: none; border-width: medium"><font size="2">:</font></td>\n')
  oFile.write('		<td width="15%" align="right"  style="border-style: none; border-width: medium"><font size="2">'+ moduleapi.FormatFloatStd(config, sumDanaTotal+saldo_awal) +'</font></td>\n')
  oFile.write('		<td width="28%" align="left"  style="border-style: none; border-width: medium"><font size="2"></font></td>\n')
  oFile.write('	</tr>\n')
  oFile.write('</table>&nbsp;\n')

def resSQLCatMutasiIndv(config, no_peserta, str_dari_tanggal, str_hingga_tanggal_plus):
  strSQL = '\
    select tgl_transaksi \
      , kode_jenis_transaksi \
      , isnull(kode_transaksi_manual,\'M\') as kode_transaksi_manual \
      , isnull(mutasi_peralihan,0.0) + isnull(mutasi_pengembangan,0.0) + isnull(mutasi_iuran_pst,0.0) + isnull(mutasi_iuran_pk,0.0) as mutasi_total \
      , substring(keterangan,21,10) as keterangan \
      , substring(keterangan,1,26) as keteranganM \
      , ispindahpaket \
    from TransaksiDPLK \
    where tgl_transaksi >= \'%s\' \
      and tgl_transaksi < \'%s\' \
      and no_peserta = \'%s\' \
      and kode_jenis_transaksi not in (\'A\',\'B\') \
      and isCommitted = \'T\' \
    order by  tgl_transaksi, id_transaksi ' \
    % (str_dari_tanggal, str_hingga_tanggal_plus, no_peserta)
  config.SendDebugMsg(strSQL)
  return config.CreateSQL(strSQL).RawResult

def ConstructReportValues(config, no_peserta, str_dari_tanggal, str_hingga_tanggal_plus, saldo_awal, oFile):
  #inisiasi tabel report values, write to file
  oFile.write('<table border="2" width="100%" id="table3" bordercolorlight="#000000" bordercolordark="#000000" style="border-collapse: collapse" bordercolor="#000000" cellpadding="2">\n')
  oFile.write('	<tr>\n')
  oFile.write('		<td width="15%" align="center" style="border-style: solid; border-width: 1px"><font size="2"><b>TANGGAL<br>\n')
  oFile.write('		(dd/mm/yyyy)</b></font></td>\n')
  oFile.write('		<td width="25%" align="center" style="border-style: solid; border-width: 1px"><font size="2"><b>TRANSAKSI</b></font></td>\n')
  oFile.write('		<td width="20%" align="center" style="border-style: solid; border-width: 1px"><font size="2"><b>DEBET</b></font></td>\n')
#  oFile.write('		<td width="40%" align="center" style="border-style: solid; border-width: 1px"><b>KETERANGAN</b></td>\n')
  oFile.write('		<td width="20%" align="center" style="border-style: solid; border-width: 1px"><font size="2"><b>KREDIT</b></font></td>\n')
  oFile.write('		<td width="20%" align="center" style="border-style: solid; border-width: 1px"><font size="2"><b>SALDO</b></font></td>\n')
  oFile.write('	</tr>\n')

  resSQL = resSQLCatMutasiIndv(config, no_peserta, str_dari_tanggal, str_hingga_tanggal_plus)

  dictJenisTransaksiDPLK = {'A':'Pendaftaran','B':'Pembayaran Premi',\
    'C':'Biaya Pengelolaan','D':'Biaya Administrasi',\
    'F':'Pengubahan Jenis Investasi','G':'Hasil Investasi','H':'Pengalihan ke DPLK Lain',\
    'I':'Pengalihan dari DPLK Lain','J':'Pengambilan Manfaat','K':'Iuran',\
    'M':'Transaksi DPLK Manual','O':'Pengalihan dari DPPK Lain',\
    'P':'Pengalihan dari DPK Lain','V':'Penarikan Dana Iuran 30%',\
    'W':'Penarikan Dana PHK','X':'Biaya Penarikan',\
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


# Ditutup By Ade Herman 2010-03-24

#    if resSQL.kode_jenis_transaksi != 'M':
      # bukan transaksi manual
#      transaksi = '(%s) <font size="2">%s</font>' % (resSQL.kode_jenis_transaksi, dictJenisTransaksiDPLK[resSQL.kode_jenis_transaksi])
#    else:
      # transaksi manual, disesuaikan dengan kode_transaksi_manual
#      transaksi = '(%s) <font size="2">%s</font>' % (resSQL.kode_transaksi_manual, dictJenisTransaksiDPLK[resSQL.kode_transaksi_manual])
    #keterangan = '<font size="2">%s</font>' % (resSQL.keterangan or '&nbsp;')

#    transaksi = '(%s) <font size="2">%s</font>' % (resSQL.kode_jenis_transaksi, '&nbsp;')
#    keterangan = '<font size="2">%s</font>' % (dictJenisTransaksiDPLK[resSQL.kode_jenis_transaksi] or '&nbsp;')

## end By Ade Herman 2010-03-24

    #ketTrans = resSQL.keterangan
    #ketTrans = ketTrans.replace(' ','.')
    

    if re.search('[a-z,A-Z,.]+', resSQL.keterangan):
       r = re.search('[a-z,A-Z,.]+', resSQL.keterangan)		
       keterangan = r.group()
    else:
       keterangan = ''


    if resSQL.kode_jenis_transaksi not in ['M','X']:
      # bukan transaksi manual
      if resSQL.mutasi_total < 0.0 and resSQL.kode_jenis_transaksi == 'K':
         transaksi = '<font size="2">Koreksi %s</font>' % (dictJenisTransaksiDPLK[resSQL.kode_jenis_transaksi])
      else:
         if resSQL.kode_jenis_transaksi == 'G':
            transaksi = '<font size="2">%s %s</font>' % (dictJenisTransaksiDPLK[resSQL.kode_jenis_transaksi], keterangan)
         else:
            transaksi = '<font size="2">%s</font>' % (dictJenisTransaksiDPLK[resSQL.kode_jenis_transaksi])
    else:
      # transaksi manual, disesuaikan dengan kode_transaksi_manual
      #transaksi = '(%s) <font size="2">%s</font>' % (resSQL.kode_transaksi_manual, dictJenisTransaksiDPLK[resSQL.kode_transaksi_manual])
      #transaksi = '(%s) <font size="2">%s </font>' % (resSQL.kode_jenis_transaksi, resSQL.keteranganM)

      if resSQL.ispindahpaket == 'T':
         transaksi = '<font size="2">Biaya Pindah Paket Investasi</font>'
      else:
         transaksi = '<font size="2">%s </font>' % string.capwords((resSQL.keteranganM))


    #transaksi = string.capwords(string.upper(transaksi))
    saldo_curr += resSQL.mutasi_total or 0.0

    oFile.write('	<tr>\n')
    oFile.write('		<td width="10%" align="center" style="border-style: solid; border-width: 1px"><font size="2">'+ tanggal +'</font></td>\n')
    oFile.write('		<td width="30%" align="left" style="border-style: solid; border-width: 1px"><font size="2">'+transaksi+'</font></td>\n')
    
    ## Transaksi Debet
    
    if mutasi in ['D']:
      oFile.write('		<td width="20%" align="right" style="border-style: solid; border-width: 1px"><font size="2">'+ moduleapi.FormatFloatStd(config, abs(resSQL.mutasi_total or 0.0)) +'</font></td>\n')
      oFile.write('		<td width="20%" align="right" style="border-style: solid; border-width: 1px"><font size="2"></font></td>\n')
    else:
      # oFile.write('		<td width="40%" align="left" style="border-style: solid; border-width: 1px">'+ keterangan +'</td>\n')
      ## Transaksi Kredit
      oFile.write('		<td width="20%" align="right" style="border-style: solid; border-width: 1px"><font size="2"></font></td>\n')
      oFile.write('		<td width="20%" align="right" style="border-style: solid; border-width: 1px"><font size="2">'+ moduleapi.FormatFloatStd(config, abs(resSQL.mutasi_total or 0.0)) +'</font></td>\n')


    oFile.write('		<td width="20%" align="right" style="border-style: solid; border-width: 1px"><font size="2">'+ moduleapi.FormatFloatStd(config, saldo_curr) +'</font></td>\n')
    oFile.write('	</tr>\n')

    resSQL.Next()

  return saldo_curr

def ConstructReportTrailer(config, saldo_akhir, oFile):
  oFile.write('	<tr>\n')
#  oFile.write('		<td width="90%" style="border-style: solid; border-width: 1px" colspan="5" align="right"><b>SALDO AKHIR</b></td>\n')
#  oFile.write('		<td width="10%" style="border-style: solid; border-width: 1px">\n')
  oFile.write('		<td width="80%" style="border-style: solid; border-width: 1px" colspan="4" align="left"><font size="2"><b>SALDO AKHIR</b></font></td>\n')
  oFile.write('		<td width="20%" style="border-style: solid; border-width: 1px">\n')
  oFile.write('		<p align="right"><font size="2"><b>'+ moduleapi.FormatFloatStd(config, saldo_akhir) +'</b></font></td>\n')
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
