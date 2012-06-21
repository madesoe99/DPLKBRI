def FormShow(form, parameter):
  uipInput = form.GetUIPartByName('uipInput')
  if uipInput.TanggalAwal not in ['',None]:
    #sudah pernah menghitung SRR sebelumnya
    form.GetControlByName('pInput.TanggalAwal').Enabled = 1

def bOKClick(sender):
  app = sender.OwnerForm.ClientApplication
  uipInput = sender.OwnerForm.GetUIPartByName('uipInput')
  
  #checking rentang tanggal penghitungan SRR
  if uipInput.TanggalAkhir[:3] > uipInput.TanggalHariIni[:3]:
    app.ShowMessage('Tanggal Akhir tidak boleh melebihi '\
      'tanggal hari ini, %d-%d-%d.' % (uipInput.TanggalHariIni[2],\
      uipInput.TanggalHariIni[1],uipInput.TanggalHariIni[0]))
    return
  elif uipInput.TanggalAwal in [None,'']:
    app.ShowMessage('Tanggal Awal masih kosong. Mohon diisi dahulu.')
    return
  elif uipInput.TanggalAwal[:3] >= uipInput.TanggalAkhir[:3]:
    app.ShowMessage('Rentang tanggal penghitungan salah. Mohon dibetulkan.')
    return

  try:
    if app.ConfirmDialog('Anda yakin akan melakukan penghitungan SALDO RATA-RATA '\
      '\nsampai tanggal %d-%d-%d untuk semua Peserta DPLK ?' % (uipInput.TanggalAkhir[2],\
      uipInput.TanggalAkhir[1],uipInput.TanggalAkhir[0])):
      
      #checking all before long script calculation
      dh = app.ExecuteScript('transaksi/CekBeforeHitungSRR', \
        app.CreateValues(['tglhitung',uipInput.TanggalAkhir]))
      if dh.FirstRecord.openbatch != 0:
        app.ShowMessage('PERINGATAN!\n\nMasih terdapat %d Batch Transaksi yang belum ditutup! '\
          'Penghitungan SRR akan dilakukan jika semua Batch Transaksi hingga tanggal %s '\
          'sudah ditutup. Mohon tutup terlebih dahulu Batch Transaksi yang masih terbuka '\
          'di Daftar Batch.' % (dh.FirstRecord.openbatch,\
          '%d-%d-%d' % (uipInput.TanggalAkhir[2],uipInput.TanggalAkhir[1],\
          uipInput.TanggalAkhir[0])))
        sender.Enabled = sender.Default = 0
        sender.OwnerForm.GetControlByName('pButton.bCancel').Default = 1
        return

      #code 0, berarti untuk simulasi only, not necessary to save in DB
      #code 1, berarti untuk hasil perhitungan disimpan dalam DB
      #pid = app.ExecuteScriptTrackable('transaksi/L_HitungSRR', \
      param =   app.CreateValues(['code',1],['tglawal',uipInput.TanggalAwal],
        ['tglakhir',uipInput.TanggalAkhir],
        ['execFile','transaksi/L_HitungSRR'])
      app.ExecuteScript('longscripts/ExecuteLongScript', param)

      #pcConsole.ConsoleFilterName = 'HitungSRR_' + str(pid)
      sender.Enabled = sender.Default = 0
      sender.OwnerForm.GetControlByName('pButton.bCancel').Caption = '&Tutup'
      sender.OwnerForm.GetControlByName('pButton.bCancel').Default = 1
  finally:
    app = None
