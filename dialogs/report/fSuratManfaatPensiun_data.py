import sys, string
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
  rec.tepi_kiri = 0
  rec.baris_per_halaman = 55

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
    periode = periode + 2
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

def ConstructReportHeader(config, no_peserta, nama_lengkap, jenis_kelamin, tgl_pensiun, strTepiKiri, oFile):

  dictBulan = {'01':'Januari','02':'Februari','03':'Maret',\
               '04':'April','05':'Mei','06':'Juni',\
               '07':'Juli','08':'Agustus','09':'September',\
               '10':'Oktober','11':'November','12':'Desember'}
               
  oNasabahDPLK = config.CreatePObjImplProxy('NasabahDPLK')
  oNasabahDPLK.Key = no_peserta

  if jenis_kelamin == 'P': ket = 'Bapak'
  elif jenis_kelamin == 'W': ket = 'Ibu'
  else: ket = 'Bapak/Ibu'

  alamat = '%s' % (oNasabahDPLK.alamat_surat_jalan)
  alamat1 = '%s' % (oNasabahDPLK.alamat_surat_jalan2)
  alamat2 = 'RT/RW: %s %s' % (oNasabahDPLK.alamat_surat_rtrw, oNasabahDPLK.alamat_surat_kelurahan)

  kecamatan = '%s' % (oNasabahDPLK.alamat_surat_kecamatan)
  kota_kodepos   = '%s %s' % (oNasabahDPLK.alamat_surat_kota, oNasabahDPLK.alamat_surat_kode_pos)
  
  y,m,d = oNasabahDPLK.LRekeningDPLK.tgl_pensiun[:3]
  tglPensiun = config.FormatDateTime('d mmmm yyyy',\
    config.ModLibUtils.EncodeDate(y,m,d))

  tglNow = config.FormatDateTime('dd', config.Now())
  blnNow = config.FormatDateTime('mm', config.Now())
  thnNow = config.FormatDateTime('yyyy', config.Now())
  nama_bulan = '%s' % (dictBulan[blnNow])
  nama_bulan = tglNow+' '+nama_bulan+' '+thnNow

  pensiun = '%d [%s]' % (oNasabahDPLK.LRekeningDPLK.usia_pensiun, tglPensiun)
  no_peserta = ''
  #periode = '%s - %s' % (config.FormatDateTime('d mmmm yyyy',dari_tanggal), config.FormatDateTime('d mmmm yyyy',hingga_tanggal))

  #if jenis_kelamin == 'P' or jenis_kelamin == 'W':
  #   oFile.write(strTepiKiri +' ');NextLine(config, oFile)
  #   oFile.write(strTepiKiri +' ');NextLine(config, oFile)
  #   oFile.write(strTepiKiri +' ');NextLine(config, oFile)
  #   oFile.write(strTepiKiri +' ');NextLine(config, oFile)
  #   NextLine(config, oFile)
  #else:
  #   oFile.write(strTepiKiri +' ');NextLine(config, oFile)
  #   oFile.write(strTepiKiri +' ');NextLine(config, oFile)
  #   oFile.write(strTepiKiri +' ');NextLine(config, oFile)
  #   oFile.write(strTepiKiri +' ');NextLine(config, oFile)
  #   NextLine(config, oFile)

  oFile.write(strTepiKiri +'%-11s %-40s %s %s' % ('Kepada Yth :', no_peserta, 'Jakarta,',nama_bulan ));NextLine(config, oFile)
  oFile.write(strTepiKiri +'%s %-15s ' % ( ket, oNasabahDPLK.nama_lengkap));NextLine(config, oFile)
  oFile.write(strTepiKiri +'%-11s' % (alamat));NextLine(config, oFile)

  if len(alamat1) > 4:
     oFile.write(strTepiKiri +'%s%s' % ('', alamat1));NextLine(config, oFile)

  oFile.write(strTepiKiri +'%s' % (alamat2));NextLine(config, oFile)
  if kecamatan =='':
     oFile.write(strTepiKiri +'%s' % (kota_kodepos));NextLine(config, oFile)
  else:
     oFile.write(strTepiKiri +'%s' % (kecamatan));NextLine(config, oFile)
     oFile.write(strTepiKiri +'%s' % (kota_kodepos));NextLine(config, oFile)
     
  NextLine(config, oFile)
  NextLine(config, oFile)
  NextLine(config, oFile)
  oFile.write(strTepiKiri +'%s' % ("Assalamu'alaikum Warahmatullahi Wabarakatuh,"));NextLine(config, oFile)
  NextLine(config, oFile)
  oFile.write(strTepiKiri +'%s' % ('Semoga ALLAH SWT senantiasa memberikan rahmat dan hidayah-Nya kepada kita semua' \
                            ' dalam menjalankan aktivitas sehari-hari, Amin.'));NextLine(config, oFile)
  NextLine(config, oFile)
  oFile.write(strTepiKiri +'%s %s %s %s%s' % ('Terima kasih kami ucapkan atas kepercayaan yang telah',ket,\
                           'berikan kepada kami dalam mengelola dana untuk mempersiapkan masa tidak aktif lagi/pensiun'\
                           ,ket,'.'));NextLine(config, oFile)
  NextLine(config, oFile)
  oFile.write(strTepiKiri +'%s %s %s %s%s %s %s %s %s' % ('Berdasar data yang kami kelola, kami sampaikan bahwa '\
                           'masa kepesertaan DPLK',ket,'akan berakhir pada tanggal',tgl_pensiun,'. Dana tersebut pada '\
                           'prinsipnya dapat',ket,'cairkan sesuai dengan ketentuan yang telah kami sampaikan sebelumnya. '\
                           'Namun dapat juga tetap',ket,'amanahkan pengelolaannya kepada kami sampai dengan usia maksimal 65' \
                           ' tahun dengan melakukan registrasi ulang kepesertaan kembali.'));NextLine(config, oFile)
  NextLine(config, oFile)
  oFile.write(strTepiKiri +'%s %s %s' % ('Informasi lebih lanjut,',ket,'mohon dapat menghubungi :'));NextLine(config, oFile)
  NextLine(config, oFile)
  NextLine(config, oFile)
  oFile.write(strTepiKiri +'%24s %s' % ('','Customer Service DPLK Muamalat'));NextLine(config, oFile)
  oFile.write(strTepiKiri +'%26s %s' % ('','Gedung Arthaloka lantai 9'));NextLine(config, oFile)
  NextLine(config, oFile)
  oFile.write(strTepiKiri +'%25s %s' % ('','Jl. Jend. Sudirman Kav.2 No.2'));NextLine(config, oFile)
  oFile.write(strTepiKiri +'%20s %s' % ('','Telp. (021) 2511303   Fax (021) 2511438'));NextLine(config, oFile)
  oFile.write(strTepiKiri +'%25s %s' % ('','Email : adm@dplkmuamalat.com'));NextLine(config, oFile)
  oFile.write(strTepiKiri +'%40s %s' % ('','atau'));NextLine(config, oFile)
  oFile.write(strTepiKiri +'%25s %s' % ('','Email : info@dplkmuamalat.com'));NextLine(config, oFile)
  NextLine(config, oFile)
  NextLine(config, oFile)
  oFile.write(strTepiKiri +'%s %s %s' % ('Demikian kami sampaikan. Atas perhatian',ket,\
                        'kami sampaikan terima kasih.'));NextLine(config, oFile)
  NextLine(config, oFile)
  oFile.write(strTepiKiri +'%s' % ("Wassalamu'alaikum Warahmatullahi Wabarakatuh"));NextLine(config, oFile)
  NextLine(config, oFile)
  NextLine(config, oFile)
  oFile.write(strTepiKiri +'%32s %s' % ('','DPLK Muamalat,'));NextLine(config, oFile)
  NextLine(config, oFile)
  NextLine(config, oFile)
  NextLine(config, oFile)
  NextLine(config, oFile)
  oFile.write(strTepiKiri +'%s' % ('Nur Alfa Agustina'));
  oFile.write(strTepiKiri +'%50s' % ('Rasmita Dinata'));  NextLine(config, oFile)
  oFile.write(strTepiKiri +'%s' % ('Pelaksana Tugas Pengurus'));
  oFile.write(strTepiKiri +'%50s' % ('Team Leader Marketing'));  NextLine(config, oFile)


def resSQLNasabahDPLK(config, str_bulan, str_tahun):

  strSQL = \
    'select n.no_peserta,n.nama_lengkap,n.jenis_kelamin, r.tgl_pensiun '\
    'from NasabahDPLK n, RekeningDPLK r '\
    'where r.status_dplk = \'A\' '\
    '  and n.no_peserta = r.no_peserta '\
    '  and datepart(month,r.tgl_pensiun) = \'%s\' '\
    '  and datepart(year,r.tgl_pensiun) = \'%s\' ;'\
    % (str_bulan, str_tahun)
  return config.CreateSQL(strSQL).RawResult

def WriteToFile(config, parameter, returnpacket):
  #dari_tanggal = parameter.FirstRecord.dari_tanggal
  #hingga_tanggal = parameter.FirstRecord.hingga_tanggal

  global tepi_atas, tepi_bawah, baris_per_halaman

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

  str_bulan = config.FormatDateTime('mm', dari_tanggal)
  str_tahun = config.FormatDateTime('yyyy', dari_tanggal)

  resSQL = resSQLNasabahDPLK(config, str_bulan, str_tahun)
  resSQL.First()

  if not resSQL.Eof:
    nbOfPst = 0


    # ada data peserta yang akan dicetak
    strTglFile = config.FormatDateTime('yyyymmdd', config.Now())

    sTextFile = 'surat_manfaat_pensiun_%s' % (strTglFile)
    sBaseFileName = '%s_1.txt' % (sTextFile)
    sFileName = config.UserHomeDirectory + sBaseFileName

    oFile = open(sFileName, 'w')
    TepiAtas(config, oFile)

    while not resSQL.Eof:
    
      y, m, d = resSQL.tgl_pensiun[:3]
      # tanggal dengan format dd/mm/yyyy
      tgl_pensiun = '%s/%s/%s' % (moduleapi.MyZFill(str(d),2), moduleapi.MyZFill(str(m),2), str(y))


      config.SendDebugMsg('No peserta : '+resSQL.no_peserta)
      
      ConstructReportHeader(config, resSQL.no_peserta, resSQL.nama_lengkap, \
      resSQL.jenis_kelamin, tgl_pensiun, strTepiKiri, oFile)

      config.SendDebugMsg('testtttt')
      resSQL.Next()


      NextPagePeserta(config, oFile)
      
      nbOfPst += 1
      if (not resSQL.Eof) and (nbOfPst % MAXPST_PERFILE) == 0:
        oFile.close()
        config.SendDebugMsg('Masukkkkkkkkkkk if')
        # pack as stream
        sw = returnpacket.AddStreamWrapper()
        sw.LoadFromFile(sFileName)
        sw.MIMEType = config.AppObject.GetMIMETypeFromExtension(sFileName)

        sBaseFileName = '%s_%d.doc' % (sTextFile, (nbOfPst / MAXPST_PERFILE) + 1)
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

