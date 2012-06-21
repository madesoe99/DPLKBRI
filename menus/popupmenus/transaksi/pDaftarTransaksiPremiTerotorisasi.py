#konvensi NumberTag
# 2000 Lihat Detil Titipan Premi / Transaksi Premi Manual

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
    #mode view untuk transaksi premi

    JenisTransaksi = context.GetFieldValue('TransaksiPremi.hidden_jenis_transaksi')
    idTransaksi = context.GetFieldValue('TransaksiPremi.ID_Transaksi')
    #noPeserta = ''
    
    if JenisTransaksi == 'T':
      #titipan premi
      key = 'PObj:TitipanPremi#ID_Transaksi=' + str(idTransaksi)
      form_id = 'fOtorisasiTitipanPremi'
    elif JenisTransaksi == 'M':
      #transaksi premi manual
      key = 'PObj:TransaksiPremiManual#ID_Transaksi=' + str(idTransaksi)
      form_id = 'fOtorisasiTransaksiPremiManual'

    uipName = 'uipTransaksi'
    #KODE INI SEHARUSNYA DIHAPUS
    #ShowDataPacket = app.CreateValues( \
      #['nopeserta',noPeserta], \
      #['code',sender.NumberTag])

  group_id = sender.StringTag
  form = app.GetFormWithData(group_id+'/'+form_id, form_id, 0, key, uipName)

  form.Show(ShowDataPacket)
