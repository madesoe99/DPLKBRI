def FormShow(form, parameter):
  uipInput = form.GetUIPartByName('uipInput')

  uipInput.Edit()
  uipInput.Code = parameter.FirstRecord.code

  if uipInput.Code in [5000] :
    #Lihat detil data nasabah / rekening
    form.Caption = 'Input untuk Lihat Detil Data Peserta'

def bOKClick(sender):
  app = sender.OwnerForm.ClientApplication
  uipInput = sender.OwnerForm.GetUIPartByName('uipInput')
  NoPeserta = uipInput.GetFieldValue('LPeserta.no_peserta')
  
  #checking nomor peserta dan status aktif/non aktif rekeningnya
  if NoPeserta in [None,'']:
    app.ShowMessage('Nomor Peserta masih kosong! Mohon diisi terlebih dahulu.')
    return
  else:
    #no peserta terisi, cek kebenaran no peserta pake script
    '''
    dh = app.ExecuteScript('transaksi\CekPesertaDPLK', \
      app.CreateValues(['nopeserta', NoPeserta]))
    '''
    #konvensi status nomor peserta
    # 0 nomor peserta tidak ada
    # 1 nomor peserta ada, rekening Aktif
    # 2 nomor peserta ada, rekening Non Aktif
    # 3 nomor peserta ada, rekening Suspend
    # 4 nomor peserta ada, peserta belum melunasi biaya pendaftaran
    
    '''
    if not dh.FirstRecord.status:
      app.ShowMessage('PERINGATAN!\n\nData Peserta tidak ditemukan! Mohon cek Nomor Peserta kembali.')
      return
    elif dh.FirstRecord.status == 2:
      app.ShowMessage('PEMBERITAHUAN:\n\nRekening Peserta telah Non Aktif.')
    elif dh.FirstRecord.status == 3:
      app.ShowMessage('PEMBERITAHUAN:\n\nRekening Peserta berstatus Suspend.')
    elif dh.FirstRecord.status == 4:
      app.ShowMessage('PEMBERITAHUAN:\n\nBiaya Pendaftaran Peserta belum lunas.')
    '''

  group_id = 'transaction'
  if uipInput.Code in [5000]:
    #lihat detil Peserta / Rekening

    form_id = 'fNasabahRekening'
    key = 'PObj:NasabahDPLK#no_peserta=' + NoPeserta
    uipName = 'uipNasabahDPLK'
  #elif yang lainnya...
  
  try:
    ph = app.CreateValues(['key', key])
    oform = app.CreateForm(group_id+'/'+form_id, form_id, 0, ph, None)
    oform.Show(app.CreateValues(['nopeserta',NoPeserta]))

    #clean it and exit form
    sender.OwnerForm.ResetAndClearData()
    sender.ExitAction = 1
  finally:
    oform = None
    app = None
