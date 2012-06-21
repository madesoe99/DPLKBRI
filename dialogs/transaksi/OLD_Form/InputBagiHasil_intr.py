def SRRCalcAfterLookup(sender, linkui):
  form = sender.OwnerForm
  app = form.ClientApplication
  uipInput = form.GetUIPartByName('uipInput')
  
  y, m, d = uipInput.GetFieldValue('SRRCalc.tgl_akhir_hitung')[:3]
  uipInput.tgl_akhir_hitung = '%s/%s/%d' % (str(m).zfill(2), str(d).zfill(2), y)

def bOKClick(sender):
  app = sender.OwnerForm.ClientApplication
  uipInput = sender.OwnerForm.GetUIPartByName('uipInput')
  uipPI = sender.OwnerForm.GetUIPartByName('uipPaketInvestasi')
  
  #checking SRRCalc
  if uipInput.GetFieldValue('SRRCalc.ID_SRRCalc') in ['',None]:
    app.ShowMessage('SRR yang dipakai untuk bagi hasil masih kosong! Mohon dipilih dahulu.')
    return

  #checking batch transaksi
  if uipInput.GetFieldValue('BatchTransaksi.ID_TransactionBatch') in ['',None]:
    app.ShowMessage('Batch Transaksi masih kosong! Mohon dipilih dahulu.')
    return

  #preparing packet
  ph = app.CreatePacket()
  packet = ph.Packet
  packet.AddDataPacketStructureEx('__Info','idSRRCalc:integer;idBatch:integer;execFile:string;')
  packet.AddDataPacketStructureEx('__PaketInvestasi','kodePaket:string;kode_jns_investasi:string;laba:float;')
  packet.BuildAllStructure()

  dsInfo = packet.AddNewDataset('__Info')
  recInfo = dsInfo.AddRecord()
  recInfo.idSRRCalc = uipInput.GetFieldValue('SRRCalc.ID_SRRCalc')
  recInfo.idBatch = uipInput.GetFieldValue('BatchTransaksi.ID_TransactionBatch')
  #tambahan haris
  recInfo.execFile = 'transaksi/L_BagiHasil'
  
  dsPI = packet.AddNewDataset('__PaketInvestasi')
  uipPI.First()
  while not uipPI.Eof:
    recPI = dsPI.AddRecord()
    recPI.kodePaket =  uipPI.kode_paket_investasi
    recPI.kode_jns_investasi = uipPI.kode_jns_investasi
    recPI.laba = uipPI.NominalProfit
    uipPI.Next()

  try:
    if app.ConfirmDialog('Anda yakin akan melakukan penghitungan BAGI HASIL '\
      'untuk semua Peserta DPLK?'):
      
      #pid = app.ExecuteScriptTrackable('transaksi/L_BagiHasil', ph)        
      #app.ExecuteScript('transaksi/S_BagiHasil', ph)
      app.ExecuteScript('longscripts/ExecuteLongScript', ph)

      #pcConsole.ConsoleFilterName = 'BagiHasil_%d' % (pid)
      sender.Enabled = sender.Default = 0
      sender.OwnerForm.GetControlByName('pButton.bCancel').Caption = '&Tutup'
      sender.OwnerForm.GetControlByName('pButton.bCancel').Default = 1
  finally:
    app = None
