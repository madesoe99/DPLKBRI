def FormShow(form, parameter):
  app = form.ClientApplication
  uipTransaksi = form.GetUIPartByName('uipTransaksi')
  uipNasabah = form.GetUIPartByName('uipNasabah')
  uipTransaksi.Edit()
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

  #set nominal batas penarikan PHK dari jumlah dana iuran pk dan pst
  uipTransaksi.BatasTarikMaks = uipTransaksi.jml_tarik = \
    uipNasabah.DanaPk + uipNasabah.DanaPst
  uipTransaksi.BatasTarikMin = 0 #uipNasabah.DanaPk


  #disable tanggal transaksi, supaya diset dengan tanggal pakai batch
  #uipTransaksi.tgl_transaksi = parameter.FirstRecord.tglpakai
  uipTransaksi.tgl_transaksi = app.ModDateTime.Now()
  form.GetControlByName('pTransaksi.tgl_transaksi').Enabled = 1

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
  if uipTransaksi.BatasTarikMaks < uipParameter.PRESISI_ANGKA_FLOAT:
    form.ShowMessage('Jumlah Akumulasi Dana Iuran ialah 0! Untuk itu, tidak ada dana yang bisa ditarik.')
    return

  #cek nominal penarikan
  if uipTransaksi.jml_tarik in [None,'']:
    form.ShowMessage('Nominal penarikan tidak boleh kosong!')
    return
  elif uipTransaksi.jml_tarik < uipParameter.PRESISI_ANGKA_FLOAT:
    form.ShowMessage('Nominal Penarikan tidak boleh 0!')
    return
  elif uipTransaksi.jml_tarik < uipTransaksi.BatasTarikMin:
    form.ShowMessage('Nominal Penarikan tidak boleh kurang dari Batas Penarikan Minimal!')
    return
  elif uipTransaksi.jml_tarik > uipTransaksi.BatasTarikMaks:
    form.ShowMessage('Nominal Penarikan melebihi batas nominal dana yang boleh ditarik!')
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
  if uipTransaksi.jml_tarik in [None,'']:
    form.ShowMessage('Nominal penarikan tidak boleh kosong!')
    return
  elif uipTransaksi.jml_tarik < uipParameter.PRESISI_ANGKA_FLOAT:
    form.ShowMessage('Nominal Penarikan tidak boleh 0!')
    return
  elif uipTransaksi.jml_tarik < uipTransaksi.BatasTarikMin:
    form.ShowMessage('Nominal Penarikan tidak boleh kurang dari Batas Penarikan Minimal!')
    return
  elif uipTransaksi.jml_tarik > uipTransaksi.BatasTarikMaks:
    form.ShowMessage('Nominal Penarikan melebihi batas nominal dana yang boleh ditarik!')
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
