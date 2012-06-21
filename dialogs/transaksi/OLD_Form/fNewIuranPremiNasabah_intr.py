
def FormShow(form, parameter):
  uip = form.GetUIPartByName('uipUserInfo')
  uipT = form.GetUIPartByName('uipTransaksi')
  uipN = form.GetUIPartByName('uipNasabah')

  #cek wasiat ummat dan titipan premi
  if uipN.isWasiatUmmat == 'F' or uipN.isWasiatUmmat == None:
    #bukan peserta wasiat ummat, matikan input titipan premi
    form.GetControlByName('pDataTransaksi.titipan_premi').Enabled = 0
    form.GetControlByName('pDataTransaksi.TB_Premi').Enabled = 0
    form.GetControlByName('pDataTransaksi.isOnlyTitipanPremi').Enabled = 0
  else:
    #peserta wasiat ummat
    #penanganan khusus untuk TELLER dalam memilih Batch Premi
    if uip.isTeller:
      #matikan lookup batch premi
      form.GetControlByName('pDataTransaksi.TB_Premi').Enabled = 0
      
      #cek Batch Premi Exist
      uipBD = form.GetUIPartByName('uipBatchDefined')
      if not uipBD.isBatchPremiExist:
        #batch premi tidak ditemukan
        form.ShowMessage('Peringatan!\n\nBatch Transaksi Premi untuk hari ini '\
          'belum ada/tidak ditemukan. Untuk itu, Titipan Premi peserta tidak '\
          'bisa dilakukan dan nilai nominalnya harus diisi dengan 0.')

  #set batch transaksi
  uipT.Edit()
  uipT.SetFieldValue('LTransactionBatch.ID_TransactionBatch', \
    parameter.FirstRecord.idbatch)
  uipT.SetFieldValue('LTransactionBatch.no_batch', \
    parameter.FirstRecord.nobatch)
  form.GetControlByName('pDataTransaksi.LTransactionBatch').Enabled = 0
  
  #set branch code untuk transaction batch
  uipT.TB_BranchCode = parameter.FirstRecord.branchcode

  #disable tanggal transaksi, supaya diset dengan tanggal pakai batch
  uipT.tgl_transaksi = parameter.FirstRecord.tglpakai
  form.GetControlByName('pDataTransaksi.tgl_transaksi').Enabled = 0

  #penanganan khusus untuk TELLER
  if uip.isTeller:
    #don't visible iuran pemberi kerja
    uipT.IuranPemberiKerja = 0.0
    form.GetControlByName('pDataTransaksi.IuranPemberiKerja').Visible = 0
    
  #set pilihan pindah buku
  uipT.isPindahBuku = 'F'

def isOnlyTitipanPremiClick(sender):
  form = sender.OwnerForm
  uipT = form.GetUIPartByName('uipTransaksi')
  uipN = form.GetUIPartByName('uipNasabah')

  uipT.Edit()
  if sender.Checked:
    uipT.IuranPeserta = uipT.IuranPemberiKerja = 0.0
    form.GetControlByName('pDataTransaksi.IuranPemberiKerja').Enabled = \
    form.GetControlByName('pDataTransaksi.IuranPeserta').Enabled = \
    form.GetControlByName('pDataTransaksi.catatan_bayar_iuran').Enabled = \
    form.GetControlByName('pDataTransaksi.keterangan').Enabled = 0
  else:
    uipT.IuranPeserta = uipN.IuranPeserta
    uipT.IuranPemberiKerja = uipN.IuranPk
    form.GetControlByName('pDataTransaksi.IuranPemberiKerja').Enabled = \
    form.GetControlByName('pDataTransaksi.IuranPeserta').Enabled = \
    form.GetControlByName('pDataTransaksi.catatan_bayar_iuran').Enabled = \
    form.GetControlByName('pDataTransaksi.keterangan').Enabled = 1

def isPindahBukuClick(sender):
  form = sender.OwnerForm
  uipT = form.GetUIPartByName('uipTransaksi')

  uipT.Edit()
  if sender.Checked:
    form.GetControlByName('pPindahBuku.Rekening_Pindah_Buku').Enabled = \
    form.GetControlByName('pPindahBuku.bCekRekening').Enabled = \
    form.GetControlByName('pPindahBuku.bCekRekening').Default = 1
    form.GetControlByName('pButton.bSimpan').Enabled = \
    form.GetControlByName('pButton.bSimpan').Default = 0
  else:
    uipT.Tipe_Rekening_Pindah_Buku = uipT.Rekening_Pindah_Buku = \
      uipT.NamaPemilikRekening = uipT.IDNumber = uipT.BranchCode = \
      uipT.CurrencyCode = None
    form.GetControlByName('pPindahBuku.Rekening_Pindah_Buku').Enabled = \
    form.GetControlByName('pPindahBuku.bCekRekening').Enabled = \
    form.GetControlByName('pPindahBuku.bCekRekening').Default = 0
    form.GetControlByName('pButton.bSimpan').Enabled = \
    form.GetControlByName('pButton.bSimpan').Default = 1

def bCekRekeningClick(sender):
  app = sender.OwnerForm.ClientApplication
  uipT = sender.OwnerForm.GetUIPartByName('uipTransaksi')

  #cek field nomor rekening pindah buku
  if uipT.Rekening_Pindah_Buku in [None,'']:
    #belum ada nomor rekening
    app.ShowMessage('Nomor Rekening Pindah Buku masih kosong, mohon diisi dahulu.')
  else:
    #nomor rekening sudah ada
    res = app.ExecuteScript('transaksi/CekRekeningCoreBanking',\
      app.CreateValues(['noRekening',uipT.Rekening_Pindah_Buku]))

    uipT.Edit()
    uipT.NamaPemilikRekening = res.FirstRecord.namaPemilikRekening
    if uipT.NamaPemilikRekening != 'Rekening tidak terdefinisi':
      #tampilkan informasi lain rekening
      uipT.Tipe_Rekening_Pindah_Buku = res.FirstRecord.accountType
      uipT.IDNumber = res.FirstRecord.idNumber
      uipT.BranchCode = res.FirstRecord.branchCode
      uipT.CurrencyCode = res.FirstRecord.currencyCode
      sender.OwnerForm.GetControlByName('pButton.bSimpan').Enabled = \
      sender.OwnerForm.GetControlByName('pButton.bSimpan').Default = 1
    else:
      uipT.Tipe_Rekening_Pindah_Buku = uipT.IDNumber = uipT.BranchCode = \
      uipT.CurrencyCode = None

def bSimpanClick(sender):
  #import rpdb2; rpdb2.start_embedded_debugger("000")
  
  form = sender.OwnerForm
  app = form.ClientApplication
  
  uipT = sender.OwnerForm.GetUIPartByName('uipTransaksi')
  uipN = sender.OwnerForm.GetUIPartByName('uipNasabah')
  uipRWU = sender.OwnerForm.GetUIPartByName('uipRekeningWU')
  uipP = sender.OwnerForm.GetUIPartByName('uipParameter')

  #cek isOnlyTitipanPremi
  if not uipT.isOnlyTitipanPremi:
    #tidak sedang membayar titipan premi saja, cek nominal iuran peserta
    if uipT.IuranPeserta == None or uipT.IuranPeserta == '' or \
      uipT.IuranPeserta < uipP.PRESISI_ANGKA_FLOAT:
      form.ShowMessage('Nominal Iuran Peserta masih kosong atau 0! Mohon untuk diisi.')
      return
##    else:
##      #cek nominal iuran peserta dengan iuran peserta seharusnya
##      if uipT.IuranPeserta < uipN.IuranPeserta:
##        #nominal iuran peserta harus >= iuran peserta seharusnya
##        sender.OwnerForm.ShowMessage('Nominal Iuran Peserta harus sama atau lebih besar dari Iuran Peserta!')
##        return

  #cek untuk peserta wasiat umat
  if uipN.isWasiatUmmat == 'T':
    #cek titipan premi dan kolektibilitas titipan premi
    if uipN.KolektibilitasPremi == 'F':
      #pembayaran premi tidak lancar (masih ada hutang premi)
      if uipT.titipan_premi in [None,'']:
        sender.OwnerForm.ShowMessage('Nasabah termasuk peserta Wasiat Ummat dan '\
          'masih memiliki Kewajiban Premi yang belum terbayar sebesar Rp %0.2f! '\
          'Mohon sekaligus lunasi kewajiban premi tersebut.' % (uipN.KewajibanWasiatUmmat))
        return
      elif uipT.titipan_premi > uipP.PRESISI_ANGKA_FLOAT:
        #cek nominal iuran premi dengan iuran premi seharusnya
        if uipT.titipan_premi < (uipRWU.besar_premi + uipN.KewajibanWasiatUmmat):
          #nominal iuran peserta harus >= iuran peserta seharusnya
          sender.OwnerForm.ShowMessage('Nominal Titipan Premi harus sama atau lebih besar dari '\
            'Besar Premi Peserta plus Kewajiban Premi yang belum terbayarkan!')
          return
        elif uipT.GetFieldValue('TB_Premi.ID_TransactionBatch') == None or \
          uipT.GetFieldValue('TB_Premi.ID_TransactionBatch') == '':
          #batch premi harus dipilih
          sender.OwnerForm.ShowMessage('Batch Premi belum dipilih! Mohon pilih terlebih dahulu.')
          return
    else:
      #pembayaran premi lancar
      if uipT.titipan_premi in [None,'']:
        sender.OwnerForm.ShowMessage('Nasabah termasuk peserta Wasiat Ummat. Mohon isi Titipan Premi terlebih dahulu!'\
          '\nBila sedang tidak melakukan penitipan, isi dengan 0.')
        return
      elif uipT.titipan_premi > uipP.PRESISI_ANGKA_FLOAT:
        #cek nominal iuran premi dengan iuran premi seharusnya
        if uipT.titipan_premi < uipRWU.besar_premi:
          #nominal iuran peserta harus >= iuran peserta seharusnya
          sender.OwnerForm.ShowMessage('Nominal Titipan Premi harus sama atau lebih besar dari Besar Premi Peserta!')
          return
        elif uipT.GetFieldValue('TB_Premi.ID_TransactionBatch') == None or \
          uipT.GetFieldValue('TB_Premi.ID_TransactionBatch') == '':
          #batch premi harus dipilih
          sender.OwnerForm.ShowMessage('Batch Premi belum dipilih! Mohon pilih terlebih dahulu.')
          return

  form.CommitBuffer()
  form.PostResult()
  form.ShowMessage('Transaksi Iuran Peserta Berhasil. Siapkan printer untuk mencetak Slip Transaksi.')
  if uipP.FileSlipIuran not in [None,'']:
    downloadRes = form.CallServerMethod("downloadFile", \
      app.CreateValues(["fileName", uipP.FileSlipIuran]))
    libDLClass = form.ClientApplication.GetClientClass("libDownload", "libDownload")
    libDL = libDLClass()
    libDL.printStream(form.ClientApplication, downloadRes.Packet.GetStreamWrapper(0))

  if uipP.FileSlipPremi not in [None,'']:
    downloadRes = form.CallServerMethod("downloadFile", \
      app.CreateValues(["fileName", uipP.FileSlipPremi]))
    libDLClass = form.ClientApplication.GetClientClass("libDownload", "libDownload")
    libDL = libDLClass()
    libDL.printStream(form.ClientApplication, downloadRes.Packet.GetStreamWrapper(0))

  #clear it and exit from it
  #form.ResetAndClearData()
  sender.ExitAction = 1
