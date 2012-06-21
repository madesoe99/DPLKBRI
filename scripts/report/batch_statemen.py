import sys
sys.path.append('c:/dafapp/dplk07/script_modules')
import moduleapi
import textutils
import string

def GetMutasiIuran(config, no_pst, str_tgl_awal, str_tgl_akhir_plus):
  ## mengembalikan nilai semua transaksi positif (credit)
  ## mengecualikan transaksi pendaftaran, premi, dan bagi hasil

  strSQL = \
    'select sum(mutasi_peralihan + mutasi_pengembangan + mutasi_iuran_pst + mutasi_iuran_pk) as mutasi_total '\
    'from TransaksiDPLK '\
    'where tgl_transaksi >= \'%s\' '\
    '  and tgl_transaksi < \'%s\' '\
    '  and no_peserta = \'%s\' '\
    '  and kode_jenis_transaksi not in (\'A\', \'B\', \'G\', \'I\') '\
    '  and isCommitted = \'T\' '\
    '  and mutasi_peralihan >= 0.0 '\
    '  and mutasi_pengembangan >= 0.0 '\
    '  and mutasi_iuran_pst >= 0.0 '\
    '  and mutasi_iuran_pk >= 0.0 '\
    % (str_tgl_awal, str_tgl_akhir_plus, no_pst)
  resSQL = config.CreateSQL(strSQL).RawResult

  resSQL.First()
  if resSQL.Eof:
    return 0.0
  else:
    if resSQL.mutasi_total == None:
      return 0.0
    else:
      return resSQL.mutasi_total

def GetMutasiPenarikan(config, no_pst, str_tgl_awal, str_tgl_akhir_plus):
  ## mengembalikan nilai semua transaksi negatif (debet)
  ## mengecualikan transaksi pendaftaran A, premi B, dan biaya (C, D, X)

  strSQL = \
    'select sum(mutasi_peralihan + mutasi_pengembangan + mutasi_iuran_pst + mutasi_iuran_pk) as mutasi_total '\
    'from TransaksiDPLK '\
    'where tgl_transaksi >= \'%s\' '\
    '  and tgl_transaksi < \'%s\' '\
    '  and no_peserta = \'%s\' '\
    '  and kode_jenis_transaksi not in (\'A\', \'B\', \'C\', \'D\', \'X\') '\
    '  and isCommitted = \'T\' '\
    '  and mutasi_peralihan < 0.0 '\
    '  and mutasi_pengembangan < 0.0 '\
    '  and mutasi_iuran_pst < 0.0 '\
    '  and mutasi_iuran_pk < 0.0 '\
    % (str_tgl_awal, str_tgl_akhir_plus, no_pst)
  resSQL = config.CreateSQL(strSQL).RawResult

  resSQL.First()
  if resSQL.Eof:
    return 0.0
  else:
    if resSQL.mutasi_total == None:
      return 0.0
    else:
      return resSQL.mutasi_total

def GetMutasiBagiHasil(config, no_pst, str_tgl_awal, str_tgl_akhir_plus):
  ## mengembalikan nilai transaksi bagi hasil

  strSQL = \
    'select sum(mutasi_peralihan + mutasi_pengembangan + mutasi_iuran_pst + mutasi_iuran_pk) as mutasi_total '\
    'from TransaksiDPLK '\
    'where tgl_transaksi >= \'%s\' '\
    '  and tgl_transaksi < \'%s\' '\
    '  and no_peserta = \'%s\' '\
    '  and kode_jenis_transaksi = \'G\' '\
    '  and isCommitted = \'T\' '\
    % (str_tgl_awal, str_tgl_akhir_plus, no_pst)
  resSQL = config.CreateSQL(strSQL).RawResult

  resSQL.First()
  if resSQL.Eof:
    return 0.0
  else:
    if resSQL.mutasi_total == None:
      return 0.0
    else:
      return resSQL.mutasi_total

def GetMutasiBiaya(config, no_pst, str_tgl_awal, str_tgl_akhir_plus):
  ## mengembalikan nilai transaksi biaya

  strSQL = \
    'select sum(mutasi_peralihan + mutasi_pengembangan + mutasi_iuran_pst + mutasi_iuran_pk) as mutasi_total '\
    'from TransaksiDPLK '\
    'where tgl_transaksi >= \'%s\' '\
    '  and tgl_transaksi < \'%s\' '\
    '  and no_peserta = \'%s\' '\
    '  and kode_jenis_transaksi in (\'C\', \'D\', \'X\') '\
    '  and isCommitted = \'T\' '\
    % (str_tgl_awal, str_tgl_akhir_plus, no_pst)
  resSQL = config.CreateSQL(strSQL).RawResult

  resSQL.First()
  if resSQL.Eof:
    return 0.0
  else:
    if resSQL.mutasi_total == None:
      return 0.0
    else:
      return resSQL.mutasi_total

def GetMutasiPengalihanDariDPLKLain(config, no_pst, str_tgl_awal, str_tgl_akhir_plus):
  ## mengembalikan nilai pengalihan dari dplk lain

  strSQL = \
    'select sum(mutasi_peralihan + mutasi_pengembangan + mutasi_iuran_pst + mutasi_iuran_pk) as mutasi_total '\
    'from TransaksiDPLK '\
    'where tgl_transaksi >= \'%s\' '\
    '  and tgl_transaksi < \'%s\' '\
    '  and no_peserta = \'%s\' '\
    '  and kode_jenis_transaksi = \'I\' '\
    '  and isCommitted = \'T\' '\
    % (str_tgl_awal, str_tgl_akhir_plus, no_pst)
  resSQL = config.CreateSQL(strSQL).RawResult

  resSQL.First()
  if resSQL.Eof:
    return 0.0
  else:
    if resSQL.mutasi_total == None:
      return 0.0
    else:
      return resSQL.mutasi_total

def WriteToTextFile(f, mutasi, nominal, sandi, tp_nosaldo, tanggal_trans, jenis_trans):
  from textutils import Pad, symbol, space, formatfloat
  from string import upper

  if upper(str(mutasi))=='D':
    tp_nosaldo = tp_nosaldo-nominal
  elif upper(str(mutasi))=='C':
    tp_nosaldo = tp_nosaldo+nominal

  space(f,17)
  f.WriteText(Pad(1,str(tanggal_trans),14))
  space(f,3)
  f.WriteText(Pad(2,sandi,3))
  space(f,3)
  f.WriteText(Pad(0,jenis_trans,27))
  space(f,1)
  f.WriteText(Pad(2,formatfloat(nominal),17))
  f.WriteText(Pad(1,mutasi,3))
  space(f,2)
  f.WriteText(Pad(2,formatfloat(tp_nosaldo),19))
  f.Writeline()

  return tp_nosaldo  

def resSQLCatMutasiIndv(config, no_peserta, str_dari_tanggal, str_hingga_tanggal_plus):
  strSQL = '\
    select tgl_transaksi \
      , j.kode_jenis_transaksi \
      , j.nama_transaksi \
      , mutasi_peralihan + mutasi_pengembangan + mutasi_iuran_pst + mutasi_iuran_pk as mutasi_total \
    from TransaksiDPLK t, JenisTransaksiDPLK j \
    where tgl_transaksi >= \'%s\' \
      and tgl_transaksi < \'%s\' \
      and no_peserta = \'%s\' \
      and j.kode_jenis_transaksi not in (\'A\',\'B\') \
      and t.kode_jenis_transaksi = j.kode_jenis_transaksi \
      and isCommitted = \'T\' \
    order by tgl_transaksi' \
    % (str_dari_tanggal, str_hingga_tanggal_plus, no_peserta)
  return config.CreateSQL(strSQL).RawResult

def WriteTransaction(config, f, no_pst, str_tgl_awal, str_tgl_akhir_plus, tp_nosaldo):
  from textutils import Pad, symbol, space, formatfloat
  from time import strftime

  resSQL = resSQLCatMutasiIndv(config, no_pst, str_tgl_awal, str_tgl_akhir_plus)
  resSQL.First()
  while not resSQL.Eof:
    if resSQL.mutasi_total < 0.0:
      mutasi = 'D'
    else:
      mutasi = 'C'

    y, m, d = resSQL.tgl_transaksi[:3]
    # tanggal dengan format dd mmm yyyy
    tanggal_trans = config.FormatDateTime('dd mmm yyyy', config.ModDateTime.EncodeDate(y, m, d))

    tp_nosaldo = WriteToTextFile(f, mutasi, resSQL.mutasi_total, resSQL.kode_jenis_transaksi, tp_nosaldo, tanggal_trans, resSQL.nama_transaksi)

    resSQL.Next()

  return tp_nosaldo    

def WriteIdentity(config, f, no_pst, saldo_awal, str_tgl_awal, str_tgl_akhir_plus, strPeriode, tahun, kirim_statemen):
  from time import strftime, gmtime
  from fpformat import fix
  from textutils import Pad, symbol, space, formatfloat

  if kirim_statemen == 'K':
    jnsAlamat = 'kantor'
    almtRTRW = '\'\''
  else:
    ## kirim_statemen == 'R':
    jnsAlamat = 'surat'
    almtRTRW = 'isnull(alamat_surat_rtrw,\'\')'

  strSQL = \
    'select isnull(nama_lengkap,\'\') nama_lengkap '\
    '  , isnull(alamat_%s_jalan,\'\') jalan '\
    '  , isnull(alamat_%s_kelurahan,\'\') kelurahan '\
    '  , isnull(alamat_%s_kecamatan,\'\') kecamatan '\
    '  , isnull(alamat_%s_kota,\'\') kota '\
    '  , isnull(alamat_%s_kode_pos,\'\') kode_pos '\
    '  , isnull(alamat_%s_propinsi,\'\') propinsi '\
    '  , %s rtrw '\
    '  , isnull(usia_pensiun, 0) usia_pensiun '\
    '  , tgl_pensiun '\
    '  , i.kode_paket_investasi '\
    '  , nama_paket_investasi '\
    '  from NasabahDPLK n, RekeningDPLK R, PaketInvestasi i '\
    '  where n.no_peserta = r.no_peserta '\
    '    and n.no_peserta = \'%s\' '\
    '    and r.kode_paket_investasi = i.kode_paket_investasi '\
    % (jnsAlamat, jnsAlamat, jnsAlamat, jnsAlamat, jnsAlamat, jnsAlamat, almtRTRW, no_pst)
  resSQL = config.CreateSQL(strSQL).RawResult

  nama = resSQL.nama_lengkap
  nomor = no_pst
  alamatjalan = resSQL.jalan
  alamatrt = resSQL.rtrw
  kelurahan = resSQL.kelurahan
  alamatkota = resSQL.kota
  provinsi2 = resSQL.propinsi
  kodepos = resSQL.kode_pos
  propinsi = provinsi2 + ' ' + Pad(0,kodepos,6)
  paket = resSQL.kode_paket_investasi + ' ' + resSQL.nama_paket_investasi

  Usia = resSQL.usia_pensiun
  tgl_pensiun = resSQL.tgl_pensiun

  saldo = saldo_awal
  iuran = GetMutasiIuran(config, no_pst, str_tgl_awal, str_tgl_akhir_plus)
  penarikan = -1 * GetMutasiPenarikan(config, no_pst, str_tgl_awal, str_tgl_akhir_plus)
  pengembangan = GetMutasiBagiHasil(config, no_pst, str_tgl_awal, str_tgl_akhir_plus)
  biaya = -1 * GetMutasiBiaya(config, no_pst, str_tgl_awal, str_tgl_akhir_plus)
  pengalihan = GetMutasiPengalihanDariDPLKLain(config, no_pst, str_tgl_awal, str_tgl_akhir_plus)
  saldoakhir = saldo_awal + iuran - penarikan + pengembangan + pengalihan - biaya

  space(f,9)
  f.WriteText('DANA PENSIUN LEMBAGA KEUANGAN')
  space(f,50)
  f.WriteText(strftime('%d %B %Y', gmtime()))
  f.Writeline()

  space(f,9)
  f.WriteText('PT.Bank Rakyat Indonesia,Tbk.')
  f.Writeline()
  f.Writeline()

  space(f,9)
  f.WriteText('PERIODE '+ string.upper(strPeriode))
  f.Writeline()
  f.Writeline()

  space(f,9)
  f.WriteText(nama)
  f.Writeline()

  space(f,9)
  f.WriteText('Nomor Peserta   :')
  f.WriteText(nomor)
  f.Writeline()

  space(f,9)
  f.WriteText(alamatjalan)
  space(f,50-len(alamatjalan))
  f.WriteText('Usia pensiun    :')
  f.WriteText(str(Usia))
  f.WriteText('  (')
  if tgl_pensiun <> None:
    f.WriteText(strftime('%d-%B-%Y', tgl_pensiun))
  f.WriteText(')')
  f.Writeline()

  space(f,9)
  f.WriteText('RT/RW  : ')
  f.WriteText(alamatrt+' '+kelurahan)
  space(f,41-len(alamatrt+' '+kelurahan))
  f.WriteText('Investasi       :')
  f.WriteText(paket)
  f.Writeline()

  space(f,9)
  f.WriteText(alamatkota)
  f.Writeline()

  space(f,9)
  f.WriteText(propinsi)
  f.Writeline()
  f.Writeline()
  f.Writeline()
  f.Writeline()
 
  space(f,13)
  f.WriteText(Pad(0,'Saldo Akhir',41))
  f.WriteText(':')
  f.WriteText(Pad(2,formatfloat(saldo_awal),16))
  f.Writeline()

  space(f,13)
  f.WriteText(Pad(0,'Akumulasi Iuran',41))
  f.WriteText(':')
  f.WriteText(Pad(2,formatfloat(iuran),16))
  f.Writeline()

  space(f,13)
  f.WriteText(Pad(0,'Akumulasi Penarikan',41))
  f.WriteText(':')
  f.WriteText(Pad(2,formatfloat(penarikan),16))
  f.Writeline()

  space(f,13)
  f.WriteText(Pad(0,'Hasil Pengembangan/Investasi',41))
  f.WriteText(':')
  f.WriteText(Pad(2,formatfloat(pengembangan),16))
  f.Writeline()

  space(f,13)
  f.WriteText(Pad(0,'Biaya Adm. & Pengelolaan',41))
  f.WriteText(':')
  f.WriteText(Pad(2,formatfloat(biaya),16))
  f.Writeline()

  space(f,13) 
  f.WriteText(Pad(0,'Pengalihan Dana Dari DPLK Lain',41))
  f.WriteText(':')
  f.WriteText(Pad(2,formatfloat(pengalihan),16))
  f.Writeline()

  space(f,13)
  symbol(f, '-',59)
  f.Writeline()

  space(f,13)
  f.WriteText(Pad(2,'Total Dana Peserta',41))
  f.WriteText(':')
  f.WriteText(Pad(2,formatfloat(saldoakhir),16))
  f.Writeline()

  space(f,15)
  symbol(f, '=',97)
  f.Writeline()

  space(f,17)
  f.WriteText('TGL.TRANSAKSI')
  space(f,5)
  f.WriteText(Pad(1,'KT',3))
  space(f,3)
  f.WriteText(Pad(1,'KETERANGAN',27))
  space(f,1)
  f.WriteText(Pad(2,'JML.TRANSAKSI',17))
  space(f,4)
  f.WriteText(Pad(2,'S A L D O',19))
  f.Writeline()

  space(f,15)
  symbol(f,'-',97)
  f.Writeline()

def DAFLongScriptMain(config, parameter, pid, monfilename):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # pid: Process ID of this script
  # monfilename: Monitor file name to store status

  from textutils import Pad, symbol, space, formatfloat, TextFileClass
  from string import split

  dataset = parameter.GetDataset(0)
  record = dataset.GetRecord(0)

  from_date = record.fromdate
  to_date = record.todate
  line = record.line
  bottom = record.bottom
  top = record.top
  filename = record.filename
  kode_cab_daftar = record.kode_cab_daftar
  kode_kelompok = record.kode_kelompok
  kode_nasabah_corporate = record.kode_nasabah_corporate
  str_ordering = record.str_ordering

  fromdate = config.FormatDateTime('mm/dd/yyyy', from_date)
  todate = config.FormatDateTime('mm/dd/yyyy', to_date)
  str_tgl_awal = config.FormatDateTime('yyyy-mm-dd', from_date)
  str_tgl_akhir_plus = config.FormatDateTime('yyyy-mm-dd', to_date+1)
  strPeriode = '%s-%s' % (config.FormatDateTime('d mmmm yyyy', from_date), config.FormatDateTime('d mmmm yyyy', to_date))
  tgl_awal = config.FormatDateTime('mm/dd/yyyy', from_date) 
  tahuntpl = config.ModDateTime.DecodeDate(to_date)
  tahun = tahuntpl[0]

  #write to file
  fl = TextFileClass()
  result_location = 'c:\\DAFApp\\dplk07\\Reports\\'+filename
  fl.BeginWrite(result_location)
  fl.SetPageMode(int(line), int(top), int(bottom))

  str_filter = ''
  if kode_cab_daftar <> '':
    str_filter +=  '  and kode_cab_daftar = \'%s\' ' % (kode_cab_daftar)
  if kode_kelompok <> '':
    str_filter +=  '  and kode_kelompok = \'%s\' ' % (kode_kelompok)
  if kode_nasabah_corporate <> '':
    str_filter +=  '  and kode_nasabah_corporate = \'%s\' ' % (kode_nasabah_corporate)

  if str_ordering <> '':
    str_ordering = 'order by '+ str_ordering

  strSQL = \
    'select n.no_peserta '\
    '  , kirim_statemen '\
    'from NasabahDPLK n '\
    '  , RekeningDPLK r '\
    '  , TransaksiDPLK t '\
    'where n.no_peserta = r.no_peserta '\
    '  and n.no_peserta = t.no_peserta '\
    '  and kirim_statemen <> \'N\' '\
    '  and tgl_transaksi >= \'%s\' '\
    '  and tgl_transaksi < \'%s\' '\
    '%s'\
    '%s'\
    % (str_tgl_awal, str_tgl_akhir_plus, str_filter, str_ordering)
  resSQL = config.CreateSQL(strSQL).RawResult

  while not resSQL.Eof:
    #write individual statement
    RekeningDPLK = config.CreatePObjImplProxy('RekeningDPLK')
    RekeningDPLK.key = resSQL.no_peserta
    saldoawal = moduleapi.GetSaldoAwal(config, resSQL.no_peserta, str_tgl_awal)
    tp_nosaldo = saldoawal

    config.ProgressTracker.SetProgressInfo2(1, 'processing customer ' + resSQL.no_peserta)
    WriteIdentity(config, fl, resSQL.no_peserta, saldoawal, str_tgl_awal, str_tgl_akhir_plus, strPeriode, tahun, resSQL.kirim_statemen)
    saldoakhir = WriteTransaction(config, fl, resSQL.no_peserta, fromdate, todate, tp_nosaldo)

    #write finalization
    space(fl,15)
    symbol(fl,'-',95)
    fl.Writeline()

    space(fl,15)
    fl.WriteText(Pad(1,'S A L D O  A K H I R ',75))
    fl.WriteText(Pad(2,formatfloat(saldoakhir),19))
    fl.Writeline()

    space(fl,15)
    symbol(fl,'=',95)
    fl.Writeline()

    fl.FillUntilEndOfPage()
    resSQL.Next()

  fl.StopWrite()

  config.SetINIKey(monfilename, 'GENERAL','STATUS','2')
  config.SetINIKey(monfilename, 'GENERAL','RESULT_LOCATION', result_location)

  return 1
