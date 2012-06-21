def FormShow(form, parameter):
  uipT = form.GetUIPartByName('uipTransaksi')
  
  #cek kode_jenis_transaksi, untuk dapetin I,O,P
  #jenis pengalihan dari: DPLK, DPPK, DPK
  if uipT.kode_jenis_transaksi == 'I':
    #pengalihan dari DPLK lain
    addCaption = 'DPLK Lain'
    form.GetControlByName('pDataTransaksi.saldo_iuran_pk').Visible = 0
    form.GetControlByName('pDataTransaksi.saldo_iuran_pst').ControlCaption = \
      'akumulasi iuran'
  elif uipT.kode_jenis_transaksi == 'O':
    #pengalihan dari DPPK lain
    addCaption = 'DPPK Lain'
  elif uipT.kode_jenis_transaksi == 'P':
    #pengalihan dari DPK lain
    addCaption = 'DPK Lain'
    form.GetControlByName('pDataTransaksi.no_dplk_lain').Visible = 0
    
  form.Caption = form.Caption + addCaption

  #cek code number tag parameter
  if parameter.FirstRecord.code in [2000,3000]:
    #mode view, disable button Approve dan Reject
    form.GetControlByName('pButton.bApprove').Enabled = 0
    form.GetControlByName('pButton.bApprove').Default = 0
    form.GetControlByName('pButton.bReject').Enabled = 0
    form.GetControlByName('pButton.bCancel').Caption = '&Tutup'
    form.GetControlByName('pButton.bCancel').Default = 1
    form.Caption = 'Lihat Detil Pengalihan Dana Dari ' + addCaption

def bRejectClick(sender):
  app = sender.OwnerForm.ClientApplication
  uipT = sender.OwnerForm.GetUIPartByName('uipTransaksi')

  if app.ConfirmDialog('Anda yakin membatalkan transaksi Pengalihan Dana dari DP lain peserta %s?' \
    % (uipT.no_peserta)):
    try:
      #reject transaksi, perlu script eksternal untuk menghapus transaksi
      dh = app.ExecuteScript('transaksi/AuthorizeTransaksi', \
        app.CreateValues(['jenisTransaksi', 'PengalihanDariDPLKLain'], \
        ['idtransaksi',uipT.ID_Transaksi], \
        ['mode','R']))
      #belum perlu untuk menampikan status keberhasilan script
    except:
      raise

    sender.OwnerForm.ResetAndClearData()
