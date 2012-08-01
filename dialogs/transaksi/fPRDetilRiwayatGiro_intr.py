class fPRDetilRiwayatGiro:
  def __init__(self, formObj, parentForm):
    self.app = formObj.ClientApplication
    self.caption =''
    self.DictFormId = {
      'E':'transaksi/fPRDetilRiwayatGiroEdit'
    }
       
  def Show(self):
    jenis = self.uipart.jenis_reconcile
    if jenis == 'A':
       self.caption = 'Auto Payment'
    elif jenis == 'E':
       self.caption = 'e - Channel'
    if self.uipart.is_reconciled =='T':
       self.tutup_bProses.Enabled = 0
       #self.tutup_bPindahbuku.Enabled = 1
      
    self.FormObject.Caption += self.caption
    self.TampilGrid()
    self.FormContainer.Show()

  def TampilkanOnClick(self, sender):
    self.TampilGrid()
    
  def TampilGrid(self):
    qValid = self.qValid
    qValid.OQLText = self.oText('T')
    qValid.DisplayData()
    
    qInvalid = self.qInvalid
    qInvalid.OQLText = self.oText('F')
    qInvalid.DisplayData()

  def oText(self, jenis):
    uip = self.uipart
    norek = uip.no_rekening or ''
    AddParam =" ('A'='%s' or is_created_transaction = '%s' )" % (uip.is_created_transaction,uip.is_created_transaction)
    AddParam +=" and id_reconcile = %s and is_valid = '%s'" % (uip.id_reconcile, jenis)
    if norek != '':
       AddParam +=" and no_rekening LLIKE '%s' " % norek
    valid ={} 

    oText = " select from detilriwayatgiro [ %s ] " % (AddParam)
    oText += "( account_giro, \
      id_reconcile, \
      no_rekening, \
      is_corporate, \
      is_valid $, \
      is_created_transaction $, \
      nominal, \
      rekening_sumber, \
      keterangan, \
      self \
    );" 
    
    return oText
  

  def EditClick(self, sender):
    group_id, form_id = self.DictFormId['E'].split('/')
    o_nominal = self.qInvalid.GetFieldValue('detilriwayatgiro.nominal')
    form = self.app.FindForm(form_id)
    if form == None:
      key = self.qInvalid.KeyObjConst 
      ph = self.app.CreateValues(['key', key])
      form = self.app.CreateForm(group_id+'/'+form_id, form_id, 0, ph, None)
      #form = f.FormContainer
    nominal = form.Show()
    if nominal !=None:
      selisih = nominal - o_nominal
      self.uipart.Edit()
      self.uipart.sum_nominal += selisih
      self.qInvalid.Refresh()    
      self.qValid.Refresh()    

  def InvalidClick(self, sender):
    ict = self.qValid.GetFieldValue('detilriwayatgiro.is_created_transaction')
    if ict =='true':
      self.app.ShowMessage('Sudah dibuat transaksi, tidak bisa dijadikan invalid!!')
      return 0

    if self.app.ConfirmDialog('Yakin akan menjadikan invalid??'):
      pass
    else:
      return 0
  
    key = self.qValid.KeyObjConst 
    resp = self.app.ExecuteScript('DRG3.invalid_status',self.app.CreateValues(['key', key]))

    status = resp.FirstRecord
    if status.IsErr :
      self.app.ShowMessage(status.ErrMessage)
      return
    
    self.qInvalid.Refresh()    
    self.qValid.Refresh()    


  def bProsesOnClick(self, sender):
    if self.app.ConfirmDialog('Anda yakin Proses Otorisasi '+self.caption+' ?'):
      ph = self.app.CreateValues(['id_reconcile', self.uipart.id_reconcile],
                                 ['jenis', self.uipart.jenis_reconcile],
                                 ['waktu_mulai', self.uipart.waktu_mulai])
      resp = self.app.ExecuteScript("DRG3.SimpanTransaksi", ph)
  
      #process return
      status = resp.FirstRecord
      if status.IsErr :
        self.app.ShowMessage(status.ErrMessage)
        return
      
      self.uipart.Edit()
      self.uipart.sum_procced_nominal += status.proced_nominal
      self.uipart.sum_sisa -= status.proced_nominal
      self.qValid.Refresh()    

  def bPindahbukuOnClick(self, sender):
    if self.app.ConfirmDialog('Anda yakin Proses Pindah bukukan '+self.caption+' ?'):
      ph = self.app.CreateValues(['id_reconcile', self.uipart.id_reconcile],
                                 ['jenis', self.uipart.jenis_reconcile],
                                 ['account_giro', self.uipart.acc_giro])
      resp = self.app.ExecuteScript('DRG3.Pindah_Bukukan', ph)
  
      #process return
      status = resp.FirstRecord
      if status.IsErr :
        self.app.ShowMessage(status.ErrMessage)
        return
      
      self.uipart.Edit()
      self.uipart.sum_pindahbuku += status.proced_nominal
      self.qValid.Refresh()    
    
