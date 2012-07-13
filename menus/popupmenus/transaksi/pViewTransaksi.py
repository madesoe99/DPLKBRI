def GetFormInfoByJnsTransCode(kode_jenis_trinvestasi, clsfTransaksiInvestasi):
  if kode_jenis_trinvestasi == 'A':
    return ['fAlokInvTambahan','TransPiutangInvestasi','uipTransPiutangInvestasi']
  elif kode_jenis_trinvestasi == 'B':
    return ['fPendapatanInvestasiTunai','TransLRInvestasi','uipTransLRInvestasi']
  elif kode_jenis_trinvestasi == 'P':

    if clsfTransaksiInvestasi == 'C':
      return ['fPendapatanInvestasiPiutang','TransLRInvestasi','uipTransLRInvestasi']
    else:
      # piutang lr investasi
      return ['fPendapatanInvestasiPiutang_PiutLR','TransPiutangLRInvestasi','uipTransPiutangLRInvestasi']

  elif kode_jenis_trinvestasi == 'C':

    if clsfTransaksiInvestasi == 'A':
      return ['fTutupDeposito','TutupDeposito','uipTutupDeposito']
    else:
      # piutang lr investasi
      return ['fTutupDeposito_PiutLR','TransPiutangLRInvestasi','uipTransPiutangLRInvestasi']

  elif kode_jenis_trinvestasi == 'D':
    return ['fBiayaInvestasi','TransLRInvestasi','uipTransLRInvestasi']

  elif kode_jenis_trinvestasi == 'E':

    if clsfTransaksiInvestasi == 'C':
      return ['fBagiHasilDeposito','BagiHasilDeposito','uipBagiHasilDeposito']
    else:
      # piutang lr investasi
      return ['fBagiHasilDeposito_PiutLR','TransPiutangLRInvestasi','uipTransPiutangLRInvestasi']

  elif kode_jenis_trinvestasi == 'F':

    if clsfTransaksiInvestasi == 'A':
      return ['fRolloverInvestasi','RolloverDeposito','uipRolloverDeposito']
    else:
      # piutang lr investasi
      return ['fRolloverInvestasi_PiutLR','TransPiutangLRInvestasi','uipTransPiutangLRInvestasi']

  elif kode_jenis_trinvestasi == 'O':

    if clsfTransaksiInvestasi == 'A':
      return ['fBeliObligasi','BeliObligasi','uipBeliObligasi']
    else:
      # piutang lr investasi
      return ['fPendapatanObligasi','PendapatanObligasi','uipPendapatanObligasi']

  elif kode_jenis_trinvestasi == 'K':
    return ['fPendapatanObligasi','PendapatanObligasi','uipPendapatanObligasi']

  elif kode_jenis_trinvestasi == 'J':
    if clsfTransaksiInvestasi == 'A':
      return ['fJualObligasi','JualObligasi','uipJualObligasi']
    else:
      # piutang lr investasi
      return ['fPendapatanObligasi','PendapatanObligasi','uipPendapatanObligasi']

  elif kode_jenis_trinvestasi == 'S':
    return ['fSubscribeReksadana','SubscribeReksadana','uipSubscribeReksadana']

  elif kode_jenis_trinvestasi == 'R':

    if clsfTransaksiInvestasi == 'A':
      return ['fRedemptionReksadana','RedemptReksadana','uipRedemptionReksadana']
    else:
      # lr investasi
      return ['fPendapatanReksadana','PendapatanReksadana','uipPendapatanReksadana']

  elif kode_jenis_trinvestasi == 'L':

    if clsfTransaksiInvestasi == 'C':
      return ['fBagiHasilReksadana','BagiHasilReksadana','uipBagiHasilReksadana']
    else:
      # piutang investasi
      return ['fBagiHasilReksadana_PiutInv','TransPiutangInvestasi','uipTransPiutangInvestasi']

  elif kode_jenis_trinvestasi == 'U':
    return ['fRealisasiReturn', 'RealisasiReturn', 'uipRealisasiReturn']

  elif kode_jenis_trinvestasi == 'G':

    if clsfTransaksiInvestasi == 'A':
      return ['fManInvestasi','TransPiutangInvestasi','uipTransPiutangInvestasi']
    elif clsfTransaksiInvestasi == 'B':
      return ['fManPiutangLRInvestasi','TransPiutangLRInvestasi','uipTransPiutangLRInvestasi']
    else:
      return ['fManLRInvestasi','TransLRInvestasi','uipTransLRInvestasi']

  elif kode_jenis_trinvestasi == 'H':

    if clsfTransaksiInvestasi == 'A':
      return ['fManInvestasi','TransPiutangInvestasi','uipTransPiutangInvestasi']
    elif clsfTransaksiInvestasi == 'B':
      return ['fManPiutangLRInvestasi','TransPiutangLRInvestasi','uipTransPiutangLRInvestasi']
    else:
      return ['fManLRInvestasi','TransLRInvestasi','uipTransLRInvestasi']

  elif kode_jenis_trinvestasi == 'I':

    if clsfTransaksiInvestasi == 'A':
      return ['fManInvestasi','TransPiutangInvestasi','uipTransPiutangInvestasi']
    elif clsfTransaksiInvestasi == 'B':
      return ['fManPiutangLRInvestasi','TransPiutangLRInvestasi','uipTransPiutangLRInvestasi']
    else:
      return ['fManLRInvestasi','TransLRInvestasi','uipTransLRInvestasi']

  else:
    raise Exception, 'PERINGATAN' + 'Kode jenis transaksi investasi tidak dikenali / belum terdefinisi.'

def mnuCetakAdvisClick(sender, context):
  app = context.OwnerForm.ClientApplication
  uipTB = context.OwnerForm.GetUIPartByName('uipTransactionBatch')

  if uipTB.batch_type == 'T':
    JenisTransaksi = context.GetFieldValue('TransaksiDPLK.kode_jenis_transaksi')
    if JenisTransaksi in ['V','W','J','H']:
      #cetak advis
      if app.ConfirmDialog('Anda bermaksud membuat Advis Transaksi?'):
        idTransaksi = context.GetFieldValue('TransaksiDPLK.ID_Transaksi')

        #identify jenis transaksi
        if JenisTransaksi == 'V':
          #penarikan dana 30%
          classTransaksi = 'PenarikanDanaNormal'
        elif JenisTransaksi == 'W':
          #penarikan dana PHK
          classTransaksi = 'PenarikanDanaPHK'
        elif JenisTransaksi == 'J':
          #pengambilan manfaat
          classTransaksi = 'PengambilanManfaat'
        elif JenisTransaksi == 'H':
          #pengalihan ke DPLK lain
          classTransaksi = 'PengalihanKeDPLKLain'

        try:
          res = app.ExecuteScript('report/AdvisTransaksi', \
            app.CreateValues(['classtransaksi',classTransaksi],['idtransaksi',idTransaksi]))
          app.DownloadItem(res.FirstRecord.filename,'v')
        except:
          app = None
          raise
    else:
      #tidak ada advis yang dicetak
      app.ShowMessage('Tidak ada Advis yang dapat dibuat untuk jenis transaksi ini!')
  else:
    #tidak ada advis yang dicetak
    app.ShowMessage('Tidak ada Advis yang dapat dibuat untuk jenis transaksi ini!')

#event click umum---------------------------------------------------------------

#konvensi NumberTag
# 310 Pengalihan ke DPLK Lain
# 311 Pengalihan dari DPLK lain
# 312 Pengalihan dari DPPK lain
# 313 Pengalihan dari DPK lain
# 360 Penarikan Dana Normal 30%
# 361 Penarikan Dana PHK
# 370 Pembayaran Iuran Peserta
# 380 Pengambilan Manfaat Pensiun

# 3100 Input Transaksi DPLK Manual
# 3110 Input Iuran Pendaftaran Manual
# 3120 Input Titipan Premi
# 3121 Input Transaksi Premi Manual

# 1000 Pembayaran Iuran Peserta (Otorisasi)
# 3000 Lihat Detil Transaksi

def mnuShowModal(sender, context):
  app = context.OwnerForm.ClientApplication
  
  #cek jenis batch yang mewadahi transaksi: Registrasi, Transaksi, Premi
  uipTB = context.OwnerForm.GetUIPartByName('uipTransactionBatch')
  
  if uipTB.batch_status == 'O':
    #batch masih berstatus Open
    if sender.NumberTag == 3110 and (uipTB.batch_type != 'R' or \
      uipTB.batch_sub_type != 'M'):
      #Iuran Pendaftaran
      app.ShowMessage('Menu ini hanya bisa dipakai untuk jenis Batch Registrasi/Pendaftaran!')
      return
    elif sender.NumberTag in [310,311,312,313,360,361,370,380,3100] and \
      (uipTB.batch_type != 'T' or uipTB.batch_sub_type != 'M'):
      #Transaksi DPLK manual
      app.ShowMessage('Menu ini hanya bisa dipakai untuk jenis Batch Transaksi!')
      return
    elif sender.NumberTag in [3120,3121] and (uipTB.batch_type != 'P' or \
      uipTB.batch_sub_type != 'M'):
      #Transaksi Premi
      app.ShowMessage('Menu ini hanya bisa dipakai untuk jenis Batch Premi!')
      return
  else:
    #batch berstatus Closed
    app.ShowMessage('Batch telah berstatus Tutup! Penambahan transaksi tidak dapat dilakukan.')
    return

  form_id = sender.Name
  group_id = sender.StringTag
  form = app.GetForm(group_id+'/'+form_id, form_id, 0)

  form.Show(app.CreateValues(['code',sender.NumberTag]))

def mnuShowModalWithData(sender, context):
  app = context.OwnerForm.ClientApplication

  #cek jenis batch yang mewadahi transaksi: Registrasi, Transaksi, Premi
  uipTB = context.OwnerForm.GetUIPartByName('uipTransactionBatch')
  
  if uipTB.batch_status == 'O':
    #batch masih berstatus Open
    if sender.NumberTag == 3110 and (uipTB.batch_type != 'R' or \
      uipTB.batch_sub_type != 'M'):
      #Iuran Pendaftaran
      app.ShowMessage('Menu ini hanya bisa dipakai untuk jenis Batch '\
        'Registrasi/Pendaftaran dan Sub Tipenya Manual!')
      return
    elif sender.NumberTag in [310,311,312,313,360,361,370,380,3100] and \
      (uipTB.batch_type != 'T' or uipTB.batch_sub_type != 'M'):
      #Transaksi DPLK manual
      app.ShowMessage('Menu ini hanya bisa dipakai untuk jenis Batch Transaksi '\
        'dan Sub Tipenya Manual!')
      return
    elif sender.NumberTag in [3120,3121] and (uipTB.batch_type != 'P' or \
      uipTB.batch_sub_type != 'M'):
      #Transaksi Premi
      app.ShowMessage('Menu ini hanya bisa dipakai untuk jenis Batch Premi dan '\
        'Sub Tipenya Manual!')
      return
    elif sender.NumberTag == 1000 and (uipTB.batch_type != 'T' or \
      context.GetFieldValue('TransaksiDPLK.kode_jenis_transaksi') != 'K'):
      #Pembayaran Iuran
      app.ShowMessage('Menu ini hanya bisa dipakai untuk jenis Batch Transaksi dan jenis transaksi Iuran Peserta!')
      return
  else:
    #batch berstatus Closed
    if sender.NumberTag != 3000:
      #kecuali NumberTag 3000 (Lihat Detil Transaksi), tampilkan error ini
      app.ShowMessage('Batch telah berstatus Tutup! Penambahan transaksi tidak dapat dilakukan.')
      return

  #inisialisasi
  ShowDataPacket = app.CreateValues(['code',sender.NumberTag])
  form_id = sender.Name
  group_id = sender.StringTag

  #cek NumberTag
  if sender.NumberTag in [310,311,312,313,360,361,370,380,3100,3110,3120,3121]:
    #mode New untuk transaksi DPLK, transaksi premi, dan iuran pendaftaran manual
    #panggil form InputSingle
    key = 'x'
    uipName = 'x'
    
    #kirim properti batch untuk pengesetan inputan batch
    uipTB = context.OwnerForm.GetUIPartByName('uipTransactionBatch')
    ShowDataPacket = app.CreateValues( \
      ['code',sender.NumberTag], \
      ['idbatch',uipTB.ID_TransactionBatch], \
      ['nobatch',uipTB.no_batch], \
      ['branchcode',uipTB.branch_code], \
      ['tglpakai',uipTB.tgl_used])

  elif sender.NumberTag == 1000:
    #untuk pembayaran iuran (otorisasi)

    #cek status otorisasi
    if context.GetFieldValue('TransaksiDPLK.status_otorisasi') == 'true':
      #pembayaran iuran sudah terotorisasi
      app.ShowMessage('Pembayaran Iuran sudah diotorisasi, tidak bisa diotorisasi ulang!')
      return
    elif context.GetFieldValue('TransaksiDPLK.sub_tipe_batch') == 'Teller Transaction':
      #Teller transaction
      app.ShowMessage('Transaksi ini dibuat oleh Teller. Otorisasi hanya bisa '\
        'dilakukan lewat proses Rekonsiliasi dengan Core Banking.')
      return

    key = 'PObj:IuranPeserta#ID_Transaksi=' + \
      str(context.GetFieldValue('TransaksiDPLK.ID_Transaksi'))
    uipName = 'uipTransaksi'
    ShowDataPacket = app.CreateValues( \
      ['nopeserta',context.GetFieldValue('TransaksiDPLK.no_peserta')], \
      ['code',sender.NumberTag])
      
  elif sender.NumberTag == 3000:
    #mode view untuk transaksi DPLK, transaksi premi dan iuran pendaftaran manual
    #dipilih berdasarkan batch type lalu kode jenis transaksi
    uipName = 'uipTransaksi'
    
    #cek batch type, cocokkan dengan kode jenis transaksi
    if uipTB.batch_type == 'R':
      #untuk iuran pendaftaran manual
      idTransaksi = context.GetFieldValue('IuranPendaftaran.ID_Transaksi')
      key = 'PObj:IuranPendaftaran#ID_Transaksi=' + str(idTransaksi)
      form_id = 'fOtorisasiIuranPendaftaran'

    elif uipTB.batch_type == 'P':
      #untuk transaksi premi
      idTransaksi = context.GetFieldValue('TransaksiPremi.ID_Transaksi')

      #cek jenis transaksi premi
      JenisTransaksi = context.GetFieldValue('TransaksiPremi.jenis_transaksi')
      if JenisTransaksi == 'Titipan Premi':
        key = 'PObj:TitipanPremi#ID_Transaksi=' + str(idTransaksi)
        form_id = 'fOtorisasiTitipanPremi'
      elif JenisTransaksi == 'Transaksi Premi Manual':
        key = 'PObj:TransaksiPremiManual#ID_Transaksi=' + str(idTransaksi)
        form_id = 'fOtorisasiTransaksiPremiManual'

    elif uipTB.batch_type == 'T':
      #untuk transaksi DPLK
      idTransaksi = context.GetFieldValue('TransaksiDPLK.ID_Transaksi')
      
      #cek jenis transaksi DPLK
      JenisTransaksi = context.GetFieldValue('TransaksiDPLK.kode_jenis_transaksi')
      if JenisTransaksi in ['I','O','P']:
        #pengalihan dari DPLK, DPPK, DPK lain
        key = 'PObj:PengalihanDariDPLKLain#ID_Transaksi=' + str(idTransaksi)
        form_id = 'fOtorisasiPengalihanDariDPLK'
      elif JenisTransaksi == 'H':
        #pengalihan ke DPLK lain
        key = 'PObj:PengalihanKeDPLKLain#ID_Transaksi=' + str(idTransaksi)
        form_id = 'fOtorisasiPengalihanKeDPLK'
      elif JenisTransaksi == 'V':
        #penarikan dana 30%
        key = 'PObj:PenarikanDanaNormal#ID_Transaksi=' + str(idTransaksi)
        form_id = 'fOtorisasiPenarikanDana30'
      elif JenisTransaksi == 'W':
        #penarikan dana PHK
        key = 'PObj:PenarikanDanaPHK#ID_Transaksi=' + str(idTransaksi)
        form_id = 'fOtorisasiPenarikanDanaPHK'
      elif JenisTransaksi == 'J':
        #pengambilan manfaat
        key = 'PObj:PengambilanManfaat#ID_Transaksi=' + str(idTransaksi)
        form_id = 'fOtorisasiPengambilanManfaat'
      elif JenisTransaksi == 'M':
        #transaksi DPLK Manual
        key = 'PObj:TransaksiDPLKManual#ID_Transaksi=' + str(idTransaksi)
        form_id = 'fOtorisasiTransaksiDPLKManual'
      elif JenisTransaksi == 'K':
        #transaksi Iuran Nasabah
        key = 'PObj:IuranPeserta#ID_Transaksi=' + str(idTransaksi)
        form_id = 'fOtorisasiIuranPremiNasabah'
      elif JenisTransaksi == 'C':
        #Biaya Pengelolaan Dana
        key = 'PObj:BiayaPengelolaanDana#ID_Transaksi=' + str(idTransaksi)
        form_id = 'fBiayaTransaksi_View'
        ShowDataPacket = app.CreateValues(['code',10002])
      elif JenisTransaksi == 'D':
        #Biaya Administrasi Tahunan
        key = 'PObj:BiayaAdmTahunan#ID_Transaksi=' + str(idTransaksi)
        form_id = 'fBiayaTransaksi_View'
        ShowDataPacket = app.CreateValues(['code',10001])
      elif JenisTransaksi == 'X':
        #Biaya Administrasi Transaksi
        key = 'PObj:BiayaAdmTransaksi#ID_Transaksi=' + str(idTransaksi)
        form_id = 'fBiayaTransaksi_View'
        ShowDataPacket = app.CreateValues(['code',10000])
      elif JenisTransaksi == 'F':
        #Biaya Pindah Paket Investasi
        key = 'PObj:BiayaAdmTransaksi#ID_Transaksi=' + str(idTransaksi)
        form_id = 'fBiayaTransaksi_View'
        ShowDataPacket = app.CreateValues(['code',10004])
      elif JenisTransaksi == 'G':
        #transaksi Bagi Hasil
        key = 'PObj:TransaksiBagiHasil#ID_Transaksi=' + str(idTransaksi)
        form_id = 'fBiayaTransaksi_View'
        ShowDataPacket = app.CreateValues(['code',10003])
      #elif yang lainnya...

    elif uipTB.batch_type == 'I':
      #untuk transaksi Investasi
      form_id, classname, uipName = \
        GetFormInfoByJnsTransCode(
          context.GetFieldValue('TransaksiInvestasi.kode_jenis_transaksi'),\
          context.GetFieldValue('TransaksiInvestasi.kelompok_transaksi')
        )[:3]
      key = 'PObj:%s#ID_TRANSAKSIINVESTASI=%d' % (classname, \
        context.GetFieldValue('TransaksiInvestasi.ID_Transaksi'))
      group_id = 'investasi/transaksi'
      ShowDataPacket = app.CreateValues(
                         ['mode','viewdoc']
                         , ['caption',sender.Caption.replace('...','')]
                       )

  try:
    form = app.GetFormWithData(group_id+'/'+form_id, form_id, 0, key, uipName)
    form.Show(ShowDataPacket)
  finally:
    app = None
