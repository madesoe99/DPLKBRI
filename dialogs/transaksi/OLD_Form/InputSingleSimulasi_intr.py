def FormShow(form, parameter):
  uipInput = form.GetUIPartByName('uipInput')
  uipUI = form.GetUIPartByName('uipUserInfo')

  uipInput.Edit()
  uipInput.Code = parameter.FirstRecord.code
  uipInput.SetFieldValue('LPeserta.no_peserta','')
  
  #nilai untuk inisialisasi jenis transaksi bukan teller

  if uipInput.Code in [10,310]:
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
    form.Caption = 'Input Untuk Penarikan Dana 30% Simulasi'
  elif uipInput.Code in [61,361]:
    #Pengalihan dari DPLK lain, set batch type dan batch sub type
    form.Caption = 'Input Untuk Penarikan Dana PHK Simulasi'
  elif uipInput.Code in [80,380]:
    #Pengambilan manfaat pensiun, set batch type dan batch sub type
    form.Caption = 'Input Untuk Pengambilan Manfaat Pensiun Simulasi'



def bOKClick(sender):
  app = sender.OwnerForm.ClientApplication
  uipInput = sender.OwnerForm.GetUIPartByName('uipInput')
  uipUI = sender.OwnerForm.GetUIPartByName('uipUserInfo')
  NoPeserta = uipInput.GetFieldValue('LPeserta.no_peserta')

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
      #elif dh.FirstRecord.status == 6 and uipInput.Code in [60,360]:
      #  app.ShowMessage('PERINGATAN!\n\nPeserta tidak diperkenankan menarik dana '\
      #    'Harap hubungi Bagian Marketing DPLK Pusat!')
      #  return

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
      form_id = 'PenarikanDana30SimulasiRev'
    elif uipInput.Code in [61,361]:
      #penarikan dana PHK
      form_id = 'PenarikanDanaPHKSimulasi'
    elif uipInput.Code in [80,380]:
      #pengambilan manfaat pensiun
      form_id = 'PengambilanManfaatSimulasi'

    key = 'PObj:NasabahDPLK#no_peserta=' + NoPeserta
    uipName = 'uipNasabah'

  try:
    oform = app.GetFormWithData(group_id+'/'+form_id, form_id, 0, key, uipName)
    oform.Show(app.CreateValues(['nopeserta', NoPeserta or '']))

    #clean it and exit form
    sender.OwnerForm.ResetAndClearData()
    sender.ExitAction = 1
  finally:

    oform = None
    app = None

