import pyFlexcel

def FormShow(form, parameter):
  app = form.ClientApplication
  uipTransaksi = form.GetUIPartByName('uipTransaksi')
  uipTransaksi.Edit()

  #set batch transaksi
  uipTransaksi.SetFieldValue('LTransactionBatch.ID_TransactionBatch', \
    parameter.FirstRecord.idbatch)
  uipTransaksi.SetFieldValue('LTransactionBatch.no_batch', \
    parameter.FirstRecord.nobatch)
  form.GetControlByName('pTransaksi.LTransactionBatch').Enabled = 0

  #set branch code untuk transaction batch
  uipTransaksi.TB_BranchCode = parameter.FirstRecord.branchcode
  form.GetControlByName('pTransaksi.TB_BranchCode').Enabled = 0

  #disable tanggal transaksi, supaya diset dengan tanggal pakai batch
  uipTransaksi.tgl_transaksi = parameter.FirstRecord.tglpakai
  form.GetControlByName('pTransaksi.tgl_transaksi').Enabled = 0
  
  #cek kepesertaan < 1 tahun
  uipParameter = form.GetUIPartByName('uipParameter')
  uipNasabah = form.GetUIPartByName('uipNasabah')
  tglTransaksi = app.ModDateTime.EncodeDate(uipTransaksi.tgl_transaksi[0],\
    uipTransaksi.tgl_transaksi[1],uipTransaksi.tgl_transaksi[2])
  tglRegistrasi = app.ModDateTime.EncodeDate(uipNasabah.tgl_registrasi[0],\
    uipNasabah.tgl_registrasi[1],uipNasabah.tgl_registrasi[2])
  
  uipTransaksi.isKurangSetahunKepesertaan = \
    (tglTransaksi - tglRegistrasi) < uipParameter.JUMLAH_HARI_SETAHUN
  form.GetControlByName('pTransaksi.isKurangSetahunKepesertaan').Enabled = 0
  form.GetControlByName('pTransaksi.isAdaKurangSetahunPengalihan').Enabled = 0
  

  #form.ShowMessage(str(uipTransaksi.SumKurangSetahunMutasiPeralihan))

def FormAfterProcessServerData(form, opID, datapacket):
  app = form.ClientApplication
  uipNasabah = form.GetUIPartByName('uipNasabah')
  uipNasabah.Edit()

  #set akumulasi dana dan nama paket investasi
  uipNasabah.SetFieldValue('DanaPk', \
    uipNasabah.GetFieldValue('LRekeningDPLK.akum_dana_iuran_pk'))
  uipNasabah.SetFieldValue('DanaPst', \
    uipNasabah.GetFieldValue('LRekeningDPLK.akum_dana_iuran_pst'))
  uipNasabah.SetFieldValue('DanaPengembangan', \
    uipNasabah.GetFieldValue('LRekeningDPLK.akum_dana_pengembangan'))
  uipNasabah.SetFieldValue('DanaPeralihan', \
    uipNasabah.GetFieldValue('LRekeningDPLK.akum_dana_peralihan'))
  uipNasabah.SetFieldValue('PaketInvestasi', \
    uipNasabah.GetFieldValue('LRekeningDPLK.LPaketInvestasi.nama_paket_investasi'))

  #set usia pensiun, tgl pensiun dan tgl pensiun dipercepat
  uipNasabah.SetFieldValue('UsiaPensiun', \
    uipNasabah.GetFieldValue('LRekeningDPLK.usia_pensiun'))
  y,m,d = uipNasabah.GetFieldValue('LRekeningDPLK.tgl_pensiun')[:3]
  uipNasabah.TglPensiun = app.ModDateTime.EncodeDate(y,m,d)
  y,m,d = uipNasabah.GetFieldValue('LRekeningDPLK.tgl_pensiun_dipercepat')[:3]
  uipNasabah.TglPensiunDipercepat = app.ModDateTime.EncodeDate(y,m,d)

  #set total dana peserta dari jumlah dana iuran pk, pst, pengembangan, peralihan
  uipTransaksi = form.GetUIPartByName('uipTransaksi')
  uipTransaksi.Edit()
  uipTransaksi.TotalDana = uipNasabah.DanaPk + uipNasabah.DanaPst + \
    uipNasabah.DanaPengembangan + uipNasabah.DanaPeralihan
  form.GetControlByName('pTransaksi.TotalDana').ReadOnly = 1

  #set pilihan untuk jenis penerimaan manfaat
  uipJM = form.GetUIPartByName('uipJenisManfaat')

  if uipJM.isBiasaAllowed:
    kodeManfaat = 'B'
    namaPensiun = 'Pensiun Biasa'
  elif uipJM.isDipercepatAllowed:
    kodeManfaat = 'D'
    namaPensiun = 'Pensiun Dipercepat'
    form.ShowMessage('Tanggal pensiun biasa belum tercapai. Pengambilan '\
      'manfaat hanya diperbolehkan untuk jenis Pensiun Cacat / Meninggal (ahli '\
      'waris) / Dipercepat.')
  else:
##    #langsung set pensiun meninggal saja
##    kodeManfaat = 'J'
##    namaPensiun = 'Pensiun Meninggal'
    form.ShowMessage('Tanggal pensiun dipercepat belum tercapai. Pengambilan '\
      'manfaat hanya diperbolehkan untuk jenis Pensiun Cacat / Meninggal (ahli waris).')

  if uipJM.isBiasaAllowed or uipJM.isDipercepatAllowed:
      uipTransaksi.SetFieldValue('Ljenis_penerimaan_manfaat.kode_jns_manfaat',\
        kodeManfaat)
      uipTransaksi.SetFieldValue('Ljenis_penerimaan_manfaat.nama_jns_manfaat',namaPensiun)

  return 1

def JenisBiayaChange(sender):
  uipTransaksi = sender.OwnerForm.GetUIPartByName('uipTransaksi')
  uipParameter = sender.OwnerForm.GetUIPartByName('uipParameter')
  uipTransaksi.Edit()

  index = sender.OwnerForm.GetControlByName('pTransaksi.jenis_biaya').ItemIndex
  if index == 0:
    uipTransaksi.biaya_lain = uipParameter.BiayaTunai
  elif index == 1:
    uipTransaksi.biaya_lain = uipParameter.BiayaSKN
  elif index == 2:
    uipTransaksi.biaya_lain = uipParameter.BiayaRTGS
  elif index == 3:
    uipTransaksi.biaya_lain = uipParameter.BiayaPindahBuku

def JenisPenerimaanManfaatBeforeLookup(sender, linkui):
  uipTransaksi = sender.OwnerForm.GetUIPartByName('uipTransaksi')
  uipTransaksi.Edit()

  #bersihkan dulu lookup LAhliWaris
  uipTransaksi.ClearLink('LAhliWaris')

  return 1

def JenisPenerimaanManfaatAfterLookup(sender, linkui):
  uipTransaksi = sender.OwnerForm.GetUIPartByName('uipTransaksi')
  
  #cek jenis penerimaan manfaat pensiun janda / anak
  if uipTransaksi.GetFieldValue('Ljenis_penerimaan_manfaat.kode_jns_manfaat') == 'J':
    sender.OwnerForm.GetControlByName('pTransaksi.LAhliWaris').Enabled = 1
  else:
    sender.OwnerForm.GetControlByName('pTransaksi.LAhliWaris').Enabled = 0

def bHitungClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipTransaksi = form.GetUIPartByName('uipTransaksi')
  uipNasabah = form.GetUIPartByName('uipNasabah')
  uipParameter = form.GetUIPartByName('uipParameter')
  uipHitung = form.GetUIPartByName('uipHitung')

  #cek jumlah total dana
  if uipTransaksi.TotalDana < uipParameter.PRESISI_ANGKA_FLOAT:
    #total dana 0, tidak akan pernah dihitungkan dan button Simpan tetap disable
    form.ShowMessage('Total Dana Peserta ialah 0! Untuk itu, tidak ada dana yang bisa ditarik.')
    return

  #checking jenis penerimaan manfaat
  if uipTransaksi.GetFieldValue('Ljenis_penerimaan_manfaat.kode_jns_manfaat') in [None,'']:
    form.ShowMessage('Mohon isi terlebih dahulu Jenis Penerimaan Manfaat.')
    return

  if uipNasabah.NPWP in ['','-', None]:
    if not app.ConfirmDialog('Nasabah yang tidak memiliki NPWP akan dikenai pajak tambahan 20%. ' \
    '\nUntuk mendaftarkan NPWP nasabah dapat melalui menu Nasabah >> Buat Register CIF >> Register Lain-Lain '\
    '\nYakin lanjutkan transaksi penarikan?'): return


  form.CommitBuffer()
  try:
    form.PostResult()
  except:
    raise

  #cek keharusan mengisi nama anuitas
  if uipTransaksi.isKurangSetahunKepesertaan and \
    uipHitung.manfaat_anuitas > 0.0:
    #peserta diharuskan ikut anuitas, enabling nama anuitas
    form.GetControlByName('pTransaksi.nama_anuitas').Enabled = 1

  #set readonly all control page perhitungan
  form.GetPanelByName('pHitung').SetAllControlsReadOnly()

  #aktifkan button Simpan
  form.GetControlByName('pButton.bSimpan').Enabled = 1

  #notify user
  form.ShowMessage('Silahkan lihat di bagian Perhitungan.')
  form.GetControlByName('pButton.btCetak').Enabled = 1

def bSimpanClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipTransaksi = form.GetUIPartByName('uipTransaksi')
  uipUserInfo = form.GetUIPartByName('uipUserInfo')

  #checking jenis penerimaan manfaat
  if uipTransaksi.GetFieldValue('Ljenis_penerimaan_manfaat.kode_jns_manfaat') == None or \
    uipTransaksi.GetFieldValue('Ljenis_penerimaan_manfaat.kode_jns_manfaat') == '':
    form.ShowMessage('Jenis Penerimaan Manfaat masih kosong! Mohon dipilih terlebih dahulu.')
    return
    
  #checking ahli waris penerima manfaat
  if form.GetControlByName('pTransaksi.LAhliWaris').Enabled and \
    (uipTransaksi.GetFieldValue('LAhliWaris.ahliwaris_id') == None or \
    uipTransaksi.GetFieldValue('LAhliWaris.ahliwaris_id') == ''):
    form.ShowMessage('Ahli Waris Penerimaan Manfaat masih kosong! Mohon dipilih terlebih dahulu.')
    return

  #checking nama anuitas
  if form.GetControlByName('pTransaksi.nama_anuitas').Enabled and \
    (uipTransaksi.nama_anuitas == None or uipTransaksi.nama_anuitas == ''):
    form.ShowMessage('Hasil perhitungan menunjukkan peserta memperoleh Manfaat Anuitas. ' \
      '\nUntuk itu, mohon isi Nama Anuitas yang akan diikuti peserta.')
    return
  
  form.CommitBuffer()
  try:
    uipUserInfo.Edit()
    uipUserInfo.isPrintAdvis = 0
    uipUserInfo.HitungMode = 0
    
    if app.ConfirmDialog('Anda ingin mencetak advis transaksi?'):
      uipUserInfo.isPrintAdvis = 1

    form.PostResult()
  except:
    raise

  #cek cetak advis
  if uipUserInfo.isPrintAdvis:
    app.DownloadItem(uipUserInfo.FileAdvis,'v')

  sender.ExitAction = 1
  
  form.GetControlByName('pButton.btCetak').Enabled = 1
  
  
def btCetakClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipTransaksi = form.GetUIPartByName('uipTransaksi')
  uipNasabah = form.GetUIPartByName('uipNasabah')
  uipHitung = form.GetUIPartByName('uipHitung')
  uipParameter = form.GetUIPartByName('uipParameter')

  xl_filename = 'C:/__accountingDPLK/template/bukti potong PPh 21.xls'
  as_filename = 'C:/__accountingDPLK/PPh21-%s.xls' % (uipNasabah.no_peserta)

  wb = pyFlexcel.Open(xl_filename)

  wb.SetCellValue(11,6, '')
  wb.SetCellValue(13,5, FormatStr(uipNasabah.NPWP))
  wb.SetCellValue(15,5, uipNasabah.nama_lengkap)
  wb.SetCellValue(17,5, FormatStr(uipNasabah.alamat_jalan) + ' ' + FormatStr(uipNasabah.alamat_rtrw) + ' ' +\
                        FormatStr(uipNasabah.alamat_kelurahan) + ' ' + FormatStr(uipNasabah.alamat_kecamatan) + ' ' + \
                        FormatStr(uipNasabah.alamat_kota) + ' ' + FormatStr(uipNasabah.alamat_kode_pos))
  wb.SetCellValue(43,7, uipHitung.saldo_manfaat)
  if uipNasabah.NPWP in ['', None]:
    wb.SetCellValue(43,9, uipParameter.PERSEN_DENDA_NPWP/100)
  else:
    wb.SetCellValue(43,9, 0)

  wb.SetCellValue(43,13, uipHitung.pajak)
  wb.SaveAs(as_filename)

  app.ShowMessage('Bukti potong PPh 21 telah tergenerate di %s' % (as_filename))

def FormatStr(s):
  if s == None : s = ''

  return s
