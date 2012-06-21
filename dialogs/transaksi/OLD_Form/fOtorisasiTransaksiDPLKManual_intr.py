def FormShow(form, parameter):

  #cek code number tag parameter
  if parameter.FirstRecord.code in [2000,3000,10000,10001,10002]:
    #mode view, disable button Approve dan Reject
    form.GetControlByName('pButton.bApprove').Enabled = 0
    form.GetControlByName('pButton.bApprove').Default = 0
    form.GetControlByName('pButton.bReject').Enabled = 0
    form.GetControlByName('pButton.bCancel').Caption = '&Tutup'
    form.GetControlByName('pButton.bCancel').Default = 1

    if parameter.FirstRecord.code in [2000,3000]:
      form.Caption = 'Lihat Detil Transaksi DPLK Manual'
    elif parameter.FirstRecord.code == 10000:
      form.Caption = 'Lihat Detil Biaya Administrasi Transaksi'
    elif parameter.FirstRecord.code == 10001:
      form.Caption = 'Lihat Detil Biaya Administrasi Tahunan'
    elif parameter.FirstRecord.code == 10002:
      form.Caption = 'Lihat Detil Biaya Pengelolaan Dana'

def bApproveClick(sender):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipTransaksi = sender.OwnerForm.GetUIPartByName('uipTransaksi')

  res = app.ExecuteScript(
    'transaksi/counttranspeserta'
    , app.CreateValues(
        ['no_peserta', uipTransaksi.no_peserta]
        , ['excludeIDTrans', uipTransaksi.ID_Transaksi]
      )
  )

  if res.FirstRecord.nbOfTrans:
    # nbOfTrans > 0
    # ada transaksi peserta tersebut yang belum diotorisasi

    confMsg = 'Terdapat %d transaksi peserta %s yang belum diotorisasi.\nLanjutkan?' % (res.FirstRecord.nbOfTrans, uipTransaksi.no_peserta)
    if not app.ConfirmDialog(confMsg):
      return

  form.CommitBuffer()
  form.PostResult()

  sender.ExitAction = 1 # eaQuitOK

def bRejectClick(sender):
  app = sender.OwnerForm.ClientApplication
  uipT = sender.OwnerForm.GetUIPartByName('uipTransaksi')

  if app.ConfirmDialog('Anda yakin membatalkan transaksi DPLK Manual peserta %s?' \
    % (uipT.no_peserta)):
    try:
      #reject transaksi, perlu script eksternal untuk menghapus transaksi
      dh = app.ExecuteScript('transaksi/AuthorizeTransaksi', \
        app.CreateValues(['jenisTransaksi', 'TransaksiDPLKManual'], \
        ['idtransaksi',uipT.ID_Transaksi], \
        ['mode','R']))
      #belum perlu untuk menampikan status keberhasilan script
    except:
      raise

    sender.OwnerForm.ResetAndClearData()

