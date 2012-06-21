import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi

lineNumber = 1
tepi_atas = None
tepi_bawah = None
baris_per_halaman = None

MAXPST_PERFILE = 25000

def FormSetDataEx(buffers, params):
  ds = buffers.uipNoData.Dataset
  rec = ds.AddRecord()
  rec.tepi_atas = 5
  rec.tepi_bawah = 5
  rec.tepi_kiri = 5
  rec.baris_per_halaman = 66

def CekJumlahBaris(config, tepi_kiri):
  global tepi_atas, tepi_bawah, baris_per_halaman

  if tepi_atas < 0:
    raise 'Kesalahan Tepi Atas', '\nTepi atas tidak boleh kurang dari nol.'

  if tepi_bawah < 0:
    raise 'Kesalahan Tepi Bawah', '\nTepi bawah tidak boleh kurang dari nol.'

  if tepi_kiri < 0:
    raise 'Kesalahan Tepi Kiri', '\nTepi kiri tidak boleh kurang dari nol.'

  if baris_per_halaman < 25 + tepi_atas + tepi_bawah:
    raise 'Kesalahan Jumlah Baris', '\nBaris per halaman tidak boleh kurang dari 25 + tepi atas + tepi bawah.'

def getAwalAkhirTanggal(config, periode, tahun):
  if periode == 13:
    # semester 1 (Januari-Juni)
    periodeAwal = 1
    periodeAkhir = 6
  elif periode == 14:
    # semester 2 (Juli-Desember)
    periodeAwal = 7
    periodeAkhir = 12
  else:
    periodeAwal = periodeAkhir = periode

  tglAkhir = moduleapi.GetLastDayOfMonth(periodeAkhir, tahun)
  dtTglAwal = config.ModLibUtils.EncodeDate(tahun, periodeAwal, 1)
  dtTglAkhir = config.ModLibUtils.EncodeDate(tahun, periodeAkhir, tglAkhir)

  return dtTglAwal, dtTglAkhir

def NextPagePeserta(config, oFile):
  # pindah ke halaman berikutnya untuk peserta berikutnya
  global lineNumber, tepi_atas

  # terus pindah baris hingga ke halaman berikutnya
  stop = tepi_atas + 1
  while lineNumber > stop:
    NextLine(config, oFile)

def NextPage(config, oFile):
  global lineNumber, tepi_bawah

  for i in range(tepi_bawah):
    oFile.write('\n')
  lineNumber = 1
  TepiAtas(config, oFile)

def NextLine(config, oFile):
  global lineNumber, tepi_bawah, baris_per_halaman

  oFile.write('\n')
  lineNumber += 1
  if lineNumber > (baris_per_halaman - tepi_bawah):
    # posisi baris sudah berada di margin bawah, pindah halaman
    NextPage(config, oFile)

def TepiAtas(config, oFile):
  global lineNumber, tepi_atas

  for i in range(tepi_atas):
    oFile.write('\n')
    lineNumber += 1

def ConstructReportHeader(config, no_peserta, dari_tanggal, hingga_tanggal, saldo_awal, strTepiKiri, oFile):
  oNasabahDPLK = config.CreatePObjImplProxy('NasabahDPLK')
  oNasabahDPLK.Key = no_peserta

  #alamat = '%s %s RTRW: %s' % (oNasabahDPLK.alamat_jalan, oNasabahDPLK.alamat_jalan2,\
  #  oNasabahDPLK.alamat_rtrw)
  alamat = '%s ' % (oNasabahDPLK.alamat_jalan)
  alamat1 = '%s RTRW: %s' % (oNasabahDPLK.alamat_jalan2, oNasabahDPLK.alamat_rtrw)

  kota_kodepos = '%s %s' % (oNasabahDPLK.alamat_kota, oNasabahDPLK.alamat_kode_pos)
  paket_investasi = '(%s) %s' % (oNasabahDPLK.LRekeningDPLK.LPaketInvestasi.kode_paket_investasi, oNasabahDPLK.LRekeningDPLK.LPaketInvestasi.nama_paket_investasi)

  y,m,d = oNasabahDPLK.LRekeningDPLK.tgl_pensiun[:3]
  tglPensiun = config.FormatDateTime('d mmmm yyyy',\
    config.ModLibUtils.EncodeDate(y,m,d))

  pensiun = '%d [%s]' % (oNasabahDPLK.LRekeningDPLK.usia_pensiun, tglPensiun)
  periode = '%s - %s' % (config.FormatDateTime('d mmmm yyyy',dari_tanggal), config.FormatDateTime('d mmmm yyyy',hingga_tanggal))

  oFile.write(strTepiKiri +'DANA PENSIUN LEMBAGA KEUANGAN');NextLine(config, oFile)
  oFile.write(strTepiKiri +'PT. Bank Rakyat Indonesia, Tbk.');NextLine(config, oFile)
  NextLine(config, oFile)
  oFile.write(strTepiKiri +'%-11s: %-40s %-15s: %s' % ('No. Peserta', no_peserta, 'Usia Pensiun', pensiun));NextLine(config, oFile)
  oFile.write(strTepiKiri +'%-11s: %-40s %-15s: %s' % ('Nama', oNasabahDPLK.nama_lengkap, 'Paket Investasi', paket_investasi));NextLine(config, oFile)
  oFile.write(strTepiKiri +'%-11s: %s' % ('Alamat', alamat));NextLine(config, oFile)
  oFile.write(strTepiKiri +'%13s%s' % ('', alamat1));NextLine(config, oFile)
  oFile.write(strTepiKiri +'%13s%s' % ('', kota_kodepos));NextLine(config, oFile)
  oFile.write(strTepiKiri +'%-11s: %s' % ('Periode', periode));NextLine(config, oFile)
  NextLine(config, oFile)

def ContructSumValues(config, no_peserta, str_dari_tanggal, str_hingga_tanggal_plus, \
  saldo_awal, oFile, dari_tanggal, hingga_tanggal, strTepiKiri):

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
          group by t.KODE_JENIS_TRANSAKSI, kode_transaksi_manual;'\
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

  akumPenarikanTotal = abs((dictJenisTransaksi['V'] or 0.0) + (dictJenisTransaksi['W'] or 0.0) + (dictJenisTransaksi['E'] or 0.0))
  akumBiayaTotal = abs((dictJenisTransaksi['D'] or 0.0) + (dictJenisTransaksi['C'] or 0.0)+ (dictJenisTransaksi['X'] or 0.0))
  akumPengalihanTotal = abs((dictJenisTransaksi['I'] or 0.0) + (dictJenisTransaksi['O'] or 0.0) + (dictJenisTransaksi['P'] or 0.0))

  #write to file
  oFile.write(strTepiKiri +'%13s%-40s: %18s' % ('', 'Saldo Akhir per '+ config.FormatDateTime('d mmmm yyyy',dari_tanggal-1), moduleapi.FormatFloatStd(config, saldo_awal)));NextLine(config, oFile)
  oFile.write(strTepiKiri +'%13s%-40s: %18s' % ('', 'Akumulasi Iuran', moduleapi.FormatFloatStd(config, dictJenisTransaksi['K'])));NextLine(config, oFile)
  oFile.write(strTepiKiri +'%13s%-40s: %18s' % ('', 'Akumulasi Penarikan', moduleapi.FormatFloatStd(config, akumPenarikanTotal)));NextLine(config, oFile)
  oFile.write(strTepiKiri +'%13s%-40s: %18s' % ('', 'Hasil Pengembangan', moduleapi.FormatFloatStd(config, dictJenisTransaksi['G'])));NextLine(config, oFile)
  oFile.write(strTepiKiri +'%13s%-40s: %18s' % ('', 'Biaya Adm. dan Pengelolaan Dana', moduleapi.FormatFloatStd(config, akumBiayaTotal)));NextLine(config, oFile)
  oFile.write(strTepiKiri +'%13s%-40s: %18s' % ('', 'Pengalihan Dari DPLK/DPPK/DPK Lain', moduleapi.FormatFloatStd(config, akumPengalihanTotal)));NextLine(config, oFile)
  #oFile.write(strTepiKiri +'%13s%-40s: %18s' % ('', 'Pengalihan Dari DPLK/DPPK/DPK Lain', moduleapi.FormatFloatStd(config, sumDanaTotal + akumPengalihanTotal)));NextLine(config, oFile)
  oFile.write(strTepiKiri +'%13s------------------------------------------------------------' % (''));NextLine(config, oFile)
  oFile.write(strTepiKiri +'%13s%-40s: %18s' % ('', 'Total Dana per '+ config.FormatDateTime('d mmmm yyyy',hingga_tanggal), moduleapi.FormatFloatStd(config, sumDanaTotal + saldo_awal)));NextLine(config, oFile)
  NextLine(config, oFile)

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
    order by tgl_transaksi' \
    % (str_dari_tanggal, str_hingga_tanggal_plus, no_peserta)
  config.SendDebugMsg(strSQL)
  return config.CreateSQL(strSQL).RawResult

def ConstructReportValues(config, no_peserta, str_dari_tanggal, str_hingga_tanggal_plus, saldo_awal, strTepiKiri, oFile):
##  tanggal 12
##  mutasi 8
##  transaksi 35
##  nominal 19
##  saldo 19

  capTanggal = '  TANGGAL   '
  capMutasi = ' MUTASI '
  capTransaksi = '             TRANSAKSI             '
  capNominal = '      NOMINAL      '
  capSaldo = '       SALDO       '

  oFile.write(strTepiKiri +'==============================================================================================');NextLine(config, oFile)
  oFile.write(strTepiKiri +'%s%s%s%s%s' % (capTanggal, capMutasi, capTransaksi, capNominal, capSaldo));NextLine(config, oFile)
  oFile.write(strTepiKiri +'----------------------------------------------------------------------------------------------');NextLine(config, oFile)

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
      transaksi = '(%s) %s' % (resSQL.kode_jenis_transaksi, dictJenisTransaksiDPLK[resSQL.kode_jenis_transaksi])
    else:
      # transaksi manual, disesuaikan dengan kode_transaksi_manual
      transaksi = '(%s) %s' % (resSQL.kode_transaksi_manual, dictJenisTransaksiDPLK[resSQL.kode_transaksi_manual])

    saldo_curr += resSQL.mutasi_total or 0.0

    oFile.write(strTepiKiri +' %s     %s    %-34s%19s%19s' %
      (tanggal
       , mutasi
       , transaksi
       , moduleapi.FormatFloatStd(config, abs(resSQL.mutasi_total or 0.0))
       , moduleapi.FormatFloatStd(config, saldo_curr))
      );NextLine(config, oFile)
    resSQL.Next()

  oFile.write(strTepiKiri +'----------------------------------------------------------------------------------------------');NextLine(config, oFile)
  oFile.write(strTepiKiri +'%74s%19s' % ('SALDO AKHIR', moduleapi.FormatFloatStd(config, saldo_curr)));NextLine(config, oFile)
  oFile.write(strTepiKiri +'==============================================================================================');NextLine(config, oFile)
  # terus pindah baris hingga ke halaman berikutnya
  NextPagePeserta(config, oFile)

def resSQLNasabahDPLK(config, kode_nasabah_corporate):
  strSQL = \
    'select n.no_peserta '\
    'from NasabahDPLK n, RekeningDPLK r  '\
    'where kode_nasabah_corporate = \'%s\' '\
    'and n.no_peserta = r.no_peserta '\
    'and r.status_dplk = \'A\' '\
    'and (isnull(r.akum_dana_iuran_pst,0.0) + isnull(r.akum_dana_iuran_pk,0.0) + isnull(r.akum_dana_pengembangan,0.0) + isnull(r.akum_dana_peralihan,0.0)) > 0; '\
    % (kode_nasabah_corporate)
  config.SendDebugMsg(strSQL)
  return config.CreateSQL(strSQL).RawResult

def WriteToFile(config, parameter, returnpacket):
  #dari_tanggal = parameter.FirstRecord.dari_tanggal
  #hingga_tanggal = parameter.FirstRecord.hingga_tanggal

  global tepi_atas, tepi_bawah, baris_per_halaman

  kode_nasabah_corporate = parameter.FirstRecord.kode_nasabah_corporate
  periode = parameter.FirstRecord.periode
  tahun = parameter.FirstRecord.tahun
  tepi_atas = parameter.FirstRecord.tepi_atas
  tepi_bawah = parameter.FirstRecord.tepi_bawah
  tepi_kiri = parameter.FirstRecord.tepi_kiri
  baris_per_halaman = parameter.FirstRecord.baris_per_halaman

  CekJumlahBaris(config, tepi_kiri)

  strTepiKiri = ''
  for i in range(tepi_kiri):
    strTepiKiri += ' '

  dari_tanggal, hingga_tanggal = getAwalAkhirTanggal(
    config
    , periode
    , tahun
  )

  str_dari_tanggal = config.FormatDateTime('yyyy-mm-dd', dari_tanggal )
 
  str_hingga_tanggal_plus = config.FormatDateTime('yyyy-mm-dd', hingga_tanggal + 1)

  resSQL = resSQLNasabahDPLK(config, kode_nasabah_corporate)
  resSQL.First()

  if not resSQL.Eof:
    nbOfPst = 0

    # ada data peserta yang akan dicetak
    strTglFile = config.FormatDateTime('yyyymmdd', config.Now())

    sTextFile = 'statemen_korporat_%s' % (strTglFile)
    sBaseFileName = '%s_1.txt' % (sTextFile)
    sFileName = config.UserHomeDirectory + sBaseFileName

    oFile = open(sFileName, 'w')
    TepiAtas(config, oFile)
    while not resSQL.Eof:

      saldo_awal = moduleapi.GetSaldoAwal(config, resSQL.no_peserta, str_dari_tanggal)
      ConstructReportHeader(config, resSQL.no_peserta, dari_tanggal, hingga_tanggal, \
        saldo_awal, strTepiKiri, oFile)
      ContructSumValues(config, resSQL.no_peserta, str_dari_tanggal, str_hingga_tanggal_plus, \
        saldo_awal, oFile, dari_tanggal, hingga_tanggal, strTepiKiri)
      ConstructReportValues(config, resSQL.no_peserta, str_dari_tanggal, \
        str_hingga_tanggal_plus, saldo_awal, strTepiKiri, oFile)

      resSQL.Next()

      nbOfPst += 1
      if (not resSQL.Eof) and (nbOfPst % MAXPST_PERFILE) == 0:
        oFile.close()

        # pack as stream
        sw = returnpacket.AddStreamWrapper()
        sw.LoadFromFile(sFileName)
        sw.MIMEType = config.AppObject.GetMIMETypeFromExtension(sFileName)

        sBaseFileName = '%s_%d.txt' % (sTextFile, (nbOfPst / MAXPST_PERFILE) + 1)
        sFileName = config.UserHomeDirectory + sBaseFileName

        oFile = open(sFileName, 'w')

        TepiAtas(config, oFile)

    # buat pembatas akhir file
    oFile.write('====End of File. Ganti baris ini dengan tulisan teratas dari file lainnya jika ingin menyambungkan.====')

    # tutup file terakhir dan isi nama file terakhir ke wrapper
    oFile.close()

    # pack as stream
    sw = returnpacket.AddStreamWrapper()
    sw.LoadFromFile(sFileName)
    sw.MIMEType = config.AppObject.GetMIMETypeFromExtension(sFileName)

def CreateReport(config, parameter, returnpacket):
  WriteToFile(config, parameter, returnpacket)
