def FormShow(form, parameter):
  app = form.ClientApplication
  uipTransaksi = form.GetUIPartByName('uipTransaksi')
  uipNasabah = form.GetUIPartByName('uipNasabah')
  uipTransaksi.Edit()
  uipNasabah.Edit()

  ph = app.CreateValues(['no_peserta',uipNasabah.no_peserta])
  phret = app.ExecuteScript('transaksi/GetReturnInvestasi', ph)
  rec = phret.FirstRecord
  
  uipNasabah.return_reksadana = rec.return_reksadana
  uipNasabah.return_saham = rec.return_saham
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
    uipTransaksi.biaya_lain = uipParameter.BiayaSKN
  elif index == 1:
    uipTransaksi.biaya_lain = uipParameter.BiayaRTGS

def bHitungClick(sender):
  form = sender.OwnerForm
  uipTransaksi = form.GetUIPartByName('uipTransaksi')

  #checking nama dplk, alamat dan nomor DPLK lain
  if uipTransaksi.GetFieldValue('LLDP.kode_dp') in  ['',None]:
    form.ShowMessage('DPLK lain belum terisi, mohon diisi dahulu.')
    return

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
  uipUserInfo = form.GetUIPartByName('uipUserInfo')

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
