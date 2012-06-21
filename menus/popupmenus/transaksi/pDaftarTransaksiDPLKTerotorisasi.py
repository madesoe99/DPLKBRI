def mnuCetakAdvisClick(sender, context):
  app = context.OwnerForm.ClientApplication
  JenisTransaksi = context.GetFieldValue('TransaksiDPLK.hidden_kode_Jenis_Transaksi')

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

#event click umum---------------------------------------------------------------
def mnuShowModal(sender, context):
  app = context.OwnerForm.ClientApplication

  form_id = sender.Name
  group_id = sender.StringTag
  form = app.GetForm(group_id+'/'+form_id, form_id, 0)

  form.Show(app.CreateValues(['code',sender.NumberTag]))

def mnuShowModalWithData(sender, context):
  app = context.OwnerForm.ClientApplication
  form_id = sender.Name

  #cek NumberTag
  ShowDataPacket = app.CreateValues(['code',sender.NumberTag])
  if sender.NumberTag == 2000:
    #mode view untuk semua jenis transaksi DPLK, dipilah based on kode jenis transaksi

    #cek nomor peserta, idbatch dan no batch
    if context.GetFieldValue('TransaksiDPLK.Nomor_Peserta') == None or \
      context.GetFieldValue('TransaksiDPLK.Nomor_Peserta') == '' or \
      context.GetFieldValue('TransaksiDPLK.idbatch') == None or \
      context.GetFieldValue('TransaksiDPLK.idbatch') == '' or \
      context.GetFieldValue('TransaksiDPLK.nobatch') == None or \
      context.GetFieldValue('TransaksiDPLK.nobatch') == '':
      app.ShowMessage('Belum ada data Nomor Peserta atau Batch Transaksi!')
      return

    JenisTransaksi = context.GetFieldValue('TransaksiDPLK.hidden_kode_Jenis_Transaksi')
    idTransaksi = context.GetFieldValue('TransaksiDPLK.ID_Transaksi')
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

    uipName = 'uipTransaksi'

  group_id = sender.StringTag
  form = app.GetFormWithData(group_id+'/'+form_id, form_id, 0, key, uipName)

  #show the form
  form.Show(ShowDataPacket)
