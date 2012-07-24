class fPRAutoPayment_Daftar:
  def __init__(self, formObj, parentForm):
    self.app = formObj.ClientApplication
    self.DictFormId = {
      'D':'transaksi/fPRDetilRiwayatGiro'
    }
       
  def Show(self,jenis):
    self.uipart.Edit()
    self.uipart.jenis_reconcile = jenis
    if jenis == 'A':
       caption = 'Auto Payment'
    elif jenis == 'E':
       caption = 'e - Channel'
    self.FormObject.Caption += caption
    self.FormContainer.Show()

  def TampilkanOnClick(self, sender):
    qPR = self.qPR
    uip = self.uipart
    Data={'jenis':uip.jenis_reconcile,'is_berhasil':uip.is_berhasil,'is_reconciled':uip.is_reconciled}
    if uip.tgl_awal[:3] > uip.tgl_akhir[:3]:
      self.FormObject.ShowMessage('Rentang tanggal salah, mohon untuk dibetulkan dahulu!')
      return
    Data['tgl_awal']  = '%s/%s/%d' % (str(uip.tgl_awal[1]).zfill(2), str(uip.tgl_awal[2]).zfill(2),uip.tgl_awal[0])
    Data['tgl_akhir'] = '%s/%s/%d' % (str(uip.tgl_akhir[1]).zfill(2), str(uip.tgl_akhir[2]).zfill(2),uip.tgl_akhir[0])

    AddParam ="LReconcile.jenis_reconcile='%(jenis)s' and \
               LReconcile.tanggal_transaksi >='%(tgl_awal)s' and \
               LReconcile.tanggal_transaksi <= '%(tgl_akhir)s' and \
               LReconcile.is_file_valid = '%(is_berhasil)s' and \
               is_reconciled = '%(is_reconciled)s' " % Data

    qPR.OQLText = " select from riwayatgiro [ %s ] \
    ( account_giro, \
      is_reconciled $, \
      is_pindahbuku $, \
      id_reconcile, \
      sum_procced_nominal, \
      sum_pindahbuku, \
      sum_nominal, \
      LReconcile.tanggal_transaksi, \
      LReconcile.waktu_mulai, \
      LReconcile.waktu_selesai, \
      LReconcile.jenis_reconcile $, \
      LReconcile.nama_file, \
      LReconcile.is_file_valid $, \
      self \
    );" % (AddParam)     
    qPR.DisplayData()

  def bViewDetilOnClick(self, sender):
    group_id, form_id = self.DictFormId['D'].split('/')
    form = self.app.FindForm(form_id)
    if form == None:
      key = self.qPR.KeyObjConst 
      ph = self.app.CreateValues(['key', key])
      form = self.app.CreateForm(group_id+'/'+form_id, form_id, 0, ph, None)
    form.Show()
    
    self.qPR.Refresh()    

  def Form_OnClose(self, formObj):
    # procedure(formobj: TrtfForm)
    app = formObj.ClientApplication
    userApp = app.UserAppObject
    userApp.unregisterForm('fPRAutoPayment_Daftar')
  #--