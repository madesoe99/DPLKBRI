class fInvestasi:

  def __init__(self, formObj, parentForm):
    self.app = formObj.ClientApplication

  def FormShow(self, form, parameter):
    uipInvestasi = form.GetUIPartByName('uipInvestasi')

    qTransPiutangInvestasi = form.GetPanelByName('qTransPiutangInvestasi')
    qTransPiutangInvestasi.SetParameter('id_investasi',uipInvestasi.id_investasi)
    qTransPiutangInvestasi.DisplayData()

    qTransPiutangLRInvestasi = form.GetPanelByName('qTransPiutangLRInvestasi')
    qTransPiutangLRInvestasi.SetParameter('id_investasi',uipInvestasi.id_investasi)
    qTransPiutangLRInvestasi.DisplayData()

    qTransLRInvestasi = form.GetPanelByName('qTransLRInvestasi')
    qTransLRInvestasi.SetParameter('id_investasi',uipInvestasi.id_investasi)
    qTransLRInvestasi.DisplayData()

    #kode_jns_investasi = uipInvestasi.GetFieldValue('LRincianPaketInvestasi.kode_jns_investasi')
    kode_jns_investasi = uipInvestasi.kode_jns_investasi
    if kode_jns_investasi == 'D':
      # deposito
      formID = 'investasi/transaksi/fDepositoInfo'
      key = 'PObj:Deposito#ID_INVESTASI=%d' % uipInvestasi.id_investasi
      caption = 'Investasi MM'
      self.MultiPagesTop.GetPage(2).TabVisible = 1
    elif kode_jns_investasi == 'O':
      # obligasi
      formID = 'investasi/transaksi/fObligasiInfo'
      key = 'PObj:Obligasi#ID_INVESTASI=%d' % uipInvestasi.id_investasi
      caption = 'Investasi FIX'
    elif kode_jns_investasi == 'R':
      # reksadana
      formID = 'investasi/transaksi/fReksadanaInfo'
      key = 'PObj:Reksadana#ID_INVESTASI=%d' % uipInvestasi.id_investasi
      caption = 'Investasi EQ'
    elif kode_jns_investasi == 'S':
      # reksadana
      formID = 'investasi/transaksi/fSahamInfo'
      key = 'PObj:Saham#ID_INVESTASI=%d' % uipInvestasi.id_investasi
      caption = 'Saham'
    else:
      raise 'Kesalahan Jenis Investasi','Jenis Investasi \'%s\' tidak dikenali' % str(kode_jns_investasi)

    form.Caption = caption

    # test
    frmInvestasi = form.GetPanelByName('frmInvestasi')
    frmDetailInvestasi = frmInvestasi.Activate(
      formID
      , self.app.CreateValues(['key', key])
      , None
    )
    if kode_jns_investasi == 'A':
      frmDetailInvestasi.SetVisibility()

  def btnPrintClick(self, sender):
    pass
    
  def bTampilkanClick(self, sender) :
      uipRek = self.uipInvestasi
      if uipRek.TglAwal == None:
          raise 'PERINGATAN', 'Tanggal awal harus diisi!'
      if uipRek.TglAkhir == None:
          raise 'PERINGATAN', 'Tanggal akhir harus diisi!'
      if uipRek.TglAwal > uipRek.TglAkhir:
          raise 'PERINGATAN', 'Tanggal awal tidak boleh lebih besar dari akhir!'

      ph = self.app.ExecuteScript(
          'investasi/master/HistTransaksi',
          self.app.CreateValues(
              ['id_investasi', uipRek.id_investasi],
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
          uipTran.TglTransaksi          = rec.TglTransaksi
          uipTran.Kode                  = rec.Kode
          uipTran.Keterangan            = rec.Keterangan
          uipTran.Mutasi_Debet          = rec.Mutasi_Debet
          uipTran.Mutasi_Kredit         = rec.Mutasi_Kredit
          uipTran.Status_Otorisasi      = rec.Status_Otorisasi
          uipTran.TglEfektif            = rec.TglEfektif

          i += 1
      # end of while

      uipTran.First()
      
  def bCetakClick(self, sender) :
      uipRek = self.uipInvestasi
      if uipRek.TglAwal == None:
          raise 'PERINGATAN', 'Tanggal awal harus diisi!'
      if uipRek.TglAkhir == None:
          raise 'PERINGATAN', 'Tanggal akhir harus diisi!'
      if uipRek.TglAwal > uipRek.TglAkhir:
          raise 'PERINGATAN', 'Tanggal awal tidak boleh lebih besar dari akhir!'

      phret = self.app.ExecuteScript(
          'investasi/master/CetakTransaksi',
          self.app.CreateValues(
              ['id_investasi', uipRek.id_investasi],
              ['TglAwal', uipRek.TglAwal],
              ['TglAkhir', uipRek.TglAkhir]
          )
      )

      rec = phret.FirstRecord
      if rec.Is_Err:
        raise 'Peringatan!',rec.Err_Message
      else:
       if phret.Packet.StreamWrapperCount > 0:
        #sw = phret.Packet.GetStreamWrapper(0)
        sw = phret.Packet.GetStreamWrapperByName("upload")
        if sw == None:
          raise 'PERINGATAN',"Stream tidak ditemukan"

        sFileName = 'c:/temphistinv.txt'
        sw.SaveToFile(sFileName)
        self.app.ShellExecuteFile(sFileName)

