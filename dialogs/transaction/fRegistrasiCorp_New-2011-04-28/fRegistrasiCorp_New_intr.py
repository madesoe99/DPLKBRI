def FormShow(form, parameter):
  app = form.ClientApplication
  uipRegEditNasabahDPLKCorporate = form.GetUIPartByName('uipRegEditNasabahDPLKCorporate')

  uipRegEditNasabahDPLKCorporate.Edit()
  uipRegEditNasabahDPLKCorporate.mode = parameter.FirstRecord.mode

def btnOKClick(sender):
  form = sender.OwnerForm
  uipRegEditNasabahDPLKCorporate = form.GetUIPartByName('uipRegEditNasabahDPLKCorporate')
  uipP = form.GetUIPartByName('uipParameter')

  #checking tgl bayar iuran
  if uipRegEditNasabahDPLKCorporate.tgl_bayar_iuran in ['',None]:
    form.ShowMessage('Tanggal Bayar Iuran masih kosong. Mohon untuk diisi.')
    return
    
  #checking biaya daftar anggota
  if uipRegEditNasabahDPLKCorporate.biaya_daftar_anggota in ['',None] or \
    uipRegEditNasabahDPLKCorporate.biaya_daftar_anggota < 0.0:
    #memakai batas 0.0 sebab dimungkinkan gratis
    form.ShowMessage('Biaya Daftar Anggota tidak boleh kosong atau negatif.')
    return

  # seusaikan flag akibat formendsetdata
  uipRegEditNasabahDPLKCorporate.Edit()
  uipRegEditNasabahDPLKCorporate.__SYSFLAG = 'N'

  form.CommitBuffer()
  form.PostResult()

  sender.ExitAction = 1

