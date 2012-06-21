def SetToCenterForm(prevForm, currForm):
  currForm.Left = (prevForm.Width - currForm.Width)/2 + prevForm.Left
  currForm.Top = (prevForm.Height - currForm.Height)/2 + prevForm.Top

#konvensi NumberTag
# 0 Input Iuran Pendaftaran Manual
# 100 Lihat Detil Iuran Pendaftaran

#event click umum---------------------------------------------------------------
def mnuShowModal(sender, context):
  app = context.OwnerForm.ClientApplication

  form_id = sender.Name
  group_id = sender.StringTag
  form = app.GetForm(group_id+'/'+form_id, form_id, 0)
  #SetToCenterForm(context.OwnerForm, form.FormObject)
  form.Show(app.CreateValues(['code',sender.NumberTag]))

def mnuShowModalWithData(sender, context):
  app = context.OwnerForm.ClientApplication
  form_id = sender.Name
  
  #cek NumberTag
  ShowDataPacket = app.CreateValues(['code',sender.NumberTag])
  if sender.NumberTag in [0,110]:
    #Input Iuran Pendaftaran Manual
    key = 'x'
    uipName = 'x'
  elif sender.NumberTag in [1000,2000]:
    #otorisasi untuk iuran pendaftaran

    #cek status otorisasi
    if sender.NumberTag == 1000 and \
      context.GetFieldValue('IuranPendaftaran.Status_Otorisasi') == 'true':
      #mode otorisasi
      app.ShowMessage('Pendaftaran sudah diotorisasi, tidak bisa diotorisasi ulang!')
      return
    elif sender.NumberTag == 1000 and \
      context.GetFieldValue('IuranPendaftaran.batchSubType') == 'T':
      #teller transaction
      app.ShowMessage('Transaksi ini dibuat oleh Teller. Otorisasi hanya bisa '\
        'dilakukan lewat proses Rekonsiliasi dengan Core Banking.')
      return

    key = context.KeyObjConst
    uipName = 'uipTransaksi'
    ShowDataPacket = app.CreateValues( \
      ['nopeserta',context.GetFieldValue('IuranPendaftaran.Nomor_Peserta')], \
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
