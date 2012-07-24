class fDaftarIuran:
  def __init__(self, formObj, parentForm):
    # nextForm akan dipanggil setelah rekening dipilih
    #self.NextForm = nextForm
    self.FormObj = formObj
    self.App = formObj.ClientApplication
    self.DictFormId = {
      'D':'transaksi/fIuranPendaftaran_otor'
    }
  #--

  def cbAllCabangClick(self, checkbox):
    if self.pFilter_cbAllCabang.Checked:
      self.pFilter_LCabang.Enabled = 0  
    else:
      self.pFilter_LCabang.Enabled = 1
  #--
  
  def oText(self):
    uip = self.uipFilter
    tgl_awal  = '%s/%s/%d' % (str(uip.eAwalTanggal[1]).zfill(2), str(uip.eAwalTanggal[2]).zfill(2),uip.eAwalTanggal[0])
    #ubah rentang akhirTanggal
    y,m,d = uip.eHinggaTanggal[:3] 
    akhirTanggal = self.App.ModLibUtils.EncodeDate(y,m,d) + 1
    y,m,d = self.App.ModLibUtils.DecodeDate(akhirTanggal)
    tgl_akhir = '%s/%s/%s' % (str(m).zfill(2),str(d).zfill(2),str(y).zfill(2))
    
    AddParam =" (1=%s or branch_code ='%s')" % (uip.cbAllCabang, uip.GetFieldValue('LCabang.branch_code'))
    AddParam +=" and ('A' = '%s' or isCommitted ='%s') " % (uip.cbStatusOtorisasi,uip.cbStatusOtorisasi)
    AddParam +=" and (tgl_transaksi >= '%s') and (tgl_transaksi <= '%s') " % (tgl_awal,tgl_akhir)

    oText = " select from IuranPendaftaran [ %s ] " % (AddParam)
    oText += "(tgl_transaksi,\
       branch_code as Kode_Cabang,\
       isCommitted,\
       LRekeningDPLK.LNasabahDPLK.nama_lengkap, \
       ID_Transaksi,\
       besar_biaya_daftar,\
       no_rekening,\
       keterangan,\
       self) \
       then order by tgl_transaksi;"
    
    #raise Exception, oText
    return oText

  def bTampilkanOnClick(self, sender):
    #cek cabang transaksi
    if not self.uipFilter.cbAllCabang and self.uipFilter.GetFieldValue('LCabang.branch_code') in (None,''):
      self.FormObj.ShowMessage("Pilih Cabang terlebih dahulu!")
      return
            
    #cek rentang tanggal filter
    awalTanggal = self.uipFilter.eAwalTanggal
    akhirTanggal = self.uipFilter.eHinggaTanggal
    if (awalTanggal[:3] > akhirTanggal[:3]):
      self.FormObj.ShowMessage('Rentang tanggal filter salah, mohon untuk dibetulkan dahulu!')
      return

    self.qTransaksi.OQLText = self.oText()
    self.qTransaksi.DisplayData()

  def ShowNextForm(self, button, mode):
    group_id, form_id = self.DictFormId['D'].split('/')
    form = self.App.FindForm(form_id)
    if form == None:
      nomorRekening = self.qTransaksi.GetFieldValue('IuranPendaftaran.no_rekening')
      idTransaksi = str(self.qTransaksi.GetFieldValue('IuranPendaftaran.ID_Transaksi')) 
      ph = self.App.CreateValues(["no_rekening", nomorRekening], ["id_transaksi", idTransaksi])
      f = self.App.CreateForm(group_id+'/'+form_id, form_id, 0, ph, mode)
      form = f.FormContainer
    form.Show()    
  #--
  
  def bOtorisasi_Click(self, button):
    if self.qTransaksi.GetFieldValue('IuranPendaftaran.isCommitted').upper() in ['T','TRUE']:
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
    userApp.unregisterForm('fDaftarIuran')
  #--

