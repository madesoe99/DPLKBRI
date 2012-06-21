#konvensi NumberTag
# 0 Input Titipan Premi / Transaksi Premi Manual
# 100 Lihat Detil Titipan Premi / Transaksi Premi Manual

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
  if sender.NumberTag in [0,120,121]:
    #Input Titipan Premi / Transaksi Premi Manual
    key = 'x'
    uipName = 'x'
  elif sender.NumberTag in [1000,2000]:
    #otorisasi untuk transaksi premi

    #cek status otorisasi
    if sender.NumberTag == 1000 and \
      context.GetFieldValue('TransaksiPremi.Status_Otorisasi') == 'true':
      app.ShowMessage('Transaksi Premi sudah diotorisasi, tidak bisa diotorisasi ulang!')
      return
    elif sender.NumberTag == 1000 and \
      context.GetFieldValue('TransaksiPremi.batchSubType') == 'T':
      #teller transaction
      app.ShowMessage('Transaksi ini dibuat oleh Teller. Otorisasi hanya bisa '\
        'dilakukan lewat proses Rekonsiliasi dengan Core Banking.')
      return

    JenisTransaksi = context.GetFieldValue('TransaksiPremi.hidden_jenis_transaksi')
    idTransaksi = context.GetFieldValue('TransaksiPremi.ID_Transaksi')
    noPeserta = ''
    
    if JenisTransaksi == 'T':
      #titipan premi
      key = 'PObj:TitipanPremi#ID_Transaksi=' + str(idTransaksi)
      form_id = 'fOtorisasiTitipanPremi'
    elif JenisTransaksi == 'M':
      #transaksi premi manual
      key = 'PObj:TransaksiPremiManual#ID_Transaksi=' + str(idTransaksi)
      form_id = 'fOtorisasiTransaksiPremiManual'

    uipName = 'uipTransaksi'
    ShowDataPacket = app.CreateValues( \
      ['nopeserta',noPeserta], \
      ['code',sender.NumberTag])

  group_id = sender.StringTag
  form = app.GetFormWithData(group_id+'/'+form_id, form_id, 0, key, uipName)

  if sender.NumberTag == 1000:
    if form.Show(ShowDataPacket) == 1:
      #menu otorisasi dipilih dan otorisasi berhasil, hapus context row query
      context.DeleteRow()
  else:
    #selain menu otorisasi
    form.Show(ShowDataPacket)
