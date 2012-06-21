def FormShow(form, parameter):
  uipInput = form.GetUIPartByName('uipInput')
  uipUI = form.GetUIPartByName('uipUserInfo')

  uipInput.Edit()
  uipInput.Code = parameter.FirstRecord.code
  uipInput.SetFieldValue('LPeserta.no_peserta','')
  
  #nilai untuk inisialisasi jenis transaksi bukan teller
  uipInput.BatchType = 'T'
  uipInput.BatchSubType = 'M'
  uipInput.AccountLinkType = 'S'
  uipInput.isNotNeedTanggalPakai = 0

  if uipInput.Code == 20:
    #View detil Batch Transaksi, disable no peserta dan hidden it
    form.GetControlByName('pInput.LPeserta').Enabled = 0
    form.GetControlByName('pInput.LPeserta').Visible = 0
    uipInput.isNeedType = 0
    uipInput.isNotNeedTanggalPakai = 0
    uipInput.isOpenOnly = 0
    uipInput.BatchType = ''
    uipInput.BatchSubType = ''
    form.Caption = 'Input Untuk Lihat Detil Batch Transaksi'
  elif uipInput.Code in [10,310]:
    #Pengalihan ke DPLK lain, set batch type dan batch sub type
    form.Caption = 'Input Untuk Pengalihan ke DPLK Lain'
  elif uipInput.Code in [11,311]:
    #Pengalihan dari DPLK lain, set batch type dan batch sub type
    form.Caption = 'Input Untuk Pengalihan dari DPLK Lain'
  elif uipInput.Code in [12,312]:
    #Pengalihan dari DPPK lain, set batch type dan batch sub type
    form.Caption = 'Input Untuk Pengalihan dari DPPK Lain'
  elif uipInput.Code in [13,313]:
    #Pengalihan dari DPK lain, set batch type dan batch sub type
    form.Caption = 'Input Untuk Pengalihan dari DPK Lain'
  elif uipInput.Code in [60,360]:
    #Pengalihan ke DPLK lain, set batch type dan batch sub type
    form.Caption = 'Input Untuk Penarikan Dana 30%'
  elif uipInput.Code in [61,361]:
    #Pengalihan dari DPLK lain, set batch type dan batch sub type
    form.Caption = 'Input Untuk Penarikan Dana PHK'
  elif uipInput.Code in [70,370]:
    #Pembayaran iuran peserta, set batch type dan batch sub type
    if uipUI.isTeller:
      uipInput.BatchSubType = 'T'
      form.Caption = 'Pembayaran Iuran Peserta (Lewat Teller)'
    else:
      form.Caption = 'Pembayaran Iuran Peserta (Manual)'
  elif uipInput.Code in [80,380]:
    #Pengambilan manfaat pensiun, set batch type dan batch sub type
    form.Caption = 'Input Untuk Pengambilan Manfaat Pensiun'
  elif uipInput.Code in [100,3100]:
    #Input Transaksi DPLK Manual, set batch type dan batch sub type
    form.Caption = 'Input Transaksi DPLK Manual'
    uipInput.AccountLinkType = 'C'
    uipInput.isManualTransaction = 1
  elif uipInput.Code in [110,3110]:
    #Input Iuran Pendaftaran Manual, set batch type dan batch sub type
    uipInput.BatchType = 'R'
    uipInput.AccountLinkType = 'C'
    uipInput.isManualTransaction = 1
    form.Caption = 'Input Iuran Pendaftaran Manual'
  elif uipInput.Code in [120,3120]:
    #Input Titipan Premi, set batch type dan batch sub type
    uipInput.BatchType = 'P'
    form.Caption = 'Input Titipan Premi'
  elif uipInput.Code in [121,3121]:
    #Input Transaksi Premi Manual, set batch type dan batch sub type
    form.GetControlByName('pInput.LPeserta').Enabled = 0
    form.GetControlByName('pInput.LPeserta').Visible = 0
    uipInput.BatchType = 'P'
    uipInput.AccountLinkType = 'C'
    uipInput.isManualTransaction = 1
    form.Caption = 'Input Transaksi Premi Manual'

  #penanganan khusus untuk TELLER
  if uipUI.isTeller and uipInput.isNeedType:
    #cari batch yang bersesuaian
    uipBD = form.GetUIPartByName('uipBatchDefined')
    found = 0

    uipBD.First()
    while (not uipBD.Eof) and (not found):
      if uipBD.batch_type == uipInput.BatchType:
        #batch yang bersesuaian ketemu, langsung assign batch transaksi
        uipInput.SetFieldValue('LTransactionBatch.ID_TransactionBatch',uipBD.ID_TransactionBatch)
        uipInput.SetFieldValue('LTransactionBatch.no_batch',uipBD.no_batch)
        uipInput.SetFieldValue('LTransactionBatch.batch_type',uipInput.BatchType)
        uipInput.SetFieldValue('LTransactionBatch.batch_sub_type',uipInput.BatchSubType)
        uipInput.SetFieldValue('LTransactionBatch.branch_code',uipBD.branch_code)
        uipInput.SetFieldValue('LTransactionBatch.tgl_used',uipBD.tgl_used)

        found = 1
      else:
        uipBD.Next()
    
    if not found:
      #batch yang bersesuaian tidak ketemu
      raise 'Error','\nBatch yang sesuai untuk transaksi tidak ditemukan!'

    #matikan lookup batch transaksi
    form.GetControlByName('pInput.LTransactionBatch').Enabled = 0

  #handling khusus untuk InputSingle berasal ViewBatchDetail
  if uipInput.Code in [310,311,312,313,360,361,370,380,3100,3110,3120,3121]:
    uipInput.SetFieldValue('LTransactionBatch.ID_TransactionBatch',parameter.FirstRecord.idbatch)
    uipInput.SetFieldValue('LTransactionBatch.no_batch',parameter.FirstRecord.nobatch)
    uipInput.SetFieldValue('LTransactionBatch.batch_type',uipInput.BatchType)
    uipInput.SetFieldValue('LTransactionBatch.batch_sub_type',uipInput.BatchSubType)
    uipInput.SetFieldValue('LTransactionBatch.branch_code',parameter.FirstRecord.branchcode)
    uipInput.SetFieldValue('LTransactionBatch.tgl_used',parameter.FirstRecord.tglpakai)

    #matikan lookup batch transaksi
    form.GetControlByName('pInput.LTransactionBatch').Enabled = 0
    
def TB_BeforeLookup(sender, linkui):
  uipUI = sender.OwnerForm.GetUIPartByName('uipUserInfo')
  
  sRestriksiSU = ''
  #constructing Transaction Batch OQL Text
  if uipUI.isBackOffice:
    #buat another SuperUser OQL Restriction
    uipSU = sender.OwnerForm.GetUIPartByName('uipSuperUser')
    
    uipSU.First()
    while not uipSU.Eof:
      sRestriksiSU += 'user_id_owner <> \'%s\'' % (uipSU.UserID)
      uipSU.Next()
      if not uipSU.Eof:
        sRestriksiSU += ' and '
    #tambahkan 'and' di depan
    sRestriksiSU = ' and ' + sRestriksiSU
        
  #the Transaction Batch OQL constructing
  uipInput = sender.OwnerForm.GetUIPartByName('uipInput')
  #sender.OwnerForm.ShowMessage('isNotNeedTanggalPakai=' + str(uipInput.isNotNeedTanggalPakai))
  oqltext = 'select from TransactionBatch '\
    '[(0 = :isTeller or user_id_owner = :UserIDOwner) and '\
    '(0 = :isBackOffice or user_id_owner = :UserIDOwner) and '\
    '(0 = :isBackOfficeCabang or branch_code = :BranchCode) and '\
    '(0 = :isNeedType or batch_type = :BatchType) and '\
    '(0 = :isNeedType or batch_sub_type = :BatchSubType) and '\
    '(0 = :isNotNeedTanggalPakai or tgl_used = :TanggalPakai) and '\
    '(0 = :isManualTransaction or account_link_type = :AccountLinkType) and '\
    '(0 = :isOpenOnly or batch_status = \'O\') %s] '\
    '(no_batch, tgl_create, tgl_used, batch_type$, batch_sub_type$, account_link_type$, '\
    'branch_code, ID_TransactionBatch, self) then order by desc tgl_used;'\
    % (sRestriksiSU)
    
  linkui.OQLText = oqltext
    
  return 1
    
def bOKClick(sender):
  app = sender.OwnerForm.ClientApplication
  uipInput = sender.OwnerForm.GetUIPartByName('uipInput')
  uipUI = sender.OwnerForm.GetUIPartByName('uipUserInfo')
  NoPeserta = uipInput.GetFieldValue('LPeserta.no_peserta')

  #checking teller timezone
  if uipUI.isTeller:
    dhUTZ = app.ExecuteScript('transaksi\CekUserTimeZone', \
      app.CreateValues(['userid', uipUI.UserIDOwner]))
    if not dhUTZ.FirstRecord.allowtransaction:
      app.ShowMessage('PERINGATAN!\n\nWaktu resmi aktivitas banking telah selesai. '\
        'Tidak diperbolehkan melakukan transaksi.\nHubungi Administrator jika masih ada transaksi yang akan dilakukan.')
      return

  #checking batch transaksi
  if uipInput.GetFieldValue('LTransactionBatch.ID_TransactionBatch') == None or \
    uipInput.GetFieldValue('LTransactionBatch.ID_TransactionBatch') == '':
    app.ShowMessage('Batch Transaksi belum dipilih! Mohon dipilih dahulu.')
    return

  #checking nomor peserta dan status aktif/non aktif rekeningnya
  if uipInput.Code not in [20,121,3121] and (NoPeserta == None or \
    NoPeserta == ''):
    app.ShowMessage('Nomor Peserta masih kosong! Mohon diisi terlebih dahulu.')
    return
  else:
    #selain View Batch Detail
    if uipInput.Code not in [20,121,3121]:
      #no peserta terisi, cek kebenaran no peserta pake script
      dh = app.ExecuteScript('transaksi\CekPesertaDPLK', \
        app.CreateValues(['nopeserta', NoPeserta]))
      #konvensi status nomor peserta
      # 0 nomor peserta tidak ada
      # 1 nomor peserta ada, rekening Aktif
      # 2 nomor peserta ada, rekening Non Aktif
      # 3 nomor peserta ada, rekening Suspend
      # 4 nomor peserta ada, peserta belum melunasi biaya pendaftaran
      # 5 peserta sudah memasuki masa pensiun, tidak bisa iuran dan nitip premi lagi
      if not dh.FirstRecord.status:
        app.ShowMessage('PERINGATAN!\n\nData Peserta tidak ditemukan! Mohon cek '\
          'Nomor Peserta kembali.')
        return
      elif dh.FirstRecord.status == 2:
        app.ShowMessage('PERINGATAN!\n\nRekening Peserta telah Non Aktif! Semua '\
          'transaksi akan ditolak.')
        return
      elif dh.FirstRecord.status == 3:
        app.ShowMessage('PERINGATAN!\n\nRekening Peserta berstatus Suspend! Mohon '\
          'cek Rekening Peserta kembali.')
        return
      elif dh.FirstRecord.status == 4 and uipInput.Code not in [110,3110]:
        app.ShowMessage('PERINGATAN!\n\nBiaya Pendaftaran Peserta belum lunas! '\
          'Mohon lunasi terlebih dahulu.')
        return
      elif dh.FirstRecord.status == 5 and uipInput.Code in [70,370]:
        app.ShowMessage('PERINGATAN!\n\nPeserta sudah memasuki usia pensiun! '\
          'Tidak diperkenankan lagi melakukan iuran peserta ataupun titipan premi')
        return
      elif dh.FirstRecord.status == 6 and uipInput.Code in [60,360]:
        app.ShowMessage('PERINGATAN!\n\nPeserta tidak diperkenankan menarik dana (by regulasi korporat)!')
        return
        
      elif dh.FirstRecord.status == 7 and uipInput.Code in [60,360]:
        app.ShowMessage('PERINGATAN!\n\nPeserta hanya diperkenankan menarik dana jika persyaratan berikut terpenuhi :\n%s' % dh.FirstRecord.persyaratan or '')
        return
                
      if dh.FirstRecord.nbOfTrans:
        # nbOfTrans > 0
        # ada transaksi peserta tersebut yang belum diotorisasi
        confMsg = 'Terdapat %d transaksi peserta %s yang belum diotorisasi.\nLanjutkan?' % (dh.FirstRecord.nbOfTrans, NoPeserta)
        if not app.ConfirmDialog(confMsg):
          return

  group_id = 'transaksi'
  if uipInput.Code in [10,11,12,13,60,61,70,80,100,110,120,310,311,312,313,360,\
    361,370,380,3100,3110,3120]:
    #KHUSUS TRANSAKSI YANG MELIBATKAN NOMOR PESERTA/NASABAH
    #input manual, pengalihan dana DPLK, penarikan dana dan pengambilan manfaat
    if uipInput.Code in [10,310]:
      #pengalihan dana ke DPLK lain
      form_id = 'PengalihanKeDPLK'
    elif uipInput.Code in [11,311]:
      #pengalihan dana dari DPLK lain
      form_id = 'PengalihanDariDPLK'
    elif uipInput.Code in [12,312]:
      #pengalihan dana dari DPPK lain
      form_id = 'PengalihanDariDPPK'
    elif uipInput.Code in [13,313]:
      #pengalihan dana dari DPK lain
      form_id = 'PengalihanDariDPK'
    elif uipInput.Code in [60,360]:
      #penarikan dana 30%
      form_id = 'PenarikanDana30'
    elif uipInput.Code in [61,361]:
      #penarikan dana PHK
      form_id = 'PenarikanDanaPHK'
    elif uipInput.Code in [70,370]:
      #pembayaran iuran peserta
      form_id = 'fNewIuranPremiNasabah'
    elif uipInput.Code in [80,380]:
      #pengambilan manfaat pensiun
      form_id = 'PengambilanManfaat'
    elif uipInput.Code in [100,3100]:
      #input transaksi DPLK manual
      form_id = 'fNewTransaksiDPLKManual'
    elif uipInput.Code in [110,3110]:
      #input iuran pendaftaran manual
      form_id = 'fNewIuranPendaftaranManual'
    elif uipInput.Code in [120,3120]:
      #input titipan premi
      form_id = 'fNewInputTitipanPremi'

    key = 'PObj:NasabahDPLK#no_peserta=' + NoPeserta
    uipName = 'uipNasabah'
  elif uipInput.Code == 20:
    #KHUSUS NON TRANSAKSI
    #view detil batch transaksi
    form_id = 'fViewBatchDetail'
    key = 'PObj:TransactionBatch#ID_TransactionBatch=' + \
      str(uipInput.GetFieldValue('LTransactionBatch.ID_TransactionBatch'))
    uipName = 'uipTransactionBatch'
    
    #set parameter NoPeserta bernilai InputSingle, menandakan input dari form InputSingle
    uipInput.Edit()
    uipInput.SetFieldValue('LPeserta.no_peserta','InputSingle')
  elif uipInput.Code in [121,3121]:
    #KHUSUS TRANSAKSI PREMI MANUAL (TANPA NOMOR PESERTA/NASABAH)
    #input transaksi premi manual
    form_id = 'fNewTransaksiPremiManual'
    key = 'x'
    uipName = 'x'

    #set parameter NoPeserta bernilai InputSingle, menandakan input dari form InputSingle
    uipInput.Edit()
    uipInput.SetFieldValue('LPeserta.no_peserta','InputSingle')
  #elif yang lainnya...

  try:
    oform = app.GetFormWithData(group_id+'/'+form_id, form_id, 0, key, uipName)
    oform.Show(app.CreateValues(['nopeserta', NoPeserta or ''], \
      ['idbatch',uipInput.GetFieldValue('LTransactionBatch.ID_TransactionBatch')], \
      ['nobatch',uipInput.GetFieldValue('LTransactionBatch.no_batch')], \
      ['branchcode',uipInput.GetFieldValue('LTransactionBatch.branch_code')], \
      ['tglpakai',uipInput.GetFieldValue('LTransactionBatch.tgl_used')]))

    #clean it and exit form
    sender.OwnerForm.ResetAndClearData()
    sender.ExitAction = 1
  finally:
    oform = None
    app = None

