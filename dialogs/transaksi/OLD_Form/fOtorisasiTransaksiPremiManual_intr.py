def FormShow(form, parameter):

  #cek code number tag parameter
  if parameter.FirstRecord.code in [2000,3000]:
    #mode view, disable button Approve dan Reject
    form.GetControlByName('pButton.bApprove').Enabled = 0
    form.GetControlByName('pButton.bApprove').Default = 0
    form.GetControlByName('pButton.bReject').Enabled = 0
    form.GetControlByName('pButton.bCancel').Caption = '&Tutup'
    form.GetControlByName('pButton.bCancel').Default = 1
    form.Caption = 'Lihat Detil Transaksi Premi Manual'

def bRejectClick(sender):
  app = sender.OwnerForm.ClientApplication
  uipT = sender.OwnerForm.GetUIPartByName('uipTransaksi')

  if app.ConfirmDialog('Anda yakin membatalkan transaksi Premi Manual?'):
    try:
      #reject transaksi, perlu script eksternal untuk menghapus transaksi
      dh = app.ExecuteScript('transaksi/AuthorizeTransaksi', \
        app.CreateValues(['jenisTransaksi', 'TransaksiPremiManual'], \
        ['idtransaksi',uipT.ID_Transaksi], \
        ['mode','R']))
      #belum perlu untuk menampikan status keberhasilan script
    except:
      raise

    sender.OwnerForm.ResetAndClearData()
