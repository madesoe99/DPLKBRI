#import sys, string, re
#sys.path.append('c:/dafapp/dplk07/script_modules')
#import moduleapi

import sys, string, time
import com.ihsan.util.modman as modman
import com.ihsan.foundation.appserver as appserver

moduleapi = modman.getModule(appserver.ActiveConfig, 'moduleapi')

def FormSetDataEx(buffers, params):
  if params.DatasetCount == 0:
    return

  config = buffers.config
  no_rekening = params.FirstRecord.no_rekening
  oRekInv = config.CreatePObjImplProxy("RekInvDPLK")
  oRekInv.Key = no_rekening
  
  ds = buffers.uipNoData.Dataset
  rec = ds.AddRecord()
  rec.SetFieldByName("LNasabahDPLK.no_peserta", oRekInv.no_peserta)
  rec.SetFieldByName("LNasabahDPLK.nama_lengkap", oRekInv.LNasabahDPLK.nama_lengkap)
  rec.SetFieldByName("no_rekening", no_rekening)
  
def ConstructReportHeader(config, no_rekening, dari_tanggal, hingga_tanggal, saldo_awal, oFile):
  oRekInv = config.CreatePObjImplProxy('RekInvDPLK')
  oRekInv.Key = no_rekening
  
  oNasabahDPLK = oRekInv.LNasabahDPLK

  #alamat = '%s %s RTRW: %s %s ' % (oNasabahDPLK.alamat_surat_jalan, oNasabahDPLK.alamat_jalan2,\
  #  oNasabahDPLK.alamat_rtrw, oNasabahDPLK.alamat_surat_kelurahan, )
  no_peserta = '%s' % (oNasabahDPLK.no_peserta)
  alamat = '%s' % (oNasabahDPLK.alamat_surat_jalan)
  alamat1 = '%s' % (oNasabahDPLK.alamat_surat_jalan2)
  alamat2 = 'RT/RW: %s %s ' % (oNasabahDPLK.alamat_surat_rtrw, oNasabahDPLK.alamat_surat_kelurahan)
  kota_kodepos = '%s %s %s' % (oNasabahDPLK.alamat_surat_kecamatan, oNasabahDPLK.alamat_surat_kota,\
    oNasabahDPLK.alamat_surat_kode_pos)
  #paket_investasi = '%s' % (oNasabahDPLK.LRekeningDPLK.LPaketInvestasi.kode_paket_investasi)
  paket_investasi = ''

  y,m,d = oRekInv.tgl_pensiun[:3]
  tglPensiun = config.FormatDateTime('d mmmm yyyy',\
    config.ModLibUtils.EncodeDate(y,m,d))

  pensiun = '%d [%s]' % (oRekInv.usia_pensiun, tglPensiun)
  periode = '%s - %s' % (config.FormatDateTime('d mmmm yyyy',dari_tanggal), config.FormatDateTime('d mmmm yyyy',hingga_tanggal))

  oFile.write('<html>')
  oFile.write('<head>')
  oFile.write('<title>Statemen Individual</title>')
  oFile.write('</head>')
  oFile.write('<style type="text/css">')
  oFile.write('td.general {border-style:none; border-width:medium; font-size:12px;}')
  oFile.write('</style>')
  oFile.write('<b>DANA PENSIUN LEMBAGA KEUANGAN</b><br />')
  oFile.write('<b>PT. Bank Rakyat Indonesia, Tbk.</b>')
  oFile.write('<table border="2" width="100%" id="table1" style="border-width: 0px">')
  oFile.write('	<tr>')
  oFile.write('		<td colspan="6" align="center" class="general">STATEMEN INDIVIDUAL</td>')
  oFile.write('	</tr>')
  oFile.write('	<tr>')
  oFile.write('		<td width="100px" class="general"><b>No. Peserta</b></td>')
  oFile.write('		<td width="10px" class="general">:</td>')
  oFile.write('		<td class="general">'+ no_peserta +'</td>')
  oFile.write('		<td width="100px" class="general"><b>No. Rekening</b></td>')
  oFile.write('		<td width="10px" class="general">:</td>')
  oFile.write('		<td width="20%" class="general">'+ no_rekening +'</td>')
  oFile.write('	</tr>')
  oFile.write('	<tr>')
  oFile.write('		<td class="general"><b>Nama</b></td>')
  oFile.write('		<td class="general">:</td>')
  oFile.write('		<td class="general">'+ oNasabahDPLK.nama_lengkap +'</td>')
  oFile.write('		<td class="general"><b>Usia Pensiun</b></td>')
  oFile.write('		<td class="general">:</td>')
  oFile.write('		<td class="general">'+ pensiun +'</td>')
  oFile.write('	</tr>')
  #Alamat
  oFile.write('	<tr>')
  oFile.write('		<td valign="center" class="general"><b>Alamat</b></td>')
  oFile.write('		<td valign="center" class="general">:</td>')
  oFile.write('		<td valign="center" class="general">'+ alamat +'</td>')
  oFile.write('		<td valign="center" class="general"><b>Paket Investasi</b></td>')
  oFile.write('		<td valign="center" class="general">:</td>')
  oFile.write('		<td valign="center" class="general">'+ paket_investasi +'</td>')
  oFile.write('	</tr>')

  if len(alamat1) > 4:
  #alamat1
     oFile.write('	<tr>')
     oFile.write('		<td valign="center" class="general"></td>')
     oFile.write('		<td valign="center" class="general"></td>')
     oFile.write('		<td valign="center" class="general">'+ alamat1 +'</td>')
     oFile.write('		<td valign="center" class="general"></td>')
     oFile.write('		<td valign="center" class="general"></td>')
     oFile.write('		<td valign="center" class="general"></td>')
     oFile.write('	</tr>')

  #alamat2
  oFile.write('	<tr>')
  oFile.write('		<td valign="center" class="general"></td>')
  oFile.write('		<td valign="center" class="general"></td>')
  oFile.write('		<td valign="center" class="general">'+ alamat2 +'</td>')
  oFile.write('		<td valign="center" class="general"></td>')
  oFile.write('		<td valign="center" class="general"></td>')
  oFile.write('		<td valign="center" class="general"></td>')
  oFile.write('	</tr>')
  oFile.write('	<tr>')
  oFile.write('		<td class="general">&nbsp;</td>')
  oFile.write('		<td class="general">&nbsp;</td>')
  oFile.write('		<td class="general">'+ kota_kodepos +'</td>')
  oFile.write('		<td class="general"></td>')
  oFile.write('		<td class="general"></td>')
  oFile.write('		<td class="general"></td>')
  oFile.write('	</tr>')

  oFile.write('	<tr>')
  oFile.write('		<td class="general">&nbsp;</td>')
  oFile.write('		<td class="general">&nbsp;</td>')
  oFile.write('		<td class="general">&nbsp;</td>')
  oFile.write('		<td class="general">&nbsp;</td>')
  oFile.write('		<td class="general">&nbsp;</td>')
  oFile.write('		<td class="general">&nbsp;</td>')
  oFile.write('	</tr>')

  oFile.write('	<tr>')
  oFile.write('		<td class="general"><b>Periode</b></td>')
  oFile.write('		<td class="general">:</td>')
  oFile.write('		<td class="general">'+ periode +'</td>')
  oFile.write('		<td class="general"></td>')
  oFile.write('		<td class="general"></td>')
  oFile.write('		<td class="general"></td>')
  oFile.write('	</tr>')
  oFile.write('</table>')

def ContructSumValues(config, no_rekening, str_dari_tanggal, str_hingga_tanggal_plus, \
  saldo_awal, oFile, dari_tanggal, hingga_tanggal):

  sSQL = '''
    SELECT 
      t.KODE_JENIS_TRANSAKSI,
      isnull(t.JENIS_TRANSAKSI,'M') as kode_transaksi_manual,
      isnull(sum(t.MUTASI_IURAN_PK),0.0) as sumIuranPK,
      isnull(sum(t.MUTASI_IURAN_PST),0.0) as sumIuranPeserta,
      (isnull(sum(t. MUTASI_pmb_pk),0.0) + isnull(sum(t.MUTASI_pmb_pst),0.0)) as sumPengembangan,
      isnull(sum(t.MUTASI_psl),0.0) as sumPeralihan
    FROM 
      TRANSAKSIREKINVDPLK t
    WHERE 
      t.TGL_TRANSAKSI >= '%s' 
      AND t.TGL_TRANSAKSI < '%s' 
      AND t.no_rekening = '%s' 
      AND t.KODE_JENIS_TRANSAKSI not in ('A','B') AND
      t.ISCOMMITTED = 'T'
    GROUP BY 
      t.KODE_JENIS_TRANSAKSI, t.JENIS_TRANSAKSI'''\
      % (str_dari_tanggal,str_hingga_tanggal_plus,no_rekening)
  #config.SendDebugMsg(sSQL)
  rSQL = config.CreateSQL(sSQL).RawResult

  #inisialisasi dictionary kode jenis transaksi dan sum dana untuk kode tersebut
  dictJenisTransaksi = {'C':0.0,'D':0.0,'F':0.0,'G':0.0,'H':0.0,'I':0.0,'J':0.0,\
    'K':0.0,'M':0.0,'O':0.0,'P':0.0,'V':0.0,'W':0.0,'X':0.0,'E':0.0}

  #tentukan jenis transaksi
  sumDanaTotal = 0.0
  sumIuranPst = 0.0
  sumIuranPK = 0.0
  sumBagiHasil = 0.0
  rSQL.First()
  while not rSQL.Eof:
    sumDana = (rSQL.sumIuranPK or 0.0) \
      + (rSQL.sumIuranPeserta or 0.0) \
      + (rSQL.sumPengembangan or 0.0) \
      + (rSQL.sumPeralihan or 0.0)
      
    if rSQL.KODE_JENIS_TRANSAKSI in ['K']:
       sumIuranPst += rSQL.sumIuranPeserta or 0.0
       sumIuranPK  += rSQL.sumIuranPK or 0.0
       
    if rSQL.KODE_JENIS_TRANSAKSI in ['G']:
       sumBagiHasil += rSQL.sumPengembangan or 0.0
    
    if rSQL.KODE_JENIS_TRANSAKSI != 'M':
      # bukan transaksi manual
      dictJenisTransaksi[rSQL.KODE_JENIS_TRANSAKSI] += sumDana
    else:
      # transaksi manual, disesuaikan dengan kode_transaksi_manual
      sumIuranPst += rSQL.sumIuranPeserta or 0.0
      sumIuranPK  += rSQL.sumIuranPK or 0.0
      sumBagiHasil += rSQL.sumPengembangan or 0.0

      dictJenisTransaksi[rSQL.kode_transaksi_manual] += sumDana

    sumDanaTotal += sumDana
    rSQL.Next()

  #write to file
  oFile.write('<table border="2" width="95%" id="table2" style="border-width: 0px">')
  oFile.write('	<tr>')
  oFile.write('		<td width="20%" align="left"   class="general"></td>')
  oFile.write('		<td width="35%" align="left"   class="general">Saldo Akhir per '+ config.FormatDateTime('d mmmm yyyy',dari_tanggal-1) +'</td>')
  oFile.write('		<td width="2%"  align="center" class="general">:</td>')
  oFile.write('		<td width="15%" align="right"  class="general">'+ moduleapi.FormatFloatStd(config, saldo_awal) +'</td>')
  oFile.write('		<td width="28%" align="left"  class="general"></td>')
  oFile.write('	</tr>')
  oFile.write('	<tr>')
  oFile.write('		<td width="20%" align="left"   class="general"></td>')
  oFile.write('		<td width="35%" align="left"   class="general">Akumulasi Iuran Peserta</td>')
  oFile.write('		<td width="2%"  align="center" class="general">:</td>')
  oFile.write('		<td width="15%" align="right"  class="general">'+ moduleapi.FormatFloatStd(config, sumIuranPst) +'</td>')
  oFile.write('		<td width="28%" align="left"  class="general"></td>')
  oFile.write('	</tr>')
  
  oFile.write('	<tr>')
  oFile.write('		<td width="20%" align="left"   class="general"></td>')
  oFile.write('		<td width="35%" align="left"   class="general">Akumulasi Iuran Pemberi Kerja</td>')
  oFile.write('		<td width="2%"  align="center" class="general">:</td>')
  oFile.write('		<td width="15%" align="right"  class="general">'+ moduleapi.FormatFloatStd(config, sumIuranPK) +'</td>')
  oFile.write('		<td width="28%" align="left"  class="general"></td>')
  oFile.write('	</tr>')

  akumPenarikanTotal = abs((dictJenisTransaksi['V'] or 0.0) + (dictJenisTransaksi['W'] or 0.0) + (dictJenisTransaksi['E'] or 0.0))
  oFile.write('	<tr>')
  oFile.write('		<td width="20%" align="left"   class="general"></td>')
  oFile.write('		<td width="35%" align="left"   class="general">Akumulasi Penarikan Tahun '+config.FormatDateTime('yyyy',hingga_tanggal)+'</td>')
  oFile.write('		<td width="2%"  align="center" class="general">:</td>')
  oFile.write('		<td width="15%" align="right"  class="general">'+ moduleapi.FormatFloatStd(config, akumPenarikanTotal) +'</td>')
  oFile.write('		<td width="28%" align="left"  class="general"></td>')
  oFile.write('	</tr>')
#   oFile.write('	<tr>')
#   oFile.write('		<td width="20%" align="left"   class="general"></td>')
#   oFile.write('		<td width="30%" align="left"   class="general">Akumulasi Penarikan Sebagian</td>')
#   oFile.write('		<td width="2%"  align="center" class="general">:</td>')
#   oFile.write('		<td width="20%" align="right"  class="general">'+ moduleapi.FormatFloatStd(config, abs(dictJenisTransaksi['V'] or 0.0)) +'</td>')
#   oFile.write('		<td width="28%" align="left"  class="general"></td>')
#   oFile.write('	</tr>')
#   oFile.write('	<tr>')
#   oFile.write('		<td width="20%" align="left"   class="general"></td>')
#   oFile.write('		<td width="30%" align="left"   class="general">Akumulasi Penarikan PHK</td>')
#   oFile.write('		<td width="2%"  align="center" class="general">:</td>')
#   oFile.write('		<td width="20%" align="right"  class="general">'+ moduleapi.FormatFloatStd(config, abs(dictJenisTransaksi['W'] or 0.0)) +'</td>')
#   oFile.write('		<td width="28%" align="left"  class="general"></td>')
#   oFile.write('	</tr>')
#   oFile.write('	<tr>')
#   oFile.write('		<td width="20%" align="left"   class="general"></td>')
#   oFile.write('		<td width="30%" align="left"   class="general">Akumulasi Penarikan Dana</td>')
#   oFile.write('		<td width="2%"  align="center" class="general">:</td>')
#   oFile.write('		<td width="20%" align="right"  class="general">'+ moduleapi.FormatFloatStd(config, abs(dictJenisTransaksi['E'] or 0.0)) +'</td>')
#   oFile.write('		<td width="28%" align="left"  class="general"></td>')
#   oFile.write('	</tr>')
  oFile.write('	<tr>')
  oFile.write('		<td width="20%" align="left"   class="general"></td>')
  oFile.write('		<td width="35%" align="left"   class="general">Total Hasil Investasi</td>')
  oFile.write('		<td width="2%"  align="center" class="general">:</td>')
  #oFile.write('		<td width="15%" align="right"  class="general">'+ moduleapi.FormatFloatStd(config, dictJenisTransaksi['G']) +'</td>')
  oFile.write('		<td width="15%" align="right"  class="general">'+ moduleapi.FormatFloatStd(config, sumBagiHasil) +'</td>')
  oFile.write('		<td width="28%" align="left"  class="general"></td>')
  oFile.write('	</tr>')
  akumBiayaTotal = abs((dictJenisTransaksi['D'] or 0.0) + (dictJenisTransaksi['C'] or 0.0)+ (dictJenisTransaksi['X'] or 0.0))
  oFile.write('	<tr>')
  oFile.write('		<td width="20%" align="left"   class="general"></td>')
  oFile.write('		<td width="35%" align="left"   class="general">Biaya Adm. dan Pengelolaan Dana</td>')
  oFile.write('		<td width="2%"  align="center" class="general">:</td>')
  oFile.write('		<td width="15%" align="right"  class="general">'+ moduleapi.FormatFloatStd(config, akumBiayaTotal) +'</td>')
  oFile.write('		<td width="28%" align="left"  class="general"></td>')
  oFile.write('	</tr>')
#   oFile.write('	<tr>')
#   oFile.write('		<td width="20%" align="left"   class="general"></td>')
#   oFile.write('		<td width="30%" align="left"   class="general">Biaya Administrasi</td>')
#   oFile.write('		<td width="2%"  align="center" class="general">:</td>')
#   oFile.write('		<td width="20%" align="right"  class="general">'+ moduleapi.FormatFloatStd(config, abs(dictJenisTransaksi['D'] or 0.0)) +'</td>')
#   oFile.write('		<td width="28%" align="left"  class="general"></td>')
#   oFile.write('	</tr>')
#   oFile.write('	<tr>')
#   oFile.write('		<td width="20%" align="left"   class="general"></td>')
#   oFile.write('		<td width="30%" align="left"   class="general">Biaya Pengelolaan Dana</td>')
#   oFile.write('		<td width="2%"  align="center" class="general">:</td>')
#   oFile.write('		<td width="20%" align="right"  class="general">'+ moduleapi.FormatFloatStd(config, abs(dictJenisTransaksi['C'] or 0.0)) +'</td>')
#   oFile.write('		<td width="28%" align="left"  class="general"></td>')
#   oFile.write('	</tr>')
  akumPengalihanTotal = abs((dictJenisTransaksi['I'] or 0.0) + (dictJenisTransaksi['O'] or 0.0) + (dictJenisTransaksi['P'] or 0.0))
  oFile.write('	<tr>')
  oFile.write('		<td width="20%" align="left"   class="general"></td>')
  oFile.write('		<td width="35%" align="left"   class="general">Pengalihan Dari Dana Pensiun Lain</td>')
  oFile.write('		<td width="2%"  align="center" class="general">:</td>')
  oFile.write('		<td width="15%" align="right"  class="general">'+ moduleapi.FormatFloatStd(config, akumPengalihanTotal) +'</td>')
  oFile.write('		<td width="28%" align="left"  class="general"></td>')
  oFile.write('	</tr>')
#   oFile.write('	<tr>')
#   oFile.write('		<td width="20%" align="left"   class="general"></td>')
#   oFile.write('		<td width="30%" align="left"   class="general">Pengalihan Dari DPLK Lain</td>')
#   oFile.write('		<td width="2%"  align="center" class="general">:</td>')
#   oFile.write('		<td width="20%" align="right"  class="general">'+ moduleapi.FormatFloatStd(config, abs(dictJenisTransaksi['I'] or 0.0)) +'</td>')
#   oFile.write('		<td width="28%" align="left"  class="general"></td>')
#   oFile.write('	</tr>')
#   oFile.write('	<tr>')
#   oFile.write('		<td width="20%" align="left"   class="general"></td>')
#   oFile.write('		<td width="30%" align="left"   class="general">Pengalihan Dari DPPK Lain</td>')
#   oFile.write('		<td width="2%"  align="center" class="general">:</td>')
#   oFile.write('		<td width="20%" align="right"  class="general">'+ moduleapi.FormatFloatStd(config, abs(dictJenisTransaksi['O'] or 0.0)) +'</td>')
#   oFile.write('		<td width="28%" align="left"  class="general"></td>')
#   oFile.write('	</tr>')
#   oFile.write('	<tr>')
#   oFile.write('		<td width="20%" align="left"   class="general"></td>')
#   oFile.write('		<td width="30%" align="left"   class="general">Pengalihan Dari DPK Lain</td>')
#   oFile.write('		<td width="2%"  align="center" class="general">:</td>')
#   oFile.write('		<td width="20%" align="right"  class="general">'+ moduleapi.FormatFloatStd(config, abs(dictJenisTransaksi['P'] or 0.0)) +'</td>')
#   oFile.write('		<td width="28%" align="left"  class="general"></td>')
#   oFile.write('	</tr>&nbsp;')
  oFile.write('</table>')
  oFile.write('<table border="2"  width="95%" id="table4" style="border-width: 0px; border-collapse:collapse" bordercolorlight="#000000" bordercolordark="#000000">')
  oFile.write('	<tr>')
  oFile.write('		<td width="20%" align="center"   class="general"></td>')
  oFile.write('		<td width="52%" <td align="left" style="border-left-style: none; border-left-width: medium; border-right-style: none; border-right-width: medium; border-top-style: none; border-top-width: medium; border-bottom-style: solid; border-bottom-width: 1px"> </td>')
  oFile.write('		<td width="28%" align="left"  class="general"></td>')
  oFile.write('	</tr>')
  oFile.write('</table>')
  oFile.write('<table border="2" width="95%" id="table2" style="border-width: 0px">')
  oFile.write('	<tr>')
  oFile.write('		<td width="20%" align="left"   class="general"></td>')
  oFile.write('		<td width="35%" align="left"   class="general">Total Dana per '+ config.FormatDateTime('d mmmm yyyy',hingga_tanggal) +'</td>')
  oFile.write('		<td width="2%"  align="center" class="general">:</td>')
  oFile.write('		<td width="15%" align="right"  class="general">'+ moduleapi.FormatFloatStd(config, sumDanaTotal+saldo_awal) +'</td>')
  oFile.write('		<td width="28%" align="left"  class="general"></td>')
  oFile.write('	</tr>')
  oFile.write('</table>&nbsp;')

def resSQLCatMutasiIndv(config, no_rekening, str_dari_tanggal, str_hingga_tanggal_plus):
  strSQL = '''
    SELECT 
      tgl_transaksi, 
      id_transaksi,
      kode_jenis_transaksi,
      isnull(jenis_transaksi,'M') as kode_transaksi_manual,
      isnull(mutasi_psl,0.0) + isnull(mutasi_pmb_pk,0.0) + isnull(mutasi_pmb_pst,0.0) + isnull(mutasi_iuran_pst,0.0) + isnull(mutasi_iuran_pk,0.0) as mutasi_total,
      substring(keterangan,21,10) as keterangan,
      substring(keterangan,1,26) as keteranganM,
      ispindahpaket
    FROM 
      TransaksiRekInvDPLK
    WHERE 
      tgl_transaksi >= \'%s\'
      AND tgl_transaksi < \'%s\'
      AND no_rekening = \'%s\'
      AND kode_jenis_transaksi not in (\'A\',\'B\')
      AND isCommitted = \'T\'
    ORDER BY tgl_transaksi,id_transaksi'''\
    % (str_dari_tanggal, str_hingga_tanggal_plus, no_rekening)
  #config.SendDebugMsg(strSQL)
  return config.CreateSQL(strSQL).RawResult

def ConstructReportValues(config, no_rekening, str_dari_tanggal, str_hingga_tanggal_plus, saldo_awal, oFile):
  #inisiasi tabel report values, write to file
  oFile.write('<table border="2" width="100%" id="table3" bordercolorlight="#000000" bordercolordark="#000000" style="border-collapse: collapse" bordercolor="#000000" cellpadding="2">')
  oFile.write('	<tr>')
  oFile.write('		<td width="10%" align="center" style="border-style: solid; border-width: 1px"><b>TANGGAL<br>')
  oFile.write('		(dd/mm/yyyy)</b></td>')
  oFile.write('		<td width="10%" align="center" style="border-style: solid; border-width: 1px"><b>MUTASI</b></td>')
  oFile.write('		<td width="30%" align="center" style="border-style: solid; border-width: 1px"><b>TRANSAKSI</b></td>')
#  oFile.write('		<td width="40%" align="center" style="border-style: solid; border-width: 1px"><b>KETERANGAN</b></td>')
  oFile.write('		<td width="20%" align="center" style="border-style: solid; border-width: 1px"><b>NOMINAL</b></td>')
  oFile.write('		<td width="20%" align="center" style="border-style: solid; border-width: 1px"><b>SALDO</b></td>')
  oFile.write('	</tr>')

  resSQL = resSQLCatMutasiIndv(config, no_rekening, str_dari_tanggal, str_hingga_tanggal_plus)
  
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
#      transaksi = '(%s) %s' % (resSQL.kode_jenis_transaksi, dictJenisTransaksiDPLK[resSQL.kode_jenis_transaksi])
#    else:
      # transaksi manual, disesuaikan dengan kode_transaksi_manual
#      transaksi = '(%s) %s' % (resSQL.kode_transaksi_manual, dictJenisTransaksiDPLK[resSQL.kode_transaksi_manual])
    #keterangan = '%s' % (resSQL.keterangan or '&nbsp;')

#    transaksi = '(%s) %s' % (resSQL.kode_jenis_transaksi, '&nbsp;')
#    keterangan = '%s' % (dictJenisTransaksiDPLK[resSQL.kode_jenis_transaksi] or '&nbsp;')

## end By Ade Herman 2010-03-24

    #ketTrans = resSQL.keterangan
    #ketTrans = ketTrans.replace(' ','.')
    
    keterangan = ''
    """
    if re.search('[a-z,A-Z,.]+', resSQL.keterangan):
       r = re.search('[a-z,A-Z,.]+', resSQL.keterangan)		
       keterangan = r.group()
    else:
       keterangan = ''
    """
    
    if len(keterangan) == 0:
       keterangan = ''
    else:
       if keterangan[0] not in ['D','S','R']:
          keterangan = ''

    if resSQL.kode_jenis_transaksi not in ['M','X']:
      # bukan transaksi manual
      if resSQL.mutasi_total < 0.0 and resSQL.kode_jenis_transaksi == 'K':
         transaksi = 'Koreksi %s' % (dictJenisTransaksiDPLK[resSQL.kode_jenis_transaksi])
      else:
         if resSQL.kode_jenis_transaksi == 'G':
            transaksi = '%s %s' % (dictJenisTransaksiDPLK[resSQL.kode_jenis_transaksi], keterangan)
         else:
            transaksi = '%s' % (dictJenisTransaksiDPLK[resSQL.kode_jenis_transaksi])
    else:
      # transaksi manual, disesuaikan dengan kode_transaksi_manual
      #transaksi = '(%s) %s' % (resSQL.kode_transaksi_manual, dictJenisTransaksiDPLK[resSQL.kode_transaksi_manual])
      #transaksi = '(%s) %s ' % (resSQL.kode_jenis_transaksi, resSQL.keteranganM)

      if resSQL.ispindahpaket == 'T':
         transaksi = 'Biaya Pindah Paket Investasi'
      else:
         transaksi = '%s ' % string.capwords((resSQL.keteranganM))


    #transaksi = string.capwords(string.upper(transaksi))
    saldo_curr += resSQL.mutasi_total or 0.0

    oFile.write('	<tr>')
    oFile.write('		<td width="10%" align="center" style="border-style: solid; border-width: 1px">'+ tanggal +'</td>')
    oFile.write('		<td width="10%" align="center" style="border-style: solid; border-width: 1px">'+mutasi+'</td>')
    oFile.write('		<td width="30%" align="left" style="border-style: solid; border-width: 1px">'+transaksi+'</td>')
    oFile.write('		<td width="20%" align="right" style="border-style: solid; border-width: 1px">'+ moduleapi.FormatFloatStd(config, abs(resSQL.mutasi_total or 0.0)) +'</td>')
    ## Transaksi Debet
    
    #if mutasi in ['D']:
    #  oFile.write('		<td width="20%" align="right" style="border-style: solid; border-width: 1px">'+ moduleapi.FormatFloatStd(config, abs(resSQL.mutasi_total or 0.0)) +'</td>')
    #  oFile.write('		<td width="20%" align="right" style="border-style: solid; border-width: 1px"></td>')
    #else:
      # oFile.write('		<td width="40%" align="left" style="border-style: solid; border-width: 1px">'+ keterangan +'</td>')
      ## Transaksi Kredit
     # oFile.write('		<td width="20%" align="right" style="border-style: solid; border-width: 1px"></td>')
     # oFile.write('		<td width="20%" align="right" style="border-style: solid; border-width: 1px">'+ moduleapi.FormatFloatStd(config, abs(resSQL.mutasi_total or 0.0)) +'</td>')


    oFile.write('		<td width="20%" align="right" style="border-style: solid; border-width: 1px">'+ moduleapi.FormatFloatStd(config, saldo_curr) +'</td>')
    oFile.write('	</tr>')

    resSQL.Next()

  return saldo_curr

def ConstructReportTrailer(config, saldo_akhir, oFile):
  oFile.write('	<tr>')
  oFile.write('		<td width="80%" style="border-style: solid; border-width: 1px" colspan="4" align="left"><b>SALDO AKHIR</b></td>')
  oFile.write('		<td width="20%" style="border-style: solid; border-width: 1px">')
  oFile.write('		<p align="right"><b>'+ moduleapi.FormatFloatStd(config, saldo_akhir) +'</b></td>')
  oFile.write('	</tr>')
  oFile.write('</table>')
  oFile.write('<p>&nbsp;</p>')
  oFile.write('<table border="2" width="100%" id="table4" style="border-width: 0px; border-collapse:collapse" bordercolorlight="#000000" bordercolordark="#000000">')
  oFile.write('	<tr>')
  oFile.write('		<td align="right" style="border-left-style: none; border-left-width: medium; border-right-style: none; border-right-width: medium; border-top-style: none; border-top-width: medium; border-bottom-style: solid; border-bottom-width: 1px">')
  oFile.write('		Dicetak tanggal '+ config.FormatDateTime('d mmmm yyyy', config.Now()) +'</td>')
  oFile.write('	</tr>')
  oFile.write('	<tr>')
  oFile.write('		<td style="border-left-style: none; border-left-width: medium; border-right-style: none; border-right-width: medium; border-top-style: solid; border-top-width: 1px; border-bottom-style: none; border-bottom-width: medium"></td>')
  oFile.write('	</tr>')
  oFile.write('</table>')
  oFile.write('')
  oFile.write('</body>')
  oFile.write('')
  oFile.write('</html>')

def WriteToFile(config, parameter, oFile):
  no_rekening = parameter.FirstRecord.no_rekening
  dari_tanggal = parameter.FirstRecord.dari_tanggal
  hingga_tanggal = parameter.FirstRecord.hingga_tanggal

  str_dari_tanggal = config.FormatDateTime('yyyy-mm-dd', dari_tanggal)
  str_hingga_tanggal_plus = config.FormatDateTime('yyyy-mm-dd', hingga_tanggal + 1)

  #import rpdb2; rpdb2.start_embedded_debugger('solusi', True, True)
  saldo_awal = moduleapi.GetSaldoAwal(config, no_rekening, str_dari_tanggal)

  ConstructReportHeader(config, no_rekening, dari_tanggal, hingga_tanggal, saldo_awal, oFile)
  ContructSumValues(config, no_rekening, str_dari_tanggal, str_hingga_tanggal_plus, saldo_awal, oFile, dari_tanggal, hingga_tanggal)
  saldo_akhir = ConstructReportValues(config, no_rekening, str_dari_tanggal, str_hingga_tanggal_plus, saldo_awal, oFile)
  ConstructReportTrailer(config, saldo_akhir, oFile)

def CreateReport(config, parameter, returnpacket):
  sBaseFileName = 'statemen_individual.htm'
  sFileName = config.UserHomeDirectory + sBaseFileName

  #branch_code = config.SecurityContext.GetUserInfo()[4]
  userid = config.SecurityContext.userid
  
  oRekInv = config.CreatePObjImplProxy('RekInvDPLK')
  oRekInv.key = parameter.FirstRecord.no_rekening
  
  oFile = open(sFileName, 'w')
  WriteToFile(config, parameter, oFile)
  oFile.close()
  
  # pack as stream
  sw = returnpacket.AddStreamWrapper()
  sw.LoadFromFile(sFileName)
  sw.MIMEType = config.AppObject.GetMIMETypeFromExtension(sFileName)

