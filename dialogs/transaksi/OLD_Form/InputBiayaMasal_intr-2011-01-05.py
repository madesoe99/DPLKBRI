def zfill(s):
  #fungsi ini untuk menambahkan satu angka 0 pada string s
  #digunakan terutama untuk representasi penanggalan bagi hari / bulan
  #prekondisi: s haruslah literal string yang hanya berisi angka

  if len(s) == 1:
    s = '0' + s
  #selain berjumlah karakter sama dengan satu, tidak akan diutak-atik

  return s
#-----------------------------------------------------------------------

def FormShow(form, parameter):
  uipInput = form.GetUIPartByName('uipInput')

  uipInput.Edit()
  uipInput.Code = parameter.FirstRecord.code

  if uipInput.Code == 130:
    #Biaya Administrasi Transaksi (Tahunan)
    form.Caption = form.Caption + ' Administrasi (Tahunan)'
  elif uipInput.Code == 131:
    #Biaya Pengelolaan Dana (Tahunan)
    form.Caption = form.Caption + ' Pengelolaan Dana (Tahunan)'

def TB_BeforeLookup(sender, linkui):
  uipI = sender.OwnerForm.GetUIPartByName('uipInput')

  #define modified tanggal hitung, untuk OQL: mm/dd/yyyy
  y,m,d = uipI.TanggalHitung[:3]
  sDate = '%s/%s/%d' % (zfill(str(m)), zfill(str(d)),y)

  uipI.Edit()
  uipI.ModifiedTanggalHitung = sDate

  return 1

def bOKClick(sender):
  app = sender.OwnerForm.ClientApplication
  uipInput = sender.OwnerForm.GetUIPartByName('uipInput')
  
  #checking tanggal penghitungan
  if uipInput.TanggalHitung in ['',None]:
    app.ShowMessage('Tanggal Penghitungan masih kosong! Mohon diisi dahulu.')
    return

  #checking batch transaksi
  if uipInput.GetFieldValue('LTransactionBatch.ID_TransactionBatch') in [None,'']:
    app.ShowMessage('Batch Transaksi belum dipilih! Mohon dipilih dahulu.')
    return

  if uipInput.Code == 130:
    #Biaya Administrasi Transaksi (Tahunan)
    codeBiaya = 1
    namaBiaya = 'Biaya Administrasi Tahunan'
  elif uipInput.Code == 131:
    #Biaya Pengelolaan Dana (Tahunan)
    codeBiaya = 2
    namaBiaya = 'Biaya Pengelolaan Dana'
  #elif yang lainnya...
  
  try:
    if app.ConfirmDialog('Anda yakin akan melakukan pengenaan %s \nkepada semua '\
      'Peserta DPLK?' % (namaBiaya)):

      #pid = app.ExecuteScriptTrackable('transaksi/L_BiayaTahunan', \
      param =  app.CreateValues(['code',codeBiaya],
        ['tglhitung',uipInput.TanggalHitung],
        ['idbatch',uipInput.GetFieldValue('LTransactionBatch.ID_TransactionBatch')],
        [execFile,'transaksi/L_BiayaTahunan'])
        
      app.ExecuteScript('longscripts/ExecuteLongScript', param)
      #pcConsole.ConsoleFilterName = namaBiaya + '_' + str(pid)
      sender.Enabled = sender.Default = 0
      sender.OwnerForm.GetControlByName('pButton.bCancel').Caption = '&Tutup'
      sender.OwnerForm.GetControlByName('pButton.bCancel').Default = 1
  finally:
    app = None
