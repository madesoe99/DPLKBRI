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
  if sender.NumberTag == 2000:
    #mode view untuk iuran pendaftaran

    key = context.KeyObjConst
    uipName = 'uipTransaksi'
    #KODE INI SEHARUSNYA DIHAPUS
    #ShowDataPacket = app.CreateValues( \
      #['nopeserta',context.GetFieldValue('IuranPendaftaran.Nomor_Peserta')], \
      #['code',sender.NumberTag])

  group_id = sender.StringTag
  form = app.GetFormWithData(group_id+'/'+form_id, form_id, 0, key, uipName)
  #SetToCenterForm(context.OwnerForm, form.FormObject)
  form.Show(ShowDataPacket)
