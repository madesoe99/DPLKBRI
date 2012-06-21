import pyFlexcel

def FormShow(form, parameter):
  uipTransaksi = form.GetUIPartByName('uipTransaksi')
  uipNasabah = form.GetUIPartByName('uipNasabah')
  uipParameter = form.GetUIPartByName('uipParameter')
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

  #set nominal batas penarikan 30% dari jumlah dana iuran pk dan pst
  uipTransaksi.BatasPenarikan = uipParameter.PERSEN_PENARIKAN_NORMAL * \
    uipNasabah.DanaPst

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

  #notify user
  form.ShowMessage('Silahkan lihat di bagian Perhitungan.')



def FormatStr(s):
  if s == None : s = ''
  
  return s
