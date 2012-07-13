class fInvestasi:

  def __init__(self, formObj, parentForm):
    self.app = formObj.ClientApplication

  def FormShow(self, form, parameter):

    kode_jns_investasi = self.uipInvestasi.kode_jns_investasi
    if kode_jns_investasi == 'D':
      # deposito
      caption = 'Peragaan Transaksi Investasi MM'
      gHist = self.FormObject.GetPanelByName('gHistori')
    elif kode_jns_investasi == 'O':
      # obligasi
      caption = 'Peragaan Transaksi Investasi Fix'
    elif kode_jns_investasi == 'R':
      # reksadana
      caption = 'Peragaan Transaksi Investasi EQ'
    else:
      raise Exception, 'Kesalahan Jenis Investasi' + 'Jenis Investasi \'%s\' tidak dikenali' % str(kode_jns_investasi)

    form.Caption = caption

    # Frame
    #frmInvestasi = form.GetPanelByName('frmInvestasi')
    #frmDetailInvestasi = frmInvestasi.Activate(
    #  formID
    #  , self.app.CreateValues(['key', key])
    #  , None
    #)
    #if kode_jns_investasi == 'A':
    #  frmDetailInvestasi.SetVisibility()

  def btnPrintClick(self, sender):
    pass
    
  def bTampilkanClick(self, sender) :
      uipRek = self.uipInvestasi
      if uipRek.TglAwal == None:
          raise Exception, 'PERINGATAN' +  'Tanggal awal harus diisi!'
      if uipRek.TglAkhir == None:
          raise Exception, 'PERINGATAN' +  'Tanggal akhir harus diisi!'
      if uipRek.TglAwal > uipRek.TglAkhir:
          raise Exception, 'PERINGATAN' +  'Tanggal awal tidak boleh lebih besar dari akhir!'

      ph = self.app.ExecuteScript(
          'investasi/master/HistTransaksiInvestasi',
          self.app.CreateValues(
              ['kode_jns_investasi', uipRek.kode_jns_investasi],
              ['TglAwal', uipRek.TglAwal],
              ['TglAkhir', uipRek.TglAkhir]
          )
      )


      uipTran = self.uipTransaksi
      uipTran.ClearData()

      ds = ph.packet.histori
      i = 0
      while i < ds.RecordCount:
          rec = ds.GetRecord(i)
          uipTran.Append()

          uipTran.id_transaksiinvestasi = rec.id_transaksiinvestasi
          uipTran.No_Investasi          = rec.No_Investasi
          uipTran.TglTransaksi          = rec.TglTransaksi
          uipTran.Kode                  = rec.Kode
          uipTran.Keterangan            = rec.Keterangan
          uipTran.Mutasi_Debet          = rec.Mutasi_Debet
          uipTran.Mutasi_Kredit         = rec.Mutasi_Kredit
          uipTran.Status_Otorisasi      = rec.Status_Otorisasi
          uipTran.TglEfektif            = rec.TglEfektif
          uipTran.StatusInvestasi       = rec.StatusInvestasi

          i += 1
      # end of while

      uipTran.First()
