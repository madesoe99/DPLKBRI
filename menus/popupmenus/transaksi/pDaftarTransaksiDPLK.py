def zfill(s):
  #fungsi ini untuk menambahkan satu angka 0 pada string s
  #digunakan terutama untuk representasi penanggalan bagi hari / bulan
  #prekondisi: s haruslah literal string yang hanya berisi angka

  if len(s) == 1:
    s = '0' + s
  #selain berjumlah karakter sama dengan satu, tidak akan diutak-atik

  return s

def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

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

#konvensi NumberTag
# 0 mode New

#event click umum---------------------------------------------------------------
def mnuShowModal(sender, context):
  app = context.OwnerForm.ClientApplication

  form_id = sender.Name
  group_id = sender.StringTag
  form = app.GetForm(group_id+'/'+form_id, form_id, 0)
  SetToCenterForm(context.OwnerForm, form.FormObject)
  form.Show(app.CreateValues(['code',sender.NumberTag]))

def mnuShowModalWithData(sender, context):
  app = context.OwnerForm.ClientApplication
  form_id = sender.Name
  
  #cek NumberTag
  ShowDataPacket = app.CreateValues(['code',sender.NumberTag])
  if sender.NumberTag in [0,10,11,12,13,60,61,70,80,100]:
    #mode New
    key = 'x'
    uipName = 'x'
  elif sender.NumberTag == 200:
    #KODE INI SEHARUSNYA SUDAH TIDAK DIPAKAI LAGI
    #untuk semua jenis transaksi: penarikan, pengalihan, pengambilan
    #key dan uipname untuk loading data nasabah
    #untuk batch dikirim paket untuk FormShow

    #cek nomor peserta, idbatch dan no batch
    if context.GetFieldValue('TransaksiDPLK.Nomor_Peserta') == None or \
      context.GetFieldValue('TransaksiDPLK.Nomor_Peserta') == '' or \
      context.GetFieldValue('TransaksiDPLK.idbatch') == None or \
      context.GetFieldValue('TransaksiDPLK.idbatch') == '' or \
      context.GetFieldValue('TransaksiDPLK.nobatch') == None or \
      context.GetFieldValue('TransaksiDPLK.nobatch') == '':
      app.ShowMessage('Belum ada data Nomor Peserta atau Batch Transaksi!')
      return
      
    key = 'PObj:NasabahDPLK#no_peserta=' + \
      context.GetFieldValue('TransaksiDPLK.Nomor_Peserta')
    uipName = 'uipNasabah'
    ShowDataPacket = app.CreateValues( \
      ['nopeserta',context.GetFieldValue('TransaksiDPLK.Nomor_Peserta')], \
      ['idbatch',context.GetFieldValue('TransaksiDPLK.idbatch')], \
      ['nobatch',context.GetFieldValue('TransaksiDPLK.nobatch')],
      ['branchcode',context.GetFieldValue('TransaksiDPLK.Kode_Cabang')])
  elif sender.NumberTag in [1000,2000]:
    #otorisasi untuk semua jenis transaksi DPLK, dipilah based on kode jenis transaksi
    
    #cek status otorisasi
    if sender.NumberTag == 1000 and \
      context.GetFieldValue('TransaksiDPLK.Status_Otorisasi') == 'true':
      app.ShowMessage('Transaksi sudah diotorisasi, tidak bisa diotorisasi ulang!')
      return
    elif sender.NumberTag == 1000 and \
      context.GetFieldValue('TransaksiDPLK.batchSubType') == 'T':
      #Teller transaction
      app.ShowMessage('Transaksi ini dibuat oleh Teller. Otorisasi hanya bisa '\
        'dilakukan lewat proses Rekonsiliasi dengan Core Banking.')
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
      #transaksi pembayaran iuran peserta
      key = 'PObj:IuranPeserta#ID_Transaksi=' + str(idTransaksi)
      form_id = 'fOtorisasiIuranPremiNasabah'
    #elif yang lainnya...

    uipName = 'uipTransaksi'
    ShowDataPacket = app.CreateValues( \
      ['nopeserta',context.GetFieldValue('TransaksiDPLK.Nomor_Peserta')], \
      ['code',sender.NumberTag])

  group_id = sender.StringTag
  form = app.GetFormWithData(group_id+'/'+form_id, form_id, 0, key, uipName)
  #SetToCenterForm(context.OwnerForm, form.FormObject)

  if sender.NumberTag == 1000:
    if form.Show(ShowDataPacket) == 1:
      #menu otorisasi dipilih dan otorisasi berhasil, hapus context row query
      context.DeleteRow()
  else:
    #selain menu otorisasi
    form.Show(ShowDataPacket)
    
def PilihClick(sender, context):
##  if context.Eof:
##    raise Exception, 'data kosong +  tidak bisa dipilih!'
  app = context.OwnerForm.ClientApplication
  flag = sender.StringTag
  flagquery = context.GetFieldValue('TransaksiDPLK.Flag_Pilih')
  if flagquery == None: flagquery = ''
  if context.GetFieldValue('TransaksiDPLK.Status_Otorisasi') == 'true':
    app.ShowMessage('Transaksi sudah diotorisasi, tidak bisa dipilih utk otorisasi!')
    return
  elif context.GetFieldValue('TransaksiDPLK.batchSubType') == 'T':
    #Teller transaction
    app.ShowMessage('Transaksi tidak bisa dipilih krn dibuat oleh Teller. \nOtorisasi hanya bisa '\
        'dilakukan lewat proses Rekonsiliasi dengan Core Banking.')
    return
  elif flag == flagquery:
    app.ShowMessage('Transaksi sudah di '+sender.Caption+', tidak bisa di '+sender.Caption+' lagi!')
    return
    
  app.ExecuteScript('transaksi/updateflagpilih', \
  app.CreateValues(['id', context.GetFieldValue('TransaksiDPLK.ID_Transaksi')],\
  ['flag', flag]))
  context.Refresh()
  
def PilihSemuaClick(sender, context):
##  if context.Eof:
##    raise Exception, 'data kosong +  tidak bisa dipilih!'
  app = context.OwnerForm.ClientApplication
  uip = context.OwnerForm.GetUIPartByName('uipUserInfo')
  uipFilter = context.OwnerForm.GetUIPartByName('uipFilter')
  flag = sender.StringTag
  if uip.isBackOffice:
    branch_code = uip.BranchCode
  else:
    branch_code = uipFilter.GetFieldValue('LBranch.branch_code')

  awalTanggal = uipFilter.GetFieldValue('AwalTanggal')
  akhirTanggal = uipFilter.GetFieldValue('AkhirTanggal')

  awalTanggal = '%s/%s/%d' % (zfill(str(awalTanggal[1])), \
    zfill(str(awalTanggal[2])),awalTanggal[0])

  akhirTanggal = '%s/%s/%d' % (zfill(str(akhirTanggal[1])), \
    zfill(str(akhirTanggal[2])),akhirTanggal[0])


  rph = app.ExecuteScript('transaksi/updateflagpilihsemua', \
  app.CreateValues(['kode_cbg', branch_code], ['tgl_awal', awalTanggal], \
  ['tgl_akhir', akhirTanggal], ['flag', flag]))
  
  if flag == 'Y': msg = 'selected'
  else: msg = 'unselected'
  app.ShowMessage(str(rph.FirstRecord.n) + ' row(s) '+msg)
  context.Refresh()

def OtomassalClick(sender, context):
  app = context.OwnerForm.ClientApplication
  if app.ConfirmDialog(sender.StringTag):
    uip = context.OwnerForm.GetUIPartByName('uipUserInfo')
    uipFilter = context.OwnerForm.GetUIPartByName('uipFilter')
    if uip.isBackOffice:
      branch_code = uip.BranchCode
    else:
      branch_code = uipFilter.GetFieldValue('LBranch.branch_code')

    awalTanggal = uipFilter.GetFieldValue('AwalTanggal')
    akhirTanggal = uipFilter.GetFieldValue('AkhirTanggal')

    awalTanggal = '%s/%s/%d' % (zfill(str(awalTanggal[1])), \
    zfill(str(awalTanggal[2])),awalTanggal[0])

    akhirTanggal = '%s/%s/%d' % (zfill(str(akhirTanggal[1])), \
    zfill(str(akhirTanggal[2])),akhirTanggal[0])

    app.ExecuteScript('transaksi/OtorisasiMassal', \
    app.CreateValues(['kode_cbg', branch_code], ['tgl_awal', awalTanggal], \
    ['tgl_akhir', akhirTanggal]))

    context.Refresh()

