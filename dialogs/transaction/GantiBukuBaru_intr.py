def FormShow(form, parameter):
  uipInput = form.GetUIPartByName('uipInput')

  #uipInput.Edit()
  #uipInput.Code = parameter.FirstRecord.code

  #if uipInput.Code in [5000] :
    #Lihat detil data nasabah / rekening
  #  form.Caption = 'Input untuk Lihat Detil Data Peserta'

def bOKClick(sender):
  app = sender.OwnerForm.ClientApplication
  uipInput = sender.OwnerForm.GetUIPartByName('uipInput')
  NoPeserta = uipInput.GetFieldValue('LPeserta.no_peserta')
  NoRekening = uipInput.GetFieldValue('LRekInvDPLK.no_rekening')
  NomorBuku = uipInput.GetFieldValue('nomor_buku')
  
  #checking nomor peserta dan status aktif/non aktif rekeningnya
  if NoPeserta in [None,'']:
    app.ShowMessage('Nomor Peserta masih kosong! Mohon diisi terlebih dahulu.')
    return
  else:
    #no peserta terisi, cek kebenaran no peserta pake script
    dh = app.ExecuteScript('transaksi\CekPesertaDPLK', \
      app.CreateValues(['nopeserta', NoPeserta]))

    if not dh.FirstRecord.status:
      app.ShowMessage('PERINGATAN!\n\nData Peserta tidak ditemukan! Mohon cek Nomor Peserta kembali.')
      return
    elif dh.FirstRecord.status == 2:
      app.ShowMessage('PEMBERITAHUAN:\n\nRekening Peserta telah Non Aktif.')
    elif dh.FirstRecord.status == 3:
      app.ShowMessage('PEMBERITAHUAN:\n\nRekening Peserta berstatus Suspend.')

  if NomorBuku in [None,'']:
    app.ShowMessage('Nomor Buku DPLK masih kosong.')
    return
  ### Sementara ditutup By ade herman 2011-11-21
  #else:
  #  dh = app.ExecuteScript('transaksi\CekMasterBukuDPLK', \
  #   app.CreateValues(['nobuku',NomorBuku]))

  #  if not dh.FirstRecord.status:
  #    app.ShowMessage('PERINGATAN!\n\nNomor Buku DPLK Tidak Terdaftar.')
  #    return
  ### end

  try:
    #oform = app.GetFormWithData(group_id+'/'+form_id, form_id, 0, key, uipName)
    #oform.Show(app.CreateValues(['nopeserta',NoPeserta]))

    if app.ConfirmDialog('Anda yakin akan menyimpan Nomor Buku DPLK %s\n'\
      'ke Nomor DPLK %s (Nomor Peserta: %s)?' % (NomorBuku,NoRekening,NoPeserta)):
      dh = app.ExecuteScript('transaksi/CekGantiBukuBaruDPLK', \
        app.CreateValues(['nopeserta',NoPeserta],['norekening',NoRekening],['nobuku',NomorBuku]))
        

    #clean it and exit form
    sender.OwnerForm.ResetAndClearData()
    sender.ExitAction = 1
  finally:
    oform = None
    app = None
