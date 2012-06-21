import pyFlexcel

def FormShow(form, parameter):
  app = form.ClientApplication
  uipTransaksi = form.GetUIPartByName('uipTransaksi')
  uipNasabah = form.GetUIPartByName('uipNasabah')
  uipParameter = form.GetUIPartByName('uipParameter')
  uipTransaksi.Edit()
  uipNasabah.Edit()

  ph = app.CreateValues(['no_peserta',uipNasabah.no_peserta])
  phret = app.ExecuteScript('transaksi/GetReturnInvestasi', ph)
  rec = phret.FirstRecord

  #set akumulasi dana dan nama paket investasi
  uipNasabah.return_reksadana = rec.return_reksadana
  uipNasabah.return_saham = rec.return_saham
  uipNasabah.SetFieldValue('DanaPk', \
    uipNasabah.GetFieldValue('LRekeningDPLK.akum_dana_iuran_pk'))
  uipNasabah.SetFieldValue('DanaPst', \
    uipNasabah.GetFieldValue('LRekeningDPLK.akum_dana_iuran_pst'))
  uipNasabah.DanaPengembangan = uipNasabah.GetFieldValue('LRekeningDPLK.akum_dana_pengembangan')
  uipNasabah.SetFieldValue('DanaPeralihan', \
    uipNasabah.GetFieldValue('LRekeningDPLK.akum_dana_peralihan'))
  uipNasabah.SetFieldValue('PaketInvestasi', \
    uipNasabah.GetFieldValue('LRekeningDPLK.LPaketInvestasi.nama_paket_investasi'))

  #set nominal batas penarikan 30% dari jumlah dana iuran pk dan pst
  uipTransaksi.BatasPenarikan = uipParameter.PERSEN_PENARIKAN_NORMAL * \
    uipNasabah.DanaPst

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

def bHitungClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipTransaksi = form.GetUIPartByName('uipTransaksi')
  uipParameter = form.GetUIPartByName('uipParameter')
  uipNasabah = form.GetUIPartByName('uipNasabah')
  
  #checking dana peserta dulu (bisa lewat nominal BatasPenarikan)
  if uipTransaksi.BatasPenarikan < uipParameter.PRESISI_ANGKA_FLOAT:
    #batas nominal penarikan 0, artinya akumulasi dana iuran peserta juga 0
    form.ShowMessage('Jumlah Akumulasi Dana Iuran Peserta ialah 0! Untuk itu, tidak ada dana yang bisa ditarik.')
    return

  #cek jumlah akumulasi dana iuran peserta dulu
  if uipNasabah.DanaPst >= uipParameter.MIN_JML_AKUM_IURAN_PST:
    #cek nominal penarikan
    if uipTransaksi.jml_tarik == None or uipTransaksi.jml_tarik == '':
      form.ShowMessage('Nominal penarikan tidak boleh kosong!')
      return
    elif uipTransaksi.jml_tarik < uipParameter.PRESISI_ANGKA_FLOAT:
      form.ShowMessage('Nominal Penarikan tidak boleh 0!')
      return
    elif uipTransaksi.jml_tarik > uipTransaksi.BatasPenarikan:
      form.ShowMessage('Nominal Penarikan melebihi batas nominal dana yang boleh ditarik!')
      return
  else:
    form.ShowMessage('Akumulasi Dana Iuran Peserta kurang dari jumlah minimum '\
      'yang boleh ditarik, yakni Rp %.0f. Untuk itu, transaksi akan ditolak.' \
      % (uipParameter.MIN_JML_AKUM_IURAN_PST))
    return

  if uipNasabah.NPWP in ['', None]:
    if not app.ConfirmDialog('Nasabah yang tidak memiliki NPWP akan dikenai pajak tambahan 20%. ' \
    '\nUntuk mendaftarkan NPWP nasabah dapat melalui menu Nasabah >> Buat Register CIF >> Register Lain-Lain '\
    '\nYakin lanjutkan transaksi penarikan?'): return

  form.CommitBuffer()
  try:
    form.PostResult()
  except:
    raise

  #set readonly all control page perhitungan
  form.GetPanelByName('pHitung').SetAllControlsReadOnly()

  #aktifkan button Simpan
  form.GetControlByName('pButton.bSimpan').Enabled = 1

  #notify user
  form.ShowMessage('Silahkan lihat di bagian Perhitungan.')

def bSimpanClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipTransaksi = form.GetUIPartByName('uipTransaksi')
  uipParameter = form.GetUIPartByName('uipParameter')
  uipUserInfo = form.GetUIPartByName('uipUserInfo')

  #cek nominal penarikan
  if uipTransaksi.jml_tarik == None or uipTransaksi.jml_tarik == '':
    form.ShowMessage('Nominal penarikan tidak boleh kosong!')
    return
  elif uipTransaksi.jml_tarik < uipParameter.PRESISI_ANGKA_FLOAT:
    form.ShowMessage('Nominal Penarikan tidak boleh 0!')
    return
  elif uipTransaksi.jml_tarik > uipTransaksi.BatasPenarikan:
    form.ShowMessage('Nominal Penarikan melebihi batas nominal dana yang boleh ditarik!')
    return

  form.CommitBuffer()
  try:
    uipUserInfo.Edit()
    uipUserInfo.HitungMode = 0
    uipUserInfo.isPrintAdvis = 0

    if app.ConfirmDialog('Anda ingin mencetak advis transaksi?'):
      uipUserInfo.isPrintAdvis = 1

    form.PostResult()
  except:
    raise

  #cek cetak advis
  if uipUserInfo.isPrintAdvis:
    app.DownloadItem(uipUserInfo.FileAdvis,'v')
    
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
  wb.SetCellValue(43,7, uipHitung.jml_tarik)
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
