def FormShow(form, parameter):
  uipInput = form.GetUIPartByName('uipInput')

  #uipInput.Edit()
  #uipInput.Code = parameter.FirstRecord.code

  #if uipInput.Code in [5000] :
    #Lihat detil data nasabah / rekening
  #  form.Caption = 'Input untuk Lihat Detil Data Peserta'

def bSimpanClick(sender):
  app = sender.OwnerForm.ClientApplication
  uipInput = sender.OwnerForm.GetUIPartByName('uipInput')
  NoPeserta = uipInput.GetFieldValue('LPeserta.no_peserta')
  Keterangan = uipInput.GetFieldValue('keterangan')
  
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

  if Keterangan in [None,'']:
    app.ShowMessage('Keterangan masih belum diisi.')
    return

  try:
    #oform = app.GetFormWithData(group_id+'/'+form_id, form_id, 0, key, uipName)
    #oform.Show(app.CreateValues(['nopeserta',NoPeserta]))

    if app.ConfirmDialog('Anda yakin akan menyimpan informasi pendingan alkhairat dengan  '\
      'Nomor DPLK %s?' % (NoPeserta)):
      dh = app.ExecuteScript('transaksi/SimpanPendingAlkhairat', \
        app.CreateValues(['nopeserta',NoPeserta],['keterangan',Keterangan]))
        
    #clean it and exit form
    sender.OwnerForm.ResetAndClearData()
    sender.ExitAction = 1
  finally:
    oform = None
    app = None
