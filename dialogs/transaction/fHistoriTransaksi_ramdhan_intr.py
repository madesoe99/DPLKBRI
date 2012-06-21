class fHistoriTransaksi:
  def __init__(self, formObj, parentForm):
    if parentForm != None:
      self.parentForm = parentForm
    else:
      self.parentForm = None

  def Show(self):
    app = self.FormObject.ClientApplication
    
    self.FormShow(self.FormObject, None)
    self.FormContainer.Show()
    
  def MyZFill(self, str, maxlen):
  	while len(str) < maxlen:
  		str = '0' + str
  	return str
  
  def DateTupToOQLFormat(self, datetup):
    y, m, d = datetup[:3]
    m = self.MyZFill(str(m),2)
    d = self.MyZFill(str(d),2)
    y = str(y)
  
    return '%s/%s/%s' % (m,d,y)
  
  def FormShow(self, form, parameter):
    app = form.ClientApplication
    uipRekeningDPLK = form.GetUIPartByName('uipRekeningDPLK')
    
    uipRekeningDPLK.Edit()
    uipRekeningDPLK.tanggal_filter = app.ModDateTime.Now()
    uipRekeningDPLK.tanggal_filter_akhir = app.ModDateTime.Now()
  
    self.btnShowClick(form.GetControlByName('pDataUmumRek.btnShow'))
  
  def btnShowClick(self, sender):
    form = sender.OwnerForm
    uipNasabahDPLK = form.GetUIPartByName('uipNasabahDPLK')
    uipRekeningDPLK = form.GetUIPartByName('uipRekeningDPLK')
  
    qTransaksiDPLK = form.GetPanelByName('qTransaksiDPLK')
    qTitipanPremi = form.GetPanelByName('qTitipanPremi')
  
    strDateFilterAwal = self.DateTupToOQLFormat(uipRekeningDPLK.tanggal_filter)
    strDateFilterAkhir = self.DateTupToOQLFormat(uipRekeningDPLK.tanggal_filter_akhir)
  
    qTransaksiDPLK.SetParameter('no_peserta',uipNasabahDPLK.no_peserta)
    qTransaksiDPLK.SetParameter('tgl_transaksi_awal',strDateFilterAwal)
    qTransaksiDPLK.SetParameter('tgl_transaksi_akhir',strDateFilterAkhir)
    qTransaksiDPLK.DisplayData()
  
    qTitipanPremi.SetParameter('no_peserta',uipNasabahDPLK.no_peserta)
    qTitipanPremi.SetParameter('tgl_transaksi_awal',strDateFilterAwal)
    qTitipanPremi.SetParameter('tgl_transaksi_akhir',strDateFilterAkhir)
    qTitipanPremi.DisplayData()

