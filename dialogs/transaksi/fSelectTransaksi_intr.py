class fSelectTransaksi:
  def __init__(self, formObj, parentForm):
    # nextForm akan dipanggil setelah rekening dipilih
    #self.NextForm = nextForm
    self.FormObj = formObj
    self.App = formObj.ClientApplication
    self.DictFormId = {
      'K':'transaksi/fOtorisasiIuranPeserta',
      'I':'transaksi/fOtorisasiPengalihanDariDPLKLain',
      'O':'transaksi/fOtorisasiPengalihanDariDPPKLain',
      'P':'transaksi/fOtorisasiPengalihanDariDPKLain',
      'H':'transaksi/fOtorisasiPengalihanKeDPLKLain',
      'V':'transaksi/fOtorisasiPenarikanDana30',
      'W':'transaksi/fOtorisasiPenarikanDanaPHK',
      'J':'transaksi/fOtorisasiPengambilanManfaatPensiun',
      'C':'transaksi/fViewBiaya',
      'D':'transaksi/fViewBiaya',
      'X':'transaksi/fViewBiaya'
    }
  #--
  
  def cbAllCabangClick(self, checkbox):
    if self.pFilter_cbAllCabang.Checked:
      self.pFilter_LCabang.Enabled = 0  
    else:
      self.pFilter_LCabang.Enabled = 1
  #--
  
  def cbAllTransaksiClick(self, checkbox):
    if self.pFilter_cbAllTransaksi.Checked:
      self.pFilter_LJenisTransaksi.Enabled = 0  
    else:
      self.pFilter_LJenisTransaksi.Enabled = 1
  #--

  def bTampilkanClick_Client(self, button):
    #cek cabang transaksi
    if not self.uipFilter.cbAllCabang and self.uipFilter.GetFieldValue('LCabang.branch_code') in (None,''):
      self.FormObj.ShowMessage("Pilih Cabang terlebih dahulu!")
      return
      
    #cek jenis transaksi
    if not self.uipFilter.cbAllTransaksi and self.uipFilter.GetFieldValue('LJenisTransaksi.kode_jenis_transaksi') in (None,''):
      self.FormObj.ShowMessage("Pilih jenis transaksi terlebih dahulu!")
      return
      
    #cek rentang tanggal filter
    awalTanggal = self.uipFilter.eAwalTanggal
    akhirTanggal = self.uipFilter.eHinggaTanggal
    if (awalTanggal[:3] > akhirTanggal[:3]):
      self.FormObj.ShowMessage('Rentang tanggal filter salah, mohon untuk dibetulkan dahulu!')
      return

    #set parameter OQL and show it
    self.qTransaksi.OQLText = \
      "select from TransaksiDPLK \
        [(1 = :all_cabang or branch_code = :filter_cabang) \
        and (1 = :all_jenis_transaksi or kode_jenis_transaksi = :filter_jenis_transaksi) \
        and (('A' = :filter_otorisasi) or isCommitted = :filter_otorisasi)\
        and tgl_transaksi >= :tanggal_awal \
        and tgl_transaksi < :tanggal_akhir] \
      (tgl_transaksi,\
       branch_code,\
       isCommitted,\
       ID_Transaksi,\
       LJenisTransaksiDPLK.kode_jenis_transaksi,\
       LJenisTransaksiDPLK.nama_transaksi,\
       no_rekening,\
       keterangan,\
       self) \
       then order by tgl_transaksi;" \

    #setting date untuk OQL: mm/dd/yyyy
    self.qTransaksi.SetParameter('all_cabang',self.uipFilter.cbAllCabang)
    self.qTransaksi.SetParameter('filter_cabang',self.uipFilter.GetFieldValue('LCabang.branch_code'))
    self.qTransaksi.SetParameter('all_jenis_transaksi',self.uipFilter.cbAllTransaksi)
    self.qTransaksi.SetParameter('filter_jenis_transaksi',self.uipFilter.GetFieldValue('LJenisTransaksi.kode_jenis_transaksi'))
    self.qTransaksi.SetParameter('filter_otorisasi',self.uipFilter.cbStatusOtorisasi)

    awalTanggal = '%s/%s/%d' % (str(awalTanggal[1]).zfill(2), \
      str(awalTanggal[2]).zfill(2),awalTanggal[0])

    #ubah rentang akhirTanggal
    y,m,d = akhirTanggal[:3] 
    akhirTanggal = self.App.ModLibUtils.EncodeDate(y,m,d) + 1
    y,m,d = self.App.ModLibUtils.DecodeDate(akhirTanggal)
    akhirTanggal = '%s/%s/%s' % (str(m).zfill(2), \
      str(d).zfill(2),str(y).zfill(2))

    self.qTransaksi.SetParameter('tanggal_awal',awalTanggal)
    self.qTransaksi.SetParameter('tanggal_akhir',akhirTanggal)
    
    self.qTransaksi.DisplayData()
    
    #debug code
    #formObj.ShowMessage(self.qTransaksi.OQLText)
  #--

  def bTampilkanClick_Server(self, button):
    #cek cabang transaksi
    if not self.uipFilter.cbAllCabang and self.uipFilter.GetFieldValue('LCabang.branch_code') in (None,''):
      self.FormObj.ShowMessage("Pilih Cabang terlebih dahulu!")
      return
      
    #cek jenis transaksi
    if not self.uipFilter.cbAllTransaksi and self.uipFilter.GetFieldValue('LJenisTransaksi.kode_jenis_transaksi') in (None,''):
      self.FormObj.ShowMessage("Pilih jenis transaksi terlebih dahulu!")
      return
      
    #cek rentang tanggal filter
    awalTanggal = self.uipFilter.eAwalTanggal
    akhirTanggal = self.uipFilter.eHinggaTanggal
    if (awalTanggal[:3] > akhirTanggal[:3]):
      self.FormObj.ShowMessage('Rentang tanggal filter salah, mohon untuk dibetulkan dahulu!')
      return

    paramQuery = app.CreateValues( \
      ['nomorRekening', nomorRekening], \
      ['namaPeserta', namaPeserta]) 
    ph = self.FormObj.CallServerMethod("searchTransaksi", paramQuery)
    
    # process return
    dsStatus = ph.packet.status
    rec = dsStatus.GetRecord(0)
    if rec.error_status:
      # show error message
      self.FormObj.ShowMessage(rec.error_message)
    else:
      self.qNomorRekening.SetDirectResponse(ph.Packet)
      if rec.has_more_data:
        self.FormObj.ShowMessage("Diketahui ada data lebih. Silahkan isi filter lebih detil!")
        return
  #--
  
  def ShowNextForm(self, button, mode):
    group_id, form_id = self.DictFormId[self.qTransaksi.GetFieldValue('TransaksiDPLK.kode_jenis_transaksi')].split('/')
    form = self.App.FindForm(form_id)
    if form == None:
      nomorRekening = self.qTransaksi.GetFieldValue('TransaksiDPLK.no_rekening')
      idTransaksi = str(self.qTransaksi.GetFieldValue('TransaksiDPLK.ID_Transaksi')) 
      ph = self.App.CreateValues(["no_rekening", nomorRekening], ["id_transaksi", idTransaksi])
      f = self.App.CreateForm(group_id+'/'+form_id, form_id, 0, ph, mode)
      form = f.FormContainer
    form.Show()    
  #--
  
  def bOtorisasi_Click(self, button):
    if self.qTransaksi.GetFieldValue('TransaksiDPLK.isCommitted').upper() in ['T','TRUE']:
      self.FormObj.ShowMessage("Transaksi telah terotorisasi!")
      return
      
    # show form otorisasi
    self.ShowNextForm(button, ['otorisasi'])

    #refresh qTransaksi
    self.qTransaksi.Refresh()
  #--
  
  def bView_Click(self, button):
    # show form view
    self.ShowNextForm(button, ['view'])
    
    #refresh qTransaksi
    self.qTransaksi.Refresh()
  #--    

  def Form_OnClose(self, formObj):
    # procedure(formobj: TrtfForm)
    app = formObj.ClientApplication
    userApp = app.UserAppObject
    userApp.unregisterForm('fSelectTransaksi')
  #--