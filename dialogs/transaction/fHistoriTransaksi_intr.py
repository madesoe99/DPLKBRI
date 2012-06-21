class fHistoriTransaksi:
  def __init__(self, formObj, parentForm):
    if parentForm != None:
      self.parentForm = parentForm
    else:
      self.parentForm = None

  def Show(self):
    app = self.FormObject.ClientApplication
    
    self.FormShow(self.FormObject)
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
  
  def FormShow(self, form):
    app = form.ClientApplication
    uipRekInvDPLK = form.GetUIPartByName('uipRekInvDPLK')
    
    uipRekInvDPLK.Edit()
    uipRekInvDPLK.tanggal_filter = app.ModDateTime.Now()
    uipRekInvDPLK.tanggal_filter_akhir = app.ModDateTime.Now()
  
    self.btnShowClick(form.GetPanelByName("pDataUmumRek").GetControlByName('btnShow'))
  
  def btnShowClick(self, sender):
    form = sender.OwnerForm
    uipNasabahDPLK = form.GetUIPartByName('uipNasabahDPLK')
    uipRekInvDPLK = form.GetUIPartByName('uipRekInvDPLK')
  
    qTransaksiDPLK = form.GetPanelByName('qTransaksiDPLK')
    qTitipanPremi = form.GetPanelByName('qTitipanPremi')
  
    strDateFilterAwal = self.DateTupToOQLFormat(uipRekInvDPLK.tanggal_filter)
    strDateFilterAkhir = self.DateTupToOQLFormat(uipRekInvDPLK.tanggal_filter_akhir)
  
    qTransaksiDPLK.SetParameter('no_peserta',uipNasabahDPLK.no_peserta)
    qTransaksiDPLK.SetParameter('all_tgl_awal',0)
    qTransaksiDPLK.SetParameter('tgl_transaksi_awal',strDateFilterAwal)
    if strDateFilterAwal in [None]:
      qTransaksiDPLK.SetParameter('all_tgl_awal',1)
      qTransaksiDPLK.SetParameter('tgl_transaksi_awal',1)
      
    qTransaksiDPLK.SetParameter('all_tgl_akhir',0)
    qTransaksiDPLK.SetParameter('tgl_transaksi_akhir',strDateFilterAkhir)
    if strDateFilterAkhir in [None]:
      qTransaksiDPLK.SetParameter('all_tgl_akhir',1)
      qTransaksiDPLK.SetParameter('tgl_transaksi_akhir',1)
    
    qTransaksiDPLK.DisplayData()
    
    qTitipanPremi.SetParameter('no_peserta',uipNasabahDPLK.no_peserta)
    qTitipanPremi.SetParameter('all_tgl_awal',0)
    qTitipanPremi.SetParameter('tgl_transaksi_awal',strDateFilterAwal)
    if strDateFilterAwal in [None]:
      qTitipanPremi.SetParameter('all_tgl_awal',1)
      qTitipanPremi.SetParameter('tgl_transaksi_awal',1)
      
    qTitipanPremi.SetParameter('all_tgl_akhir',0)
    qTitipanPremi.SetParameter('tgl_transaksi_akhir',strDateFilterAkhir)
    if strDateFilterAkhir in [None]:
      qTitipanPremi.SetParameter('all_tgl_akhir',1)
      qTitipanPremi.SetParameter('tgl_transaksi_akhir',1)
    
    qTitipanPremi.DisplayData()

